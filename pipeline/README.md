# Pipeline

This folder should contain all code and resources required for the pipeline.

# Project Description

- This folder contains all the information needed to perform a ETL (Extract,Transform,Load) on truck data stored in a csv file to then upload it to a Redshift cluster.

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

## 🗂️ Files Explained

- `extract.py`
    - A script to extract data from the truck s3 bucket located on AWS
- `transform.py`
    - A script to merge and clean all the data found in a csv file to ensure its the correct format and contains the correct information.
- `load.py`
    - A script to load the cleaned csv output into a redshift cluster.
- `pipeline.py`
    - A script to load a CSV output into a Redshift Cluster.
    - Cleans the data (Making sure its in the correct format)
    - Uploads the data to a Redshift Cluster.
    - Arguments:
        - --rows : Enter the amount of rows you would like to upload to the database




# My Three recommendations  
    - Change truck 4.
        - Truck 4 currently has the lowest transaction count, average sale and is losing money.
        - Changing Truck 4's location, menu, prices needs to happen.
    - Create another truck or give other trucks the same menu items as truck 3.
        - Truck 3 is the current most popular truck and its menu or organisation should be brought into other trucks.
    - Add a card reader to truck 6.
        - Truck 6 is the second worse performing truck and this may be due to the no card reader as the proportion of all truck sales have been card.