"""Extracts data from the s3 buckets found on AWS."""

# pylint: disable=C0103
# pylint: disable=E1136
# pylint: disable=E0401
# pylint: disable=R0913

from os import environ, path, remove
from pathlib import Path
import datetime

from dotenv import load_dotenv
from boto3 import client


FOLDER_PATH = "./trucks"


def load_s3_client() -> client:
    """Loads an S3 client."""

    s3_client = client("s3", aws_access_key_id=environ["AWS_ACCESS_KEY_ID"],
                       aws_secret_access_key=environ["AWS_SECRET_ACCESS_KEY"])

    return s3_client


def get_object_keys(s3_client: client, bucket: str, date: str,
                    time: str, year: str, month: str) -> list[str]:
    """Returns a list of object keys"""

    contents = s3_client.list_objects(Bucket=bucket)["Contents"]

    parquet_name = f"trucks/{year}-{month}/{date}/{time}"
    xlsx_name = "metadata/details"

    return [content["Key"] for content in contents if parquet_name in content["Key"]
            or xlsx_name in content["Key"]]


def download_truck_data_files(s3_client: client, bucket: str, file_type: str, date: str,
                              time: str, year: str, month: str) -> None:
    """Downloads all files from a bucket to a given folder."""

    keys = get_object_keys(s3_client, bucket, date, time, year, month)

    for k in keys:
        if file_type in k:
            # remove the file name from the object key
            obj_path = path.dirname(k)

            # create nested directory structure
            Path(obj_path).mkdir(parents=True, exist_ok=True)

            # save file with full path locally
            s3_client.download_file(bucket, k, k)


def remove_old_file(date: str, time: str, year: str, month: str):
    """Removes the old data from the directory"""
    try:
        remove(
            f"{FOLDER_PATH}/{year}-{month}/{date}/{time}/truck-{year}-{month}-{date}-{time}.csv")
    except FileNotFoundError:
        pass


def get_latest_time_information() -> dict:
    """Gets today's date and the last hour that is dividable by 3"""

    current_date = datetime.datetime.now()

    current_hour = current_date.hour
    hour_incorrect = True

    while hour_incorrect:
        if current_hour % 3 == 0:
            hour_incorrect = False
        else:
            current_hour -= 1

    return {"year": current_date.year, "month": current_date.month,
            "day": current_date.day, "hour": current_hour}


if __name__ == "__main__":

    remove_old_file("27", "12", "2023", "11")

    load_dotenv()

    s3 = load_s3_client()

    current_time = get_latest_time_information()

    print(get_object_keys(s3, "sigma-resources-truck",
          current_time["day"], current_time["hour"], current_time["year"], current_time["month"]))

    download_truck_data_files(
        s3, "sigma-resources-truck", ".csv", current_time["day"],
        current_time["hour"], current_time["year"], current_time["month"])
    download_truck_data_files(
        s3, "sigma-resources-truck", ".xlsx", current_time["day"],
        current_time["hour"], current_time["year"], current_time["month"])
