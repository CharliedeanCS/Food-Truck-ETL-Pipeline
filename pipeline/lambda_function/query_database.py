"""Queries a database for the previous batch of data and creates a JSON report"""
from os import environ
import json
import datetime
from datetime import timedelta

from dotenv import load_dotenv
import redshift_connector
import pandas as pd

# pylint: disable=W0613


def get_database_connection() -> redshift_connector.Connection:
    """Return a connection our database"""

    return redshift_connector.connect(user=environ["DATABASE_USERNAME"],
                                      password=environ["DATABASE_PASSWORD"],
                                      host=environ["DATABASE_IP"],
                                      port=environ["DATABASE_PORT"],
                                      database=environ["DATABASE_NAME"]
                                      )


def query_previous_days_data(db_connection: redshift_connector.Connection) -> None:
    """Query's the database for the previous days data"""

    curr = redshift_connector.Cursor = db_connection.cursor()

    curr.execute("""SELECT * from charlie_schema.transactions
                 WHERE at > trunc(getdate())-1 AND at < trunc(getdate());""")

    result: pd.DataFrame = curr.fetch_dataframe()

    return result


def extract_data_from_trucks(trucks: pd.DataFrame) -> list:
    """Extracts the required data from the trucks dataframe"""

    trucks_number_of_transactions = trucks.groupby(['truck_id'])[
        'total_price'].count()
    trucks_transaction_sums = trucks.groupby(['truck_id'])[
        'total_price'].sum()

    truck_list = []

    for i in range(1, len(trucks_number_of_transactions)+1):
        singular_truck = {}
        trucks_dict = {
            "amount_of_transactions": trucks_number_of_transactions[i].item(),
            "total_transactions_sum": trucks_transaction_sums[i].item()}
        singular_truck[f"truck_{i}"] = trucks_dict
        truck_list.append(singular_truck)

    return truck_list


def create_html_string(trucks: dict, yesterday) -> str:
    """Creates a html string to create tables of data for the email report"""

    html_style = """
<head>
<style>
table {
}

td, th {
border: 1px solid #dddddd;
text-align: left;
padding: 8px;
}

tr:nth-child(even) {
background-color: #dddddd;
}
</style>
</head>"""
    body_beginning = f"""<body>

<h2>Daily Report for {yesterday}</h2>
<p>&nbsp;&nbsp;&nbsp;&nbsp;</p>
<h3>Collected Truck Data</h3>
<table>
<tr>
    <th>Metric</th>
    <th>Value</th>
</tr>
<tr>"""

    values_in_html = f"""<td>Total Number of Transactions</td>
<td>{trucks["all_trucks_transactions_count"]}</td>
</tr>
<tr>
<td>Total Sum of Transactions</td>
<td>{trucks["all_trucks_transactions_sum"]}</td>
</tr>
<tr>
<td>Total Average of Transactions</td>
<td>{trucks["all_trucks_transactions_average"]}</td>
</tr>
</table>

<p>&nbsp;&nbsp;&nbsp;&nbsp;</p>
<h3>Singular Truck Data</h3>

<table>
<tr>
<th>Truck ID</th>
<th>Amount of Transactions</th>
<th>Sum of Transactions</th>
</tr>
<tr>
    <td>1</td>
    <td>{trucks["trucks"][0]["truck_1"]["amount_of_transactions"]}</td>
    <td>{trucks["trucks"][0]["truck_1"]["total_transactions_sum"]}</td>
</tr>
<tr>
    <td>2</td>
    <td>{trucks["trucks"][1]["truck_2"]["amount_of_transactions"]}</td>
    <td>{trucks["trucks"][1]["truck_2"]["total_transactions_sum"]}</td>
</tr>
<tr>
    <td>3</td>
    <td>{trucks["trucks"][2]["truck_3"]["amount_of_transactions"]}</td>
    <td>{trucks["trucks"][2]["truck_3"]["total_transactions_sum"]}</td>
</tr>
<tr>
    <td>4</td>
    <td>{trucks["trucks"][3]["truck_4"]["amount_of_transactions"]}</td>
    <td>{trucks["trucks"][3]["truck_4"]["total_transactions_sum"]}</td>
</tr>
<tr>
    <td>5</td>
    <td>{trucks["trucks"][4]["truck_5"]["amount_of_transactions"]}</td>
    <td>{trucks["trucks"][4]["truck_5"]["total_transactions_sum"]}</td>
</tr>
<tr>
    <td>6</td>
    <td>{trucks["trucks"][5]["truck_6"]["amount_of_transactions"]}</td>
    <td>{trucks["trucks"][5]["truck_6"]["total_transactions_sum"]}</td>
</tr>
</table>

</body>"""
    updated_html = html_style + body_beginning + values_in_html

    updated_html = updated_html.replace("\n", "")

    return updated_html


def create_report_data(trucks: pd.DataFrame) -> dict:
    """Creates and calls all the data needed in the report"""

    yesterday = datetime.datetime.now().date() - timedelta(days=1)

    report_data_dict = {}

    report_data_dict["all_trucks_transactions_sum"] = trucks.total_price.sum()
    report_data_dict["all_trucks_transactions_count"] = trucks.total_price.count(
    ).item()
    report_data_dict["all_trucks_transactions_average"] = trucks.total_price.mean(
    ).item()

    report_data_dict["trucks"] = extract_data_from_trucks(trucks)

    exported_html = create_html_string(report_data_dict, yesterday)

    return {"html_body": exported_html}


def handler(event=None, context=None) -> int:
    """Handler for the lambda function"""

    try:

        load_dotenv()

        connection = get_database_connection()

        yesterdays_transaction_data = query_previous_days_data(connection)

        report_dict = create_report_data(yesterdays_transaction_data)

        return {
            'statusCode': 200,
            'body': json.dumps(report_dict["html_body"])
        }
    except Exception as e:
        return {
            'statusCode': 200,
            'body': json.dumps(e)
        }


if __name__ == "__main__":
    print(handler())
