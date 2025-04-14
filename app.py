
import streamlit as st
from dotenv import load_dotenv
import os
import requests
import pandas as pd

# Load environment variables
load_dotenv()

# API Keys
GEOAPIFY_API_KEY = os.getenv("GEOAPIFY_API_KEY")
OPEN_METEO_API_KEY = os.getenv("OPEN_METEO_API_KEY")
WEBCAM_API_KEY = os.getenv("WEBCAM_API_KEY")

st.set_page_config(page_title="KNOW BEFORE YOU GO", layout="centered")

st.markdown("## KNOW BEFORE YOU GO")
st.markdown("### Plan smarter. Ride safer. Stay updated.")

location = st.text_input("Search location")

if location:
    geo_url = f"https://api.geoapify.com/v1/geocode/search?text={location}&apiKey={GEOAPIFY_API_KEY}"
    geo_response = requests.get(geo_url).json()
    
    if geo_response.get("features"):
        coords = geo_response["features"][0]["geometry"]["coordinates"]
        lon, lat = coords[0], coords[1]
        
        st.map({'lat': [lat], 'lon': [lon]})
        
        # Current Weather
        st.subheader("Current Weather")

        meteo_url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current_weather=true"
        meteo_response = requests.get(meteo_url).json()

        if "current_weather" in meteo_response:
            weather = meteo_response["current_weather"]
            st.metric("Temperature", f"{weather['temperature']}°C")
            st.metric("Windspeed", f"{weather['windspeed']} km/h")
        else:
            st.info("Weather data not available.")

        # 5-Day Weather Forecast
        st.subheader("5-Day Weather Forecast")

        forecast_url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&daily=temperature_2m_max,temperature_2m_min,precipitation_sum&timezone=auto"
        forecast_response = requests.get(forecast_url).json()

        if "daily" in forecast_response:
            df = pd.DataFrame({
                "Date": forecast_response["daily"]["time"],
                "Temp Max (°C)": forecast_response["daily"]["temperature_2m_max"],
                "Temp Min (°C)": forecast_response["daily"]["temperature_2m_min"],
                "Precipitation (mm)": forecast_response["daily"]["precipitation_sum"]
            })
            st.table(df.head(5))
        else:
            st.info("Forecast data not available.")

        st.warning("Avalanche risk data coming soon based on your area.")

        webcam_url = f"https://api.windy.com/api/webcams/v2/list/nearby={lat},{lon},10?show=webcams:location,image&key={WEBCAM_API_KEY}"
        webcam_response = requests.get(webcam_url).json()
        
        if webcam_response.get("result", {}).get("webcams"):
            st.subheader("Nearby Webcams")
            for cam in webcam_response["result"]["webcams"][:3]:
                st.image(cam["image"]["current"]["preview"])
        else:
            st.info("No webcams found nearby.")
    else:
        st.error("Location not found. Try another one.")
