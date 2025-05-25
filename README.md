# Vividha
See India. Sustain India.

## Project Structure

- `app.py`: Main Streamlit app entry point
- `modules/`: Feature modules (art explorer, experiences, dashboards, preservation, settings)
- `data/`: Sample and ingested datasets
- `assets/`: Images, icons, and static files
- `requirements.txt`: Python dependencies
- `docs/`: Documentation (e.g., Snowflake setup)

## Setup Instructions

1. **Clone the repository**
2. **Create a virtual environment:**
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```
3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```
4. **Run the app:**
   ```bash
   streamlit run app.py
   ```

## Snowflake Integration
- See `docs/snowflake_setup.md` for step-by-step Snowflake setup and data ingestion guidance.

## Contribution
- Please see the `modules/` folder for feature-specific contributions.

## Demo Script

See [`demo_script.md`](./demo_script.md) for a step-by-step demo walkthrough for hackathon judges or reviewers.

## Features

- Modular sidebar navigation: Home, Discover Art, Cultural Experiences, Responsible Tourism, Preservation Hub, Settings, and (optionally) Cultural Impact Analytics
- Data-driven insights: All data loaded from CSVs in `/data` (Snowflake selector present, but only CSV is enabled for demo)
- Accessibility: Font size, high contrast mode, and session state for user preferences
- Multilingual: English and Hindi demo support
- Interactive visualizations: Map, charts, metrics, and dashboards (Plotly, Streamlit)
- Robust error handling and fallback to CSV
- Modern UI: Custom CSS, branding, and responsive layout
- Artifact registry, site monitoring, and community feedback in Preservation Hub
- Advanced analytics in Cultural Impact Analytics (if enabled)
- Professional engineering: Modular code, type hints, docstrings, and code reuse

## Data Source Selection

- Each module includes a sidebar selector for data source:
  - **Local CSV** (enabled)
  - **Snowflake (Cloud)** (disabled for demo; help message shown)

## Accessibility & Multilingual
- Use the Settings module to adjust font size, enable high contrast, and switch language.
