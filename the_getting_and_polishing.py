import requests
import datetime
import pandas as pd
import matplotlib as plt

today = datetime.date.today()
#maybe for 3 day forecast?
tomorrow = datetime.date.today() + datetime.timedelta(days=2)

#get url and raw JSON
url = f"https://api.open-meteo.com/v1/forecast?latitude=63.79&longitude=20.28&hourly=temperature_2m,weathercode,windspeed_10m,winddirection_10m&windspeed_unit=ms&timezone=Europe%2FBerlin&start_date={today}&end_date={today}"
returned_weather = requests.get(url)
data = returned_weather.json()
data = pd.json_normalize(data)
data.to_json(f"raw_forecast_{today}.json")

#drops unnecessary columns in JSON-file and formats timestamp to better suited format

data = pd.read_json(f'forecast_harmonized.json')

# data['time'] = pd.to_datetime(data['time'])
# data['time'] = data['time'].dt.strftime('%Y-%m-%d_%H:%M:%S')

# data.loc[data.weathercode == 0, 'weathercode'] = 'Cloudfree'
# data.loc[data.weathercode == 1, 'weathercode'] = 'Mainly clear'
# data.loc[data.weathercode == 2, 'weathercode'] = 'Partly cloudy'
# data.loc[data.weathercode == 3, 'weathercode'] = 'Overcast'
# data.loc[data.weathercode == 71, 'weathercode'] = 'Light snowfall'
# data.loc[data.weathercode == 73, 'weathercode'] = 'Moderate snowfall'
# data.loc[data.weathercode == 75, 'weathercode'] = 'Heavy snowfall'

# data.loc[data.winddirection_10m.between(0, 22) , 'Column1'] = 'N'
# data.loc[data.winddirection_10m.between(23, 67) , 'Column1'] = 'NE'
# data.loc[data.winddirection_10m.between(68, 112) , 'Column1'] = 'E'
# data.loc[data.winddirection_10m.between(113, 157) , 'Column1'] = 'SE'
# data.loc[data.winddirection_10m.between(158, 203) , 'Column1'] = 'S'
# data.loc[data.winddirection_10m.between(204, 249) , 'Column1'] = 'SW'
# data.loc[data.winddirection_10m.between(250, 295) , 'Column1'] = 'W'
# data.loc[data.winddirection_10m.between(296, 341) , 'Column1'] = 'NW'
# data.loc[data.winddirection_10m.between(342, 359) , 'Column1'] = 'N'

# data.to_json(f'forecast_{today}.json')














