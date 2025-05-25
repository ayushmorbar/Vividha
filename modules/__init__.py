import os
import snowflake.connector
import pandas as pd
import streamlit as st
from typing import Optional
from utils.snowflake_connector import init_snowflake_connection
from utils.dataloader import load_cultural_data, load_tourism_data

def get_snowflake_connection() -> Optional[snowflake.connector.SnowflakeConnection]:
    """Establish a Snowflake connection using environment variables."""
    try:
        conn = snowflake.connector.connect(
            user=os.getenv('SNOWFLAKE_USER'),
            password=os.getenv('SNOWFLAKE_PASSWORD'),
            account=os.getenv('SNOWFLAKE_ACCOUNT'),
            warehouse=os.getenv('SNOWFLAKE_WAREHOUSE', 'vividha_wh'),
            database=os.getenv('SNOWFLAKE_DATABASE', 'vividha_db'),
            schema=os.getenv('SNOWFLAKE_SCHEMA', 'vividha_schema'),
        )
        return conn
    except Exception as e:
        st.error(f"Snowflake connection error: {e}")
        return None

@st.cache_data(show_spinner=False)
def fetch_snowflake_data(query: str, params=None) -> Optional[pd.DataFrame]:
    """Fetch data from Snowflake and return as a DataFrame."""
    conn = get_snowflake_connection()
    if conn is None:
        return None
    try:
        df = pd.read_sql(query, conn, params=params)
        conn.close()
        return df
    except Exception as e:
        st.error(f"Snowflake query error: {e}")
        return None