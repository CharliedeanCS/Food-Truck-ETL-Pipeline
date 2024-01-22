# Food-Truck-ETL-Pipeline

# Project Description

- The aim of this project was to create a ETL pipeline that would extract data from a csv file located on a S3 bucket on AWS,transform the data ensuring it was clean and valid and load the transactional data taken from food trucks into a Redshift database then create visuals and a dashboard to show the performance of each truck, each location and current trends that are happening with the food truck business.

## 🛠️ Getting Setup
- Navigate to the pipeline folder and install requirements using `pip3 install -r requirements.txt`

## 🔐 Environment Variables
- Create a `.env` file with the following information:
- `DATABASE_IP` -> ARN to your AWS RDS.
- `DATABASE_NAME` -> Name of your database.
- `DATABASE_USERNAME` -> Your database username.
- `DATABASE_PASSWORD` -> Password to access your database.
- `DATABASE_PORT` -> Port used to access the database.
- `AWS_ACCESS_KEY_ID_ `  -> Personal AWS ACCESS KEY available on AWS.
- `AWS_SECRET_ACCESS_KEY_` -> Personal AWS SECRET ACCESS KEY available on AWS.

## 🗂️ Folders Explained

- `pipeline`
    - This folder contains the scripts that perform the extraction, transforming and loading of data into a database.
- `dashboard`
    - This folder contains all scripts to create and run the streamlit dashboard.
- `terraform`
    - This folder contains all files that init and builds AWS resources using terraform
