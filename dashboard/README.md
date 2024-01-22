# Dashboard

This folder should contain all code and resources required for the dashboard.

# Dashboard Description

- This folder contains all the information needed to create a streamlit dashboard representing the data collected from the T3 trucks database.

## 🔐 Environment Variables
- Create a `.env` file with the following information:
- `DATABASE_IP` -> ARN to your AWS RDS.
- `DATABASE_NAME` -> Name of your database.
- `DATABASE_USERNAME` -> Your database username.
- `DATABASE_PASSWORD` -> Password to access your database.
- `DATABASE_PORT` -> Port used to access the database.
- `AWS_ACCESS_KEY_ID_ `  -> Personal AWS ACCESS KEY available on AWS.
- `AWS_SECRET_ACCESS_KEY_` -> Personal AWS SECRET ACCESS KEY available on AWS.

## 🗂️ Files Explained

- `main.py`
    - A script to load the streamlit dashboard onto a webpage. Contains all design and calls to other files to fully implement the dashboard.
- `database.py`
    - This file contains all functions to connect to a redshift database and format the data so it becomes easy to manipulate and work with.
- `visuals.py`
    - This file contains all functions to create the charts and visuals shown on the dashboard.


## How to Run the streamlit Dashboard

- `streamlit run main.py`



## Wireframe

![title](./wireframe.png)



## Dashboard

![title](./dashboard_one.png)
![title](./dashboard_two.png)
![title](./dashboard_three.png)
