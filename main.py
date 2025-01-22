import requests
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo
import matplotlib.pyplot as plt

def main():
    api_key = "c86b3c8c49a759cd21dbe280885047d9"
    city = "Santiago, CL"

    fetch_weather(api_key, city)

    forecast_list = fetch_tomorrow_forecast(api_key, city)

    time_list = extract_time_list(forecast_list)
    temp_list = extract_temp_list(forecast_list)
    tomorrow_min_max(temp_list)
    plot_tomorrow_temp(temp_list, time_list)


def rounded_int(n):
    rounded_number = int(round(n, 0))
    return rounded_number


def fetch_weather(api_key, city):
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
        
        print("")
        print(f"Weather in {city.capitalize()}:")
        print(f"{weather_description.capitalize()} - Temp: {temperature}°C - Hum: {humidity}% - Wind Speed: {wind_speed} m/s")
        print(f"Sunrise: {formatted_sunrise} - Sunset: {formatted_sunset}")
        print("")

    except requests.exceptions.RequestException as e:
        print(f"Error fetching weather data: {e}")
    except KeyError:
        print("Error: Unexpected response format. Please check the city name or API key.")


def fetch_tomorrow_forecast(api_key, city):
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

        tomorrow = datetime.now() + timedelta(days=1)
        tomorrow_date = tomorrow.date()

        forecasts = data["list"]
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

    except requests.exceptions.RequestException as e:
        print(f"Error fetching weather data: {e}")
    except KeyError:
        print("Error: Unexpected response format. Please check the city name or API key.")


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


def tomorrow_min_max(temp_list):
    tomorrow = datetime.now() + timedelta(days=1)
    tomorrow_date = tomorrow.date()
    print(f"Tomorrow's forecast {tomorrow_date}:")

    min_temp = rounded_int(min(temp_list))
    max_temp = rounded_int(max(temp_list))
    print(f"Min temp: {min_temp}°c - Max temp: {max_temp}°c")
    print("")


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
