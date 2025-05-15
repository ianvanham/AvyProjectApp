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

st.markdown("<h2 style='text-align:center;'>KNOW BEFORE YOU GO</h2>", unsafe_allow_html=True)

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

    st.markdown("## 🏠 At Home: Analyze and Plan")

    col1, col2 = st.columns(2)

    with col1:
        if st.button("🧭 Terrain\ndangers", key="terrain_btn"):
            st.session_state.page = "terrain"
        if st.button("🗺️ Route\nStudy", key="route_btn"):
            st.session_state.page = "route"
        if st.button("⛏️ Equipment", key="equip_btn"):
            st.session_state.page = "equipment"

    with col2:
        if st.button("🌩️ Weather", key="weather_btn"):
            st.session_state.page = "weather"
        if st.button("💪 Capacities", key="cap_btn"):
            st.session_state.page = "capacities"
        if st.button("🧠 Possible\nproblems", key="prob_btn"):
            st.session_state.page = "problems"

    st.markdown("---")
    st.markdown("❌ **Change the activity or prepare yourself better**")

# ready to continue with page-specific sections
