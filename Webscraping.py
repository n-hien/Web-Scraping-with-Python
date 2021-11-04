from bs4 import BeautifulSoup
import requests
import pandas as pd

html_data = requests.get('https://en.wikipedia.org/wiki/List_of_largest_banks')
html_data.text

