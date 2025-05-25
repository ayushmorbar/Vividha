import streamlit as st
import pandas as pd
import os

# Preservation Hub module
def run():
    # Data source selection: CSV (offline) or Snowflake (cloud)
    use_snowflake = False
    if 'offline_mode' in st.session_state:
        use_snowflake = not st.session_state['offline_mode']
    st.sidebar.markdown('---')
    st.sidebar.write('**Data Source:**')
    data_source = st.sidebar.radio('Choose data source:', ['Local CSV', 'Snowflake (Cloud)'],
                                   index=0, key='pres_data_source',
                                   help='Snowflake is not implemented in this demo. Only Local CSV is available.')
    use_snowflake = False  # Always use CSV, Snowflake not implemented

    st.header("Cultural Preservation Hub")
    lang = st.session_state.get('language', 'English')
    font_size = st.session_state.get('font_size', 16)
    st.markdown(f"<div style='font-size:{font_size}px;'>", unsafe_allow_html=True)
    st.markdown("Contribute to preserving India's heritage. Document artifacts, monitor sites, and share knowledge.")
    # Artifact documentation
    st.subheader("Artifact Documentation")
    if 'artifact_log' not in st.session_state:
        st.session_state['artifact_log'] = []
    with st.form("artifact_form"):
        name = st.text_input("Artifact Name")
        location = st.text_input("Location/Region")
        description = st.text_area("Description")
        submitted = st.form_submit_button("Submit Artifact")
        if submitted and name and location and description:
            st.session_state['artifact_log'].append({
                'name': name, 'location': location, 'description': description
            })
            st.success("Artifact submitted for review!")
    if st.session_state['artifact_log']:
        st.subheader("Community Artifact Log (Session)")
        for art in st.session_state['artifact_log']:
            st.markdown(f"**{art['name']}** ({art['location']})")
            st.write(art['description'])
            st.markdown("---")
    # Artifact registry (persistent, simulated with CSV for demo)
    registry_path = os.path.join(os.path.dirname(__file__), '../data/artifact_registry.csv')
    st.subheader("Artifact Registry (All Submissions)")
    if os.path.exists(registry_path):
        reg_df = pd.read_csv(registry_path)
        st.dataframe(reg_df)
    else:
        st.info("No artifact registry found yet. Submit an artifact to create the registry.")
    # Save new artifact to registry CSV (append mode)
    if submitted and name and location and description:
        import csv
        file_exists = os.path.exists(registry_path)
        with open(registry_path, 'a', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=['name', 'location', 'description', 'submitted_on'])
            if not file_exists:
                writer.writeheader()
            from datetime import datetime
            writer.writerow({'name': name, 'location': location, 'description': description, 'submitted_on': datetime.now().isoformat()})

    # Community contributions (simple feedback form)
    st.subheader("Community Contributions & Feedback")
    with st.form("community_feedback"):
        contributor = st.text_input("Your Name (optional)")
        feedback = st.text_area("Share your knowledge, corrections, or suggestions:")
        feedback_submitted = st.form_submit_button("Submit Feedback")
        if feedback_submitted and feedback:
            st.success("Thank you for your contribution! (For demo, feedback is not stored persistently.)")

    # Heritage site monitoring (load from CSV or Snowflake)
    st.subheader("Heritage Site Monitoring")
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
            query = "SELECT site, region, status, threat_level, notes FROM heritage_sites;"
            df = pd.read_sql(query, conn)
            conn.close()
        else:
            st.warning("Could not fetch data from Snowflake. Showing local data instead.")
            use_snowflake = False
    if not use_snowflake:
        data_path = os.path.join(os.path.dirname(__file__), '../data/heritage_sites.csv')
        if not os.path.exists(data_path):
            st.warning("Heritage sites data not found. Please add 'heritage_sites.csv' to the data folder.")
            st.markdown("</div>", unsafe_allow_html=True)
            return
        try:
            df = pd.read_csv(data_path)
        except Exception as e:
            st.error(f"Failed to load heritage sites data: {e}")
            st.markdown("</div>", unsafe_allow_html=True)
            return
    if df is not None:
        st.dataframe(df)
        st.caption("Data source: " + ("Snowflake" if use_snowflake else "data.gov.in (mocked for demo)"))
        st.markdown("</div>", unsafe_allow_html=True)

    
    # Footer
    st.markdown("---")
    st.markdown("<div style='text-align:center; color:#64748b;'>Developed by <b>Offbeats</b> | © 2025 Vividha </div>", unsafe_allow_html=True)
