from bs4 import BeautifulSoup
import requests
import pandas as pd

###Webpage Contents
#Gather the contents of the webpage in text format using the requests library
url = "https://en.wikipedia.org/wiki/List_of_largest_banks"
html_data = requests.get(url).text

# Print out the output of the following line
html_data[101:124]          #'List of largest banks -'


###Scraping the Data
#Using BeautifulSoup parse the contents of the webpage.
soup = BeautifulSoup(html_data, 'html.parser')
'''Load the data from the 'By market capitalization' table into a pandas dataframe. 
The dataframe should have the country 'Name' and 'Market Cap (US$ Billion)'' as column names.'''
data = pd.DataFrame(columns=["Name", "Market Cap (US$ Billion)"])
for row in soup.find_all('tbody')[3].find_all('tr'):
    col = row.find_all('td')
    if (col != []):
        cap = col[2].text.strip()
        name = col[1].text.strip()
        data = data.append({"Name":name,"Market Cap (US$ Billion)":cap},ignore_index=True)

# Display the first five rows using the head function.
data.head()

###Loading the Data
#the data will be sent to another team