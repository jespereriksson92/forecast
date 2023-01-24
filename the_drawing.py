#insufficient for current plan, only for test with two columns
#not up to date with database

import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import psycopg2

conn = psycopg2.connect(
    host="localhost",
    port=5432,
    user="postgres",
    password="5731",
    database="weather"
)


cur = conn.cursor()

cur.execute("SELECT time, temperature_2m FROM forecast")

results = cur.fetchall()

time = [result[0] for result in results]
temperature_2m = [result[1] for result in results]

plt.plot(time, temperature_2m, 'b-')
plt.xlabel('time')
plt.ylabel('temperature_2m')
plt.tick_params('y', colors='b')
plt.grid(True, axis='y', alpha=0.7)
plt.gca().xaxis.set_major_locator(mdates.HourLocator(byhour=range(0,24,4)))
plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%d %H:%M'))
plt.show()