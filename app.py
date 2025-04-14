
import streamlit as st
from dotenv import load_dotenv
import os
import requests

load_dotenv()

GEOAPIFY_API_KEY = os.getenv("GEOAPIFY_API_KEY")
OPEN_METEO_API_KEY = os.getenv("OPEN_METEO_API_KEY")

st.set_page_config(page_title="KNOW BEFORE YOU GO", layout="centered")

weather_images = {
    "clear": "https://raw.githubusercontent.com/mattiavilla/icons/main/clear_bg.jpg",
    "cloud": "https://raw.githubusercontent.com/mattiavilla/icons/main/cloud_bg.jpg",
    "rain": "https://raw.githubusercontent.com/mattiavilla/icons/main/rain_bg.jpg",
    "snow": "https://raw.githubusercontent.com/mattiavilla/icons/main/snow_bg.jpg",
    "fog": "https://raw.githubusercontent.com/mattiavilla/icons/main/fog_bg.jpg",
}

def get_background(description):
    desc = description.lower()
    for key in weather_images:
        if key in desc:
            return weather_images[key]
    return weather_images["cloud"]

st.markdown("""
    <style>
        .overlay {
            position: absolute;
            top: 30%;
            left: 50%;
            transform: translate(-50%, -50%);
            color: white;
            text-align: center;
        }
        .big-temp {
            font-size: 64px;
            font-weight: bold;
        }
        .weather-desc {
            font-size: 24px;
        }
    </style>
""", unsafe_allow_html=True)

st.markdown("<h2 style='text-align:center;'>KNOW BEFORE YOU GO</h2>", unsafe_allow_html=True)

location = st.text_input("Search location")

if location:
    geo_url = f"https://api.geoapify.com/v1/geocode/search?text={location}&apiKey={GEOAPIFY_API_KEY}"
    geo_response = requests.get(geo_url).json()

    if geo_response.get("features"):
        coords = geo_response["features"][0]["geometry"]["coordinates"]
        lon, lat = coords[0], coords[1]

        weather_url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current_weather=true&daily=temperature_2m_max,temperature_2m_min&timezone=auto"
        weather_response = requests.get(weather_url).json()

        if "current_weather" in weather_response and "daily" in weather_response:
            weather = weather_response["current_weather"]
            daily = weather_response["daily"]
            condition = str(weather["weathercode"])

            bg = get_background(condition)
            st.image(bg, use_column_width=True)

            st.markdown(f"""
                <div class="overlay">
                    <div class="big-temp">{weather['temperature']}°C</div>
                    <div class="weather-desc">Nuvoloso</div>
                    <div>Max: {daily['temperature_2m_max'][0]}° Min: {daily['temperature_2m_min'][0]}°</div>
                    <div>Wind: {weather['windspeed']} km/h</div>
                </div>
            """, unsafe_allow_html=True)

        else:
            st.info("Weather data not available.")

    else:
        st.error("Location not found. Try another one.")
