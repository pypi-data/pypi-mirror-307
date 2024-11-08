import os
import io
import json
import logging
from dateutil import parser
import requests
from requests import Response
import pandas as pd

DEFAULT_TIMEOUT = 30
DEFAULT_ENDPOINT = "https://unbounded.network/api/v1"

file_access_audit_func = None


class APIError(Exception):
    "Error raised by Client in case of unexpected server response"

    def __init__(self, status=-1, message=None):
        super().__init__(': '.join([x for x in [str(status) if status > 0 else None, message] if x]))
        self.status = status
        self.message = message


class FileAccessAudit:
    "this class is used for internal file audit"

    def __init__(self, dataset_id, dataset_version, file_id, file_version, operation):
        self.dataset_id = dataset_id
        self.dataset_version = dataset_version
        self.file_id = file_id
        self.file_version = file_version
        self.operation = operation

    def to_dict(self):
        return {
            "dataset_id": self.dataset_id,
            "dataset_version": self.dataset_version,
            "file_id": self.file_id,
            "file_version": self.file_version,
            "operation": self.operation,
        }


class Client:
    """
    This client class is used to send http requests
    to query datasets from unbounded network.
    """

    def __init__(
        self,
        api_key: str = None,
        timeout: float = 30,
        endpoint_url: str = DEFAULT_ENDPOINT,
    ):
        if not api_key:
            api_key = os.getenv("UNBOUNDED_API_KEY")

        if not api_key or not api_key.strip():
            api_key = None

        if endpoint_url == DEFAULT_ENDPOINT and os.getenv("UNBOUNDED_DATA_ENDPOINT"):
            endpoint_url = os.getenv("UNBOUNDED_DATA_ENDPOINT")

        self.endpoint_url = endpoint_url
        self.api_key = api_key
        self.timeout = timeout

    def list_datasets(
        self,
        search_string: str = "",
        visibility: str = "private",
        with_files: str = "true",
    ):
        """
        description:    the function is used to query all datasets
                        associated with the user

        arguments:      search_string - a case-insensitive string
                        that must be found in the dataset name or
                        description
                        visibility - filters the resulting datasets
                        by their visibility, either private to your
                        user, or public across all users
                        with_files - when provided, each dataset
                        will have files in the response

        returns:        list of datasets
        """

        datasets_url = self.endpoint_url + "/datasets"
        parameters_dict = {
            "search": search_string,
            "visibility": visibility,
            "with_files": with_files,
        }

        client_response = self.do_request(
            "GET", datasets_url, params=parameters_dict
        )
        response_json = self.response_to_json(client_response)
        ds_list = pd.json_normalize(response_json["data"], sep="_").to_dict("records")
        ds_entries = []
        for dataset in ds_list:
            ds_entries.append(Dataset(dataset, self))

        return ds_entries

    def get_dataset(self, *, uuid: str = None, name: str = None):
        """
        description:    the function is used to query datasets
                        by either id or name

        arguments:      uuid - dataset id
                        name - dataset name

        returns:        Dataset instance
        """

        if uuid and name:
            raise ValueError("Only one query parameter can be provided at a time")

        if uuid:
            return self._get_dataset_by_uuid(uuid)

        if name:
            return self._get_dataset_by_name(name)

        raise ValueError("None of the query parameters provided")

    def _get_dataset_by_uuid(self, uuid: str):
        """
        description:    queries dataset by UUID directly from the dataset endpoint.

        arguments:      uuid - dataset id

        returns:        Dataset instance or None
        """
        try:
            dataset_url = self.endpoint_url + "/datasets/" + uuid
            client_response = self.do_request("GET", dataset_url)
            response_json = self.response_to_json(client_response)
            dataset = pd.json_normalize(response_json["data"], sep="_")
            return Dataset(dataset.iloc[0].to_dict(), self)
        except APIError as error:
            if error.status == 404:
                return None
            raise

    def _get_dataset_by_name(self, name: str):
        """
        description:    queries all datasets and searches by dataset name

        arguments:      name - dataset name

        returns:        Dataset instance or None
        """
        datasets = self.list_datasets(
            search_string=name, visibility="private"
        )
        if len(datasets) == 0:
            datasets = self.list_datasets(
                search_string=name, visibility="public"
            )
            if len(datasets) == 0:
                return None

        matched_datasets = []
        min_timestamp = None
        min_index = -1
        for dataset in datasets:
            if dataset.version["name"] == name:
                matched_datasets.append(dataset)
                index = len(matched_datasets) - 1
                timestamp = parser.parse(dataset.version["created_at"])
                if min_timestamp is None:
                    min_timestamp = timestamp
                    min_index = index
                if min_timestamp > timestamp:
                    min_timestamp = timestamp
                    min_index = index

        if len(matched_datasets) > 1:
            logging.warning(" More than one dataset with given name")

        if len(matched_datasets) == 0:
            return None

        return matched_datasets[min_index]

    def create_dataset(self, name: str, description: str, public: bool = False):
        """
        description:    the function is used to create a new dataset
                        with given name, description and visibility

        arguments:      name - new dataset name
                        description - new dataset description
                        public - new dataset visibility

        returns:        Dataset instance of the newly created dataset
        """
        if not name:
            raise ValueError("dataset must have name")

        creation_url = self.endpoint_url + "/datasets"
        request_body = json.dumps(
            {"name": name, "description": description, "public": public}
        )

        client_response = self.do_request(
            "POST",
            creation_url,
            headers={"content-type": "application/json"},
            data=request_body,
        )
        response_json = self.response_to_json(client_response)
        dataset = pd.json_normalize(response_json["data"], sep="_")
        return Dataset(dataset.iloc[0].to_dict(), self)

    def delete_dataset(self, uuid: str):
        """
        description:    the function is used to delete
                        a dataset with given uuid

        arguments:      uuid - the id of the dataset to be deleted
        """
        if uuid is None:
            raise ValueError("invalid dataset uuid")
        delete_url = self.endpoint_url + "/datasets/" + uuid
        return self.do_request("DELETE", delete_url)

    def response_to_json(self, response: Response):
        """
        converts aiohttp client response into json
        """
        return response.json()

    def response_to_text(self, response: Response):
        """
        converts aiohttp client response into text
        """
        return response.text

    def response_to_bytes_buffer(self, response: Response):
        """
        converts aiohttp client response into bytes buffer
        """
        buffer = io.BytesIO(response.content)
        buffer.seek(0)
        return buffer

    def do_request(
        self,
        method: str,
        url: str,
        *,
        params: dict = None,
        headers: dict = None,
        data: str = None,
    ):
        """
        description:    the function is used to execute http
                        requests with parameters against provided
                        url

        arguments:      method - http request method
                        url - unbounded network endpoint url
                        parameters - request parameters

        returns:        aiohttp client response
        """
        if not params:
            params = {}

        if not headers:
            headers = {}

        if method not in ("GET", "POST", "PUT", "PATCH", "DELETE"):
            raise ValueError(f"Unknown http request method: {method}")

        if self.api_key:
            headers["X-API-Key"] = self.api_key

        response = None
        if method == "GET":
            response = requests.get(url, params=params, headers=headers, timeout=DEFAULT_TIMEOUT)
        if method == "POST":
            response = requests.post(
                url, data=data, params=params, headers=headers, timeout=DEFAULT_TIMEOUT
            )
        if method == "PUT":
            response = requests.put(
                url, data=data, params=params, headers=headers, timeout=DEFAULT_TIMEOUT
            )
        if method == "PATCH":
            response = requests.patch(
                url, data=data, params=params, headers=headers, timeout=DEFAULT_TIMEOUT
            )
        if method == "DELETE":
            response = requests.delete(url, params=params, headers=headers, timeout=DEFAULT_TIMEOUT)

        if response.status_code not in (200, 204):
            try:
                error = response.json()["error"]
            except KeyError:
                error = response.text
            raise APIError(
                status=response.status_code,
                message=error,
            )

        return response

    def __repr__(self):
        return f"Client(endpoint_url: {self.endpoint_url})"


class Dataset:
    """
    This class is used to represent a dataset from Unbounded Network.
    Note: it contains all of the versions and files. To work with a
    specific version of the dataset, use latest() or version() functions
    """

    def __init__(self, dataset_desc: dict, client: Client):
        self.uuid = dataset_desc["uuid"]
        self.latest_version_number = dataset_desc["latest_version_number"]
        self.version = {
            "sequence_number": dataset_desc["version_sequence_number"],
            "name": dataset_desc["version_name"],
            "description": dataset_desc["version_description"],
            "created_at": dataset_desc["version_created_at"],
            "files": dataset_desc["version_files"]
            if "version_files" in dataset_desc
            else None,
        }
        self.public = dataset_desc["public"]
        self.thumbnail = (
            dataset_desc["thumbnail"] if "thumbnail" in dataset_desc else None
        )
        self.created_at = dataset_desc["created_at"]
        self.updated_at = dataset_desc["updated_at"]
        self.owner_id = dataset_desc.get("owner_id")
        self.owner_username = dataset_desc.get("owner_username")
        self.client = client

    def get_thumbnail(self):
        """
        description:    the function is used to retrieve
                        a thumbnail image of the dataset

        returns:        thumbnail image bytes
        """
        thumbnail_url = (
            self.client.endpoint_url + "/datasets/" + self.uuid + "/thumbnail"
        )
        resp = self.client.do_request("GET", thumbnail_url)
        buffer = self.client.response_to_bytes_buffer(resp)
        return buffer.read()

    def upload_thumbnail(self, image: bytes, image_name: str, content_type: str):
        """
        description:    the function is used to upload a thumbnail
                        image to the dataset

        arguments:      image - image bytes
                        file_name - name of the image file
                        content_type - type of image
        """
        if not isinstance(image, bytes):
            raise NotImplementedError('image must be bytes()')

        thumbnail_url = (
            self.client.endpoint_url + "/datasets/" + self.uuid + "/thumbnail/upload"
        )
        resp = self.client.do_request("POST", thumbnail_url)
        upload_info = self.client.response_to_json(resp)

        resp = self.client.do_request(
            "PUT",
            upload_info["url"],
            headers={"content-type": content_type},
            data=image,
        )

        upload_complete_url = (
            self.client.endpoint_url
            + "/datasets/"
            + self.uuid
            + "/thumbnail/upload-complete"
        )
        image_info_json = json.dumps({"id": upload_info["id"], "filename": image_name})

        self.client.do_request(
            "POST",
            upload_complete_url,
            headers={"content-type": "application/json"},
            data=image_info_json,
        )
        dataset = self.client.get_dataset(uuid=self.uuid)
        self.__update_dataset(dataset)

    def update_dataset_info(self, name: str = None, description: str = None):
        """
        description:    the function is used to update
                        dataset name or description or both.
                        Note: at least one must be defined


        arguments:      name - new dataset name
                        description - new dataset description

        exceptions:     - both name and description arguments were not defined
        """
        if name is None and description is None:
            raise ValueError("Both name and description cannot be undefined")

        update_url = self.client.endpoint_url + "/datasets/" + self.uuid

        data = {}

        if name is not None:
            data["name"] = name

        if description is not None:
            data["description"] = description

        self.client.do_request(
            "PATCH",
            update_url,
            headers={"content-type": "application/json"},
            data=json.dumps(data),
        )
        dataset = self.client.get_dataset(uuid=self.uuid)
        self.__update_dataset(dataset)

    def change_visibility(self, *, public: bool):
        """
        description:    the function is used to change the
                        visibility of the dataset


        arguments:      public - boolean that indicates if
                        dataset should be public or not. If
                        dataset visibility is the same as the
                        argument passed, nothing is done.
        """
        if self.public == public:
            return

        update_url = self.client.endpoint_url + "/datasets/" + self.uuid
        self.client.do_request(
            "PATCH",
            update_url,
            headers={"content-type": "application/json"},
            data=json.dumps({"public": public}),
        )
        self.public = public

    def delete_file(self, file_name: str):
        """
        description:    the function is used to delete
                        a new file from the dataset

        arguments:      file_name - name of the file to
                        be deleted
        """
        if "files" in self.version:
            for file in self.version["files"]:
                if file["version"]["filename"] == file_name:
                    file_uuid = file["uuid"]
                    delete_url = (
                        self.client.endpoint_url
                        + "/datasets/"
                        + self.uuid
                        + "/files/"
                        + file_uuid
                    )
                    self.client.do_request("DELETE", delete_url)
                    dataset = self.client.get_dataset(uuid=self.uuid)
                    self.__update_dataset(dataset)
                    return
        raise RuntimeError("Dataset does not have any files")

    def create_raw_file(
        self, data_buffer: io.BytesIO, file_name: str, content_type: str
    ):
        """
        description:    the function is used to create
                        a new file in the dataset

        arguments:      data_buffer - buffer containing the data
                        file_name - name of the new file
                        content_type - type of the new file
        """

        create_file_url = (
            self.client.endpoint_url + "/datasets/" + self.uuid + "/files/upload"
        )
        resp = self.client.do_request("POST", create_file_url)
        upload_info = self.client.response_to_json(resp)

        resp = self.client.do_request(
            "PUT",
            upload_info["url"],
            headers={"content-type": content_type},
            data=data_buffer.read(),
        )

        upload_complete_url = (
            self.client.endpoint_url
            + "/datasets/"
            + self.uuid
            + "/files/upload-complete"
        )
        file_info_json = json.dumps({"id": upload_info["id"], "filename": file_name})
        response = self.client.do_request(
            "POST",
            upload_complete_url,
            headers={"content-type": "application/json"},
            data=file_info_json,
        )
        dataset = self.client.get_dataset(uuid=self.uuid)
        self.__update_dataset(dataset)

        response_json = self.client.response_to_json(response)
        if file_access_audit_func is not None:
            file_access_audit_func(  # pylint: disable=not-callable
                FileAccessAudit(
                    self.uuid,
                    self.latest_version_number,
                    response_json["data"]["uuid"],
                    response_json["data"]["version"]["sequence_number"],
                    "write",
                ).to_dict()
            )

    def create_csv_file(self, file_name: str, data_frame: pd.DataFrame):
        """
        description:    the function is used to create
                        a new csv file in the dataset

        arguments:      file_name - name of the new csv file (must include extension)
                        data_frame - dataframe containing the csv data
        """
        buffer = io.BytesIO()
        data_frame.to_csv(buffer, index=False)
        buffer.seek(0)

        self.create_raw_file(buffer, file_name, "text/csv")

    def create_json_file(self, file_name: str, data_frame: pd.DataFrame):
        """
        description:    the function is used to create
                        a new json file in the dataset

        arguments:      file_name - name of the new json file (must include extension)
                        data_frame - dataframe containing the json data
        """
        buffer = io.BytesIO()
        data_frame.to_json(buffer)
        buffer.seek(0)
        self.create_raw_file(buffer, file_name, "application/json")

    def create_spreadsheet_file(self, file_name: str, data_frame: pd.DataFrame):
        """
        description:    the function is used to create
                        a new spreadsheet file in the dataset

        arguments:      file_name - name of the new spreadsheet file (must include extension)
                        data_frame - dataframe containing the spreadsheet data
        """
        spread_sheet_type = os.path.splitext(file_name)[1]
        content_type = ""
        if spread_sheet_type == ".xls":
            content_type = "application/vnd.ms-excel"
        elif spread_sheet_type == ".xlsx":
            content_type = (
                "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )
        elif spread_sheet_type == ".ods":
            content_type = "application/vnd.oasis.opendocument.spreadsheet"
        else:
            raise ValueError("Unsupported spreadsheet type")

        buffer = io.BytesIO()
        with pd.ExcelWriter(  # pylint: disable=abstract-class-instantiated
            buffer
        ) as writer:
            data_frame.to_excel(writer, index=False)
        buffer.seek(0)
        self.create_raw_file(buffer, file_name, content_type)

    def create_parquet_file(self, file_name: str, data_frame: pd.DataFrame):
        """
        description:    the function is used to create
                        a new parquet file in the dataset

        arguments:      file_name - name of the new parquet file (must include extension)
                        data_frame - dataframe containing the parquet data
        """
        buffer = io.BytesIO()
        data_frame.to_parquet(buffer)
        buffer.seek(0)
        self.create_raw_file(buffer, file_name, "application/vnd.apache.parquet")

    def latest(self):
        """
        Returns the latest version of the dataset in the form
        of a DatasetVersion instance
        """
        dataset = self.client.get_dataset(uuid=self.uuid)
        return DatasetVersion(self, dataset.version)

    def get_version(self, dataset_version: int):
        """
        This function is going to return a requested
        version of the dataset
        """

        dataset_url = self.client.endpoint_url + "/datasets/" + self.uuid
        client_response = self.client.do_request(
            "GET", dataset_url, params={"dataset_version": dataset_version}
        )
        response_json = self.client.response_to_json(client_response)
        dataset_df = pd.json_normalize(response_json["data"], sep="_")
        dataset = Dataset(dataset_df.iloc[0].to_dict(), self)
        if dataset:
            return DatasetVersion(self, dataset.version)
        return None

    def __eq__(self, other):
        """
        compares objects of Dataset class. Note: does not
        compare the session attribute.
        """
        if not isinstance(other, Dataset):
            return NotImplemented
        return (
            self.uuid == other.uuid
            and self.public == other.public
            and self.thumbnail == other.thumbnail
            and self.created_at == other.created_at
            and self.updated_at == other.updated_at
            and self.owner_id == other.owner_id
            and self.owner_username == other.owner_username
        )

    def __repr__(self):
        return f"""Dataset(
            uuid: {self.uuid}
            public: {self.public}
            owner_id: {self.owner_id}
            owner_username: {self.owner_username}
            thumbnail: {self.thumbnail}
            created_at: {self.created_at}
            updated_at: {self.updated_at}
            latest_version_number: {self.version["sequence_number"]}
            client: {{
                endpoint_url: {self.client.endpoint_url}
            }}
        )"""

    def __str__(self):
        return f"Dataset(uuid: {self.uuid}, created_at: {self.created_at}, updated_time: {self.updated_at})"

    def __update_dataset(self, dataset):
        """
        updates current dataset attributes using another dataset
        """
        self.uuid = dataset.uuid
        self.latest_version_number = dataset.latest_version_number
        self.version = dataset.version
        self.public = dataset.public
        self.thumbnail = dataset.thumbnail
        self.updated_at = dataset.updated_at


class DatasetVersion:
    """
    This class represents a specific version of UnboundedDataset.
    Used to get files associated with this version of the dataset.
    """

    def __init__(self, dataset: Dataset, version: dict):
        self.dataset = dataset
        self.sequence_number = version["sequence_number"]
        self.name = version["name"]
        self.description = version["description"]
        self.created_at = version["created_at"]
        self.files = None
        if "files" in version:
            self.files = version["files"]

    def get_file(self, file_name: str):
        """
        description:    queries an endpoint for a file with a given
                        name associated with the current version of a
                        dataset. Stores the file contents in a DatasetFile
                        instance.
        arguments:      file_name - name of the requested file
        returns:        DatasetFile instance with file contents
        """
        if self.files:
            for file in self.files:
                if file["version"]["filename"] == file_name:
                    return DatasetFile(
                        self.dataset.uuid,
                        self.sequence_number,
                        file,
                        self.dataset.client,
                    )
        return None

    def __repr__(self):
        return f"""DatasetVersion(
            dataset: Dataset(
            uuid: {self.dataset.uuid}
            public: {self.dataset.public}
            owner_id: {self.dataset.owner_id}
            owner_username: {self.dataset.owner_username}
            thumbnail: {self.dataset.thumbnail}
            created_at: {self.created_at}
            updated_at: {self.dataset.updated_at}
            latest_version_number: {self.dataset.version["sequence_number"]}
            client: {{
                endpoint_url: {self.dataset.client.endpoint_url}
            }})
            sequence_number: {self.sequence_number}
            name: {self.name}
            description: {self.description}
            create_at: {self.created_at}
            files: {self.files}
        )"""

    def __str__(self):
        return f"DatasetVersion(uuid: {self.dataset.uuid}, sequence_number: {self.sequence_number}, created_at: {self.created_at})"


class DatasetFile:
    """
    This class is used to store the details of a file from
    a DatasetVersion. Used to pull the data from the endpoint,
    covert it to different types and save as a file.
    """

    def __init__(
        self, dataset_uuid: str, dataset_version: int, file_desc: dict, client: Client
    ):
        self.dataset_uuid = dataset_uuid
        self.dataset_version = dataset_version
        self.uuid = file_desc["uuid"]
        self.created_at = file_desc["created_at"]
        self.filename = file_desc["version"]["filename"]
        self.size = file_desc["version"]["size"]
        self.version = file_desc["version"]["sequence_number"]
        self.version_created_at = file_desc["version"]["created_at"]
        self.file_type = os.path.splitext(self.filename)[1]
        self.client = client

    def as_df(self):
        """
        converts the file contents into a dataframe
        """

        if self.file_type == ".csv":
            return pd.read_csv(self.raw(), sep=",")
        if self.file_type == ".json":
            return pd.read_json(self.raw())
        if self.file_type in (".xls", ".xlsx", ".ods"):
            try:
                buffer = self.raw()
                dataframe = pd.read_excel(buffer)
                return dataframe
            except ModuleNotFoundError as error:
                raise ModuleNotFoundError(
                    f"Missing optional dependency. {error.msg}"
                ) from error

        if self.file_type == ".parquet":
            return pd.read_parquet(self.raw())

        raise ValueError("Unsupported file type")

    def raw(self):
        """
        converts the file contents into a bytes buffer
        """
        file_url = (
            self.client.endpoint_url
            + "/datasets/"
            + self.dataset_uuid
            + "/files/"
            + self.uuid
        )
        parameters = {"dataset_version": self.dataset_version}
        resp = self.client.do_request("GET", file_url, params=parameters)

        if file_access_audit_func is not None:
            file_access_audit_func(  # pylint: disable=not-callable
                FileAccessAudit(
                    self.dataset_uuid,
                    self.dataset_version,
                    self.uuid,
                    self.version,
                    "read",
                ).to_dict()
            )
        return self.client.response_to_bytes_buffer(resp)

    def __repr__(self):
        return f"""DatasetFile(
            dataset_uuid: {self.dataset_uuid}
            dataset_version: {self.dataset_version}
            file_uuid: {self.uuid}
            filename: {self.filename}
            version: {self.version}
            size: {self.size}
            created_at: {self.created_at}
            client: {{
                endpoint_url: {self.client.endpoint_url}
            }}
        )"""

    def __str__(self):
        return f"DatasetFile(file_uuid: {self.uuid}, filename: {self.filename}, version: {self.version}, size: {self.size})"
