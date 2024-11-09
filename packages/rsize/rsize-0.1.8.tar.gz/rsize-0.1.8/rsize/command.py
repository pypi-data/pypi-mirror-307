import os
import json
import logging
import argparse

from dotenv import load_dotenv
from cloud_storage_size import get_bucket_objects_count_and_bytes
from rsize import __version__
from .formatter import format_size
from .google_spreadsheets import is_google_spreadsheets_link, process_google_spreadsheets

logger = logging.getLogger(__name__)
if os.environ.get('DEBUG') == '1':
    logging.basicConfig(level=logging.DEBUG)
else:
    logging.basicConfig(level=logging.INFO)


def load_config(config_file: str) -> dict:
    with open(config_file, 'r') as f:
        return json.load(f)


def main():
    parser = argparse.ArgumentParser(description='Calculate the size of files in Cloud Storage')
    parser.add_argument('uri', type=str, help='cloud storage bucket path (e.g., gs://bucket_name), cloud sheet uri (https://docs.google.com/spreadsheets/...)')
    parser.add_argument('-v', '--version', action='version', version=f'%(prog)s {__version__}')
    parser.add_argument('-c', '--config', type=str, help='Path to config file')
    parser.add_argument('-e', '--env-file', type=str, help='Path to .env file')
    parser.add_argument('-m', '--mode', type=str, help='Method to use for calculating the size of files in Cloud Storage. Options are: auto, rclone, metrics, sdk')
    parser.add_argument('-gid', '--gcs-project-id', type=str, help='Google Cloud project ID')
    parser.add_argument('-H', '--human-readable', action='store_true', help='Display sizes in human-readable format')

    args = parser.parse_args()

    if args.env_file:
        load_dotenv(args.env_file)
    else:
        load_dotenv()

    if args.config:
        config = load_config(args.config)
        for key, value in config.items():
            os.environ[key] = value

    input_uri = args.uri
    if is_google_spreadsheets_link(input_uri):
        process_google_spreadsheets(input_uri)
        return

    kwargs = {}
    if args.mode:
        kwargs["engine"] = args.mode
    if args.gcs_project_id:
        kwargs["project_id"] = args.gcs_project_id

    result = get_bucket_objects_count_and_bytes(input_uri, **kwargs)
    if result is None:
        logger.error("Failed to get bucket objects count and bytes")
        return

    count = result["count"]
    total_bytes = result["bytes"]

    # Display results
    if args.human_readable:
        total_size = format_size(total_bytes)
        print(f"Total objects: {count}")
        print(f"Total size: {total_size}")
    else:
        print(f"Total objects: {count}")
        print(f"Total size in bytes: {total_bytes}")

if __name__ == "__main__":
    main()
