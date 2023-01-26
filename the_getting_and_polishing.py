import requests
from datetime import date
import os
import pandas as pd
import json



today = date.today()
def weather():
    url_weather = f"https://api.open-meteo.com/v1/forecast?latitude=63.79&longitude=20.28&hourly=temperature_2m,weathercode&timezone=Europe%2FBerlin&start_date=2023-01-26&end_date=2023-01-26"

    returned_weathercode = requests.get(url_weather)
    data = returned_weathercode.json()


    folder_path = os.path.join("raw", "weathercode")
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)

    filename = f"raw_weathercode_{today}.json"
    file_path = os.path.join(folder_path, filename)

    with open(file_path, 'w') as outfile:
        json.dump(data, outfile)

    harmonized_folder = "harmonized"
    weathercode_folder = "weathercode"

    if not os.path.exists(harmonized_folder):
        os.mkdir(harmonized_folder)
    if not os.path.exists(os.path.join(harmonized_folder, weathercode_folder)):
        os.mkdir(os.path.join(harmonized_folder, weathercode_folder))

    with open(f"raw/weathercode/raw_weathercode_{today}.json") as json_file:
        data = json.load(json_file)
    hourly = data['hourly']
    df = pd.DataFrame(hourly)

    file_path = os.path.join(harmonized_folder, weathercode_folder, f"harmonized_weathercode_{today}.json")
    df.to_json(file_path, orient="records")

weather()