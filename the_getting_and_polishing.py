import requests
from datetime import date
import os
import pandas as pd
import json
import psycopg2


today = date.today()

url_weathercode = f"https://api.open-meteo.com/v1/forecast?latitude=63.79&longitude=20.28&hourly=weathercode&timezone=Europe%2FBerlin&start_date={today}&end_date={today}"

returned_weathercode = requests.get(url_weathercode)

data = returned_weathercode.json()

# Create the directory path
folder_path = os.path.join("raw", "weathercode")

# Check if the directory exists, if not create it
if not os.path.exists(folder_path):
    os.makedirs(folder_path)

# Create the file path
filename = f"raw_weathercode_{today}.json"
file_path = os.path.join(folder_path, filename)

# Open and write to the file
with open(file_path, 'w') as outfile:
    json.dump(data, outfile)

#Opens raw file, harmonizes it. Saves it using a df because of reasons
harmonized_folder = "harmonized"
weathercode_folder = "weathercode"

# check if folders exists, if not create them
if not os.path.exists(harmonized_folder):
    os.mkdir(harmonized_folder)
if not os.path.exists(os.path.join(harmonized_folder, weathercode_folder)):
    os.mkdir(os.path.join(harmonized_folder, weathercode_folder))

with open(f"raw/weathercode/raw_weathercode_{today}.json") as json_file:
    data = json.load(json_file)
hourly = data['hourly']
df = pd.DataFrame(hourly)

# use os.path.join to join the file path and file name
file_path = os.path.join(harmonized_folder, weathercode_folder, "harmonized_weathercode.json")
df.to_json(file_path, orient="records")
with open(f'harmonized/weathercode/harmonized_weathercode{today}.json', 'r') as f:
    data = json.load(f)

conn = psycopg2.connect(
    host="localhost",
    port="5432",
    user="postgres",
    password="5731",
    dbname="weather"
)

map_weathercode = {0: 'Clear', 1:'Mainly clear',2:'Partly cloudy',3:'overcast',51:'Light drizzle',53:'Moderate drizzle',
71:'Slight snowfall',73:'Moderate snowfall',75:'Heavy snowfall'}

cur = conn.cursor()

for i in range(len(data)):
    time = data[i]['time'].replace('T','-')
    weathercode = map_weathercode[data[i]['weathercode']]
    cur.execute("INSERT INTO weathercode (time, weathercode) VALUES (to_timestamp(%s, 'YYYY-MM-DD-HH24:MI'), %s)", (time, weathercode))
conn.commit()

cur.close()
conn.close()