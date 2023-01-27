#Complete

import json
import psycopg2
from datetime import date

today = date.today()

def to_database():
    with open(f"harmonized/weather/harmonized_weather_{today}.json", "r") as f:
        data = json.load(f)

    conn = psycopg2.connect(
        host="localhost",
        port="5432",
        user="postgres",
        password="5731",
        dbname="weather")

    map_weathercode = {0: 'Clear', 1:'Mainly clear',2:'Partly cloudy',3:'Overcast',51:'Light drizzle',53:'Moderate drizzle',
    71:'Slight snowfall',73:'Moderate snowfall',75:'Heavy snowfall'}

    cur = conn.cursor()

    for i in range(len(data)):
        time = data[i]['time'].replace('T','-')
        weathercode = map_weathercode[data[i]['weathercode']]
        temperature_2m = data[i]['temperature_2m']
        apparent_temperature = data[i]['apparent_temperature']
        winddirection_10m = data[i]['winddirection_10m']
        windspeed_10m = data[i]['windspeed_10m']
        cur.execute("INSERT INTO one_day_forecast (time, temperature, apparent_temperature, weather_code, wind_direction, wind_speed)" + 
        "VALUES (to_timestamp(%s, 'YYYY-MM-DD-HH24:MI'), %s, %s, %s, %s,%s)", 
        (time, temperature_2m, apparent_temperature, weathercode, winddirection_10m, windspeed_10m))
    conn.commit()

    cur.close()
    conn.close()
    print("Successfully inserted to database")

to_database()