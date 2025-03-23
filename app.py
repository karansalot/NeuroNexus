import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import os
import requests
from datetime import datetime, timedelta
import numpy as np

# Page configuration
st.set_page_config(
    page_title="NeuroNexus - B2Twin Digital Twin",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
    <style>
    .main {
        background-color: #f8fafc;
    }
    .stApp {
        max-width: 1200px;
        margin: 0 auto;
    }
    .stButton>button {
        background-color: #059669;
        color: white;
    }
    .stButton>button:hover {
        background-color: #047857;
    }
    </style>
""", unsafe_allow_html=True)

def summarize_with_ollama(data_text):
    """Generate AI summary using Ollama's local API"""
    try:
        response = requests.post(
            "http://localhost:11434/api/generate",
            json={
                "model": "gemma:2b",
                "prompt": f"""Analyze this environmental dataset from Biosphere 2 and provide insights:

                {data_text}

                Focus on:
                1. Key patterns and trends
                2. Potential anomalies
                3. Recommendations for scientists
                4. Implications for ecosystem health

                Format your response in clear sections with bullet points.""",
                "stream": False
            },
            timeout=30
        )
        if response.ok:
            return response.json().get("response", "⚠️ No summary generated.")
        return "❌ Error: Invalid response from Ollama."
    except requests.exceptions.ConnectionError:
        return "❌ Error: Cannot connect to Ollama. Please ensure it's running with: ollama run gemma:2b"
    except Exception as e:
        return f"❌ Error: {str(e)}"

def load_sample_data(data_type):
    """Load sample data if no file is uploaded"""
    current_time = datetime.now()
    dates = pd.date_range(start=current_time - timedelta(hours=24), periods=24, freq='H')
    
    if data_type == 'temperature':
        base = 25
        variation = np.sin(np.linspace(0, 2*np.pi, 24)) * 3
        values = base + variation + np.random.normal(0, 0.5, 24)
        return pd.DataFrame({
            'timestamp': dates,
            'temperature': values,
            'humidity': base + 40 + variation * 2 + np.random.normal(0, 1, 24)
        })
    elif data_type == 'co2':
        base = 400
        values = base + np.random.normal(0, 10, 24)
        return pd.DataFrame({
            'timestamp': dates,
            'co2_level': values,
            'pressure': 1013 + np.random.normal(0, 2, 24)
        })
    else:  # radiation
        base = 1000
        variation = np.sin(np.linspace(0, 2*np.pi, 24)) * 500
        values = np.maximum(0, base + variation + np.random.normal(0, 50, 24))
        return pd.DataFrame({
            'timestamp': dates,
            'solar_radiation': values,
            'par_level': values * 0.45 + np.random.normal(0, 20, 24)
        })

# Sidebar navigation
st.sidebar.title("🧠 NeuroNexus")
st.sidebar.markdown("B2Twin Digital Twin System")
page = st.sidebar.radio("Navigation", ["🌱 Overview", "📊 Data Analysis", "🤖 AI Insights"])

# Initialize session state
if 'analyses' not in st.session_state:
    st.session_state.analyses = []

if page == "🌱 Overview":
    st.title("🌱 B2Twin Digital Twin System")
    
    st.markdown("""
    Welcome to NeuroNexus, an advanced digital twin system for Biosphere 2. This platform combines 
    real-time sensor data with AI-powered analysis to provide deep insights into the complex 
    interactions within Biosphere 2's unique ecosystems.
    
    ### 🎯 Key Features
    - Real-time environmental data monitoring
    - AI-powered trend analysis using Gemma 2B
    - Multi-parameter correlation analysis
    - Anomaly detection and alerting
    """)
    
    # System Status
    st.subheader("🔄 System Status")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Temperature", "26.5°C", "0.8°C")
    with col2:
        st.metric("CO₂ Levels", "412 ppm", "-3 ppm")
    with col3:
        st.metric("Humidity", "85%", "2%")

elif page == "📊 Data Analysis":
    st.title("📊 Environmental Data Analysis")
    
    # Data upload section
    st.subheader("📤 Data Upload")
    data_type = st.selectbox(
        "Select Data Type",
        ["temperature", "co2", "radiation"],
        format_func=lambda x: {
            "temperature": "🌡️ Temperature & Humidity",
            "co2": "🌿 CO₂ & Pressure",
            "radiation": "☀️ Solar Radiation & PAR"
        }[x]
    )
    
    uploaded_file = st.file_uploader("Upload CSV Data", type=['csv'])
    
    if uploaded_file:
        df = pd.read_csv(uploaded_file)
    else:
        df = load_sample_data(data_type)
    
    # Data visualization
    st.subheader("📈 Data Visualization")
    
    # Create tabs for different visualizations
    tab1, tab2 = st.tabs(["Time Series", "Correlation"])
    
    with tab1:
        fig = go.Figure()
        for col in df.columns:
            if col != 'timestamp' and not col.startswith('Unnamed'):
                fig.add_trace(go.Scatter(
                    x=df['timestamp'],
                    y=df[col],
                    name=col,
                    mode='lines+markers'
                ))
        fig.update_layout(
            title="Environmental Parameters Over Time",
            xaxis_title="Time",
            yaxis_title="Value",
            height=500
        )
        st.plotly_chart(fig, use_container_width=True)
    
    with tab2:
        if len(df.select_dtypes(include=[np.number]).columns) > 1:
            numeric_cols = df.select_dtypes(include=[np.number]).columns
            corr_matrix = df[numeric_cols].corr()
            fig = px.imshow(
                corr_matrix,
                labels=dict(color="Correlation"),
                color_continuous_scale="RdBu"
            )
            fig.update_layout(title="Parameter Correlation Matrix")
            st.plotly_chart(fig, use_container_width=True)

elif page == "🤖 AI Insights":
    st.title("🤖 AI-Powered Insights")
    
    st.markdown("""
    Upload environmental data to receive AI-generated insights using the Gemma 2B model.
    The analysis will focus on identifying patterns, anomalies, and providing recommendations.
    """)
    
    uploaded_file = st.file_uploader("Upload Data for Analysis", type=['csv'])
    
    if uploaded_file:
        df = pd.read_csv(uploaded_file)
        
        if st.button("Generate AI Analysis"):
            with st.spinner("🧠 Analyzing data..."):
                # Prepare data summary for AI analysis
                data_summary = f"""
                Dataset Summary:
                - Time range: {df['timestamp'].iloc[0]} to {df['timestamp'].iloc[-1]}
                - Parameters: {', '.join(df.columns)}
                - Key statistics:
                {df.describe().to_string()}
                """
                
                analysis = summarize_with_ollama(data_summary)
                st.session_state.analyses.append({
                    'timestamp': datetime.now(),
                    'content': analysis
                })
        
        # Display analysis history
        if st.session_state.analyses:
            st.subheader("📝 Analysis History")
            for idx, analysis in enumerate(reversed(st.session_state.analyses)):
                with st.expander(f"Analysis {len(st.session_state.analyses) - idx} - {analysis['timestamp'].strftime('%Y-%m-%d %H:%M:%S')}"):
                    st.markdown(analysis['content'])
    else:
        st.info("👆 Upload a CSV file to begin AI analysis")

# Footer
st.markdown("---")
st.markdown(
    "🌍 B2Twin Hackathon 2025 | Made with ❤️ by NeuroNexus Team"
)