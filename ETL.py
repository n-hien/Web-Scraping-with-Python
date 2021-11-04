import glob #this module helps in selecting files
import pandas as pd #this module helps in processing CSV files
import xml.etree.ElementTree as ET
from datetime import datetime
from zipfile import ZipFile #module helps in extracting files

#extract in current directory
with ZipFile("datasource.zip","r") as f:
   f.extractall()

#Set Paths
tmpfile    = "temp.tmp"               # file used to store all extracted data
logfile    = "logfile.txt"            # all event logs will be stored in this file
targetfile = "transformed_data.csv"   # file where transformed data is stored

# Extract
#CSV Extract function
def extract_from_csv(file_to_extract):
    data = pd.read_csv(file_to_extract)
    return data

#Json Extract Function
def extract_from_json(file_to_extract):
    data = pd.read_json(file_to_extract,line = True)
    return data

#XML Extract Function
def extract_from_xml(file_to_extract):
    data = pd.DataFrame(columns=['car_model', 'year_of_manufacture','price', 'fuel'])
    tree = ET.parse(file_to_extract)
    root = tree.getroot()
    for x in root:
        model = x.find('car_model').text
        year = int(x.find('year_of_manufacture').text)
        price = float(x.find('price').text)
        fule = x.find('fuel').text
        data = data.append({'car_model':model, 'year_of_manufacture':year,'price':price, 'fuel':fuel})
    return data

#Extract Function
def extract():
    data = pd.DataFrame(columns=['car_model','year_of_manufacture','price', 'fuel']) # create an empty data frame to hold extracted data
    
    #process all csv files
    for csvfile in glob.glob("dealership_data/*.csv"):
        data = data.append(extract_from_csv(csvfile), ignore_index=True)
        
    #process all json files
    for jsonfile in glob.glob("dealership_data/*.json"):
        data = data.append(extract_from_json(jsonfile), ignore_index=True)
    
    #process all xml files
    for xmlfile in glob.glob("dealership_data/*.xml"):
        data = data.append(extract_from_xml(xmlfile), ignore_index=True)
        
    return data

#Transform 
def transform(data):
    data['price']=round(data.price,2)
    return(data)

#Loading
def load(targetfile,file_to_load):
    file_to_load.to_csv(targetfile)

#Logging
def log(message):
	timestamp_format = "%Y-%h-%d-%H:%M:%S"
	now = datetime.now()
	timestamp = now.strftime(timestamp_format)
	with open("logfile.txt","a") as f:
		f.write(timestamp + ',' + message + '\n')
log("ETL Job Started")

log("Extract phase Started")
data = extract()
log("Extract phase Ended")

log("Transform phase Started")
transformed_data = transform(data)
log("Transform phase Ended")

log("Load phase Started")
load(targetfile,transformed_data)
log("Load phase Ended")

log("ETL Job Ended")

