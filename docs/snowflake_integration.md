# Snowflake Integration Guide for Vividha

This guide explains how to set up and use Snowflake as a data source for the Vividha app. For the hackathon demo, only Local CSV is enabled, but the codebase is ready for Snowflake integration.

---

## 1. Prerequisites
- A Snowflake account (trial or paid)
- Snowflake user credentials with read access
- The following environment variables set in your deployment or `.env` file:
  - `SNOWFLAKE_ACCOUNT`
  - `SNOWFLAKE_USER`
  - `SNOWFLAKE_PASSWORD`
  - `SNOWFLAKE_WAREHOUSE` (default: vividha_wh)
  - `SNOWFLAKE_DATABASE` (default: vividha_db)
  - `SNOWFLAKE_SCHEMA` (default: vividha_schema)

---

## 2. Data Preparation
- Prepare your data in CSV format (see `/data` for schema examples).
- Use Snowflake's UI or CLI to create tables matching the CSV schemas:
  - `cultural_data`
  - `cultural_experiences`
  - `tourism_stats`
  - etc.
- Load your CSV data into the corresponding Snowflake tables.

---

## 3. App Configuration
- Set the required environment variables in your deployment environment or `.env` file.
- In each module, select "Snowflake (Cloud)" as the data source in the sidebar (for production; for demo, only Local CSV is enabled).

---

## 4. How It Works in Code
- Each module uses a shared Snowflake connector utility (`utils/snowflake_connector.py`).
- If Snowflake is selected and credentials are valid, data is loaded from Snowflake using SQL queries.
- If Snowflake is unavailable or fails, the app falls back to Local CSV with a warning.

---

## 5. Troubleshooting
- If you see a warning about `pyarrow` version, run:
  ```bash
  pip install "pyarrow<19.0.0"
  ```
- If you see connection errors, check your credentials and network/firewall settings.
- For schema mismatches, ensure your Snowflake tables match the CSV column names and types.

---

## 6. Demo Mode (Hackathon)
- For the hackathon, Snowflake is disabled in the UI and only Local CSV is used for reliability.
- The codebase is ready for Snowflake and can be enabled for future production use.

---

## 7. References
- [Snowflake Documentation](https://docs.snowflake.com/en/)
- [Streamlit + Snowflake Example](https://docs.streamlit.io/knowledge-base/tutorials/databases/snowflake)

---

# Deployment on Streamlit Cloud

## 1. Prepare Your Repository
- Ensure your code, `requirements.txt`, and all data/assets are committed to GitHub.
- Recommended: Remove or disable any code that requires local environment variables for demo mode (Snowflake is already disabled by default).

## 2. Push to GitHub
- Push your project to a public or private GitHub repository.

## 3. Deploy on Streamlit Cloud
1. Go to [https://streamlit.io/cloud](https://streamlit.io/cloud)
2. Click **'New app'**
3. Connect your GitHub account and select your repository
4. Set the main file path to `app.py`
5. (Optional) Set environment variables in the Streamlit Cloud UI if you want to enable Snowflake in the future
6. Click **'Deploy'**

- The app will build and launch automatically.
- You can share the provided URL with judges or users.

## 4. Notes
- For hackathon/demo, all data is loaded from CSVs in `/data`.
- If you want to enable Snowflake, set the required environment variables in the Streamlit Cloud app settings.
- If you update your code or data, just push to GitHub and Streamlit Cloud will redeploy automatically.

---

# Changelog

## v1.0.0 (2025-05-25)
- Initial hackathon-ready release
- Modular Streamlit app with sidebar navigation
- Art Explorer, Cultural Experiences, Responsible Tourism, Preservation Hub, Settings, and Cultural Impact Analytics modules
- All data loaded from CSVs for demo reliability
- Snowflake integration code and documentation (disabled for demo)
- Accessibility: font size, high contrast, session state
- Multilingual: English/Hindi demo
- Modern UI, branding, and logo
- Robust error handling and fallback
- Demo script and full documentation
- Custom license for hackathon/commercial use

---

*Last updated: May 25, 2025*
