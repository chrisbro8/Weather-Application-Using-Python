import requests
import matplotlib.pyplot as plt
from datetime import datetime
import numpy as np
import json # for debugging purposes
'''Resources Used;
https://matplotlib.org/stable/api/_as_gen/matplotlib.pyplot.figure.html
https://www.w3schools.com/python/matplotlib_pyplot.asp
https://docs.python.org/3/library/datetime.html#strftime-and-strptime-behavior :for datetime behavours
https://www.geeksforgeeks.org/python-requests-tutorial/ :Using request
'''

def get_grid_coordinates(latitude, longitude):
    url = f'https://api.weather.gov/points/{latitude},{longitude}'
    response = requests.get(url)
    data = response.json()
    grid_id = data['properties']['gridId']
    grid_x = data['properties']['gridX']
    grid_y = data['properties']['gridY']
    return grid_id, grid_x, grid_y

def get_weather_forecast(grid_id, grid_x, grid_y):
    url = f'https://api.weather.gov/gridpoints/{grid_id}/{grid_x},{grid_y}/forecast'
    response = requests.get(url)
    data = response.json()#Parse into a JSON type convert a respose object to a python dictionary
    pretty = json.dumps(data,indent=4)
    print(pretty)
    return data['properties']['periods']

def mean_temperature(temps):
    return sum(temps)/len(temps)

def plot_temperature_time_series(dates, temps, min_temp, max_temp, mean_temp):
    #fig, ax = plt.subplots(figsize=(10, 5))#fig size is width and height in inches
    plt.xticks(rotation=45)# the x labels in degrees
    plt.xlabel('Date/Time')
    plt.ylabel('Temperature (°F)')
    plt.plot(dates, temps, color='g', label='Temperature')

    # Annotating local max temperature
    max_temp_index = np.where(temps == np.max(temps))[0][0]
    plt.annotate(f'Maximum Point: {max_temp:.2f}°F', 
                 xy=(dates[max_temp_index], max_temp), 
                 xytext=(dates[max_temp_index], max_temp + 2),  
                 arrowprops=dict(facecolor='red', shrink=0.09),
                 fontsize=4)
    # Annotating local min temperature
    min_temp_index = np.where(temps == np.min(temps))[0][0] #
    plt.annotate(f'Minimum point: {min_temp:.2f}°F', 
                 xy=(dates[min_temp_index], min_temp), 
                 xytext=(dates[min_temp_index], min_temp + 2),  
                 arrowprops=dict(facecolor='green', shrink=0.09),
                 fontsize=5)
    # Annotating Mean Point

    mean_temp_index = np.argsort(temps)[len(temps) // 2]

    plt.annotate(f'Mean: {mean_temp:.2f}°F',
                xy=(dates[mean_temp_index], mean_temp),
                xytext=(dates[mean_temp_index], mean_temp+2 ),
                arrowprops=dict(facecolor='blue', shrink=0.09),
                fontsize=5)


    plt.show()

def main(latitude, longitude):
    try:
        grid_id, grid_x, grid_y = get_grid_coordinates(latitude, longitude)
        forecast_periods = get_weather_forecast(grid_id, grid_x, grid_y)

        # Extract data for plotting
        dates = [datetime.strptime(period['startTime'], '%Y-%m-%dT%H:%M:%S%z') for period in forecast_periods]
        temps = [period['temperature'] for period in forecast_periods]
        print(temps)
        print(type(temps))
        min_temp = min(temps)
        max_temp = max(temps)
        mean_temp = mean_temperature(temps)

        # Plot temperature time series
        plot_temperature_time_series(dates, temps, min_temp, max_temp, mean_temp)

    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description='Weather API Task')#insstance of the argumentparaser
    parser.add_argument('latitude', type=float, help='Latitude of the location')
    parser.add_argument('longitude', type=float, help='Longitude of the location')#defining the argument
    args = parser.parse_args()

    main(args.latitude, args.longitude)
