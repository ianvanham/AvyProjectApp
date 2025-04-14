

import streamlit as st
from dotenv import load_dotenv
import os
import requests
from datetime import datetime

load_dotenv()

GEOAPIFY_API_KEY = os.getenv("GEOAPIFY_API_KEY")
OPEN_METEO_API_KEY = os.getenv("OPEN_METEO_API_KEY")

st.set_page_config(page_title="KNOW BEFORE YOU GO", layout="centered")

st.markdown("""
<style>
    body {background-color: #121212; color: white;}
    .header {display: flex; align-items: center; gap: 10px; margin-bottom: 20px;}
    .header img {height: 50px; border-radius: 8px;}
    .title {font-size: 28px; font-weight: bold;}
    .temp-now {font-size: 64px; font-weight: bold; color: #FFFFFF;}
    .section-title {font-size: 24px; font-weight: bold; margin-top: 20px;}
    .live-box {display: flex; background-color: #1E1E1E; padding: 20px; border-radius: 12px; margin-bottom: 20px;}
    .left {flex: 1; text-align: center; font-size: 80px;}
    .right {flex: 1; text-align: center;}
    .line {border-top: 1px solid #555; margin: 10px 0;}
    .info {color: #CCCCCC; font-size: 18px; margin-top: 4px;}
    .risk-badge {padding: 4px 12px; border-radius: 8px; font-weight: bold; display: inline-block;}
    .risk-low {background-color: #4CAF50; color: white;}
    .risk-medium {background-color: #FFC107; color: black;}
    .risk-high {background-color: #F44336; color: white;}
    table {width: 100%; border-collapse: collapse;}
    th, td {padding: 12px; text-align: center; border-bottom: 1px solid #333;}
    th {background-color: #1E1E1E; color: white;}
    tr:hover {background-color: #2A2A2A;}
    .precip-badge {color: #00BFFF; font-weight: bold;}
</style>
""", unsafe_allow_html=True)

st.markdown("""
<div class='header'>
    <img src='https://i.imgur.com/nb2yuxR.png' alt='Logo'>
    <div class='title'>KNOW BEFORE YOU GO</div>
</div>
""", unsafe_allow_html=True)

location = st.text_input("Search location")

weather_icons = {
    "clear": "☀️",
    "cloud": "☁️",
    "rain": "🌧️",
    "snow": "❄️",
    "fog": "🌫️",
}

weathercode_map = {
    0: "clear", 1: "clear", 2: "clear",
    3: "cloud", 45: "fog", 48: "fog",
    51: "rain", 53: "rain", 55: "rain", 61: "rain", 63: "rain", 65: "rain", 80: "rain",
    71: "snow", 73: "snow", 75: "snow", 85: "snow", 86: "snow"
}

def get_icon(code):
    condition = weathercode_map.get(code, "cloud")
    return weather_icons.get(condition, "🌡️")

def risk_badge(level):
    if level <= 2:
        return "<span class='risk-badge risk-low'>Low</span>"
    elif level == 3:
        return "<span class='risk-badge risk-medium'>Medium</span>"
    else:
        return "<span class='risk-badge risk-high'>High</span>"

if location:
    geo_url = f"https://api.geoapify.com/v1/geocode/search?text={location}&apiKey={GEOAPIFY_API_KEY}"
    geo_response = requests.get(geo_url).json()

    if geo_response.get("features"):
        coords = geo_response["features"][0]["geometry"]["coordinates"]
        lon, lat = coords[0], coords[1]

        st.map({'lat': [lat], 'lon': [lon]})

        forecast_url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current_weather=true&daily=temperature_2m_max,temperature_2m_min,precipitation_sum,windspeed_10m_max,weathercode&timezone=auto"
        response = requests.get(forecast_url).json()

        if "current_weather" in response and "daily" in response:
            weather = response["current_weather"]
            daily = response["daily"]
            avalanche_risk = 2

            st.markdown("<div class='section-title'>Live Weather Now</div>", unsafe_allow_html=True)
            st.markdown(f"""
                <div class='live-box'>
                    <div class='left'>{get_icon(weather['weathercode'])}</div>
                    <div class='right'>
                        <div class='temp-now'>{weather['temperature']}°C</div>
                        <div class='line'></div>
                        <div class='info'>Wind: {weather['windspeed']} km/h</div>
                        <div class='info'>Avalanche Risk: {risk_badge(avalanche_risk)}</div>
                    </div>
                </div>
            """, unsafe_allow_html=True)
