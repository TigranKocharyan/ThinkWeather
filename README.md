
# Weather Application

This Python script allows you to fetch and display current weather data or a 5-day weather forecast for a specified city using the OpenWeatherMap API. It supports temperature units in Celsius and Fahrenheit and uses color-coded output for better readability.

## Features

- Retrieve current weather data
- Get a 5-day weather forecast
- Supports temperature units: Celsius and Fahrenheit
- Handles multiple results for city searches
- Caches weather data to reduce API requests

## Requirements

Ensure you have the following Python packages installed:

- `requests`
- `colorama`

You can install the required packages using:

```bash
pip install -r requirements.txt
```

## Setup

1. **Obtain an API Key**: Sign up at [OpenWeatherMap](https://openweathermap.org/) to get your free API key.

2. **Update API Key**: Replace the placeholder API key in the script with your actual API key.

   ```python
   api_key = 'your_api_key_here'
   ```

3. **Install Dependencies**: Run the following command to install the necessary Python packages:

   ```bash
   pip install -r requirements.txt
   ```

4. **Run the Script**: Execute the script in your terminal:

   ```bash
   python weather_app.py
   ```

## Usage

1. **Enter City Name**: When prompted, enter the city name you want to get weather information for. You can also provide an optional country code (e.g., "US" for the United States).

2. **Choose Temperature Unit**: Specify the temperature unit by entering 'C' for Celsius or 'F' for Fahrenheit.

3. **Select Forecast Type**: Choose between current weather (`curr`) or a 5-day forecast (`day`).

4. **View Results**: The script will display the weather information with color-coded output for better readability.

5. **Exit**: Type 'exit' when you want to quit the program.

## Example

```plaintext
Enter the city name (or 'exit' to quit): New York
Enter the country code (optional, press Enter to skip): US
Choose temperature unit (C/F): C
Do you want the current weather or a 5-day forecast? (curr/day): curr
Fetching weather data...
Temperature: 22°C ☀️
Feels like: 21°C
Humidity: 60%
Wind Speed: 5 m/s
Weather: ☀️ Clear (clear sky)
```

## Notes

- Ensure your API key is valid and not expired.
- The script uses caching to avoid redundant API calls within a 10-minute period.


