# weather-tracker-application

**Description:** This is a weather application that gathers and displays current weather and forecast data from the openweathermap api. The application will display the current weather statistics and a 5 day forecast of a given location, along with icons representing weather descriptions. The application requires a working openweathermap api key that the user will enter along with the desired city.

**Installation:** In order to run this app, download the files: weather_extraction_etl, and weather_app_gui. All dependencies are listed in requirements.txt. Along with these files, are two additional scripts called: hourly-update.py and end_day_update.py. These scripts are used for automated database updates and must be used with windows task scheduler. The database being used is not open to the public currently but these scripts can be customized to connect to a personal database if desired. 

**Usage Instructions:** In order to use this application, the user must input a desired city, along with a valid api key for the openweathermap api. If both are entered correctly, the app will display the current and forecast weather statistics. In order to change location, the user must restart the application and re-enter the new city along with their api key.

**Future Plans:** 
- expand database to account for more locations
- add more weather statistics including weather maps
