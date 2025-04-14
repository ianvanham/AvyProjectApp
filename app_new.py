
import streamlit as st
from dotenv import load_dotenv
import os
import requests
import pandas as pd

load_dotenv()

# API Keys
GEOAPIFY_API_KEY = os.getenv("GEOAPIFY_API_KEY")
OPEN_METEO_API_KEY = os.getenv("OPEN_METEO_API_KEY")
WEBCAM_API_KEY = os.getenv("WEBCAM_API_KEY")

st.set_page_config(page_title="KNOW BEFORE YOU GO", layout="centered")

# CSS Dark Mode
st.markdown("""
    <style>
        body {
            background-color: #121212;
            color: white;
        }
        .big-temp {
            font-size: 64px;
            font-weight: bold;
            text-align: center;
        }
        .section-title {
            font-size: 28px;
            font-weight: bold;
            margin-top: 20px;
        }
    </style>
""", unsafe_allow_html=True)

st.markdown("<h2 style='text-align:center;'>KNOW BEFORE YOU GO</h2>", unsafe_allow_html=True)

location = st.text_input("Search location")

def get_background(condition):
    if "clear" in condition:
        return "https://i.imgur.com/VW6vF3p.jpg"
    elif "cloud" in condition:
        return "https://i.imgur.com/QxzFcdE.jpg"
    elif "rain" in condition:
        return "https://i.imgur.com/4Bl7D6Q.jpg"
    elif "snow" in condition:
        return "https://i.imgur.com/ITIW63y.jpg"
    else:
        return "https://i.imgur.com/sb0YVqG.jpg"

if location:
    geo_url = f"https://api.geoapify.com/v1/geocode/search?text={location}&apiKey={GEOAPIFY_API_KEY}"
    geo_response = requests.get(geo_url).json()

    if geo_response.get("features"):
        coords = geo_response["features"][0]["geometry"]["coordinates"]
        lon, lat = coords[0], coords[1]
        st.map({'lat': [lat], 'lon': [lon]})

        # Current Weather
        st.subheader("Current Weather")
        weather_url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current_weather=true"
        weather_response = requests.get(weather_url).json()

        if "current_weather" in weather_response:
            weather = weather_response["current_weather"]
            condition = str(weather["weathercode"])
            bg = get_background(condition)
            st.image(bg, use_column_width=True)
            st.markdown(f"<div class='big-temp'>{weather['temperature']}°C</div>", unsafe_allow_html=True)
            st.markdown(f"<div style='text-align:center;'>Wind: {weather['windspeed']} km/h</div>", unsafe_allow_html=True)
        else:
            st.info("Weather data not available.")

        # 5-Day Weather Forecast
        st.markdown("<div class='section-title'>5-Day Weather Forecast</div>", unsafe_allow_html=True)
        forecast_url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&daily=temperature_2m_max,temperature_2m_min&timezone=auto"
        forecast_response = requests.get(forecast_url).json()

        if "daily" in forecast_response:
            df = pd.DataFrame({
                "Date": forecast_response["daily"]["time"],
                "Max (°C)": forecast_response["daily"]["temperature_2m_max"],
                "Min (°C)": forecast_response["daily"]["temperature_2m_min"]
            })
            st.dataframe(df.head(5))
        else:
            st.info("Forecast data not available.")

        # Avalanche Risk Placeholder
        st.markdown("<div class='section-title'>Avalanche Risk</div>", unsafe_allow_html=True)
        st.warning("Avalanche risk data coming soon.")

    else:
        st.error("Location not found. Try another one.")
