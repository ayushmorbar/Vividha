# Snowflake Setup & Data Ingestion Guide

## 1. Snowflake Account Setup
- Sign up at https://signup.snowflake.com/
- Choose the free trial or the smallest warehouse size (X-Small) for cost efficiency.

## 2. Create Warehouse, Database, and Schema
```sql
CREATE WAREHOUSE vividha_wh WITH WAREHOUSE_SIZE = 'XSMALL' AUTO_SUSPEND = 60 AUTO_RESUME = TRUE;
CREATE DATABASE vividha_db;
CREATE SCHEMA vividha_schema;
```

## 3. Create Tables
- Design tables for art forms, cultural events, tourism stats, user contributions, etc.
- Example:
```sql
CREATE TABLE vividha_schema.art_forms (
    id INT AUTOINCREMENT,
    name STRING,
    region STRING,
    description STRING,
    image_url STRING,
    PRIMARY KEY(id)
);
```

## 4. Data Ingestion
- For CSVs: Use Snowflake's UI or `COPY INTO` command.
- For APIs: Use Python scripts with `snowflake-connector-python`.
- For community uploads: Use Streamlit uploader, then push to Snowflake.

## 5. Data Cleaning
- Use SQL for deduplication, normalization, and joining datasets.

## 6. Python Integration Example
```python
import snowflake.connector
conn = snowflake.connector.connect(
    user='YOUR_USER',
    password='YOUR_PASSWORD',
    account='YOUR_ACCOUNT',
    warehouse='vividha_wh',
    database='vividha_db',
    schema='vividha_schema'
)
cs = conn.cursor()
cs.execute("SELECT * FROM art_forms")
for row in cs:
    print(row)
cs.close()
conn.close()
```

## 7. Cost Optimization
- Use auto-suspend and resume for the warehouse.
- Only run queries on demand.

## 8. Troubleshooting
- Check Snowflake documentation for error codes.
- Use try/except in Python for error handling.
