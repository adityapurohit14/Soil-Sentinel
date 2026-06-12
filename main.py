from altair import value
import streamlit as st
import pandas as pd
import joblib
import base64
import time
import matplotlib.pyplot as plt
import numpy as np
from math import pi
import plotly.express as px
import plotly.graph_objects as go



model = joblib.load("random_forest.pkl")


def set_bg_clear(image_file):
    with open(image_file, "rb") as f:
        data = base64.b64encode(f.read()).decode()

    st.markdown(f"""
    <style>

    .stApp {{
        background-image: url("data:image/png;base64,{data}");
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
    }}

    /* Neon Title */
    .title {{
        text-align:center;
        font-size:40px;
        font-weight:bold;
        color:#00ffcc;
        text-shadow: 0 0 10px #00ffcc, 0 0 20px #00ffcc;
    }}

    /* Neon Card */
    .card {{
        background: rgba(0,0,0,0.4);
        border: 1px solid #00ffcc;
        padding: 20px;
        border-radius: 15px;
        box-shadow: 0 0 20px #00ffcc;
    }}

    /* Neon Button */
    .stButton>button {{
        background-color: black;
        color: #00ffcc;
        border: 1px solid #00ffcc;
        box-shadow: 0 0 10px #00ffcc;
        border-radius: 10px;
        height: 50px;
        width: 100%;
        font-size: 18px;
    }}

    label {{
        color: #00ffcc !important;
        font-weight: bold;
    }}

    </style>
    """, unsafe_allow_html=True)


def set_bg_blur(image_file):
    with open(image_file, "rb") as f:
        data = base64.b64encode(f.read()).decode()

    st.markdown(f"""
    <style>

    .stApp {{
        background: transparent;
    }}

    .stApp::before {{
        content: "";
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;

        background-image: url("data:image/png;base64,{data}");
        background-size: cover;
        background-position: center;

        filter: blur(10px);
        transform: scale(1.08);

        z-index: -2;
    }}

    .stApp::after {{
        content: "";
        position: fixed;
        width: 100%;
        height: 100%;
        background: rgba(0,0,0,0.50);
        z-index: -1;
    }}

    /* Neon Title */
    .title {{
        text-align:center;
        font-size:40px;
        font-weight:bold;
        color:#00ffcc;
        text-shadow: 0 0 10px #00ffcc, 0 0 20px #00ffcc;
    }}

    /* Neon Card */
    .card {{
        background: rgba(0,0,0,0.4);
        border: 1px solid #00ffcc;
        padding: 20px;
        border-radius: 15px;
        box-shadow: 0 0 20px #00ffcc;
    }}

    /* Neon Button */
    .stButton>button {{
        background-color: black;
        color: #00ffcc;
        border: 1px solid #00ffcc;
        box-shadow: 0 0 10px #00ffcc;
        border-radius: 10px;
        height: 50px;
        width: 100%;
        font-size: 18px;
    }}

    label {{
        color: #00ffcc !important;
        font-weight: bold;
    }}

    </style>
    """, unsafe_allow_html=True)

if "page" not in st.session_state:
    st.session_state.page = "welcome"

if "run_prediction" not in st.session_state:
    st.session_state.run_prediction = False

def calculate_percentage(temp, humidity, wind, rainfall):
    score = (wind * 2 + rainfall * 0.3 + (100 - humidity) * 0.5)
    return min(int(score), 100)

def prevention_tips(risk):
    if risk == "High":
        return ["Use vegetation cover", "Avoid overgrazing", "Windbreaks", "Terracing", "Contour plowing"]
    elif risk == "Medium":
        return ["Add mulch", "Monitor wind", "Control water runoff"]
    else:
        return ["No action needed", "Maintain current practices"]


def draw_speedometer(value):

    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=value,

        number={
            "suffix": "%",
            "font": {"size": 40}
        },

        title={
            "text": "🌍 Soil Erosion Severity",
            "font": {"size": 24}
        },

        gauge={
            "axis": {"range": [0, 100]},

            "bar": {"color": "#00ffcc"},

            "steps": [
                {"range": [0, 33], "color": "green"},
                {"range": [33, 66], "color": "yellow"},
                {"range": [66, 100], "color": "red"}
            ],

            "threshold": {
                "line": {"color": "white", "width": 6},
                "thickness": 0.75,
                "value": value
            }
        }
    ))

    fig.update_layout(
        height=400,
        template="plotly_dark",
        paper_bgcolor="rgba(0,0,0,0)",
        font={"color": "white"}
    )

    st.plotly_chart(fig, use_container_width=True)


if st.session_state.page == "welcome":
    set_bg_clear("bg.png")

    st.markdown("""
<div class='title'>
🌱 SoilSentinel AI
</div>

<div style='text-align:center;
color:white;
font-size:22px;
margin-top:20px;'>

Predict • Analyze • Prevent

</div>

<div style='text-align:center;
color:#dddddd;
font-size:16px;
margin-top:10px;'>

An Intelligent Soil Erosion Risk Assessment System

</div>
""", unsafe_allow_html=True)

    if st.button("Start"):
        st.session_state.page = "input"
        st.rerun()

elif st.session_state.page == "input":

    st.markdown("""
<div style='text-align:center;margin-top:-15px;margin-bottom:25px;'>

<h3 style='color:#00ffcc;'>
🌱 SoilSentinel AI
</h3>

<p style='color:white;font-size:18px;'>
Predict • Analyze • Prevent
</p>

</div>
""", unsafe_allow_html=True)

    set_bg_blur("bg.png")

    st.markdown("<div class='title'>📊 Enter Data</div>", unsafe_allow_html=True)

    st.markdown("<div class='card'>", unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    with col1:
        temp = st.number_input("Temperature (°C)", 0.0, 50.0, 20.0)
        humidity = st.number_input("Humidity (%)", 0.0, 100.0, 40.0)

    with col2:
        wind = st.number_input("Wind Speed", 0.0, 100.0, 10.0)
        rainfall = st.number_input("Rainfall", 0.0, 500.0, 30.0)

    soil = st.selectbox("Soil Type", ["Clay", "Loamy", "Sandy"])
    vegetation = st.selectbox("Vegetation", ["High", "Low", "Medium"])

    st.markdown("### 📊 Live Input Dashboard")

    c1,c2,c3,c4 = st.columns(4)

    cards = [
    ("🌡 Temperature", f"{temp}°C"),
    ("💧 Humidity", f"{humidity}%"),
    ("🌬 Wind", f"{wind} km/h"),
    ("🌧 Rainfall", f"{rainfall} mm")
]

    for col, (title, value) in zip([c1,c2,c3,c4], cards):
        with col:
            st.markdown(f"""
        <div style="
        background:rgba(255,255,255,0.08);
        backdrop-filter:blur(15px);
        border:1px solid #00ffcc;
        border-radius:15px;
        padding:15px;
        text-align:center;
        box-shadow:0 0 15px #00ffcc;
        ">
        <h4 style="color:#00ffcc;">{title}</h4>
        <h2 style="color:white;">{value}</h2>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("</div>", unsafe_allow_html=True)

    soil_map = {"Clay": 0, "Loamy": 1, "Sandy": 2}
    veg_map = {"High": 0, "Low": 1, "Medium": 2}

    if st.button("Predict Risk"):
        st.session_state.run_prediction = True

    if st.session_state.run_prediction:

        with st.spinner("Analyzing..."):
            time.sleep(1.5)

        input_data = pd.DataFrame(
            [[temp, humidity, wind, soil_map[soil], veg_map[vegetation], rainfall]],
            columns=['Temp', 'Humidity', 'Wind', 'Soil', 'Vegetation', 'Rainfall']
        )

        prediction = int(model.predict(input_data)[0])

        risk_map = {0: 'High', 1: 'Low', 2: 'Medium'}
        result = risk_map[prediction]
        percentage = calculate_percentage(temp, humidity, wind, rainfall)

        st.session_state.result = result
        st.session_state.percentage = percentage
        st.session_state.temp = temp
        st.session_state.humidity = humidity
        st.session_state.wind = wind
        st.session_state.rainfall = rainfall

        st.session_state.run_prediction = False
        st.session_state.page = "result"
        st.rerun()


elif st.session_state.page == "result":

    set_bg_blur("bg.png")

    st.markdown("<div class='title'>📈 Result Dashboard</div>", unsafe_allow_html=True)

    st.markdown("""
<div style='text-align:center;margin-top:-15px;margin-bottom:25px;'>

<h3 style='color:#00ffcc;'>
🌱 SoilSentinel AI
</h3>

<p style='color:white;font-size:18px;'>
Predict • Analyze • Prevent
</p>

</div>
""", unsafe_allow_html=True)

    result = st.session_state.result
    percentage = st.session_state.percentage

    

    if result == "High":
        st.markdown("""
    <div style="
    background:#5c0000;
    padding:20px;
    border-radius:15px;
    text-align:center;
    color:white;
    font-size:30px;
    font-weight:bold;
    ">
    🚨 HIGH RISK
    </div>
    """, unsafe_allow_html=True)

    elif result == "Medium":
        st.markdown("""
    <div style="
    background:#7a5a00;
    padding:20px;
    border-radius:15px;
    text-align:center;
    color:white;
    font-size:30px;
    font-weight:bold;
    ">
    ⚠️ MEDIUM RISK
    </div>
    """, unsafe_allow_html=True)

    else:
        st.markdown("""
    <div style="
    background:#006b3c;
    padding:20px;
    border-radius:15px;
    text-align:center;
    color:white;
    font-size:30px;
    font-weight:bold;
    ">
    ✅ LOW RISK
    </div>
    """, unsafe_allow_html=True)
        
        
        
    st.markdown(f"""
<div style="
background:rgba(0,0,0,0.5);
padding:15px;
border-radius:15px;
border:1px solid #00ffcc;
box-shadow:0 0 10px #00ffcc;
text-align:center;
">

<h2 style="color:#00ffcc;">
🌍 Severity Level
</h2>

<h1 style="color:white;">
{percentage}%
</h1>

</div>
""", unsafe_allow_html=True)
    
    st.markdown(f"""
<div style="
background:rgba(255,255,255,0.08);
backdrop-filter:blur(15px);
border:1px solid #00ffcc;
border-radius:20px;
padding:20px;
box-shadow:0 0 20px #00ffcc;
margin-top:20px;
">

<h2 style="color:#00ffcc;">
🤖 AI Analysis
</h2>

<p style="color:white;font-size:18px;">
<b>Risk Level:</b> {result}
</p>

<p style="color:white;font-size:18px;">
<b>Severity:</b> {percentage}%
</p>

<p style="color:white;font-size:18px;">
<b>Primary Factors:</b>
</p>

<ul style="color:white;">
<li>Wind Speed Analysis</li>
<li>Humidity Assessment</li>
<li>Rainfall Evaluation</li>
<li>Vegetation Impact</li>
</ul>

</div>
""", unsafe_allow_html=True)
   
    draw_speedometer(percentage)

    

    soil_health = max(0, 100 - percentage)

    if soil_health >= 70:
        health_status = "Excellent"
    elif soil_health >= 40:
        health_status = "Moderate"
    else:
        health_status = "Poor"

    st.markdown(f"""
    <div style="
    background:rgba(0,0,0,0.45);
    border:2px solid #00ffcc;
    border-radius:20px;
    padding:25px;
    margin-top:20px;
    margin-bottom:20px;
    text-align:center;
    box-shadow:0 0 20px #00ffcc;
    ">

    <h2 style="color:#00ffcc;">
    🌱 Soil Health Score
    </h2>

    <h1 style="color:white;font-size:55px;">
    {soil_health}/100
    </h1>

    <h3 style="color:#00ffcc;">
    {health_status}
    </h3>

    </div>
    """, unsafe_allow_html=True)

    st.progress(soil_health / 100)
    


   
    st.subheader("📊 Environmental Parameters Analysis")
    chart_df = pd.DataFrame({
        "Parameter": ["Temperature", "Humidity", "Wind Speed", "Rainfall"],
        "Value": [st.session_state.temp, st.session_state.humidity, st.session_state.wind, st.session_state.rainfall]
    })
    fig_bar= px.bar(chart_df, x="Parameter", y="Value", text="Value", title="Environmental Conditions")

    fig_bar.update_layout(template="plotly_dark",title_x=0.5,height=400,paper_bgcolor='rgba(0,0,0,0)',plot_bgcolor='rgba(0,0,0,0)')

   

    st.subheader("Environmental Risk Radar")

    categories = ['Temperature', 'Humidity', 'Wind Speed', 'Rainfall']

    values = [st.session_state.temp, st.session_state.humidity, st.session_state.wind, st.session_state.rainfall]

    fig_radar = go.Figure()

    fig_radar.add_trace(go.Scatterpolar(
    r=values,
    theta=categories,
    fill='toself',
    fillcolor='rgba(0,255,204,0.35)',
    line=dict(
        color='#00ffcc',
        width=4
    ),
    name='Current Conditions'
))
    fig_radar.update_layout(
    template="plotly_dark",
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",

    polar=dict(
        radialaxis=dict(
            visible=True
        )
    ),

    showlegend=False,
    height=400
)

    col1, col2 = st.columns(2)

    with col1:
        st.plotly_chart(fig_bar, use_container_width=True)

    with col2:
        st.plotly_chart(fig_radar, use_container_width=True)


    st.subheader("🛠 Recommendations")
    for tip in prevention_tips(result):
        st.markdown(f"""
    <div style="
    background:rgba(0,0,0,0.4);
    border-left:5px solid #00ffcc;
    padding:10px;
    margin-bottom:10px;
    border-radius:10px;
    color:white;
    ">
    🌱 {tip}
    </div>
    """, unsafe_allow_html=True)

    if st.button("Back"):
        st.session_state.page = "input"
        st.rerun()
    

        soil_health = max(0, 100 - percentage)

        st.markdown(f"""
        <div style="
        background:rgba(255,255,255,0.08);
        backdrop-filter:blur(15px);
        border:1px solid #00ffcc;
        border-radius:15px;
        padding:15px;
        text-align:center;
        box-shadow:0 0 15px #00ffcc;
        margin-top:20px;
    ">

<h2 style="color:#00ffcc;">
🌱 Soil Health Score
</h2>

<h1 style="color:white;">
{soil_health}/100
</h1>

</div>
""", unsafe_allow_html=True)

st.markdown("""
<hr>

<div style='
text-align:center;
color:white;
font-size:20px;
font-weight:bold;
background:rgba(0,0,0,0.5);
padding:15px;
border-radius:12px;
border:1px solid #00ffcc;
box-shadow:0 0 15px #00ffcc;'>

🌱 SoilSentinel AI 

<br>

👨‍💻 Developed by Aditya Purohit

</div>
""", unsafe_allow_html=True)