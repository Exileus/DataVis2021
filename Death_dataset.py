# -*- coding: utf-8 -*-
"""
Created on Tue Mar  9 16:31:22 2021

@author: Tiago
"""

import pandas as pd
import requests
import io


# Download the data.

url = "https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_deaths_global.csv" # Make sure the url is the raw version of the file on GitHub
download = requests.get(url).content

# Reading the downloaded content and turning it into a pandas dataframe

df = pd.read_csv(io.StringIO(download.decode('utf-8')))

# Printing out the first 5 rows of the dataframe

print (df.head())


#%%

# Make a new df with the rate of change to the previous days.

df_percentage


# Output the file to the present folder. Replace whatever previous version there was.

### Code here.