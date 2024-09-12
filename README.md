# CapstoneYoutubeDataHarvest
Youtube data harvesting using SQL streamlit
The problem statement is to create a Streamlit application that allows users to access and analyze data from multiple YouTube channels. The application should have the following features:
1. Ability to input a YouTube channel ID and retrieve all the relevant data (Channel name, subscribers, total video count, playlist ID, video ID, likes, dislikes, comments of each video) using Google API.
2. Ability to collect data for up to 10 different YouTube channels and store them in the data lake by clicking a button.
3. Option to store the data in a MYSQL or PostgreSQL.
4. Ability to search and retrieve data from the SQL database using different search options, including joining tables to get channel details.

![image](https://github.com/user-attachments/assets/d4f75c3f-3692-41bc-a24c-8d7b30fad2fd)


# Developer Guide
1. Tools Install
Virtual code.
Jupyter notebook.
Python 3.11.0 or higher.
MySQL.
Youtube API key.
2. Requirement Libraries to Install
pip install google-api-python-client, mysql-connector-python, sqlalchemy, pymysql, pymysql, pandas, numpy, plotly-express, streamlit.
( pip install google-api-python-client  mysql-connector-python sqlalchemy pymysql pandas numpy plotly-express streamlit )

3. Import Libraries
# Youtube API libraries
import googleapiclient.discovery
from googleapiclient.discovery import build

# File handling libraries
import json
import re

# SQL libraries
import mysql.connector
import sqlalchemy
from sqlalchemy import create_engine
import pymysql
pandas, numpy

import pandas as pd
import numpy as np

# Dashboard libraries
import streamlit as st


4. E T L Process
a) Extract data
Extract the particular youtube channel data by using the youtube channel id, with the help of the youtube API developer console.
b) Process and Transform the data
After the extraction process, takes the required details from the extraction data and transform it into python Dataframe format.
c) Load data
After the transformation process, the python Dataframe format data is stored in the Mysql database.
5. E D A Process and Framework
a) Access MySQL DB
Create a connection to the MySQL server and access the specified MySQL DataBase by using pymysql library and access tables.
b) Filter the data
Filter and process the collected data from the tables depending on the given requirements by using SQL queries and transform the processed data into a DataFrame format.
c) Visualization
Finally, create a Dashboard by using Streamlit and give dropdown options on the Dashboard to the user and select a question from that menu to analyse the data and show the output in Dataframe Table and Bar chart.
User Guide
Step 1. Data collection zone
Search channel_id, copy and paste on the input box and click the Get data and stored button in the Data collection zone.
Step 2. Channel Data Analysis zone
Select a Question from the dropdown option you can get the results in Dataframe format or bar chat format.
