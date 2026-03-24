import streamlit as st
import sqlite3
import pandas as pd
import plotly.express as px
import datetime

# --- 1. PAGE CONFIGURATION ---
st.set_page_config(
    page_title="Smart Pest AI | Dark Mode Admin", 
    layout="wide", 
    page_icon="📟"
)

# --- 2. DARK MODE PROFESSIONAL CSS ---
st.markdown("""
    <style>
    /* Main background - True Black */
    .stApp {
        background-color: #0E1117 !important;
        color: #FFFFFF !important;
    }
    
    /* Headers */
    h1, h2, h3, .stSubheader {
        color: #FFFFFF !important;
        font-weight: 700 !important;
    }

    /* Metric Cards (Dark Grey with subtle border) */
    div[data-testid="stMetric"] {
        background-color: #161B22 !important;
        border: 1px solid #30363D !important;
        padding: 20px !important;
        border-radius: 12px !important;
        box-shadow: 0 4px 20px rgba(0,0,0,0.5) !important;
    }

    /* Metric Value (White Text) */
    div[data-testid="stMetricValue"] > div {
        color: #FFFFFF !important; 
        font-size: 34px !important;
        font-weight: 700 !important;
    }

    /* Metric Label (Light Grey) */
    div[data-testid="stMetricLabel"] > div {
        color: #8B949E !important;
        font-size: 14px !important;
        text-transform: uppercase !important;
    }

    /* Sidebar Background (Deep Charcoal) */
    section[data-testid="stSidebar"] {
        background-color: #010409 !important;
        border-right: 1px solid #30363D !important;
    }
    
    /* Dataframe/Tables Dark Theme Fix */
    .stDataFrame {
        border: 1px solid #30363D !important;
    }

    /* Buttons */
    .stButton>button {
        background-color: #238636 !important; /* GitHub Green */
        color: white !important;
        border: none !important;
        width: 100%;
    }
    
    /* Horizontal Rule */
    hr {
        border: 0;
        border-top: 1px solid #30363D !important;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 3. DATABASE LOGIC ---
def get_data():
    try:
        conn = sqlite3.connect("smart_pest.db")
        df = pd.read_sql_query("SELECT * FROM logs", conn)
        conn.close()
        if not df.empty and 'timestamp' in df.columns:
            df['timestamp'] = pd.to_datetime(df['timestamp'])
        return df
    except Exception as e:
        st.error(f"Database Connection Error: {e}")
        return pd.DataFrame()

df = get_data()

# --- 4. SIDEBAR NAVIGATION ---
with st.sidebar:
    st.title("📟 Control Center")
    st.markdown("---")
    st.success("API Status: ONLINE")
    st.write(f"Server Time: {datetime.datetime.now().strftime('%H:%M:%S')}")
    if st.button('🔄 Sync Real-time Data'):
        st.rerun()

# --- 5. MAIN DASHBOARD HEADER ---
st.title("🛰️ Smart Pest AI: Strategic Insights")
st.write("Monitoring active crop threats across rural agricultural zones.")

# --- 6. TOP ROW: KEY METRICS ---
m1, m2, m3 = st.columns(3)
with m1:
    st.metric("Total Reports", len(df), "Active")
with m2:
    if not df.empty and 'diagnosis' in df.columns:
        real_pests = df[~df['diagnosis'].isin(['Menu', 'Unknown'])]
        top_pest = real_pests['diagnosis'].mode()[0] if not real_pests.empty else "None"
    else:
        top_pest = "N/A"
    st.metric("Priority Threat", top_pest)
with m3:
    st.metric("Coverage Area", "Nairobi/Tharaka", "Verified")

st.markdown("---")

# --- 7. MIDDLE ROW: ANALYTICS ---
col_left, col_right = st.columns([2, 1])

with col_left:
    st.subheader("📊 Threat Distribution Chart")
    if not df.empty:
        counts = df['diagnosis'].value_counts().reset_index()
        counts.columns = ['Pest Name', 'Reports']
        
        # Dark theme Plotly chart
        fig = px.bar(counts, 
                     x='Pest Name', 
                     y='Reports',
                     color='Reports',
                     color_continuous_scale='Viridis', # Better for dark backgrounds
                     template="plotly_dark") # Forces dark theme for charts
        
        fig.update_layout(
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            margin=dict(t=10, b=10)
        )
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("System idle. Waiting for farmer SMS logs...")

with col_right:
    st.subheader("⚡ Live Incident Feed")
    if not df.empty:
        for i, row in df.tail(5).iterrows():
            st.markdown(f"""
            <div style="background:#161B22; padding:12px; border-radius:10px; border-left:5px solid #238636; margin-bottom:10px; border:1px solid #30363D;">
                <small style="color:#8B949E;">{row['timestamp'].strftime('%d %b, %H:%M')}</small><br>
                <b style="color:white;">User:</b> {row['sender']}<br>
                <b style="color:white;">Alert:</b> <span style="color:#3FB950;">{row['diagnosis']}</span>
            </div>
            """, unsafe_allow_html=True)
    else:
        st.write("No recent alerts.")

# --- 8. BOTTOM ROW: RAW DATA ---
st.markdown("---")
with st.expander("🔍 System Logs: Full Database View"):
    # Streamlit handles dark mode dataframes automatically
    st.dataframe(df, use_container_width=True)