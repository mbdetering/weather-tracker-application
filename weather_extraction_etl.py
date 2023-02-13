import pandas as pd
import requests
import json
import sqlalchemy
import datetime
import config


# Takes in a temperature in Kelvin and converts to Fahrenheit rounding to 2 decimal places
def k2f(temp):
    temp = 1.8 * (temp - 273) + 32
    return round(temp, 2)


# Takes in an api key and city and requests the current weather from the openweathermap api as a JSON object
def extract_current_weather_data(api_key, city):
    c_url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}"
    response_c = requests.get(c_url)
    current_weather = json.loads(response_c.text)
    return current_weather


# Takes in an api key and city and requests a 5 day 3 hour forecast from the openweathermap api as a JSON object
def extract_forecast(api_key, city):
    f_url = f"https://api.openweathermap.org/data/2.5/forecast?q={city}&appid={api_key}"
    response_f = requests.get(f_url)
    forecast = json.loads(response_f.text)
    return forecast


# Takes in a JSON current weather object and extracts and converts the data within into a pandas DataFrame object
def transform_current_weather_data(data):
    current_weather = data['main']
    current_weather['temp'] = k2f(current_weather['temp'])
    current_weather['feels_like'] = k2f(current_weather['feels_like'])
    current_weather['temp_min'] = k2f(current_weather['temp_min'])
    current_weather['temp_max'] = k2f(current_weather['temp_max'])
    current_weather['pressure'] = round(current_weather['pressure'] / 33.684, 2)
    weather_main = data['weather'][0]['main']
    weather_main = {'main': weather_main}
    current_weather.update(weather_main)
    weather_desc = data['weather'][0]['description']
    weather_desc = {'description': weather_desc}
    current_weather.update(weather_desc)
    return pd.DataFrame(current_weather, index=[0])


# Takes in a JSON object of 5 day forecast data and extracts and converts to a pandas DataFrame object
def transform_weather_forecast(data):
    forecast_data = [(d['dt_txt'], k2f(d['main']['temp']), k2f(d['main']['temp_max']), k2f(d['main']['temp_min']),
                      d['main']['humidity'], d['weather'][0]['main'], d['weather'][0]['description']) for d in data['list']]
    return pd.DataFrame(forecast_data, columns=["Time", "temp", "temp_max", "temp_min", "humidity", "weather", "description"])


# Takes in a dataframe and inserts into local MySQL database
def load_current_weather_data(data):
    data.to_sql("daily", db_engine, if_exists="append")


# Extracts and summarizes weather data from local MySQL database before uploading summarized data
def daily_averages():
    df = pd.read_sql("SELECT AVG(temp) AS temp, MAX(temp_max) AS temp_max, MIN(temp_min) AS temp_min,"
                     "AVG(humidity) AS humidity, AVG(pressure) AS pressure FROM daily", db_engine)
    date = datetime.datetime.now().strftime('%Y-%m-%d')
    df.insert(0, 'Date', date)
    return df


# Takes in a dataframe of hourly weather data and aggregates summarizing by day before returning summarized DataFrame
def mode_description(df):
    df_subset = df[['Time', 'temp_max', 'temp_min', 'weather', 'description']]
    df_subset['Time'] = pd.to_datetime(df_subset['Time']).dt.date
    df_grouped = df_subset.groupby('Time', as_index=False).agg({
        'temp_max': max,
        'temp_min': min,
        'weather': lambda x: x.mode().iloc[0],
        'description': lambda x: x.mode().iloc[0]
    })
    today = datetime.datetime.now().date()
    if today in df_grouped['Time'].unique():
        df_grouped = df_grouped[df_grouped['Time'] != today]
    result = df_grouped.reset_index()
    return result


url = config.url
db_engine = sqlalchemy.create_engine(url)


