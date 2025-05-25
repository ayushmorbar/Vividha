import streamlit as st
import pandas as pd
import os

def load_cultural_data(connection=None):
    """
    Load cultural data from Snowflake if connection is provided, else from local CSV for hackathon/demo.
    """
    try:
        if connection is not None:
            # Example query (uncomment for production)
            # query = "SELECT * FROM cultural_heritage_data ORDER BY region, art_form"
            # return pd.read_sql(query, connection)
            pass  # For hackathon, skip Snowflake
        # Load from local CSV
        csv_path = os.path.join(os.path.dirname(__file__), '../data/cultural_data.csv')
        return pd.read_csv(csv_path)
    except Exception as e:
        st.error(f"Error loading cultural data: {str(e)}")
        return None

def load_tourism_data(connection=None):
    """
    Load tourism data from Snowflake if connection is provided, else from local CSV for hackathon/demo.
    """
    try:
        if connection is not None:
            # Example query (uncomment for production)
            # query = "SELECT * FROM tourism_data ORDER BY region, site_name"
            # return pd.read_sql(query, connection)
            pass  # For hackathon, skip Snowflake
        # Load from local CSV
        csv_path = os.path.join(os.path.dirname(__file__), '../data/tourism_data.csv')
        return pd.read_csv(csv_path)
    except Exception as e:
        st.error(f"Error loading tourism data: {str(e)}")
        return None
