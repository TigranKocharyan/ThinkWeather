import requests
import time
from datetime import datetime
from colorama import Fore, Style, init

init(autoreset=True)

cache = {}

CACHING_TIME = 600

weather_icons = {
    "Clear": "☀️",
    "Clouds": "☁️",
    "Rain": "🌧️",
    "Snow": "❄️",
    "Mist": "🌫️",
    "Drizzle": "🌦️",
    "Thunderstorm": "⛈️"
}


def remove_duplicates(locations):
    seen = set()
    unique_locations = []

    for loc in locations:
        loc_tuple = (loc['name'], loc.get('state', ''), loc['country'])
        if loc_tuple not in seen:
            seen.add(loc_tuple)
            unique_locations.append(loc)

    return unique_locations


def get_lat_lon(city, country_code=None, api_key=None):
    try:
        if country_code:
            url = f"http://api.openweathermap.org/geo/1.0/direct?q={city},{country_code}&limit=3&appid={api_key}"
        else:
            url = f"http://api.openweathermap.org/geo/1.0/direct?q={city}&limit=3&appid={api_key}"

        response = requests.get(url)
        response.raise_for_status()
        data = response.json()

        if not data:
            print(Fore.RED + f"No results found for {city}. Please check the input.")
            return None

        unique_data = remove_duplicates(data)

        if len(unique_data) > 1:
            print(Fore.YELLOW + f"Multiple results found for {city}:")
            for idx, place in enumerate(unique_data, start=1):
                print(f"{idx}. {place['name']}, {place['state'] if 'state' in place else ''} ({place['country']})")
            choice = int(input("Choose a location by number: ")) - 1
            chosen_place = unique_data[choice]
        else:
            chosen_place = unique_data[0]

        lat = chosen_place['lat']
        lon = chosen_place['lon']
        return lat, lon

    except requests.exceptions.HTTPError as http_err:
        print(Fore.RED + f"HTTP error occurred: {http_err}")
    except Exception as err:
        print(Fore.RED + f"An error occurred: {err}")
    return None


def get_weather(lat, lon, unit, api_key):
    cache_key = f"{lat},{lon},{unit}"
    current_time = time.time()

    if cache_key in cache:
        cached_data, timestamp = cache[cache_key]
        if current_time - timestamp < CACHING_TIME:
            print(Fore.GREEN + "Returning cached data.")
            return cached_data

    try:
        unit_param = 'metric' if unit == 'Celsius' else 'imperial'
        url = f"https://api.openweathermap.org/data/3.0/onecall?lat={lat}&lon={lon}&exclude=hourly,minutely&appid={api_key}&units={unit_param}"
        response = requests.get(url)
        response.raise_for_status()
        weather_data = response.json()

        cache[cache_key] = (weather_data, current_time)
        return weather_data
    except requests.exceptions.HTTPError as http_err:
        print(Fore.RED + f"HTTP error occurred: {http_err}")
    except Exception as err:
        print(Fore.RED + f"An error occurred: {err}")
    return None


def display_current_weather(data, unit):
    current = data['current']
    temperature = current['temp']
    feels_like = current['feels_like']
    humidity = current['humidity']
    wind_speed = current['wind_speed']
    weather_main = current['weather'][0]['main']
    weather_description = current['weather'][0]['description']

    weather_icon = weather_icons.get(weather_main, "🌍")
    temp_unit = "°C" if unit == "Celsius" else "°F"

    print(f"{Fore.YELLOW + Style.BRIGHT}Temperature: {temperature}{temp_unit} {weather_icon}")
    print(f"{Fore.YELLOW + Style.BRIGHT}Feels like: {feels_like}{temp_unit}")
    print(f"{Fore.CYAN}Humidity: {humidity}%")
    print(f"{Fore.CYAN}Wind Speed: {wind_speed} m/s")
    print(f"{Fore.BLUE + Style.BRIGHT}Weather: {weather_icon} {weather_main} ({weather_description})")


def display_5_day_forecast(data, unit):
    daily_forecast = data['daily'][:5]

    temp_unit = "°C" if unit == "Celsius" else "°F"

    print(Fore.CYAN + "\n5-Day Weather Forecast:")
    for day in daily_forecast:
        date = datetime.utcfromtimestamp(day['dt']).strftime('%Y-%m-%d')
        weather_main = day['weather'][0]['main']
        description = day['weather'][0]['description']
        weather_icon = weather_icons.get(weather_main, "🌍")
        temp_day = day['temp']['day']
        temp_min = day['temp']['min']
        temp_max = day['temp']['max']

        print(f"\n{Fore.YELLOW}Date: {date}")
        print(
            f"{Fore.YELLOW + Style.BRIGHT}Temperature: Day {temp_day}{temp_unit}, Min {temp_min}{temp_unit}, Max {temp_max}{temp_unit} {weather_icon}")
        print(f"{Fore.BLUE + Style.BRIGHT}Weather: {weather_icon} {weather_main} ({description})")


def main():
    api_key = '5b9c38b34129fc3512044e5bdf13a983'

    while True:
        city = input(Fore.CYAN + "Enter the city name (or 'exit' to quit): ")
        if city.lower() == 'exit':
            print("Exiting program...")
            break

        country_code = input("Enter the country code (optional, press Enter to skip): ").strip()

        unit_input = input(Fore.CYAN + "Choose temperature unit (C/F): ").upper()
        if unit_input == 'C':
            unit = 'Celsius'
        elif unit_input == 'F':
            unit = 'Fahrenheit'
        else:
            print(Fore.RED + "Invalid choice! Defaulting to Celsius.")
            unit = 'Celsius'

        forecast_choice = input(Fore.CYAN + "Do you want the current weather or a 5-day forecast? (curr/day): ").lower()
        if forecast_choice not in ['curr', 'day']:
            print(Fore.RED + "Invalid choice! Defaulting to current weather.")
            forecast_choice = 'curr'

        lat_lon = get_lat_lon(city, country_code, api_key)

        if lat_lon:
            lat, lon = lat_lon
            print(Fore.MAGENTA + "Fetching weather data", end="")
            for _ in range(3):
                print(".", end="", flush=True)
                time.sleep(0.5)
            print()

            weather_data = get_weather(lat, lon, unit, api_key)

            if weather_data:
                if forecast_choice == 'curr':
                    display_current_weather(weather_data, unit)
                elif forecast_choice == 'day':
                    display_5_day_forecast(weather_data, unit)
            else:
                print(Fore.RED + "Unable to retrieve weather information.")
        else:
            print(Fore.RED + "Unable to get latitude and longitude for the given city.")


if __name__ == "__main__":
    main()
