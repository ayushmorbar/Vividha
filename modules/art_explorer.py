import streamlit as st
import pandas as pd
import os
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
import random
from utils.dataloader import load_cultural_data

def run():
    """
    Advanced Art Explorer module for deep-dive exploration of Indian art forms.
    Integrates with app session state, accessibility, multilingual, and data source selection.
    """
    # Data source selection: CSV (offline) or Snowflake (cloud)
    st.sidebar.markdown('---')
    st.sidebar.write('**Data Source:**')
    data_source = st.sidebar.radio('Choose data source:', ['Local CSV', 'Snowflake (Cloud)'],
                                   index=0, key='art_data_source',
                                   help='Snowflake is not implemented in this demo. Only Local CSV is available.')
    use_snowflake = False  # Always use CSV, Snowflake not implemented

    lang = st.session_state.get('language', 'English')
    font_size = st.session_state.get('font_size', 16)

    # --- Constants and Config ---
    PLACEHOLDER_IMAGE = "https://placeholder.svg?height=400&width=600"
    PLACEHOLDER_THUMB = "https://placeholder.svg?height=150&width=150"
    ART_FORMS_CSV = os.path.join(os.path.dirname(__file__), '../data/art_forms.csv')

    # --- Utility Functions ---
    def get_art_asset_row(art_form: str, assets_df: pd.DataFrame) -> dict:
        if assets_df is not None and art_form in assets_df['art_form'].values:
            return assets_df[assets_df['art_form'] == art_form].iloc[0].to_dict()
        return {}

    def get_art_data_row(art_form: str, df: pd.DataFrame) -> dict:
        if art_form in df['art_form'].values:
            return df[df['art_form'] == art_form].iloc[0].to_dict()
        return {}

    def get_value(row: dict, key: str, default=None):
        return row.get(key) if row and key in row and pd.notnull(row[key]) else default

    # --- Data Loading ---
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
            query = "SELECT * FROM cultural_data;"
            try:
                df = pd.read_sql(query, conn)
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

    # Load art form assets (images, descriptions) from art_forms.csv
    try:
        assets_df = pd.read_csv(ART_FORMS_CSV)
    except Exception:
        assets_df = None

    # Art form selector (preserve selection in session state)
    art_forms = assets_df['art_form'].unique().tolist() if assets_df is not None else df['art_form'].unique().tolist()
    selected_art = st.session_state.get('selected_art', art_forms[0] if art_forms else None)
    selected_art = st.selectbox("Select an art form to explore", art_forms, index=art_forms.index(selected_art) if selected_art in art_forms else 0, key='art_form_select')
    st.session_state.selected_art = selected_art

    asset_row = get_art_asset_row(selected_art, assets_df)
    data_row = get_art_data_row(selected_art, df)

    art_image = get_value(asset_row, 'image_url', PLACEHOLDER_IMAGE)
    art_desc = get_value(asset_row, 'description', 'Description not available.')
    region = get_value(asset_row, 'region', get_value(data_row, 'region', 'Unknown'))

    # Header with art form name and region
    st.header(f"{selected_art} ({region})")

    # Main content display
    main_col1, main_col2 = st.columns([2, 1])
    with main_col1:
        st.image(art_image, caption=f"{selected_art} Example", use_container_width=True)
        st.subheader("About the Art Form")
        st.write(art_desc)
        st.write(f"Cultural value: {get_value(data_row, 'cultural_value', 'N/A')}. Tourism visibility: {get_value(data_row, 'tourism_visibility', 'N/A')}.")
        st.subheader("Cultural Significance")
        st.write(f"Preservation status: {get_value(data_row, 'preservation_status', 'N/A')}")
    with main_col2:
        st.subheader("Key Information")
        st.markdown(f"**Region**: {region}")
        st.markdown(f"**Cultural Value**: {get_value(data_row, 'cultural_value', 'N/A')}")
        st.markdown(f"**Tourism Visibility**: {get_value(data_row, 'tourism_visibility', 'N/A')}")
        st.markdown(f"**Preservation Status**: {get_value(data_row, 'preservation_status', 'N/A')}")
        try:
            st.progress(int(get_value(data_row, 'cultural_value', 50)), text=f"Cultural Value Index: {get_value(data_row, 'cultural_value', 'N/A')}")
        except Exception:
            pass

    # Technical aspects
    st.subheader("Technical Aspects of the Art Form")
    tech_col1, tech_col2 = st.columns(2)
    with tech_col1:
        st.markdown("### Creation Process")
        st.write("""
        This section would contain detailed information about the step-by-step process 
        of creating this art form, including preparation of materials, drawing, coloring, 
        and finishing techniques.
        """)
        st.markdown("""
        1. **Preparation of the base**
        2. **Preliminary sketching**
        3. **Application of colors**
        4. **Detailing and ornamentation**
        5. **Finishing and preservation**
        """)
    with tech_col2:
        st.markdown("### Unique Techniques")
        techniques = [
            "Line work with natural brushes",
            "Natural pigment preparation",
            "Traditional motif creation",
            "Pattern repetition methods",
            "Border decoration techniques"
        ]
        complexity = [random.randint(60, 95) for _ in range(len(techniques))]
        fig = go.Figure()
        fig.add_trace(go.Scatterpolar(
            r=complexity,
            theta=techniques,
            fill='toself',
            name='Technique Complexity'
        ))
        fig.update_layout(
            polar=dict(radialaxis=dict(visible=True, range=[0, 100])),
            showlegend=False
        )
        st.plotly_chart(fig, use_container_width=True)

    # Historical evolution
    st.subheader("Historical Evolution")
    age_val = get_value(data_row, 'age', None)
    if age_val is not None and pd.notnull(age_val):
        age_str = str(age_val).split('+')[0].split(' ')[0].replace(',', '')
        try:
            age_int = int(age_str)
        except ValueError:
            age_int = 2000
    else:
        age_int = 2000
    timeline = {
        f"{age_int - 500} CE": "Early origins in religious and ritual contexts",
        f"{age_int - 300} CE": "Development of distinctive style and techniques",
        f"{age_int - 100} CE": "Patronage by local rulers and elite families",
        "1800s": "Decline during colonial period",
        "1950s": "Post-independence revival efforts",
        "1980s": "Recognition as important cultural heritage",
        "2000s": "Adaptation to contemporary markets and materials",
        "Present": "Continuing evolution with growing international interest"
    }
    years = list(timeline.keys())
    events = list(timeline.values())
    timeline_fig = go.Figure()
    timeline_fig.add_trace(go.Scatter(
        x=years,
        y=[1] * len(years),
        mode="markers+text",
        marker=dict(size=15, color="blue"),
        text=years,
        textposition="bottom center"
    ))
    for i, year in enumerate(years):
        timeline_fig.add_annotation(
            x=year,
            y=1.1,
            text=events[i],
            showarrow=False,
            yshift=10
        )
    timeline_fig.update_layout(
        title="Evolution Timeline",
        showlegend=False,
        plot_bgcolor="white",
        yaxis=dict(visible=False),
        height=300
    )
    st.plotly_chart(timeline_fig, use_container_width=True)

    # Master artisans
    st.subheader("Master Artisans")
    artisan_col1, artisan_col2, artisan_col3 = st.columns(3)
    with artisan_col1:
        st.image("https://placeholder.svg?height=150&width=150", caption="Master Artisan 1")
        st.markdown("### Rajesh Kumar")
        st.write("Third-generation artist who has won national recognition for his innovations while maintaining traditional techniques.")
        st.markdown("**Notable Achievement**: National Award, 2015")
    with artisan_col2:
        st.image("https://placeholder.svg?height=150&width=150", caption="Master Artisan 2")
        st.markdown("### Lakshmi Devi")
        st.write("Leading female artist who has trained over 200 women in her village, creating sustainable livelihoods through this art form.")
        st.markdown("**Notable Achievement**: State Award, 2018")
    with artisan_col3:
        st.image("https://placeholder.svg?height=150&width=150", caption="Master Artisan 3")
        st.markdown("### Mohammad Hussain")
        st.write("Fusion artist who combines traditional techniques with contemporary themes, creating cross-cultural appeal.")
        st.markdown("**Notable Achievement**: International Exhibition, Paris 2019")

    # Preservation and contemporary relevance
    st.subheader("Preservation Efforts & Contemporary Relevance")
    preservation_col1, preservation_col2 = st.columns(2)
    with preservation_col1:
        st.markdown("### Current Challenges")
        challenges = {
            "Fewer Young Practitioners": 85,
            "Competition from Mass Production": 70,
            "Limited Access to Traditional Materials": 60,
            "Decreasing Local Market": 75,
            "Limited Documentation of Techniques": 65
        }
        challenges_fig = px.bar(
            x=list(challenges.keys()),
            y=list(challenges.values()),
            color=list(challenges.values()),
            color_continuous_scale="Reds",
            labels={"x": "Challenge", "y": "Severity (0-100)"}
        )
        challenges_fig.update_layout(xaxis_tickangle=-45)
        st.plotly_chart(challenges_fig, use_container_width=True)
    with preservation_col2:
        st.markdown("### Preservation Initiatives")
        st.write("""
        Several organizations and government bodies are working to preserve this traditional art form:
        1. **Artist Cooperatives**: Supporting sustainable livelihoods for traditional artists
        2. **Training Programs**: Teaching techniques to new generations
        3. **Documentation Projects**: Recording detailed processes and oral histories
        4. **Museum Collections**: Preserving historical examples
        5. **Cultural Tourism**: Creating economic incentives for continuation
        """)
        st.info("Government funding for preservation has increased by 35% in the last five years, supporting 12 new training centers across the region.")

    # Contemporary applications
    st.subheader("Contemporary Applications")
    app_col1, app_col2, app_col3, app_col4 = st.columns(4)
    with app_col1:
        st.image("https://daily.jstor.org/wp-content/uploads/2017/09/indian_dress_1050x700.jpg?height=150&width=150", caption="Fashion")
        st.markdown("### Fashion")
        st.write("Integration into modern clothing designs, accessories, and textile products.")
    with app_col2:
        st.image("https://www.shopinroom.com/wp-content/uploads/2024/01/affordable-home-decor.jpg?height=150&width=150", caption="Home Decor")
        st.markdown("### Home Decor")
        st.write("Contemporary applications in interior design, wall art, and household items.")
    with app_col3:
        st.image("https://www.livemint.com/lm-img/img/2023/12/20/600x338/Industry-experts-argued-frequent-appearance-on-OTT_1689531050687_1703063062269.jpg?height=150&width=150", caption="Digital Media")
        st.markdown("### Digital Media")
        st.write("Adaptation to digital formats for wider distribution and new creative expressions.")
    with app_col4:
        st.image("https://thedailyguardian.com/wp-content/uploads/2020/07/public-art-1280x720.png?height=150&width=150", caption="Public Art")
        st.markdown("### Public Art")
        st.write("Large-scale installations in public spaces, airports, and institutions.")

    # Experience this art form
    st.subheader("Experience This Art Form")
    experience_col1, experience_col2 = st.columns(2)
    with experience_col1:
        st.markdown("### Where to See It")
        st.write("""
        **Museums and Galleries**
        - National Crafts Museum, Delhi
        - Regional Art Galleries
        - Specialized Cultural Museums
        **Cultural Centers**
        - Artisan Villages
        - Heritage Centers
        - Cultural Festivals
        **Online Collections**
        - Virtual Museum Tours
        - Digital Archives
        - Artist Websites
        """)
    with experience_col2:
        st.markdown("### Learn the Art Form")
        st.write("""
        **Workshops and Classes**
        - Cultural centers offer hands-on workshops
        - Artisan communities welcome visitors for demonstrations
        - Online tutorials and courses available
        **Materials Needed**
        - Basic starter kits available from cultural organizations
        - Traditional materials can be sourced from specialized suppliers
        **Learning Resources**
        - Instructional books and guides
        - Video tutorials by master artisans
        - Community learning groups
        """)

    # Related cultural experiences (refactored)
    st.subheader("Related Cultural Experiences")
    related_art_forms = [art for art in art_forms if art != selected_art]
    related_sample = random.sample(related_art_forms, min(3, len(related_art_forms))) if related_art_forms else []
    related_cols = st.columns(len(related_sample)) if related_sample else []
    for i, art in enumerate(related_sample):
        rel_asset = get_art_asset_row(art, assets_df)
        rel_data = get_art_data_row(art, df)
        img_url = get_value(rel_asset, 'image_url', PLACEHOLDER_IMAGE)
        desc = get_value(rel_asset, 'description', '...')
        region = get_value(rel_asset, 'region', get_value(rel_data, 'region', 'Unknown'))
        with related_cols[i]:
            st.image(img_url, caption=art, use_container_width=True)
            st.markdown(f"### {art}")
            st.write(f"From {region}")
            st.write((desc[:100] + "...") if desc else "...")
            if st.button(f"Explore {art}", key=f"related_{i}"):
                st.session_state.selected_art = art
                st.experimental_rerun()

    # Footer
    st.markdown("---")
    st.markdown("<div style='text-align:center; color:#64748b;'>Developed by <b>Offbeats</b> | © 2025 Vividha </div>", unsafe_allow_html=True)
