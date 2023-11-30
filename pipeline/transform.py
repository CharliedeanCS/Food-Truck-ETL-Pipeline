"""Transform script to merge and clean the truck data"""

# pylint: disable=C0121
# pylint: disable=E0401

from os import path, listdir, remove

import pandas as pd

from extract import get_latest_time_information


FOLDER_PATH = "./trucks"


def merge_csv_files(date: str, time: str, year: str, month: str) -> None:
    """Merges all csv files into one easy to read file."""

    all_files = listdir(f"{FOLDER_PATH}/{year}-{month}/{date}/{time}")
    csv_files = [file for file in all_files if file.endswith('.csv')]

    df_list = []

    for csv in csv_files:
        csv_file = pd.read_csv(
            f"{FOLDER_PATH}/{year}-{month}/{date}/{time}/{csv}")
        csv_file["id"] = csv[4]

        df_list.append(csv_file)
        remove(f"{FOLDER_PATH}/{year}-{month}/{date}/{time}/{csv}")

    big_data = pd.concat(df_list, ignore_index=True)

    big_data.to_csv(
        path.join(f"{FOLDER_PATH}/{year}-{month}/{date}/{time}",
                  f'truck-{year}-{month}-{date}-{time}.csv'), index=False)


def validate_dataframe(date: str, time: str, year: str, month: str):
    """Validates the data in the dataframe ensuring it is clean"""

    data_frame = pd.read_csv(
        f"{FOLDER_PATH}/{year}-{month}/{date}/{time}/truck-{year}-{month}-{date}-{time}.csv")

    data_frame = data_frame.rename(columns={
        "type": "payment_type",
        "total": "total_price",
        "id": "truck_id"
    })

    remove_words = data_frame.total_price.str.isalpha() == True
    data_frame = data_frame.drop(data_frame[remove_words].index)

    remove_missing_entry = data_frame.total_price.isna()
    data_frame = data_frame.drop(data_frame[remove_missing_entry].index)

    remove_extreme = (data_frame.total_price.astype(float) < 1) | (
        data_frame.total_price.astype(float) > 100)
    data_frame = data_frame.drop(data_frame[remove_extreme].index)

    data_frame['total_price'] = data_frame['total_price'].astype(float)

    data_frame.to_csv(
        path.join(f"{FOLDER_PATH}/{year}-{month}/{date}/{time}",
                  f'truck-{year}-{month}-{date}-{time}.csv'), index=False)


if __name__ == "__main__":

    current_time = get_latest_time_information()

    merge_csv_files(current_time["day"],
                    current_time["hour"], current_time["year"], current_time["month"])

    validate_dataframe(current_time["day"],
                       current_time["hour"], current_time["year"], current_time["month"])
