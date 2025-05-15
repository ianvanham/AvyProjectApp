import streamlit as st
from dotenv import load_dotenv
import os
import requests
import pandas as pd
from datetime import datetime
import streamlit.components.v1 as components

load_dotenv()

GEOAPIFY_API_KEY = os.getenv("GEOAPIFY_API_KEY")
OPEN_METEO_API_KEY = os.getenv("OPEN_METEO_API_KEY")

st.set_page_config(page_title="KNOW BEFORE YOU GO", layout="centered")

st.markdown("""
<style>
    body {background-color: #121212; color: white;}
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

st.markdown("<h2 style='text-align:center;'>KNOW BEFORE YOU GO</h2>", unsafe_allow_html=True)

# Campo posizione subito dopo il titolo
location = st.text_input("\U0001F4CD Search location", placeholder="e.g. Cortina d'Ampezzo, Italy")

# --- At Home Checklist (2 colonne simmetriche con bottoni quadrati) ---
st.markdown("""
<style>
.square-button {
    display: flex;
    align-items: center;
    justify-content: center;
    background-color: #1E1E1E;
    color: white;
    border: 2px solid #555;
    border-radius: 12px;
    height: 100px;
    font-weight: bold;
    font-size: 18px;
    margin: 10px;
    width: 100%;
    transition: background-color 0.2s ease;
}
.square-button:hover {
    background-color: #333;
}
</style>
""", unsafe_allow_html=True)

st.markdown("## \U0001F3E0 At Home: Analyze and Plan")

col1, col2 = st.columns(2)

with col1:
    if st.button("\U0001F9ED Terrain\ndangers", key="terrain_btn"):
        st.session_state.page = "terrain"
    if st.button("\U0001F5FA️ Route\nStudy", key="route_btn"):
        st.session_state.page = "route"
    if st.button("⛏️ Equipment", key="equip_btn"):
        st.session_state.page = "equipment"

with col2:
    if st.button("\U0001F329️ Weather", key="weather_btn"):
        st.session_state.page = "weather"
    if st.button("\U0001F4AA Capacities", key="cap_btn"):
        st.session_state.page = "capacities"
    if st.button("\U0001F9E0 Possible\nproblems", key="prob_btn"):
        st.session_state.page = "problems"

st.markdown("---")
st.markdown("\u274c **Change the activity or prepare yourself better**")

# --- Weather Section ---
weather_icons = {
    "clear": "\u2600\ufe0f",
    "cloud": "\u2601\ufe0f",
    "rain": "\ud83c\udf27\ufe0f",
    "snow": "\u2744\ufe0f",
    "fog": "\ud83c\udf2b\ufe0f",
}

weathercode_map = {
    0: "clear", 1: "clear", 2: "clear",
    3: "cloud", 45: "fog", 48: "fog",
    51: "rain", 53: "rain", 55: "rain", 61: "rain", 63: "rain", 65: "rain", 80: "rain",
    71: "snow", 73: "snow", 75: "snow", 85: "snow", 86: "snow"
}

def get_icon(code):
    condition = weathercode_map.get(code, "cloud")
    return weather_icons.get(condition, "\ud83c\udf21\ufe0f")

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

            avalanche_risk = 2  # static for now

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

            st.markdown("<div class='section-title'>Official Avalanche Bulletin</div>", unsafe_allow_html=True)
            components.iframe("https://bollettini.aineva.it/bulletin/latest", height=600, scrolling=True)

            st.subheader("5-Day Weather Forecast")

            table_html = '''<table><thead><tr><th>Date</th><th>Icon</th><th>Max</th><th>Min</th><th>Wind</th><th>Precip.</th></tr></thead><tbody>'''

            for i in range(5):
                date = datetime.strptime(daily["time"][i], "%Y-%m-%d").strftime("%a %d %b")
                icon = get_icon(daily["weathercode"][i])
                tmax = f"{daily['temperature_2m_max'][i]}°C"
                tmin = f"{daily['temperature_2m_min'][i]}°C"
                wind = f"{daily['windspeed_10m_max'][i]} km/h"
                precip = f"<span class='precip-badge'>{daily['precipitation_sum'][i]} mm</span>"

                table_html += f'''<tr><td>{date}</td><td>{icon}</td><td>{tmax}</td><td>{tmin}</td><td>{wind}</td><td>{precip}</td></tr>'''

            table_html += "</tbody></table>"
            st.markdown(table_html, unsafe_allow_html=True)

        else:
            st.info("Weather data not available.")
