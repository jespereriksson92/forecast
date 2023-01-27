#complete

import requests
from datetime import date
import os
import pandas as pd
import json



today = date.today()
def weather():
    url_weather = f"https://api.open-meteo.com/v1/forecast?latitude=63.79&longitude=20.28&hourly=temperature_2m,apparent_temperature,weathercode,windspeed_10m,winddirection_10m&timezone=Europe%2FBerlin&start_date=2023-01-27&end_date=2023-01-27"

    returned_weather = requests.get(url_weather)
    data = returned_weather.json()


    folder_path = os.path.join("raw", "weather")
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)

    filename = f"raw_weather_{today}.json"
    file_path = os.path.join(folder_path, filename)

    with open(file_path, 'w') as outfile:
        json.dump(data, outfile)

    harmonized_folder = "harmonized"
    weather_folder = "weather"

    if not os.path.exists(harmonized_folder):
        os.mkdir(harmonized_folder)
    if not os.path.exists(os.path.join(harmonized_folder, weather_folder)):
        os.mkdir(os.path.join(harmonized_folder, weather_folder))

    with open(f"raw/weather/raw_weather_{today}.json") as json_file:
        data = json.load(json_file)
    hourly = data['hourly']
    df = pd.DataFrame(hourly)

    df['winddirection_10m'] = df['winddirection_10m'].replace(range(0,23), 'N')
    df['winddirection_10m'] = df['winddirection_10m'].replace(range(23,69), 'NE')
    df['winddirection_10m'] = df['winddirection_10m'].replace(range(69,115), 'E')
    df['winddirection_10m'] = df['winddirection_10m'].replace(range(115,161), 'SE')
    df['winddirection_10m'] = df['winddirection_10m'].replace(range(161,207), 'S')
    df['winddirection_10m'] = df['winddirection_10m'].replace(range(207,253), 'SW')
    df['winddirection_10m'] = df['winddirection_10m'].replace(range(253,295), 'W')
    df['winddirection_10m'] = df['winddirection_10m'].replace(range(295,341), 'NW')
    df['winddirection_10m'] = df['winddirection_10m'].replace(range(341,359), 'N')

    file_path = os.path.join(harmonized_folder, weather_folder, f"harmonized_weather_{today}.json")
    df.to_json(file_path, orient="records")


weather()