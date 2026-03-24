import streamlit as st
import sqlite3
import pandas as pd
import plotly.express as px
import datetime

# Page Configuration
st.set_page_config(page_title="Smart Pest AI - Admin", layout="wide")

# FIX: Changed 'unsafe_content' to 'unsafe_allow_html'
st.markdown("""
    <style>
    .main { background-color: #f5f7f9; }
    .stMetric { 
        background-color: #ffffff; 
        padding: 15px; 
        border-radius: 10px; 
        box-shadow: 0 2px 4px rgba(0,0,0,0.05); 
        border: 1px solid #e0e0e0;
    }
    </style>
    """, unsafe_allow_html=True)

st.title("🌾 Smart Pest Detection: Admin Insights")
st.write(f"🕒 **Last Data Sync:** {datetime.datetime.now().strftime('%H:%M:%S')}")

def get_data():
    try:
        conn = sqlite3.connect("smart_pest.db")
        df = pd.read_sql_query("SELECT * FROM logs", conn)
        conn.close()
        return df
    except Exception as e:
        st.error(f"Database Error: {e}")
        return pd.DataFrame()

df = get_data()

# --- TOP ROW: Key Metrics ---
col1, col2, col3 = st.columns(3)
with col1:
    st.metric("Total Consultations", len(df))
with col2:
    if not df.empty and 'diagnosis' in df.columns:
        # Get the most frequent diagnosis
        top_pest = df['diagnosis'].mode()[0] if not df['diagnosis'].mode().empty else "None"
    else:
        top_pest = "N/A"
    st.metric("Most Reported Pest", top_pest)
with col3:
    st.metric("Backend Status", "ONLINE", delta="Active Tunnel")

st.divider()

# --- MIDDLE ROW: Visuals ---
col_left, col_right = st.columns([2, 1])

with col_left:
    st.subheader("📊 Pest Frequency Analysis")
    if not df.empty:
        # Count occurrences of each diagnosis
        counts = df['diagnosis'].value_counts().reset_index()
        counts.columns = ['Pest Name', 'Reports']
        
        fig = px.bar(counts, 
                     x='Pest Name', 
                     y='Reports',
                     color='Reports',
                     color_continuous_scale='Greens')
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("Waiting for incoming SMS data... Send a text to see the chart!")

with col_right:
    st.subheader("📱 Recent Activity")
    if not df.empty:
        st.dataframe(df[['sender', 'diagnosis', 'timestamp']].tail(5), use_container_width=True)
    else:
        st.write("No messages yet.")

# --- BOTTOM ROW: Raw Data ---
with st.expander("See All Raw Logs"):
    st.dataframe(df, use_container_width=True)

if st.button('🔄 Refresh Live Data'):
    st.rerun()