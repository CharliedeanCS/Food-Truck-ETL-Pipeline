# Food-Truck-ETL-Pipeline

# Project Description

- The aim of this project was to create a ETL pipeline that would extract data from a csv file located on a S3 bucket on AWS,transform the data ensuring it was clean and valid and load the transactional data taken from food trucks into a Redshift database then create visuals and a dashboard to show the performance of each truck, each location and current trends that are happening with the food truck business.

## 🛠️ Getting Setup

'pip install -r requirements.txt'

.env keys used:
AWS_ACCESS_KEY_ID = xxxxxxxxxx
AWS_SECRET_ACCESS_KEY = xxxxxxxx
DATABASE_USERNAME = xxxxxxxx
DATABASE_PASSWORD = xxxxxxxx
DATABASE_IP = xxxxxxxxx
DATABASE_PORT = xxxxxxxx
DATABASE_NAME = xxxxxxxxx

## 🗂️ Folders Explained

- `pipeline`
    - This folder contains the scripts that perform the extraction, transforming and loading of data into a database.
- `dashboard`
    - This folder contains all scripts to create and run the streamlit dashboard.
- `terraform`
    - This folder contains all files that init and builds AWS resources using terraform
