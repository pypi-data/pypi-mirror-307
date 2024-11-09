import os
import logging
from .formatter import format_size
from .pkg_util import ensure_package

logger = logging.getLogger(__name__)


def is_google_spreadsheets_link(uri: str) -> bool:
    google_spreadsheets_prefixes = (
        "https://docs.google.com/spreadsheets/",
        "https://docs.google.com/spreadsheets/d/",
    )
    return uri.startswith(google_spreadsheets_prefixes)


def _check_credentials():
    creds = os.environ.get("GOOGLE_APPLICATION_CREDENTIALS", None)
    if creds is None:
        raise ValueError("GOOGLE_APPLICATION_CREDENTIALS is required")

    if not os.path.exists(creds):
        raise ValueError(f"GOOGLE_APPLICATION_CREDENTIALS not found: {creds}")


def process_google_spreadsheets(uri, **kwargs):
    ensure_package("gspread", "gspread", "6.1.3")
    ensure_package("cloud_sheets_slim", "cloud_sheets_slim", "0.1.3")

    from cloud_sheets_slim import CloudSheetsSlim
    from cloud_storage_size import get_bucket_objects_count_and_bytes
    _check_credentials()

    sheet_name = kwargs.get("sheet_name", "Sheet1")
    bucket_column_name = kwargs.get("bucket_column_name", "bucket")
    count_column_name = kwargs.get("count_column_name", "count")
    bytes_column_name = kwargs.get("bytes_column_name", "bytes")
    bytes_formatted_column_name = kwargs.get("bytes_column_name", "bytes_formatted")

    cloud_sheet = CloudSheetsSlim(uri, sheet_name)
    rows = cloud_sheet.find({})

    bucket_uri_list = [row.get(bucket_column_name, None) for row in rows]

    filtered_bucket_uri_list = list(filter(lambda x: x is not None, bucket_uri_list))

    logger.info(filtered_bucket_uri_list)
    for bucket_uri in filtered_bucket_uri_list:
        value = get_bucket_objects_count_and_bytes(bucket_uri)
        update_object = {
            count_column_name: value["count"],
            bytes_column_name: value["bytes"],
            bytes_formatted_column_name: format_size(value["bytes"], decimal_places=4),
        }
        logger.info(update_object)
        cloud_sheet.update_one(
            {
                bucket_column_name: bucket_uri
            },
            update_object,
            upsert=True,
        )
