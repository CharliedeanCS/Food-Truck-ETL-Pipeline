"""
# My first app
Here's our first attempt at using data to create a table:
"""

# pylint: disable=E0401
# pylint: disable=C0301
# pylint: disable=W0612

import pandas as pd
import streamlit as st

from database import get_database_connection, load_data, format_all_data
from visuals import create_transactions_bar_chart, create_sideways_value_bar_chart, transaction_by_day_pie_chart, average_price_line_chart


def create_sidebar(trucks: pd.DataFrame) -> pd.DataFrame:
    """Creates a sidebar for users to select from data"""

    st.sidebar.header("Please Filter Here:")
    truck_name = st.sidebar.multiselect(
        "Select the Truck ID:",
        options=trucks["truck_name"].unique(),
        default=trucks["truck_name"].unique()
    )

    day = st.sidebar.multiselect(
        "Select the day of the week:",
        options=trucks["day"].unique(),
        default=trucks["day"].unique(),
    )

    payment_type = st.sidebar.multiselect(
        "Select the payment type:",
        options=trucks["payment_type"].unique(),
        default=trucks["payment_type"].unique()
    )

    trucks_selection = trucks.query(
        "truck_name == @truck_name & day ==@day & payment_type == @payment_type"
    )

    if trucks_selection.empty:
        st.warning("No data available based on the current filter settings!")
        st.stop()

    return trucks_selection


def create_main_page(selection: pd.DataFrame) -> None:
    """Creates the statistics on the mainpage of the dashboard"""

    st.title(":bar_chart: Truck Sales Dashboard")
    st.markdown("##")

    # TOP STATS
    total_sales = int(selection["total_price"].sum())
    average_transaction_price = round(selection["total_price"].mean(), 2)
    best_selling_truck = selection["truck_name"].value_counts()[0]

    left_column, middle_column, right_column = st.columns(3)
    with left_column:
        st.subheader("Total Sales:")
        st.subheader(f"UK  £{total_sales}")
    with middle_column:
        st.subheader("Average Price:")
        st.subheader(f"£{average_transaction_price}")
    with right_column:
        st.subheader("Best Selling Truck:")
        st.subheader(f"Truck 3 {best_selling_truck} sales!")

    st.markdown("""---""")


def show_raw_data(selection: pd.DataFrame) -> None:
    """Shows the raw data of the database"""
    if st.checkbox('Show raw data'):
        st.subheader('Raw data')
        st.write(selection)


def create_visuals(selection: pd.DataFrame):
    """Creates all visuals to represent the data in the database"""

    st.subheader(
        '-------------------------------------------------------------------------------')
    st.subheader('Total number of transactions for each truck.')

    st.altair_chart(create_transactions_bar_chart(selection),
                    use_container_width=True, theme="streamlit")

    st.subheader(
        '-------------------------------------------------------------------------------')
    st.subheader('Total transaction value for each truck.')

    st.altair_chart(create_sideways_value_bar_chart(selection),
                    use_container_width=True, theme="streamlit")

    st.subheader(
        '-------------------------------------------------------------------------------')
    st.subheader('Amount of transactions each day of the week.')

    st.altair_chart(transaction_by_day_pie_chart(selection),
                    use_container_width=True, theme="streamlit")

    st.subheader(
        '-------------------------------------------------------------------------------')
    st.subheader(' Average total price for each truck.')

    st.altair_chart(average_price_line_chart(selection),
                    use_container_width=True, theme="streamlit")


def add_csv_footer():
    """Hide the streamlit style of the page"""

    hide_st_style = """
                <style>
                #MainMenu {visibility: hidden;}
                footer {visibility: hidden;}
                header {visibility: hidden;}
                </style>
                """
    st.markdown(hide_st_style, unsafe_allow_html=True)


if __name__ == "__main__":

    conn = get_database_connection()

    truck_data = load_data(conn)

    truck_data = format_all_data(truck_data)

    selection_data = create_sidebar(truck_data)

    create_main_page(selection_data)

    show_raw_data(selection_data)

    create_visuals(selection_data)

    add_csv_footer()
