#=============================
# Get ECB EUR-CHF data
#=============================

# From: https://www.datacareer.de/blog/accessing-ecb-exchange-rate-data-in-python/
# 29.08.2022 (tmalony)

# ------------------------------ Libraries ------------------------------

import requests
import json
import pandas as pd
import io

# ------------------------------ Building URL ------------------------------

# Building blocks for URL
entrypoint = 'https://sdw-wsrest.ecb.europa.eu/service/' # Using protocol 'https'
resource = 'data'           # The resource for data queries is always'data'
flowRef ='EXR'              # Dataflow describing the data that needs to be returned, exchange rates in this case
key = 'D.CHF.EUR.SP00.A'    # Defining the dimension values, explained below

# Define the parameters
parameters = {
    'startPeriod': '2021-01-01',  # Start date of the time series
    'endPeriod': '2022-08-26'     # End of the time series
}

# Construct the URL
request_url = entrypoint + resource + '/'+ flowRef + '/' + key
request_url

# ------------------------------ Make the HTTP request ------------------------------

# response = requests.get(request_url, params=parameters) # default is XML
response = requests.get(request_url, params=parameters, headers={'Accept': 'text/csv'}) # same request but in csv

# Check if the response returns succesfully with response code 200
print(response)

# Print the full URL
print(response.url)

# Print the first 1000 characters of the response
print(response.text[0:1000])

import csv
# open the file in the write mode
with open('C:/Users/Emma/Documents/private_credit_py/test.csv', 'w') as f: writer = csv.writer(f); writer.writerow(response)

# ------------------------------ Read response to pandas DF ------------------------------

# StringIO to read the strings as a file. This way we don't need to save it first.
df = pd.read_csv(io.StringIO(response.text)) 

# First inspection
df.head
df.head()
df.info()
df.tail()
# The columns we need are 'TIME_PERIOD' for the dates and 'OBS_VALUE' for the EURCHF prices.

# Inspect the prices. Do the mean, minimum and maximum make sense?
df['OBS_VALUE'].describe()

# ------------------------------ Make a time-series ------------------------------

# Create a new DataFrame called 'ts'
ts = df.filter(['TIME_PERIOD', 'OBS_VALUE'], axis=1)

# 'TIME_PERIOD' was of type 'object' (as seen in df.info). Convert it to datetime first
ts['TIME_PERIOD'] = pd.to_datetime(ts['TIME_PERIOD'])
ts.info()

# Set 'TIME_PERIOD' to be the index
ts = ts.set_index('TIME_PERIOD')
ts.head()
ts.tail()

# ------------------------------ Make a plot ------------------------------

%matplotlib inline
ts.plot()





