"""
This Script loads the csv truck transactions data into a redshift database.
@author:Charlie Dean
"""

# pylint: disable=R1721
# pylint: disable=E1136
# pylint: disable=C0103
# pylint: disable=E0401

from os import environ
import csv

from dotenv import load_dotenv
import redshift_connector

from extract import get_latest_time_information

MAX_ROW_LENGTH = 4
FOLDER_PATH = "./trucks"


def get_database_connection() -> redshift_connector.Connection:
    """Return a connection our database"""

    return redshift_connector.connect(user=environ["DATABASE_USERNAME"],
                                      password=environ["DATABASE_PASSWORD"],
                                      host=environ["DATABASE_IP"],
                                      port=environ["DATABASE_PORT"],
                                      database=environ["DATABASE_NAME"]
                                      )


def load_csv_files(date: str, time: str, year: str, month: str) -> list[dict]:
    """Loads all csv files into one dictionary"""

    with open(f"{FOLDER_PATH}/{year}-{month}/{date}/{time}/truck-{year}-{month}-{date}-{time}.csv",
              'r', encoding="utf-8") as transactions_csv:
        parsed_csv = csv.reader(transactions_csv)

        transactions_list = [row for row in parsed_csv][1:]

    return transactions_list


def create_transactions_list(current_transactions: list, amount_of_rows: int) -> list:
    """Creates an easy to insert transactions list"""

    transactions_data = []

    for index, transaction in enumerate(current_transactions):
        if len(transaction) != MAX_ROW_LENGTH:
            raise ValueError(
                "transactions csv must contain the correct information")

        if index == amount_of_rows:
            break

        payment_type = 1
        at = transaction[0]
        price = float(transaction[2])
        truck_id = transaction[3]

        if transaction[1] == "cash":
            payment_type = 2

        transactions_data.append(
            [price, at, int(payment_type), int(truck_id)])

    return transactions_data


def upload_transaction_data(db_connection: redshift_connector.Connection,
                            transactions_list: list) -> None:
    """Uploads transaction data to the database."""

    curr = redshift_connector.Cursor = db_connection.cursor()

    query = """INSERT INTO charlie_schema.transactions(total_price,at,payment_type_id,truck_id)
    VALUES (%s,%s,%s,%s)"""

    curr.executemany(query, transactions_list)

    db_connection.commit()


if __name__ == "__main__":

    load_dotenv()

    connection = get_database_connection()

    current_time = get_latest_time_information()

    transactions = load_csv_files(
        current_time["day"], current_time["hour"], current_time["year"], current_time["month"])

    transactions_filtered = create_transactions_list(transactions, 1000)

    upload_transaction_data(connection, transactions_filtered)
