# Streamlit Cloud Deployment Guide for Vividha

This guide explains how to deploy the Vividha app on Streamlit Cloud for hackathon demos or public access.

---

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

*Last updated: May 25, 2025*
