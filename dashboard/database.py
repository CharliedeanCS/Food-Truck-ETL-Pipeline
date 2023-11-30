"""All functions to connect and organise the database"""

# pylint: disable=E0401
# pylint: disable=W0612

from os import environ

from dotenv import load_dotenv
import redshift_connector
import pandas as pd


def get_database_connection() -> redshift_connector.Connection:
    """Return a connection our database"""

    load_dotenv()

    return redshift_connector.connect(user=environ["DATABASE_USERNAME"],
                                      password=environ["DATABASE_PASSWORD"],
                                      host=environ["DATABASE_IP"],
                                      port=environ["DATABASE_PORT"],
                                      database=environ["DATABASE_NAME"]
                                      )


def load_data(connection) -> pd.DataFrame:
    """Loads data from a redshift database to a pandas Dataframe"""

    with connection.cursor() as cur:
        cur.execute("""SELECT at,total_price,truck_id,
        charlie_schema.trucks.name AS truck_name,
        payment_type_id,
        charlie_schema.payment_type.payment_type_name AS payment_type 
        FROM charlie_schema.transactions
        INNER JOIN charlie_schema.trucks ON charlie_schema.transactions.truck_id =  charlie_schema.trucks.id
        INNER JOIN charlie_schema.payment_type ON 
        charlie_schema.transactions.payment_type_id = charlie_schema.payment_type.id;""")
        return cur.fetch_dataframe()


def format_all_data(trucks: pd.DataFrame) -> pd.DataFrame:
    """Creates new and formatted columns in pandas"""

    trucks['at'] = pd.to_datetime(trucks['at'])
    trucks['day'] = trucks['at'].dt.day_name()

    return trucks
