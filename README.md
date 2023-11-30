# Food-Truck-ETL-Pipeline

# Project Description

- Given a Case study and transactional data for food trucks. The following folders contain a operational ETL pipeline, a dashboard service hosted through streamlit and Terraform files to make AWS resources.

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
