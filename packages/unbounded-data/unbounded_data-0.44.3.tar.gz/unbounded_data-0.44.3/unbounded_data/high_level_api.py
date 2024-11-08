from typing import Union, Optional
import asyncio
import re
import csv
import json
from io import StringIO, BytesIO

import pandas as pd

from .datasets import Client, Dataset


class UnboundedDataError(RuntimeError):
    """
    High-level API error.
    """


def _refresh_client(client: Optional[Client] = None) -> Client:
    """
    description:    creates or reuses a global Client object. can use user-provided object instead.

    arguments:      client - user-provided Client to use.

    returns:        Client structure.
    """

    if client is not None:
        return client

    return Client()


def _desynchronize_async_helper(to_return: any, sync: bool = True) -> Union[asyncio.Future, any]:
    """
    description:    returns a value that was generated synchronously in a Future.

    arguments:      to_return - input value.
                    sync - whether to return the value directly or wrap it in a complete Future.

    returns:        Future or return value
    """

    if sync:
        return to_return

    future = asyncio.Future()
    future.set_result(to_return)
    return future


def _guess_mime_type(check_bytes: bytes) -> str:
    """
    description:    guesses MIME type. raises with a nice error if magic is not installed.

    arguments:      check_bytes - byte array to autodetect.

    returns:        MIME type.
    """

    try:
        # pylint: disable-next=import-outside-toplevel
        import magic

        return magic.from_buffer(check_bytes, mime=True)
    except ImportError as exc:
        raise ImportError('Python-Magic is required to detect MIME type automatically') from exc


def _get_dataset_from_arg(dataset_name_or_id: Union[Dataset, str], client: Client) -> Optional[Dataset]:
    """
    description:    returns dataset by either it's direct value, UUID, or name. guesses parameter type.

    arguments:      dataset_name_or_id - value to guess.

    returns:        Dataset instance, if found.
    """

    if isinstance(dataset_name_or_id, Dataset):
        dataset = _desynchronize_async_helper(dataset_name_or_id, sync=False)
    elif re.match(r'^[A-Fa-f0-9]{8}-[A-Fa-f0-9]{4}-[A-Fa-f0-9]{4}-[A-Fa-f0-9]{4}-[A-Fa-f0-9]{12}$', dataset_name_or_id):
        dataset = client.get_dataset(uuid=dataset_name_or_id)
    else:
        dataset = client.get_dataset(name=dataset_name_or_id)
    return dataset


def read_file(dataset_name_or_id: Union[Dataset, str],
              file_name: str,
              sync: bool = True,
              client: Optional[Client] = None) -> Union[asyncio.Future[bytes], bytes]:
    """
    description:    reads file from dataset as bytes.

    arguments:      dataset_name_or_id - either Dataset object, UUID string or name.
                    file_name - file name to read.
                    sync - whether to run the request synchronously or asynchronously. await is required if sync is false.
                    client - custom Client structure, if any.

    returns:        file content.
    """

    def read_file_func():
        real_client = _refresh_client(client=client)
        dataset = _get_dataset_from_arg(dataset_name_or_id, client=real_client)
        if not dataset:
            raise UnboundedDataError('Dataset does not exist')
        dataset_version = dataset.latest()
        if not dataset_version:
            raise UnboundedDataError('File does not exist (dataset is empty)')
        file = dataset_version.get_file(file_name)
        if not file:
            raise UnboundedDataError('File does not exist')
        buf = file.raw()
        buf.seek(0)
        return buf.read()

    return _desynchronize_async_helper(read_file_func(), sync=sync)


def write_file(dataset_name_or_id: Union[Dataset, str],
               file_name: str,
               content: Union[str, bytes],
               mime_type: Optional[str] = None,
               sync: bool = True,
               client: Optional[Client] = None) -> Optional[asyncio.Future]:
    """
    description:    writes bytes to a dataset as file.

    arguments:      dataset_name_or_id - either Dataset object, UUID string or name.
                    file_name - file name to write.
                    content - bytes or string.
                    mime_type - MIME type. preferred. will try to guess with 'magic' module if this is not specified.
                    sync - whether to run the request synchronously or asynchronously. await is required if sync is false.
                    client - custom Client structure, if any.

    returns:        future or nothing.
    """

    if mime_type is None:
        mime_type = _guess_mime_type(mime_type)

    if not isinstance(content, bytes):
        content = content.encode('utf-8')

    buf = BytesIO()
    buf.write(content)
    buf.seek(0)

    def write_file_func():
        real_client = _refresh_client(client=client)
        dataset = _get_dataset_from_arg(dataset_name_or_id, client=real_client)
        if not dataset:
            raise UnboundedDataError('Dataset does not exist')
        dataset.create_raw_file(buf, file_name, mime_type)

    return _desynchronize_async_helper(write_file_func(), sync=sync)


def read_json(dataset_name_or_id: Union[Dataset, str],
              file_name: str,
              sync: bool = True,
              client: Optional[Client] = None) -> Union[Union[dict, list, str, bool, int, float, None],
                                                        asyncio.Future[dict, list, str, bool, int, float, None]]:
    """
    description:    reads file from dataset as JSON.

    arguments:      dataset_name_or_id - either Dataset object, UUID string or name.
                    file_name - file name to read.
                    sync - whether to run the request synchronously or asynchronously. await is required if sync is false.
                    client - custom Client structure, if any.

    returns:        parsed JSON object.
    """

    return _desynchronize_async_helper(json.loads(read_file(dataset_name_or_id, file_name, sync=True, client=client)), sync=sync)


def write_json(dataset_name_or_id: Union[Dataset, str],
               file_name: str,
               content: any,
               sync: bool = True,
               client: Optional[Client] = None) -> Optional[asyncio.Future]:
    """
    description:    writes JSON-serializable object to a dataset as file.

    arguments:      dataset_name_or_id - either Dataset object, UUID string or name.
                    file_name - file name to write.
                    content - any value serializable with `json.dumps()`.
                    sync - whether to run the request synchronously or asynchronously. await is required if sync is false.
                    client - custom Client structure, if any.

    returns:        future or nothing.
    """

    bytes_content = json.dumps(content).encode('utf-8')
    return write_file(dataset_name_or_id, file_name, bytes_content, mime_type='application/json', sync=sync, client=client)


def read_csv(dataset_name_or_id: Union[Dataset, str],
             file_name: str,
             sync: bool = True,
             client: Optional[Client] = None,
             sep: str = ',') -> Union[asyncio.Future[pd.DataFrame], pd.DataFrame]:
    """
    description:    reads CSV file from dataset as DataFrame.

    arguments:      dataset_name_or_id - either Dataset object, UUID string or name.
                    file_name - file name to read.
                    sync - whether to run the request synchronously or asynchronously. await is required if sync is false.
                    client - custom Client structure, if any.
                    sep - column separator, defaults to comma (,).

    returns:        DataFrame.
    """

    as_bytes = read_file(dataset_name_or_id, file_name, sync=True, client=client)
    buf = StringIO()
    buf.write(as_bytes.decode('utf-8', errors='surrogateescape'))
    buf.seek(0)
    return _desynchronize_async_helper(pd.read_csv(buf, engine='python', sep=sep), sync=sync)


def read_tsv(dataset_name_or_id: Union[Dataset, str],
             file_name: str,
             sync: bool = True,
             client: Optional[Client] = None) -> Union[asyncio.Future[pd.DataFrame], pd.DataFrame]:
    """
    description:    reads TSV file from dataset as DataFrame.

    arguments:      dataset_name_or_id - either Dataset object, UUID string or name.
                    file_name - file name to read.
                    sync - whether to run the request synchronously or asynchronously. await is required if sync is false.
                    client - custom Client structure, if any.

    returns:        DataFrame.
    """

    return read_csv(dataset_name_or_id, file_name, sync=sync, client=client, sep='\t')


def write_csv(dataset_name_or_id: Union[Dataset, str],
              file_name: str,
              content: Union[pd.DataFrame, list[list]],
              sync: bool = True,
              client: Optional[Client] = None,
              sep: str = ',') -> Optional[asyncio.Future]:
    """
    description:    writes Python-style CSV or Pandas DataFrame to a dataset as CSV file.

    arguments:      dataset_name_or_id - either Dataset object, UUID string or name.
                    file_name - file name to write.
                    content - list of lists of str or a DataFrame.
                    sync - whether to run the request synchronously or asynchronously. await is required if sync is false.
                    client - custom Client structure, if any.
                    sep - column separator, defaults to comma (,).

    returns:        future or nothing.
    """

    mime_type = 'text/csv'
    if sep == '\t':
        mime_type = 'text/tab-separated-values'

    buf = StringIO()
    if isinstance(content, list):
        writer = csv.writer(buf)
        writer.writerows(content)
    else:
        content.to_csv(buf, index=False, sep=sep)
    buf.seek(0)
    bytes_content = buf.read().encode('utf-8', errors='surrogateescape')
    return write_file(dataset_name_or_id, file_name, bytes_content, mime_type=mime_type, sync=sync, client=client)


def write_tsv(dataset_name_or_id: Union[Dataset, str],
              file_name: str,
              content: Union[pd.DataFrame, list[list]],
              sync: bool = True,
              client: Optional[Client] = None) -> Optional[asyncio.Future]:
    """
    description:    writes Python-style CSV or Pandas DataFrame to a dataset as TSV file.

    arguments:      dataset_name_or_id - either Dataset object, UUID string or name.
                    file_name - file name to write.
                    content - list of lists of str or a DataFrame.
                    sync - whether to run the request synchronously or asynchronously. await is required if sync is false.
                    client - custom Client structure, if any.

    returns:        future or nothing.
    """

    return write_csv(dataset_name_or_id, file_name, content, sync=sync, client=client, sep='\t')


def read_parquet(dataset_name_or_id: Union[Dataset, str],
                 file_name: str,
                 sync: bool = True,
                 client: Optional[Client] = None) -> Union[asyncio.Future[pd.DataFrame], pd.DataFrame]:
    """
    description:    reads Parquet file from dataset as DataFrame.

    arguments:      dataset_name_or_id - either Dataset object, UUID string or name.
                    file_name - file name to read.
                    sync - whether to run the request synchronously or asynchronously. await is required if sync is false.
                    client - custom Client structure, if any.

    returns:        DataFrame.
    """

    as_bytes = read_file(dataset_name_or_id, file_name, sync=True, client=client)
    buf = BytesIO()
    buf.write(as_bytes)
    buf.seek(0)
    return _desynchronize_async_helper(pd.read_parquet(buf), sync=sync)


def write_parquet(dataset_name_or_id: Union[Dataset, str],
                  file_name: str,
                  content: Union[list[list], pd.DataFrame],
                  sync: bool = True,
                  client: Optional[Client] = None) -> Optional[asyncio.Future]:
    """
    description:    writes Python-style CSV or Pandas DataFrame to a dataset as Parquet file.

    arguments:      dataset_name_or_id - either Dataset object, UUID string or name.
                    file_name - file name to write.
                    content - list of lists of str or a DataFrame.
                    sync - whether to run the request synchronously or asynchronously. await is required if sync is false.
                    client - custom Client structure, if any.

    returns:        future or nothing.
    """

    if isinstance(content, list):
        content = pd.DataFrame(content[1:], columns=content[0])
    buf = BytesIO()
    content.to_parquet(buf, index=False)
    buf.seek(0)
    content_bytes = buf.read()
    return write_file(dataset_name_or_id, file_name, content_bytes, mime_type='application/vnd.apache.parquet', sync=sync, client=client)


def list_files(dataset_name_or_id: Union[Dataset, str],
               sync: bool = True,
               client: Optional[Client] = None) -> Union[asyncio.Future[list[str]], list[str]]:
    """
    description:    retrieves the list of filenames in a dataset.

    arguments:      dataset_name_or_id - either Dataset object, UUID string or name.
                    sync - whether to run the request synchronously or asynchronously. await is required if sync is false.
                    client - custom Client structure, if any.

    returns:        list of strings.
    """

    def read_list_func():
        real_client = _refresh_client(client=client)
        dataset = _get_dataset_from_arg(dataset_name_or_id, client=real_client)
        if not dataset:
            raise UnboundedDataError('Dataset does not exist')
        dataset_version = dataset.latest()
        if not dataset_version or not dataset_version.files:
            return []
        return list(sorted({x['version']['filename'] for x in dataset_version.files if 'version' in x and 'filename' in x['version']}))

    return _desynchronize_async_helper(read_list_func(), sync=sync)


__all__ = ['read_file', 'write_file',
           'read_csv', 'write_csv',
           'read_tsv', 'write_tsv',
           'read_json', 'write_json',
           'read_parquet', 'write_parquet',
           'list_files',
           'UnboundedDataError']
