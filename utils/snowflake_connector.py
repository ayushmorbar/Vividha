import streamlit as st
import snowflake.connector

def init_snowflake_connection(account, user, password, warehouse, database, schema):
    """
    Initialize a connection to Snowflake
    
    Parameters:
        account (str): Snowflake account identifier
        user (str): Snowflake username
        password (str): Snowflake password
        warehouse (str): Snowflake warehouse name
        database (str): Snowflake database name
        schema (str): Snowflake schema name
        
    Returns:
        snowflake.connector.connection.SnowflakeConnection: Snowflake connection object
    """
    try:
        # Create a connection object
        conn = snowflake.connector.connect(
            account=account,
            user=user,
            password=password,
            warehouse=warehouse,
            database=database,
            schema=schema
        )
        
        # Test the connection
        cursor = conn.cursor()
        cursor.execute("SELECT current_version()")
        version = cursor.fetchone()[0]
        st.session_state.snowflake_version = version
        cursor.close()
        
        return conn
    except Exception as e:
        raise Exception(f"Failed to connect to Snowflake: {str(e)}")
