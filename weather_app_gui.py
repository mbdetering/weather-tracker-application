import tkinter as tk
import datetime
import weather_extraction_etl as we
from PIL import ImageTk, Image


# creates temporary tkinter window which prompts user to input api key and city name before checking validity of each
# and returning the two if valid.
def key_frame():
    # creates temporary tkinter window indicating that an error has occured in requesting the openweathermap api
    def error():
        popup = tk.Toplevel()
        popup.title("ERROR!")

        label = tk.Label(popup, text="invalid api key or city, please try again")
        label.pack(pady=10)

        close_button = tk.Button(popup, text="Close", command=popup.destroy)
        close_button.pack(pady=10)

    key_window = tk.Tk()
    key_window.title("")

    key_label = tk.Label(key_window, text="Enter key:")
    key_label.grid(row=0, column=0)

    key_entry = tk.Entry(key_window)
    key_entry.grid(row=0, column=1)

    city_label = tk.Label(key_window, text="Enter city:")
    city_label.grid(row=1, column=0)

    city_entry = tk.Entry(key_window)
    city_entry.grid(row=1, column=1)

    api_key = ''
    city = ''

    # validates that the inputed city and api key are valid with the openweathermap api. If the two are not valid,
    # displays an error message, if the two are valid, closes the window and returns the inputs
    # allowing for the main app to run.
    def validate_key():
        nonlocal api_key
        nonlocal city
        api_key = key_entry.get()
        city = city_entry.get()
        if 'main' not in we.extract_current_weather_data(api_key, city):
            error()
        else:
            key_window.destroy()

    button = tk.Button(key_window, text="Enter", command=validate_key)
    button.grid(row=2, column=1)

    key_window.mainloop()
    return api_key, city


# extract validated api key and city
api_key, city = key_frame()

# extract and transforms current and forecast weather data
current_weather = we.extract_current_weather_data(api_key, city)
current_weather = we.transform_current_weather_data(current_weather)
desc = current_weather['description']
current_main = current_weather.loc[0, 'main']
current_weather = current_weather[['temp', 'feels_like', 'temp_max', 'temp_min', 'humidity', 'pressure']]
current_weather = current_weather.transpose()
forecast = we.extract_forecast(api_key, city)
forecast = we.transform_weather_forecast(forecast)
forecast_averages = we.mode_description(forecast)

# Create the main window
root = tk.Tk()
root.geometry("600x600")
root.title("Weather Tracker")

# Create the title label
title = tk.Label(root, text="Weather Tracker", font=("Arial", 20, "bold"))
title.pack(pady=10)

# Create the location and date/time labels
location = tk.Label(root, text=f"Location: {city}", font=("Arial", 14))
date_time = tk.Label(root, text=str(datetime.datetime.now()), font=("Arial", 14))
location.pack()
date_time.pack()

# Create the current weather statistics label
current_stats_label = tk.Label(root, text="Current Weather Statistics", font=("Arial", 10, "bold"))
current_stats_label.place(x=100, y=150, anchor="center")

# create and place current weather statistics
curr_y = 170
for i, row in current_weather.iterrows():
    label = tk.Label(root, text=f"{i}: {row[0]}")
    label.place(x=100, y=curr_y, anchor="center")
    curr_y += 20

# Create the weather conditions label
conditions_label = tk.Label(root, text="Weather Conditions", font=("Arial", 10, "bold"))
conditions_label.place(x=500, y=150, anchor="center")

# Create the weather conditions description
conditions_desc = tk.Label(root, text="Description: " + desc[0])
conditions_desc.place(x=500, y=170, anchor="center")

# places image of current weather conditions
current_icon = tk.PhotoImage(file=f'pics/{current_main}.png')
current_weather_icon = tk.Label(root, image=current_icon)
current_weather_icon.config(width=100, height=100)
current_weather_icon.place(x=500, y=230, anchor="center")

# Create the 5 day forecast label
forecast_label = tk.Label(root, text="5 Day Forecast", font=("Arial", 14, "bold"))
forecast_label.place(x=300, y=300, anchor="center")

# creates and places labels for averaged forecast data
current_x = 100
for i, row in forecast_averages.iterrows():
    label_date = tk.Label(text=row['Time'])
    label_date.place(x=current_x, y=350, anchor="center")
    label_max = tk.Label(text=row['temp_max'])
    label_max.place(x=current_x + 25, y=370, anchor="center")
    label_min = tk.Label(text=row['temp_min'])
    label_min.place(x=current_x - 25, y=370, anchor="center")
    label_desc = tk.Label(text=row['description'])
    label_desc.place(x=current_x, y=390, anchor="center")
    current_x += 100

# creates list of filepaths for forecast weather icons
paths = []
for desc in forecast_averages['weather']:
    line = f'pics/{desc}.png'
    paths.append(line)

# extracts and creates list of forecast weather icons
imgs = []
x = 100
for i in range(len(paths)):
    imgs.append(ImageTk.PhotoImage(Image.open(paths[i])))
    tk.Label(root, image=imgs[-1], width=50, height=50).place(x=x, y=440, anchor="center")
    x += 100

# Run the main event loop
root.mainloop()
