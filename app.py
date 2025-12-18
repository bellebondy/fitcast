# ============================================================
# FitCast – Outfit Weather Assistant
# Belle Bondy (CEN 3721)
#
# Purpose:
# A Streamlit web app that uses simplified weather data
# and HCI principles to suggest outfits without overwhelming
# the user with raw forecast numbers.
# ============================================================

import streamlit as st
import pandas as pd
import numpy as np
from datetime import date

# ============================================================
# Page Configuration
# ============================================================
st.set_page_config(
    page_title="FitCast – Outfit Weather Assistant",
    layout="wide",
)

# ============================================================
# Custom CSS (light blue theme)
# ============================================================
st.markdown(
    """
    <style>
        .main {
            background-color: #e6f4ff;
        }
        section[data-testid="stSidebar"] {
            background-color: #d9efff;
        }
        h1, h2, h3 {
            color: #1f2d3d;
        }
    </style>
    """,
    unsafe_allow_html=True
)

# ============================================================
# Session State Initialization
# ============================================================
if "generate_outfit" not in st.session_state:
    st.session_state.generate_outfit = False

if "weather_data" not in st.session_state:
    st.session_state.weather_data = None

# ============================================================
# Sidebar – Navigation
# ============================================================
st.sidebar.title("FitCast Menu")

page = st.sidebar.radio(
    "Go to",
    ["Home", "Outfit Planner", "Forecast Details", "About HCI Choices"]
)

st.sidebar.markdown("---")
st.sidebar.subheader("Outfit Settings")

# ============================================================
# User Inputs
# ============================================================
city = st.sidebar.selectbox(
    "City",
    ["Miami", "New York", "Chicago", "Los Angeles"]
)

style = st.sidebar.selectbox(
    "Style",
    ["Cozy", "Casual", "Dressy", "Sporty"]
)

selected_day = st.sidebar.date_input(
    "Day",
    value=date.today()
)

comfort_level = st.sidebar.radio(
    "My comfort level",
    [
        "I am a furnace",
        "I run warm",
        "I am normal",
        "I run cold",
        "I am freezing all the time",
    ]
)

show_shoes = st.sidebar.checkbox("Show shoe suggestions", value=True)

if st.sidebar.button("Get my outfit"):
    st.session_state.generate_outfit = True

# ============================================================
# Title
# ============================================================
st.title("FitCast – Outfit Weather Assistant")
st.caption("Weather-powered outfit ideas with a little HCI sprinkled in.")


# ============================================================
# Helper Functions
# ============================================================

def get_mock_weather(city):
    """
    Returns simplified mock weather data.
    Focus is usability, not forecast accuracy.
    """
    base = {
        "Miami": (75, 85),
        "New York": (60, 72),
        "Chicago": (55, 68),
        "Los Angeles": (65, 78),
    }

    low, high = base[city]
    feels_like = int((low + high) / 2 + np.random.randint(-2, 3))

    return {
        "low": low,
        "high": high,
        "feels_like": feels_like,
        "rain_chance": np.random.choice(["Low", "Medium", "High"])
    }


def adjust_for_comfort(feels_like, comfort):
    """
    Adjust perceived temperature based on comfort level.
    """
    adjustments = {
        "I am a furnace": 6,
        "I run warm": 3,
        "I am normal": 0,
        "I run cold": -3,
        "I am freezing all the time": -6,
    }

    return feels_like + adjustments[comfort]


def generate_outfit(adjusted_temp, style):
    """
    Generate outfit recommendations based on adjusted temp + style.
    """
    if adjusted_temp >= 80:
        top = "light tank or breathable tee"
        outer = "no jacket needed"
    elif adjusted_temp >= 70:
        top = "short-sleeve shirt"
        outer = "optional light layer"
    elif adjusted_temp >= 60:
        top = "long-sleeve top"
        outer = "light jacket or cardigan"
    else:
        top = "warm sweater"
        outer = "jacket or coat"

    bottoms = {
        "Cozy": "soft pants or leggings",
        "Casual": "jeans",
        "Dressy": "tailored pants or skirt",
        "Sporty": "athletic bottoms",
    }

    return top, outer, bottoms[style]


def shoe_suggestion(adjusted_temp, rain):
    if rain == "High":
        return "water-resistant shoes"
    if adjusted_temp >= 75:
        return "sandals or breathable sneakers"
    elif adjusted_temp >= 60:
        return "sneakers or flats"
    else:
        return "closed-toe shoes or boots"


# ============================================================
# HOME PAGE
# ============================================================
if page == "Home":
    st.subheader("Welcome")

    st.write(
        """
        FitCast helps you decide what to wear without overthinking it.

        Instead of showing raw forecast numbers, this app translates
        weather conditions into a **clear, wearable outfit idea**.

        Use the sidebar to customize your preferences and generate
        an outfit suggestion tailored to *you*.
        """
    )

# ============================================================
# OUTFIT PLANNER PAGE
# ============================================================
elif page == "Outfit Planner":
    st.subheader("Your Outfit Suggestion")

    if not st.session_state.generate_outfit:
        st.info("Choose your preferences in the sidebar and click **Get my outfit**.")
    else:
        weather = get_mock_weather(city)
        st.session_state.weather_data = weather

        adjusted_temp = adjust_for_comfort(
            weather["feels_like"],
            comfort_level
        )

        top, outer, bottom = generate_outfit(adjusted_temp, style)

        st.success(f"Outfit ready for **{city}** on **{selected_day}**")

        col1, col2 = st.columns(2)

        with col1:
            st.markdown("### Outfit Breakdown")
            st.markdown(f"**Top:** {top}")
            st.markdown(f"**Outer layer:** {outer}")
            st.markdown(f"**Bottom:** {bottom}")
            st.markdown(f"**Style vibe:** {style}")

        with col2:
            st.markdown("### Comfort Logic")
            st.markdown(f"- Feels like: **{weather['feels_like']}°F**")
            st.markdown(f"- Adjusted for comfort: **{adjusted_temp}°F**")
            st.markdown(f"- Rain chance: **{weather['rain_chance']}**")

        if show_shoes:
            shoes = shoe_suggestion(adjusted_temp, weather["rain_chance"])
            st.markdown(f"### Shoes 👟\n**{shoes}**")

# ============================================================
# FORECAST DETAILS PAGE
# ============================================================
elif page == "Forecast Details":
    st.subheader("Forecast Details")

    if st.session_state.weather_data is None:
        st.info("Generate an outfit first to view forecast details.")
    else:
        data = st.session_state.weather_data

        df = pd.DataFrame(
            {
                "Metric": ["Low Temp", "High Temp", "Feels Like", "Rain Chance"],
                "Value": [
                    f"{data['low']}°F",
                    f"{data['high']}°F",
                    f"{data['feels_like']}°F",
                    data["rain_chance"],
                ],
            }
        )

        st.table(df)

        st.caption(
            "Forecast data is intentionally simplified to support usability testing."
        )

# ============================================================
# HCI / UX PAGE
# ============================================================
elif page == "About HCI Choices":
    st.subheader("About the HCI / UX choices")

    st.markdown(
        """
        **Target users**
        - Students and young professionals getting dressed for class, work, or social plans  
        - People who want guidance without analyzing weather charts  

        **Usability goals**
        - **Effectiveness:** Convert weather data into one clear outfit suggestion  
        - **Efficiency:** All controls live in the sidebar; one click generates results  
        - **Learnability:** Uses familiar widgets (dropdowns, radio buttons, checkboxes)  
        - **User satisfaction:** Friendly language and comfort-based choices  

        **HCI principles applied**
        - **Visibility & feedback:** Success and info messages explain system state  
        - **Consistency:** Light blue theme and layout match my Project 1 usability tool  
        - **Error prevention:** Pages guide users instead of failing silently  
        - **Match with the real world:** Comfort levels like “I am a furnace” instead of numbers  

        This design prioritizes **decision support**, not raw data display.
        """
    )
