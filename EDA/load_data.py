import pandas as pd
from sqlalchemy import create_engine

# Load data from the CSV file
df = pd.read_csv(r"C:\Users\mohan\OneDrive\Desktop\Business KPI Visualizer\E-Commerce Sales Dataset\Amazon Sale Report Standardized Date.csv", low_memory=False)

# Define your PostgreSQL database connection details
db_user = 'postgres'
db_password = 'q4J6KaBe'
db_host = 'localhost'
db_port = '5432'
db_name = 'business_kpi_visualizer'

# Create a database connection string
conn_str = f'postgresql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}'

# Create an engine using SQLAlchemy
engine = create_engine(conn_str)

# Load the DataFrame to the PostgreSQL database
try:
    df.to_sql('amazon_sales', engine, if_exists='replace', index=False)  # Replace 'amazon_sales' with your desired table name
    print("Data loaded successfully")
except Exception as e:
    print(f"Error loading data: {e}")
    