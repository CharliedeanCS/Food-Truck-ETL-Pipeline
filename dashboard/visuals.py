"""All functions to connect and organise the database"""

# pylint: disable=E0401
# pylint: disable=W0612

import altair as alt
import pandas as pd


def create_transactions_bar_chart(selection: pd.DataFrame) -> alt.Chart:
    """Creates a normal bar chart representing the total transactions"""

    base_transactions = alt.Chart(selection).encode(
        x="truck_name:O",
        y='count(total_price)',
        text='count(total_price)',
        color='truck_name'
    )

    number_of_transactions = base_transactions.mark_bar(
    ) + base_transactions.mark_text(align='center', dy=-5)

    return number_of_transactions


def create_sideways_value_bar_chart(selection: pd.DataFrame) -> alt.Chart:
    """Creates a sideways bar chart"""

    base_value = alt.Chart(selection).encode(
        x="sum(total_price)",
        y='truck_name:O',
        text='sum(total_price)',
        color='truck_name'
    )

    total_transactions = base_value.mark_bar(
    ) + base_value.mark_text(align='center', dx=20)

    return total_transactions


def transaction_by_day_pie_chart(selection: pd.DataFrame) -> alt.Chart:
    """Creates a pie chart for the amount of sales each day"""

    base_popularity = alt.Chart(selection).encode(
        theta="count(payment_type)",
        color="day"
    )

    popularity_by_day = base_popularity.mark_arc()

    return popularity_by_day


def average_price_line_chart(selection: pd.DataFrame) -> alt.Chart:
    """Creates a line chart showing the average price at each truck"""

    base_average_price = alt.Chart(selection).encode(
        x="truck_name:O",
        y='average(total_price)',
        color=alt.value("#FFAA00")
    )

    average_price_per_truck = base_average_price.mark_line()

    return average_price_per_truck
