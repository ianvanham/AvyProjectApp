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
:root {
    --font-size: 16px;
    --padding: 10px;
    --color-bg: #121212;
    --color-card: #1E1E1E;
    --color-border: #555;
    --color-text: #FFFFFF;
    --radius: 12px;
}

body {
    background-color: var(--color-bg);
    color: var(--color-text);
    font-size: var(--font-size);
}

.square-button, .live-box, .risk-badge {
    font-size: 1rem;
    padding: var(--padding);
    border-radius: var(--radius);
}

@media screen and (max-width: 600px) {
    .square-button {
        width: 100% !important;
        margin: 5px auto;
        font-size: 16px;
        height: auto;
    }
    .live-box {
        flex-direction: column;
        gap: 1rem;
    }
    .left, .right {
        font-size: 48px !important;
    }
    .section-title {
        font-size: 20px;
    }
}
</style>
""", unsafe_allow_html=True)

if 'location' in locals():
    st.markdown(f"<h2 style='text-align:center;'>📍 {location} — KNOW BEFORE YOU GO</h2>", unsafe_allow_html=True)

location = st.selectbox("📍 Select location", ["Cervinia", "Bormio", "Cortina"])

if "page" not in st.session_state:
    st.session_state.page = "checklist"

if not location:
    st.info("Please select a location to continue.")
elif st.session_state.page == "checklist":
    st.markdown("""
    <style>
    .square-button {
        display: flex;
        align-items: center;
        justify-content: center;
        background: linear-gradient(145deg, #1c1c1c, #101010);
        color: white;
        border: 1px solid #333;
        border-radius: 12px;
        height: 100px;
        font-weight: 600;
        font-size: 16px;
        margin: 8px;
        width: 100%;
        box-shadow: 0 4px 8px rgba(0,0,0,0.4);
        transition: background 0.2s;
    }
    .square-button:hover {
        background: #222;
    }
    </style>
    """, unsafe_allow_html=True)

    st.markdown("## 🏠 At Home: Analyze and Plan")

    cols = st.columns(2)

    buttons = [
        ("🧭 Terrain dangers", "terrain"),
        ("🌩️ Weather", "weather"),
        ("🗺️ Route Study", "route"),
        ("💪 Capacities", "capacities"),
        ("⛏️ Equipment", "equipment"),
        ("🧠 Possible problems", "problems")
    ]

    for i, (label, key) in enumerate(buttons):
        with cols[i % 2]:
            if st.button(label, key=f"{key}_btn"):
                st.session_state.page = key

    st.markdown("---")
    st.markdown("❌ **Change the activity or prepare yourself better**")

# --- Begin page-specific sections ---

# Load coordinates
location_coords = {
    "Cervinia": (45.936, 7.627),
    "Bormio": (46.467, 10.375),
    "Cortina": (46.538, 12.135)
}

lat, lon = location_coords.get(location, (45.0, 7.0))

# Fetch weather
weather = {}
try:
    response = requests.get(
        f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current_weather=true&timezone=auto"
    )
    if response.ok:
        data = response.json()
        weather = data.get("current_weather", {})
except Exception as e:
    st.warning(f"Weather API error: {e}")

if st.session_state.page == "terrain":
    import gpxpy
    import plotly.graph_objects as go

    st.markdown(f"## 🧭 Terrain Dangers – {location}")
    st.markdown("""
    Understand avalanche-prone zones, cliffs, cornices, and glacier features.
    Use terrain classifications to decide safe approach lines.
    """)

    gpx_path = f"data/{location.lower()}.gpx"
    elevation_data = []
    distance_data = []
    total_distance = 0.0

    try:
        with open(gpx_path, 'r') as gpx_file:
            gpx = gpxpy.parse(gpx_file)
            prev_point = None
            for track in gpx.tracks:
                for segment in track.segments:
                    for point in segment.points:
                        if prev_point:
                            total_distance += point.distance_2d(prev_point) / 1000.0
                        elevation_data.append(point.elevation)
                        distance_data.append(total_distance)
                        prev_point = point

        if elevation_data and distance_data:
            fig = go.Figure()
            fig.add_trace(go.Scatter(x=distance_data, y=elevation_data, mode='lines', fill='tozeroy'))
            fig.update_layout(
                title="Terrain Elevation Profile",
                xaxis_title="Distance (km)",
                yaxis_title="Elevation (m)",
                template="plotly_dark",
                height=300
            )
            st.plotly_chart(fig)
    except Exception as e:
        st.warning(f"GPX elevation data not loaded: {e}")

    st.button("🔙 Back to checklist", on_click=lambda: st.session_state.update({"page": "checklist"}))

elif st.session_state.page == "weather":
    st.markdown(f"## 🌩️ Weather – {location}")
    st.markdown("""
    Check temperature swings, wind speed, and storm alerts.
    Weather determines timing, exposure, and safe windows.
    """)
    st.markdown(
        "<div style='height:200px;background:#333;border-radius:12px;display:flex;align-items:center;justify-content:center;color:white;'>"
        "🌡️ Temp: {}°C, 💨 Wind: {} km/h"
        "</div>".format(weather.get("temperature", "-"), weather.get("windspeed", "-")),
        unsafe_allow_html=True
    )
    st.button("🔙 Back to checklist", on_click=lambda: st.session_state.update({"page": "checklist"}))

