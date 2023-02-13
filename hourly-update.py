import weather_extraction_etl as we
import sqlalchemy
import config

url = config.url
api_key = config.api_key
db_engine = sqlalchemy.create_engine(url)

data = we.extract_current_weather_data(api_key, 'Phoenix')
data = we.transform_current_weather_data(data)
data = data[['temp', 'temp_max', 'temp_min', 'humidity', 'pressure']]
data.to_sql("daily", db_engine, if_exists="append", index=False)
