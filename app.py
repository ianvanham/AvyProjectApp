
import streamlit as st
from dotenv import load_dotenv
import os
import requests
import pandas as pd

load_dotenv()

# API Keys
GEOAPIFY_API_KEY = os.getenv("GEOAPIFY_API_KEY")
OPEN_METEO_API_KEY = os.getenv("OPEN_METEO_API_KEY")

st.set_page_config(page_title="KNOW BEFORE YOU GO", layout="centered")

# CSS Dark Mode + Custom Style
st.markdown("""
    <style>
        body {background-color: #121212; color: white;}
        .big-temp {font-size: 64px; font-weight: bold; text-align: center;}
        .section-title {font-size: 28px; font-weight: bold; margin-top: 20px;}
        .weather-desc {font-size: 22px; text-align: center;}
    </style>
""", unsafe_allow_html=True)

st.markdown("<h2 style='text-align:center;'>KNOW BEFORE YOU GO</h2>", unsafe_allow_html=True)

location = st.text_input("Search location")

weather_icons = {
    "clear": "https://raw.githubusercontent.com/mattiavilla/icons/main/clear.png",
    "cloud": "https://raw.githubusercontent.com/mattiavilla/icons/main/cloud.png",
    "rain": "https://raw.githubusercontent.com/mattiavilla/icons/main/rain.png",
    "snow": "https://raw.githubusercontent.com/mattiavilla/icons/main/snow.png",
    "fog": "https://raw.githubusercontent.com/mattiavilla/icons/main/fog.png",
}

def get_icon(description):
    desc = description.lower()
    for key in weather_icons:
        if key in desc:
            return weather_icons[key]
    return weather_icons["cloud"]

if location:
    geo_url = f"https://api.geoapify.com/v1/geocode/search?text={location}&apiKey={GEOAPIFY_API_KEY}"
    geo_response = requests.get(geo_url).json()

    if geo_response.get("features"):
        coords = geo_response["features"][0]["geometry"]["coordinates"]
        lon, lat = coords[0], coords[1]
        st.map({'lat': [lat], 'lon': [lon]})

        # Current Weather
        st.subheader("Current Weather")

        weather_url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current_weather=true&daily=temperature_2m_max,temperature_2m_min&timezone=auto"
        weather_response = requests.get(weather_url).json()

        if "current_weather" in weather_response and "daily" in weather_response:
            weather = weather_response["current_weather"]
            daily = weather_response["daily"]

            icon_url = get_icon(str(weather["weathercode"]))
            st.image(icon_url, width=150)

            st.markdown(f"<div class='big-temp'>{weather['temperature']}°C</div>", unsafe_allow_html=True)
            st.markdown("<div class='weather-desc'>Nuvoloso</div>", unsafe_allow_html=True)
            st.markdown(f"<div style='text-align:center;'>Max: {daily['temperature_2m_max'][0]}° Min: {daily['temperature_2m_min'][0]}°</div>", unsafe_allow_html=True)
            st.markdown(f"<div style='text-align:center;'>Wind: {weather['windspeed']} km/h</div>", unsafe_allow_html=True)
        else:
            st.info("Weather data not available.")
    else:
        st.error("Location not found. Try another one.")
