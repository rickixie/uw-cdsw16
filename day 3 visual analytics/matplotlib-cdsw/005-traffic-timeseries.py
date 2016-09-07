""" 

005-traffic-timeseries.py

A relatively elaborate example of plotting time-series acquired through calls to the Socrata API

""" 
from datetime import datetime
import requests
import collections 
import matplotlib.pyplot as plt 


# Get traffic data:
api_call = requests.get("https://data.seattle.gov/resource/2z5v-ecg8.json?$where=date > '2015-01-15T00:00:00'  AND date < '2015-02-15T00:00:00'")
#store the data we just pulled down from the internet into a json object called 'all counts'
all_counts = api_call.json()
#create a new, empty dictionary. When we're done, this will contain counts per day
daily_counts = {}
#trim the time values off of data/times stamps, and add them to our empty dictionary
for c in all_counts:
    count_date = c['date'][:10]
    if count_date not in daily_counts.keys():
        daily_counts[count_date]=0

#we are only interested in the data from one bike counter location, so filter out the rest
for c in all_counts:
    try:
        daily_counts[c['date'][:10]] += int(c['bgt_north_of_ne_70th_total'])
    except:
        pass

# We'll put the counts and dates into lists we will then use in plotting
count_dates = []
counts = []
for key in sorted(daily_counts):
    count_dates.append(datetime.strptime(key, '%Y-%m-%d'))
    counts.append(daily_counts[key])


# Repeat with calls to the API to get temperatures:
api_call_temp = requests.get("https://data.seattle.gov/resource/egc4-d24i.json?$select=date_trunc_ymd(datetime) AS day, MAX(airtemperature) AS top_temp&$where=datetime > '2015-01-15T00:00:00' AND datetime < '2015-02-15T00:00:00' AND stationname= 'RooseveltWay_NE80thSt'&$group=day")
raw_data = api_call_temp.json()
daily_temps = {}

for c in raw_data:
    temp_date = c['day'][:10]
    daily_temps[temp_date]=c['top_temp']

temp_dates = []
temps = []
for key in sorted(daily_temps):
    temp_dates.append(datetime.strptime(key, '%Y-%m-%d'))
    temps.append(daily_temps[key])

# We'll use the styles again
plt.style.use('ggplot') 
# This means: 2 rows, 1 column:
fig, (ax1, ax2) = plt.subplots(2, 1)
ax1.plot(temp_dates, temps)
ax2.plot(count_dates, counts)
plt.show()

# A picture is worth 1000 words.

# Challenge: plot a scatter plot showing this relationship. Consider using the 'scatter' plotting function:
# http://matplotlib.org/examples/shapes_and_collections/scatter_demo.html

# Plot a series of figures with this relationship plotted for every month in 2014