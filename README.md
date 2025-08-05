# Israel Weather Forecast App 
A **Streamlit** web app that displays **current weather**,**yesterday’s comparison**,
and a **7-day forecast** for cities in Israel using the **OpenWeatherMap API**.  

## Features
- Language toggle: Switch easily between English and Hebrew UI.
- City search: Enter any supported city name to retrieve weather data.
- Current weather metrics: Temperature, wind speed, and cloudiness with delta change from yesterday's temperature.
- Interactive map: Visualize city location with Folium map and marker.
- Weekly forecast: View 7-day weather forecast for temperature, wind speed, and cloudiness in interactive Plotly charts.
- Error handling: Friendly error messages for invalid city input or API issues.


##  Built With

- Python version 3.13.2 or higher is required to run this project.
- [Streamlit](https://streamlit.io/) – for web interface.
- [Requests](https://docs.python-requests.org/) – to call OpenWeatherMap API.
- [OpenWeatherMap API](https://openweathermap.org/api)
- [folium](https://python-visualization.github.io/folium/) – for maps.
- [dotenv](https://pypi.org/project/python-dotenv/) for environment variable management.
- [Plotly ](https://plotly.com/python/) for interactive charts.

## Project Structure
WeatherProject/
├── api/
│   └── get_weather.py         # API calls for current & historical weather
├── utills/
│   ├── __init__.py
│   └── city_list.py           # Predefined Israeli cities and coordinates
├── .env                       # Stores OpenWeatherMap API key
├── Main.py                    # Main Streamlit application
├── README.md                  # This file
├── .gitignore

## APIs Used
**Current & Forecast Weather – OpenWeatherMap One Call API 3.0**
https://api.openweathermap.org/data/3.0/onecall?lat={lat}&lon={lon}&exclude={exclude}&units={units}&appid={appid}

**Historical Weather (Yesterday) – OpenWeatherMap Timemachine API**
https://api.openweathermap.org/data/3.0/onecall/timemachine?lat={lat}&lon={lon}&dt={dt}&units={units}&appid={appid}
Where:
    lat → Latitude 
    lon → Longitude
    dt → UNIX timestamp for desired day in UTC
    units → metric for °C
    appid → Your API key


## Installation & Setup

1. Clone this repository
    git clone https://github.com/yourusername/WeatherProject.git
    cd WeatherProject

2. Create and activate a virtual environment
   python -m venv venv
   source venv/bin/activate 

3. Install dependencies
   - If you use pip: pip install -r requirements.txt
   - If you use Poetry: poetry add streamlit streamlit-folium folium python-dotenv requests
   
4. Set up your API key
- Create a .env file in the project root
- Add your OpenWeatherMap API key: API_KEY=your_openweathermap_api_key

5. requirements.txt
If you’re using pip, create a requirements.txt file with:
- streamlit
- streamlit-folium
- folium
- python-dotenv
- requests

6. Running the App
streamlit run main.py
Replace main.py with the filename of your main script if different.

7. Supported Cities
The app supports predefined Israeli cities stored in utills.py.
Example cities include:
Tel Aviv
Jerusalem
Haifa
Be’er Sheva
Ashdod
Eilat
Netanya
Herzliya
Nahariya
Kiryat Gat
... .
You can easily extend the list by editing utills.py.

8. Example Output
Interactive map view centered on the selected city with a red location marker.
Current Weather Metrics:
🌡️ Temperature in °C, including the delta change compared to yesterday’s temperature if available.
🌬️ Wind Speed in meters per second (m/s).
☁️ Cloudiness percentage (%).

7-Day Weather Forecast:
- Dates displayed horizontally in DD/MM format.
- Daily temperature values shown as a filled area chart.
- Separate tabs to view forecasts for Temperature, Wind Speed (m/s), and Cloudiness (%).
- All charts display data points with numeric values labeled above each marker.

## Notes
- Make sure to handle API rate limits when fetching weather data.
- The city name matching supports both English and Hebrew names.
- The app currently excludes minutely, hourly, and alert data for faster response.





