

import streamlit as st
from dotenv import load_dotenv
import os
import requests
import pandas as pd
from datetime import datetime

load_dotenv()

GEOAPIFY_API_KEY = os.getenv("GEOAPIFY_API_KEY")
OPEN_METEO_API_KEY = os.getenv("OPEN_METEO_API_KEY")

st.set_page_config(page_title="KNOW BEFORE YOU GO", layout="centered")

st.markdown("""
    <style>
        body {background-color: #121212; color: white;}
        .temp-now {font-size: 56px; font-weight: bold;}
        .section-title {font-size: 24px; font-weight: bold; margin-top: 20px;}
        .forecast-table {
            width: 100%;
            border-collapse: collapse;
            font-size: 16px;
        }
        .forecast-table th, .forecast-table td {
            border: 1px solid #444;
            padding: 10px;
            text-align: center;
        }
        .forecast-table th {
            background-color: #1E1E1E;
        }
        .precip-badge {
            color: #00BFFF;
            font-weight: bold;
        }
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

weathercode_map = {
    0: "clear", 1: "clear", 2: "clear",
    3: "cloud", 45: "fog", 48: "fog",
    51: "rain", 53: "rain", 55: "rain", 61: "rain", 63: "rain", 65: "rain", 80: "rain",
    71: "snow", 73: "snow", 75: "snow", 85: "snow", 86: "snow"
}

def get_icon(code):
    condition = weathercode_map.get(code, "cloud")
    return weather_icons.get(condition, "🌡️")

if location:
    geo_url = f"https://api.geoapify.com/v1/geocode/search?text={location}&apiKey={GEOAPIFY_API_KEY}"
    geo_response = requests.get(geo_url).json()

    if geo_response.get("features"):
        coords = geo_response["features"][0]["geometry"]["coordinates"]
        lon, lat = coords[0], coords[1]

        st.map({'lat': [lat], 'lon': [lon]})

        forecast_url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current_weather=true&daily=temperature_2m_max,temperature_2m_min,precipitation_sum,windspeed_10m_max,weathercode&timezone=auto"
        response = requests.get(forecast_url).json()

        if "daily" in response:
            daily = response["daily"]

            st.subheader("5-Day Weather Forecast")
            table_html = '''
            <table class="forecast-table">
                <thead>
                    <tr>
                        <th>Date</th>
                        <th>Icon</th>
                        <th>Max</th>
                        <th>Min</th>
                        <th>Wind</th>
                        <th>Precip.</th>
                    </tr>
                </thead>
                <tbody>
            '''

            for i in range(5):
                date = datetime.strptime(daily["time"][i], "%Y-%m-%d").strftime("%a %d %b")
                icon = get_icon(daily["weathercode"][i])
                tmax = f"{daily['temperature_2m_max'][i]}°C"
                tmin = f"{daily['temperature_2m_min'][i]}°C"
                wind = f"{daily['windspeed_10m_max'][i]} km/h"
                precip = f"<span class='precip-badge'>{daily['precipitation_sum'][i]} mm</span>"

                table_html += f'''
                    <tr>
                        <td>{date}</td>
                        <td>{icon}</td>
                        <td>{tmax}</td>
                        <td>{tmin}</td>
                        <td>{wind}</td>
                        <td>{precip}</td>
                    </tr>
                '''

            table_html += "</tbody></table>"
            st.markdown(table_html, unsafe_allow_html=True)

        else:
            st.info("Weather data not available.")

        # Avalanche Risk Placeholder
        st.markdown("<div class='section-title'>Avalanche Risk</div>", unsafe_allow_html=True)
        st.warning("Avalanche risk data coming soon.")

        