"""ETL pipeline to handle truck transactional data"""

# pylint: disable=C0301

from argparse import ArgumentParser, Namespace

from dotenv import load_dotenv

from extract import download_truck_data_files, load_s3_client, remove_old_file, get_latest_time_information
from transform import merge_csv_files, validate_dataframe
from load import get_database_connection, load_csv_files, create_transactions_list, upload_transaction_data

MIN_ROW_FETCH_COUNT = 5042


def setup_argparse() -> dict:
    """Creates an argument parser allowing terminal input"""

    parser = ArgumentParser(description="Basic functionality of ArgParse")

    parser.add_argument(
        "--rows", help="Optional argument for the amount of rows")

    args: Namespace = parser.parse_args()

    index = MIN_ROW_FETCH_COUNT

    if args.rows is not None and args.rows.isdigit():
        index = int(args.rows)

    return index


if __name__ == "__main__":

    time = get_latest_time_information()

    try:
        remove_old_file(time["day"], time["hour"], time["year"], time["month"])
    except FileNotFoundError:
        pass

    load_dotenv()
    ROWS = setup_argparse()

    s3 = load_s3_client()

    try:

        download_truck_data_files(
            s3, "sigma-resources-truck", ".csv", time["day"], time["hour"], time["year"], time["month"])
        download_truck_data_files(
            s3, "sigma-resources-truck", ".xlsx", time["day"], time["hour"], time["year"], time["month"])

        merge_csv_files(time["day"], time["hour"], time["year"], time["month"])
        validate_dataframe(time["day"], time["hour"],
                           time["year"], time["month"])

        connection = get_database_connection()

        transactions = load_csv_files(
            time["day"], time["hour"], time["year"], time["month"])

        transactions_filtered = create_transactions_list(transactions, ROWS)

        upload_transaction_data(connection, transactions_filtered)

    except FileNotFoundError:
        print("No Previous Data")
