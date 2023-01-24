##insufficient for current plan, only for test with two columns


import psycopg2
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import json


conn = psycopg2.connect(
    host="localhost",
    port=5432,
    user="postgres",
    password="5731",
    database="weather"
)

# Open the JSON file
with open('second_test.json') as f:
    data = json.load(f)

# Create a cursor object
cur = conn.cursor()

# Iterate through the data and insert the values into the table
for i in range(len(data['time'])):
    time = data['time'][str(i)]
    temperature = data['temperature_2m'][str(i)]
    wind_speed = data['windspeed_10m'][str(i)]
    wind_direction = data['winddirection_10m'][str(i)]
    weathercode = data['weathercode'][str(i)]
    cur.execute("INSERT INTO forecast (time, temperature, wind_speed, wind_direction, weathercode) VALUES (%s, %s, %s, %s, %s)", (time, temperature,wind_speed,wind_direction,weathercode))

# Commit the changes and close the cursor and connection
conn.commit()
cur.close()
conn.close()

