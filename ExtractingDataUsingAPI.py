import pandas as pd
import requests
import json

#collect data
url = "http://api.exchangeratesapi.io/v1/latest?base=EUR&access_key=yourkey"
data = requests.get(url).text
data = json.loads(data)     #using json library to convert string to dictionary
data.keys()

# Turn the data into a dataframe
df = pd.DataFrame(data)

# Drop unnescessary columns
df = df[["rates"]]
df.head()
df.columns = ['Rates']

# Save the Dataframe
df.to_csv("exchange_rates_1.csv")