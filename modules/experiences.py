import streamlit as st
import pandas as pd
import os
import plotly.express as px
import numpy as np
from utils.dataloader import load_cultural_data

def run():
    # Data source selection: CSV (offline) or Snowflake (cloud)
    use_snowflake = False
    if 'offline_mode' in st.session_state:
        use_snowflake = not st.session_state['offline_mode']
    st.sidebar.markdown('---')
    st.sidebar.write('**Data Source:**')
    data_source = st.sidebar.radio('Choose data source:', ['Local CSV', 'Snowflake (Cloud)'],
                                   index=0, key='exp_data_source',
                                   help='Snowflake is not implemented in this demo. Only Local CSV is available.')
    use_snowflake = False  # Always use CSV, Snowflake not implemented

    # Custom CSS for modern look
    st.markdown(
        """
        <style>
        .main {background-color: #f7f9fa;}
        .block-container {padding-top: 2rem;}
        .stButton>button {background: #1e293b; color: #fff; border-radius: 8px;}
        .stSelectbox>div>div {border-radius: 8px;}
        .stSlider>div {background: #e0e7ef; border-radius: 8px;}
        .stDataFrame {background: #fff; border-radius: 12px;}
        .stMarkdown {font-size: 1.1rem;}
        .stProgress>div>div {background: linear-gradient(90deg, #38bdf8, #6366f1);}
        .stImage>img {border-radius: 12px; border: 2px solid #e0e7ef;}
        .stSubheader {color: #2563eb;}
        .stTitle {color: #0f172a;}
        </style>
        """,
        unsafe_allow_html=True
    )

    st.title("🗺️ Cultural Mapping")
    st.markdown(
        """
        <span style='font-size:1.2rem;'>
        Explore India's rich cultural landscape through our interactive map.<br>
        <b>Discover traditional art forms, cultural festivals, historical landmarks, and more across different regions of India.</b>
        </span>
        """,
        unsafe_allow_html=True
    )
    st.markdown("---")

    # Load main cultural data (from CSV or Snowflake)
    df = None
    if use_snowflake:
        from modules import init_snowflake_connection
        conn = init_snowflake_connection(
            account=os.getenv('SNOWFLAKE_ACCOUNT'),
            user=os.getenv('SNOWFLAKE_USER'),
            password=os.getenv('SNOWFLAKE_PASSWORD'),
            warehouse=os.getenv('SNOWFLAKE_WAREHOUSE', 'vividha_wh'),
            database=os.getenv('SNOWFLAKE_DATABASE', 'vividha_db'),
            schema=os.getenv('SNOWFLAKE_SCHEMA', 'vividha_schema'),
        )
        if conn:
            try:
                df = pd.read_sql("SELECT * FROM cultural_data;", conn)
            except Exception as e:
                st.warning(f"Could not fetch data from Snowflake: {e}. Showing local data instead.")
                use_snowflake = False
            finally:
                conn.close()
        else:
            st.warning("Could not connect to Snowflake. Showing local data instead.")
            use_snowflake = False
    if not use_snowflake:
        try:
            df = load_cultural_data()
        except Exception as e:
            st.error(f"Failed to load cultural data: {e}")
            return
    if df is None or df.empty:
        st.error("No cultural data available. Please check the data source.")
        return

    # Filter options
    st.subheader("🎨 Explore Cultural Heritage")
    with st.expander("Filter Cultural Sites", expanded=True):
        filter_col1, filter_col2, filter_col3 = st.columns([2,2,3])
        with filter_col1:
            category = st.selectbox(
                "Category",
                ["All"] + sorted(df['cultural_value'].unique().tolist() if 'cultural_value' in df.columns else []),
                help="Filter by type of cultural value (e.g., Art, Festival, Landmark)"
            )
        with filter_col2:
            region = st.multiselect(
                "Region",
                sorted(df['region'].unique().tolist()),
                help="Select one or more regions to focus on"
            )
        with filter_col3:
            popularity = st.slider(
                "Tourism Popularity",
                0, 100, (0, 100),
                help="Filter by tourism visibility/popularity index"
            )

    # Apply filters
    filtered_df = df.copy()
    if category != "All" and 'cultural_value' in filtered_df.columns:
        filtered_df = filtered_df[filtered_df['cultural_value'] == category]
    if region:
        filtered_df = filtered_df[filtered_df['region'].isin(region)]
    if 'tourism_visibility' in filtered_df.columns:
        filtered_df = filtered_df[(filtered_df['tourism_visibility'] >= popularity[0]) & (filtered_df['tourism_visibility'] <= popularity[1])]

    # Interactive Map
    st.subheader("🗺️ Cultural Heritage Map")
    st.markdown("<span style='color:#64748b;'>Zoom and hover to explore cultural sites. Bubble size = popularity, color = preservation status.</span>", unsafe_allow_html=True)

    region_coords = {
        'Bihar': (25.6, 85.1), 'Maharashtra': (19.7, 75.7), 'Odisha': (20.9, 85.1),
        'Madhya Pradesh': (23.5, 78.5), 'Andhra Pradesh': (15.9, 79.7), 'Kerala': (10.8, 76.3),
        'Tamil Nadu': (11.1, 78.7), 'Rajasthan': (27.0, 74.2), 'Telangana': (17.9, 79.6),
        'West Bengal': (22.9, 87.8), 'Karnataka': (15.3, 75.7), 'Manipur': (24.8, 93.9),
        'Assam': (26.2, 92.9), 'Himachal Pradesh': (31.1, 77.2), 'Gujarat': (22.3, 71.7)
    }
    filtered_df = filtered_df.copy()
    filtered_df['Latitude'] = filtered_df['region'].map(lambda r: region_coords.get(r, (20.6, 78.9))[0] + np.random.uniform(-0.5, 0.5))
    filtered_df['Longitude'] = filtered_df['region'].map(lambda r: region_coords.get(r, (20.6, 78.9))[1] + np.random.uniform(-0.5, 0.5))

    fig = px.scatter_mapbox(
        filtered_df,
        lat='Latitude',
        lon='Longitude',
        color='preservation_status' if 'preservation_status' in filtered_df.columns else None,
        size='tourism_visibility' if 'tourism_visibility' in filtered_df.columns else None,
        hover_name='art_form',
        hover_data={
            'region': True,
            'cultural_value': True,
            'tourism_visibility': True,
            'preservation_status': True,
            'Latitude': False,
            'Longitude': False
        },
        zoom=4,
        center={"lat": 20.5937, "lon": 78.9629},
        mapbox_style="carto-positron",
        height=550
    )
    st.plotly_chart(fig, use_container_width=True)

    # Cultural site details
    st.subheader("📋 Cultural Heritage Details")
    st.dataframe(
        filtered_df[['art_form', 'region', 'cultural_value', 'tourism_visibility', 'preservation_status']],
        use_container_width=True,
        hide_index=True
    )

    # Footer
    st.markdown("---")
    st.markdown("<div style='text-align:center; color:#64748b;'>Developed by <b>Offbeats</b> | © 2025 Vividha </div>", unsafe_allow_html=True)
