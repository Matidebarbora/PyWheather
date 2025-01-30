import requests
import os
from dotenv import load_dotenv
from colorama import init, Fore, Back, Style
from tabulate import tabulate
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo
import matplotlib.pyplot as plt



def main():
    option = input("Option: ")
    
    if option == "1":
        load_dotenv("config.env")
        API_KEY = os.getenv("OPENWEATHER_API_KEY")
        city = "Santiago, CL"
        data = weather_json_data(API_KEY, city)
        forecast_data = forecast_json_data(API_KEY, city)
        forecasts = fetch_tomorrow_forecast(forecast_data)

        print(f"{Fore.GREEN}")
        fetch_weather(data, city)
        
        print(f"{Fore.YELLOW}")
        tomorrow_min_max(forecasts, 1)
        tomorrow_min_max(forecasts, 2)
        tomorrow_min_max(forecasts, 3)
        tomorrow_min_max(forecasts, 4)
        tomorrow_min_max(forecasts, 5)
        print(f"{Fore.WHITE}")

        # print(tabulate(forecast_list))
        # time_list = extract_time_list(forecast_list)
        # plot_tomorrow_temp(temp_list, time_list)
    
    elif option == "2":
        load_dotenv("config.env")

        API_KEY = os.getenv("OPENWEATHER_API_KEY")
        print(f"🔍 API Key Loaded: {API_KEY}")  # Debugging print


def rounded_int(n):
    rounded_number = int(round(n, 0))
    return rounded_number


def weather_json_data(api_key, city):
    base_url = "https://api.openweathermap.org/data/2.5/weather"
    params = {
        "q": city,
        "appid": api_key,
        "units": "metric" 
    }
    try:
        response = requests.get(base_url, params=params)
        response.raise_for_status()
        data = response.json()
        return data

    except requests.exceptions.RequestException as e:
        print(f"Error fetching weather data: {e}")
    except KeyError:
        print("Error: Unexpected response format. Please check the city name or API key.")


def forecast_json_data(api_key, city):
    base_url = "https://api.openweathermap.org/data/2.5/forecast"
    params = {
        "q": city,
        "appid": api_key,
        "units": "metric" 
    }
    try:
        response = requests.get(base_url, params=params)
        response.raise_for_status()
        data = response.json()
        return data

    except requests.exceptions.RequestException as e:
        print(f"Error fetching weather data: {e}")
    except KeyError:
        print("Error: Unexpected response format. Please check the city name or API key.")


def fetch_weather(data, city):
    weather_description = data["weather"][0]["description"]
    temperature = rounded_int(data["main"]["temp"])
    humidity = data["main"]["humidity"]
    wind_speed = data["wind"]["speed"]
    
    sunrise = data["sys"]["sunrise"]
    sunrise_time = datetime.fromtimestamp(sunrise, ZoneInfo("utc"))
    local_timezone = ZoneInfo("America/Santiago")
    local_sunrise = sunrise_time.astimezone(local_timezone)
    formatted_sunrise = local_sunrise.strftime("%H:%M:%S")
    #formatted_sunrise = local_sunrise.strftime("%Y-%m-%d %H:%M:%S")

    sunset = data["sys"]["sunset"]
    sunset_time = datetime.fromtimestamp(sunset, ZoneInfo("utc"))
    local_sunset = sunset_time.astimezone(local_timezone)
    formatted_sunset = local_sunset.strftime("%H:%M:%S")
    #formatted_sunrise = local_sunrise.strftime("%Y-%m-%d %H:%M:%S")
    
    print(f"Weather in {city.capitalize()}:")
    print(f"{weather_description.capitalize()} - Temp: {temperature}°C - Hum: {humidity}% - Wind Speed: {wind_speed} m/s")
    print(f"Sunrise: {formatted_sunrise} - Sunset: {formatted_sunset}")


def fetch_tomorrow_forecast(data):
    forecasts = data["list"]
    return forecasts
        

def day_forecast_list(forecasts, day):
    tomorrow = datetime.now() + timedelta(days=day)
    tomorrow_date = tomorrow.date()
    forecast_list = []

    for forecast in forecasts:
        forecast_dict = {}
        forecast_time = datetime.fromtimestamp(forecast["dt"])
        if forecast_time.date() == tomorrow_date:
            time = forecast_time.strftime("%H:%M")
            description = forecast["weather"][0]["description"]
            temp = forecast["main"]["temp"]
            humidity = forecast["main"]["humidity"]
            wind_speed = forecast["wind"]["speed"]

            forecast_dict["Time"] = time
            forecast_dict["Description"] = description
            forecast_dict["Temp"] = temp
            forecast_dict["Hum"] = humidity
            forecast_dict["Wind_speed"] = wind_speed
            forecast_list.append(forecast_dict)
    return forecast_list


def extract_time_list(forecast_list):
    time_list = []
    for p in forecast_list:
        time = p["Time"]
        time_list.append(time)
    return time_list


def extract_temp_list(forecast_list):
    temp_list = []
    for p in forecast_list:
        temp = p["Temp"]
        temp_list.append(temp)
    return temp_list


def tomorrow_min_max(forecasts, day):
    temp_list = extract_temp_list(day_forecast_list(forecasts, day))
    tomorrow = datetime.now() + timedelta(days=day)
    tomorrow_date = tomorrow.date()
    min_temp = rounded_int(min(temp_list))
    max_temp = rounded_int(max(temp_list))
    print(f"{tomorrow_date} --> Min temp: {min_temp}°c - Max temp: {max_temp}°c")


def plot_tomorrow_temp(temp_list, time_list):
    # Create the plot
    plt.figure(figsize=(10, 5))  # Set the figure size
    plt.plot(time_list, temp_list, marker='o', linestyle='-', color='blue', label='Temperature')

    # Add labels and title
    plt.title("Temperature Variation", fontsize=16)
    plt.xlabel("Time (e.g., Hours)", fontsize=12)
    plt.ylabel("Temperature (°C)", fontsize=12)

    # Add grid and legend
    plt.grid(alpha=0.5)
    plt.legend()

    # Show the plot
    plt.show()

if __name__ == "__main__":
    main()
    
