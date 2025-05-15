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

if st.session_state.page == "terrain":
    st.markdown(f"## 🧭 Terrain Dangers – {location}")
    st.markdown("""
    Understand avalanche-prone zones, cliffs, cornices, and glacier features.
    Use terrain classifications to decide safe approach lines.
    """)
    st.markdown("<div style='height:300px;background:#222;border-radius:12px;display:flex;align-items:center;justify-content:center;color:white;'>[Terrain Map Placeholder]</div>", unsafe_allow_html=True)
    st.button("🔙 Back to checklist", on_click=lambda: st.session_state.update({"page": "checklist"}))

elif st.session_state.page == "weather":
    st.markdown(f"## 🌩️ Weather – {location}")
    st.markdown("""
    Check temperature swings, wind speed, and storm alerts.
    Weather determines timing, exposure, and safe windows.
    """)
    st.markdown("<div style='height:200px;background:#333;border-radius:12px;display:flex;align-items:center;justify-content:center;color:white;'>[Live Weather Module]</div>", unsafe_allow_html=True)
    st.button("🔙 Back to checklist", on_click=lambda: st.session_state.update({"page": "checklist"}))

elif st.session_state.page == "route":
    st.markdown(f"## 🗺️ Route Study – {location}")
    st.markdown("""
    Visualize your path: start, key transitions, exposure zones, and safe exits.
    Study the slope gradients, altimetry, and time estimates.
    """)
    st.markdown("<div style='height:250px;background:#1a1a1a;border-radius:12px;color:white;display:flex;align-items:center;justify-content:center;'>[Route Analysis Tool]</div>", unsafe_allow_html=True)
    st.button("🔙 Back to checklist", on_click=lambda: st.session_state.update({"page": "checklist"}))

elif st.session_state.page == "capacities":
    st.markdown(f"## 💪 Group Capacities – {location}")
    st.markdown("""
    Evaluate skills, fitness, and experience level of each participant.
    Plan the objective based on the least experienced member.
    """)
    st.markdown("<div style='height:150px;background:#202020;border-radius:12px;color:white;display:flex;align-items:center;justify-content:center;'>[Capacity Checklist]</div>", unsafe_allow_html=True)
    st.button("🔙 Back to checklist", on_click=lambda: st.session_state.update({"page": "checklist"}))

elif st.session_state.page == "equipment":
    st.markdown(f"## ⛏️ Equipment – {location}")
    st.markdown("""
    Verify that every team member carries transceiver, shovel, probe, helmet, map and radio.
    Optional: crampons, skins, bivy, airbag depending on route.
    """)
    st.markdown("<div style='height:200px;background:#252525;border-radius:12px;color:white;display:flex;align-items:center;justify-content:center;'>[Equipment Overview]</div>", unsafe_allow_html=True)
    st.button("🔙 Back to checklist", on_click=lambda: st.session_state.update({"page": "checklist"}))

elif st.session_state.page == "problems":
    st.markdown(f"## 🧠 Possible Problems – {location}")
    st.markdown("""
    Think ahead: delayed return, fog, injuries, missing gear, exhaustion.
    Create backups and define checkpoints for go/no-go.
    """)
    st.markdown("<div style='height:180px;background:#2a2a2a;border-radius:12px;color:white;display:flex;align-items:center;justify-content:center;'>[Scenario Planner]</div>", unsafe_allow_html=True)
    st.button("🔙 Back to checklist", on_click=lambda: st.session_state.update({"page": "checklist"}))

