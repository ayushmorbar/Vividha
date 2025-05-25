# Vividha Streamlit App
import streamlit as st
import modules.art_explorer as art_explorer
import modules.experiences as experiences
import modules.dashboards as dashboards
import modules.preservation as preservation
import modules.settings as settings

PAGES = {
    "Home": None,
    "Discover Art": art_explorer,
    "Cultural Experiences": experiences,
    "Responsible Tourism": dashboards,
    "Preservation Hub": preservation,
    "Settings": settings,
}

st.sidebar.image('assets/logo.svg', use_column_width=True)
st.sidebar.title("Vividha Navigation")
selection = st.sidebar.radio("Go to", list(PAGES.keys()))

if selection == "Discover Art":
    art_explorer.run()
elif selection == "Cultural Experiences":
    experiences.run()
elif selection == "Responsible Tourism":
    dashboards.run()
elif selection == "Preservation Hub":
    preservation.run()
elif selection == "Settings":
    settings.run()
else:
    st.title("Vividha: Bridging India's Art, Culture & Tourism")
    st.markdown("""
    Welcome to Vividha! Explore India's diverse art forms, discover unique cultural experiences, and learn how responsible tourism can help preserve our heritage.

    **Navigate using the sidebar to explore features.**
    """)

# Placeholder for navigation and modules
# To be expanded with feature modules
