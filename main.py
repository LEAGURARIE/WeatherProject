import streamlit as st
from streamlit_folium import st_folium
import folium
from datetime import datetime, timedelta
import plotly.graph_objects as go
import os
from dotenv import load_dotenv
from api import get_weather, get_historical_weather
from utills import get_city_coordinates

load_dotenv()
appid = os.getenv("API_KEY")

# ------------------ Language Toggle ------------------
lang = st.radio("🌐 Language / שפה", ["English", "עברית"], horizontal=True)

# CSS לשינוי כיוון כל הדף לפי השפה
if lang == "עברית":
    st.markdown(
        """
        <style>
        html, body, #root > div:nth-child(1) {
            direction: rtl !important;
            text-align: right !important;
        }
        input, textarea, button, select {
            direction: rtl !important;
            text-align: right !important;
        }
        </style>
        """,
        unsafe_allow_html=True
    )
else:
    st.markdown(
        """
        <style>
        html, body, #root > div:nth-child(1) {
            direction: ltr !important;
            text-align: left !important;
        }
        input, textarea, button, select {
            direction: ltr !important;
            text-align: left !important;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

if lang == "English":
    city_label = "🏙️ Enter city name:"
    placeholder_text = "Type the city name..."
else:
    city_label = "🏙️ הקלד שם עיר:"
    placeholder_text = "הקלד את שם העיר..."

# ------------------ User Input ------------------
user_input = st.text_input(city_label, placeholder=placeholder_text)

if user_input.strip():
    city_coords = get_city_coordinates(user_input)
    if "error" in city_coords:
        st.error(f"❌ {city_coords['error']}")
        st.stop()

    lat = city_coords["lat"]
    lon = city_coords["lon"]

    units = "metric"
    exclude = "minutely,hourly,alerts"

    try:
        with st.spinner("🌤️ Fetching weather data..."):
            response = get_weather(lat, lon, exclude, units, appid)
            data = response.json()
    except Exception as e:
        st.error(f"❌ Error fetching weather data: {e}")
        st.stop()

    yesterday_dt = int((datetime.utcnow() - timedelta(days=1)).timestamp())
    try:
        hist_response = get_historical_weather(lat, lon, yesterday_dt, units, appid)
        hist_data = hist_response.json()
        temp_yesterday = hist_data.get("data", [{}])[0].get("temp", None)
    except Exception:
        temp_yesterday = None

    current_temp = data["current"]["temp"]
    wind_speed = data["current"]["wind_speed"]
    clouds = data["current"]["clouds"]

    if lang == "English":
        st.markdown(f"## 🌤️ Current Weather in **{user_input.title()}**")
    else:
        st.markdown(f"## 🌤️ מזג אוויר ב**{user_input}**")

    col1, col2, col3 = st.columns(3)
    if lang == "English":
        with col1:
            st.metric("🌡️ Temperature", f"{current_temp}°C",
                      delta=f"{current_temp - temp_yesterday:.1f}°C" if temp_yesterday else None)
        with col2:
            st.metric("🌬️ Wind Speed", f"{wind_speed} m/s")
        with col3:
            st.metric("☁️ Cloudiness", f"{clouds}%")
    else:
        with col1:
            st.metric("🌡️ טמפרטורה", f"{current_temp}°C",
                      delta=f"{current_temp - temp_yesterday:.1f}°C" if temp_yesterday else None)
        with col2:
            st.metric("🌬️ מהירות רוח", f"{wind_speed} מ/ש ")
        with col3:
            st.metric("☁️ עננות", f"{clouds}%")

    m = folium.Map(location=[lat, lon], zoom_start=10)
    folium.Marker([lat, lon], tooltip=user_input, icon=folium.Icon(color="red")).add_to(m)
    st_folium(m, width=700, height=300)

    if lang == "English":
        st.markdown(f"## 📅 Weekly Weather Forecast for {user_input.title()}")
        tab1, tab2, tab3 = st.tabs(["🌡️ Temperature", "🌬️ Wind Speed", "☁️ Cloudiness"])
    else:
        st.markdown(f"## 📅 תחזית מזג אוויר שבועית {user_input}")
        tab1, tab2, tab3 = st.tabs(["🌡️ מעלות", "🌬️ רוח", "☁️ עננות"])

    days = [datetime.fromtimestamp(d["dt"]).strftime("%d/%m") for d in data["daily"][:7]]
    temps = [d["temp"]["day"] for d in data["daily"][:7]]
    winds = [d["wind_speed"] for d in data["daily"][:7]]
    clouds_list = [d["clouds"] for d in data["daily"][:7]]

    def plot_area_chart(x, y, color, show_percent=False, add_unit=""):
        if show_percent:
            text_vals = [f"<b>{val:.1f}%</b>" for val in y]
        elif add_unit:
            text_vals = [f"<b>{val:.1f} {add_unit}</b>" for val in y]
        else:
            text_vals = [f"<b>{val:.1f}</b>" for val in y]

        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=list(range(len(x))),
            y=y,
            mode='lines+markers+text',
            fill='tozeroy',
            line=dict(color=color, width=3),
            marker=dict(size=8, color=color),
            text=text_vals,
            textposition="top center",
            textfont=dict(
                size=16,
                color="black",
                family="Arial Black, Arial, sans-serif"
            )
        ))

        fig.update_layout(
            xaxis_title="",
            yaxis=dict(visible=False, range=[0, 50]),
            height=280,
            margin=dict(l=50, r=50, t=30, b=30),
            template="plotly_white",
            hovermode=False,
            xaxis=dict(
                tickangle=-45,
                range=[-0.5, len(x) - 0.5],
                tickmode='array',
                tickvals=list(range(len(x))),
                ticktext=x,
            )
        )
        return fig

    with tab1:
            st.plotly_chart(plot_area_chart(days, temps, "red", show_percent=False), use_container_width=True)

    with tab2:
        if lang == "English":
            st.plotly_chart(plot_area_chart(days, winds, "orange", add_unit="m/s"), use_container_width=True)
        else:
            st.plotly_chart(plot_area_chart(days, winds, "orange", add_unit="מ/ש"), use_container_width=True)

    with tab3:
            st.plotly_chart(plot_area_chart(days, clouds_list, "gray", show_percent=True), use_container_width=True)
