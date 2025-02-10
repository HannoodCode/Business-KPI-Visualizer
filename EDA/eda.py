import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sqlalchemy import create_engine
import matplotlib.ticker as mtick

# Database connection
conn = create_engine('postgresql://postgres:q4J6KaBe@localhost/business_kpi_visualizer')

# Load data from the database
df = pd.read_sql('SELECT * FROM amazon_sales', conn)

# Data cleaning (Mainly Filling missing values)
df.drop(columns=['Unnamed: 23'], inplace=True, errors='ignore')
df['currency'] = df['currency'].fillna('N/A')
df['Amount'] = df['Amount'].fillna(np.nan)
df['promotion-ids'] = df['promotion-ids'].fillna('None')
df['fulfilled-by'] = df['fulfilled-by'].fillna('Not Easy Shipping')
df['Courier Status'] = df['Courier Status'].fillna('Unknown')
df['ship-city'] = df['ship-city'].fillna('Unknown')
df['ship-state'] = df['ship-state'].fillna('Unknown')
df['ship-postal-code'] = df['ship-postal-code'].fillna('Unknown')
df['ship-country'] = df['ship-country'].fillna('Unknown')
df.loc[df['Courier Status'].isin(['Cancelled', 'Unshipped', 'Unknown']), 'Amount'] = np.nan

#  Summary statistics
print(df.describe())

print(df.dtypes)

# Convert 'Date' column to datetime format
df['Date'] = pd.to_datetime(df['Date'], dayfirst=True)

# Group by Date and sum the Amount
amount_over_time = df.groupby('Date')['Amount'].sum().reset_index()

# Ensure the Date column is in datetime format
amount_over_time['Date'] = pd.to_datetime(amount_over_time['Date'], errors='coerce')

# Filter data to start from 01/04/2022 and end on 26/06/2022
filtered_data = amount_over_time[
    (amount_over_time['Date'] >= '2022-04-01') & 
    (amount_over_time['Date'] <= '2022-06-26')
]
# Visualizations
plt.figure(figsize=(12, 6))
plt.plot(filtered_data['Date'], filtered_data['Amount'], marker='o')
plt.title('Total Amount Over Time (Filtered)')
plt.xlabel('Date')
plt.ylabel('Total Amount')
plt.xticks(rotation=45)
plt.grid()
plt.tight_layout()
plt.show()

plt.figure(figsize=(8, 6))
sns.scatterplot(data=df, x='Qty', y='Amount', alpha=0.6)
plt.title('Scatter Plot of Qty vs Amount')
plt.xlabel('Quantity')
plt.ylabel('Amount')
plt.grid(True)
plt.show()

df['fulfilled-by'].value_counts().plot(kind='bar')
plt.title('Count of Fulfilled By')
plt.xlabel('Fulfilled By')
plt.ylabel('Count')
plt.show()

# Save the cleaned DataFrame to a CSV file
df.to_csv('cleaned_data.csv', index=False)
print("Cleaned data saved to 'cleaned_data.csv'")
