import weather_extraction_etl as we
import sqlalchemy
import config

url = config.url
db_engine = sqlalchemy.create_engine(url)

averages = we.daily_averages()
averages.to_sql("weather", db_engine, if_exists="append", index=False)
db_engine.execute("DELETE FROM daily")
