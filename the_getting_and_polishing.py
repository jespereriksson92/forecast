#Todo:
#create folders for files
#create functions when everything works
#Call the functions

import requests
import datetime
import pandas as pd
import json

today = datetime.date.today()
#maybe for 3 day forecast?
tomorrow = datetime.date.today() + datetime.timedelta(days=2)

#get url and raw JSON

url= "https://api.open-meteo.com/v1/forecast?latitude=63.79&longitude=20.28&hourly=temperature_2m,weathercode,windspeed_10m,winddirection_10m&windspeed_unit=ms&timezone=Europe%2FBerlin&start_date=2023-01-25&end_date=2023-01-25"
returned_weather = requests.get(url)
raw_df = returned_weather.json()
raw_df = pd.json_normalize(raw_df)

raw_df.to_json(f"raw_forecast_{today}.json", orient='records')

# #drops unnecessary columns in JSON-file, and formats timestamp to better suited format
harmonizing_df = pd.read_json(f"raw_forecast_{today}.json")



harmonizing_df.drop(columns=['latitude', 'longitude', 'generationtime_ms','utc_offset_seconds','timezone','timezone_abbreviation','elevation',
'hourly_units.time','hourly_units.temperature_2m','hourly_units.weathercode','hourly_units.windspeed_10m','hourly_units.winddirection_10m'], inplace=True)

new_cols = {col: col.replace("hourly.", "") for col in harmonizing_df.filter(regex='^hourly.').columns}
harmonizing_df = harmonizing_df.rename(columns=new_cols)

harmonizing_df['time'] = harmonizing_df['time'].apply(lambda x: [i.replace("T", " ") for i in x])

harmonizing_df.to_json(f'forecast_{today}.json', orient='records')


#Bara för minnets skull, problem med att konvertera innan, gör det vid insert istället

# harmonizing_df['weathercode'] = harmonizing_df['weathercode'].astype('str')

# print(harmonizing_df.dtypes)

# #changes numerical weathercode to descriptive title

# harmonizing_df.loc[harmonizing_df.weathercode == 0, 'weathercode'] = 'Cloudfree'
# harmonizing_df.loc[harmonizing_df.weathercode == 1, 'weathercode'] = 'Mainly clear'
# harmonizing_df.loc[harmonizing_df.weathercode == 2, 'weathercode'] = 'Partly cloudy'
# harmonizing_df.loc[harmonizing_df.weathercode == 3, 'weathercode'] = 'Overcast'
# harmonizing_df.loc[harmonizing_df.weathercode == 71, 'weathercode'] = 'Light snowfall'
# harmonizing_df.loc[harmonizing_df.weathercode == 73, 'weathercode'] = 'Moderate snowfall'
# harmonizing_df.loc[harmonizing_df.weathercode == 75, 'weathercode'] = 'Heavy snowfall'

#changes numerical winddirection to somewhat accurate heading
# harmonizing_df.loc[harmonizing_df.winddirection_10m.between(0, 22) , 'Column1'] = 'N'
# harmonizing_df.loc[harmonizing_df.hourly.winddirection_10m.between(23, 67) , 'Column1'] = 'NE'
# harmonizing_df.loc[harmonizing_df.hourly.winddirection_10m.between(68, 112) , 'Column1'] = 'E'
# harmonizing_df.loc[harmonizing_df.hourly.winddirection_10m.between(113, 157) , 'Column1'] = 'SE'
# harmonizing_df.loc[harmonizing_df.hourly.winddirection_10m.between(158, 203) , 'Column1'] = 'S'
# harmonizing_df.loc[harmonizing_df.hourly.winddirection_10m.between(204, 249) , 'Column1'] = 'SW'
# harmonizing_df.loc[harmonizing_df.hourly.winddirection_10m.between(250, 295) , 'Column1'] = 'W'
# harmonizing_df.loc[harmonizing_df.hourly.winddirection_10m.between(296, 341) , 'Column1'] = 'NW'
# harmonizing_df.loc[harmonizing_df.hourly.winddirection_10m.between(342, 359) , 'Column1'] = 'N'
















