

import streamlit as st
from dotenv import load_dotenv
import os
import requests
import pandas as pd

load_dotenv()

GEOAPIFY_API_KEY = os.getenv("GEOAPIFY_API_KEY")
OPEN_METEO_API_KEY = os.getenv("OPEN_METEO_API_KEY")
WEBCAM_API_KEY = os.getenv("WEBCAM_API_KEY")

st.set_page_config(page_title="KNOW BEFORE YOU GO", layout="centered")

# CSS Style
st.markdown(""" 
    <style>
        body {background-color: #121212; color: white;}
        .temp-now {font-size: 56px; font-weight: bold;}
        .section-title {font-size: 24px; font-weight: bold; margin-top: 20px;}
        .badge {padding: 4px 12px; border-radius: 12px; color: white; display: inline-block; font-weight: bold;}
        .low {background-color: green;}
        .medium {background-color: orange;}
        .high {background-color: red;}
    </style>
""", unsafe_allow_html=True)

st.markdown("<h2 style='text-align:center;'>KNOW BEFORE YOU GO</h2>", unsafe_allow_html=True)

location = st.text_input("Search location")

weather_icons = {
    "clear": "☀️",
    "cloud": "☁️",
    "rain": "🌧️",
    "snow": "❄️",
    "fog": "🌫️",
}

# Mapping da weathercode numerico a descrizione meteo
weathercode_map = {
    0: "clear", 1: "clear", 2: "clear",
    3: "cloud", 45: "fog", 48: "fog",
    51: "rain", 53: "rain", 55: "rain", 61: "rain", 63: "rain", 65: "rain", 80: "rain",
    71: "snow", 73: "snow", 75: "snow", 85: "snow", 86: "snow"
}

def get_icon(description):
    return weather_icons.get(description, "🌡️")

def get_risk_badge(level):
    if level == "Low":
        return "<span class='badge low'>Low</span>"
    if level == "Medium":
        return "<span class='badge medium'>Medium</span>"
    return "<span class='badge high'>High</span>"

if location:
    geo_url = f"https://api.geoapify.com/v1/geocode/search?text={location}&apiKey={GEOAPIFY_API_KEY}"
    geo_response = requests.get(geo_url).json()

    if geo_response.get("features"):
        coords = geo_response["features"][0]["geometry"]["coordinates"]
        lon, lat = coords[0], coords[1]

        st.map({'lat': [lat], 'lon': [lon]})

        weather_url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current_weather=true&daily=temperature_2m_max,temperature_2m_min,weathercode&timezone=auto"
        weather_response = requests.get(weather_url).json()

        if "current_weather" in weather_response and "daily" in weather_response:
            weather = weather_response["current_weather"]
            daily = weather_response["daily"]

            code = weather["weathercode"]
            condition = weathercode_map.get(code, "cloud")

            st.subheader("Current Weather")
            col1, col2 = st.columns([2, 1])
            with col1:
                st.markdown(f"<div class='temp-now'>{weather['temperature']}°C</div>", unsafe_allow_html=True)
                st.markdown(f"Max: {daily['temperature_2m_max'][0]}° Min: {daily['temperature_2m_min'][0]}°")
                st.markdown(f"Wind: {weather['windspeed']} km/h")
            with col2:
                st.markdown(get_icon(condition), unsafe_allow_html=True)

            st.markdown("<div class='section-title'>5-Day Weather Forecast</div>", unsafe_allow_html=True)
            days = pd.to_datetime(daily["time"]).strftime("%a")
            icons = [get_icon(weathercode_map.get(code, "cloud")) for code in daily["weathercode"]]
            df = pd.DataFrame({
                "Day": days,
                "Icon": icons,
                "Max (°C)": daily["temperature_2m_max"],
                "Min (°C)": daily["temperature_2m_min"],
            })
            st.dataframe(df.head(5), use_container_width=True)

            st.markdown("<div class='section-title'>Avalanche Risk</div>", unsafe_allow_html=True)
            st.markdown(get_risk_badge("Low"), unsafe_allow_html=True)

            st.markdown("<div class='section-title'>Webcams</div>", unsafe_allow_html=True)
            for i in range(2):
                st.image("https://raw.githubusercontent.com/mattiavilla/icons/main/mountain.jpg", use_container_width=True)

        else:
            st.info("Weather data not available.")

    else:
        st.error("Location not found. Try another one.")