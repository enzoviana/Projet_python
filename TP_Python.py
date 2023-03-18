#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Mar 13 15:06:38 2023

@author: enzo
"""

import unittest
import pandas as pd
import matplotlib.pyplot as plt
import requests
from bs4 import BeautifulSoup
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import yfinance as yf
from pymongo import MongoClient
import streamlit as st

#connection to the DB
client = MongoClient("mongodb://localhost:27017/")
db = client['Stock_market']
collection = db['Netflix']


#import data 

url = "https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBMDeveloperSkillsNetwork-PY0220EN-SkillsNetwork/labs/project/netflix_data_webpage.html"
data = requests.get(url).text
soup = BeautifulSoup(data, 'html5lib')

#Create the dataframe w pandas
Netflix_data = pd.DataFrame(columns=["Date", "Open", "High", "Low", "Close", "Adj Close", "Volume"])


#for loop to extract all data
for row in soup.find('tbody').find_all('tr'):
    col = row.find_all('td')
    date = col[0].text
    Open = col[1].text
    high = col[2].text
    low = col[3].text
    close = col[4].text
    adj_close = col[5].text
    volume = col[6].text
    Netflix_data = Netflix_data.append({"Date":date, "Open":Open, "High":high, "Low":low, "Close":close, "Adj Close":adj_close, "Volume":volume}, ignore_index=True)


#convert Date column to datetime format
Netflix_data['Date'] = pd.to_datetime(Netflix_data['Date'])

#Make the mean of open each year
Netflix_data['Open'] = pd.to_numeric(Netflix_data['Open'], errors='coerce')
df = Netflix_data.groupby(Netflix_data['Date'].dt.year)['Open'].mean()


#make the graph
graph_evo_y = Netflix_data['Open']
graph_evo_x = Netflix_data['Date']
plt.plot(graph_evo_x, graph_evo_y)


#insert the Data from pandas to MongoDB
records = Netflix_data.to_dict('records')
collection.insert_many(records)


data = collection.find().limit(3000)
data_list = list(data)
df = pd.DataFrame(data_list)
st.write(df)

import plotly.graph_objects as go

# Create the figure object
fig = go.Figure()

# Add a trace to the figure
fig.add_trace(go.Scatter(x=df['Date'], y=df['Open'], mode='lines'))

# Set the layout of the figure
fig.update_layout(title='Netflix Stock Open Price', xaxis_title='Date', yaxis_title='Open Price', autosize=True)

# Display the figure on the Streamlit dashboard
st.plotly_chart(fig)
    

class TestNetflixScraper(unittest.TestCase):

    def test_scraper(self):
        # Test that the scraper correctly extracts data from the website
        url = "https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBMDeveloperSkillsNetwork-PY0220EN-SkillsNetwork/labs/project/netflix_data_webpage.html"
        data = requests.get(url).text
        soup = BeautifulSoup(data, 'html5lib')
        Netflix_data = pd.DataFrame(columns=["Date", "Open", "High", "Low", "Close", "Adj Close", "Volume"])
        for row in soup.find('tbody').find_all('tr'):
            col = row.find_all('td')
            date = col[0].text
            Open = col[1].text
            high = col[2].text
            low = col[3].text
            close = col[4].text
            adj_close = col[5].text
            volume = col[6].text
            Netflix_data = Netflix_data.append({"Date":date, "Open":Open, "High":high, "Low":low, "Close":close, "Adj Close":adj_close, "Volume":volume}, ignore_index=True)
        self.assertEqual(len(Netflix_data), 70)

if __name__ == '__main__':
    unittest.main()
    

    
    
    