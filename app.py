from dash import Dash, html, dcc, callback, Output, Input, State
import dash_bootstrap_components as dbc
import pandas as pd
import plotly.express as px
from sqlalchemy import create_engine
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
import os
from database import DATABASE_URL
from llm import call_llm
import json
from dash.exceptions import PreventUpdate
from dash import no_update
import asyncio

# Load environment variables from .env file
load_dotenv()

# Access your OpenAI API key
openai_api_key = os.getenv("OPENAI_API_KEY")

# Database setup
DATABASE_URL = os.getenv("DATABASE_URL")
engine = create_engine(DATABASE_URL)

# Querying the database
query = "SELECT date, amount, qty, status FROM amazon_sales"
df = pd.read_sql_query(query, engine)

# Convert the date column to datetime
df['date'] = pd.to_datetime(df['date'], format='%d/%m/%Y')


# Dash app setup
app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

# Layout with styling
app.layout = dbc.Container([
    dbc.Row([
        dbc.Col(html.H1("Business KPI Visualizer", className="text-center my-4"), width=12)
    ]),
    dbc.Row([
        dbc.Col([
            html.Label("Select Status:", className="fw-bold"),
            dcc.Dropdown(
                options=[
                    {"label": status, "value": status} for status in df["status"].unique()
                ],
                id="dropdown-selection",
                placeholder="Select a status",
                className="mb-3"
            )
        ], width=6),
        dbc.Col([
            html.Label("Select Y-Axis:", className="fw-bold"),
            dcc.RadioItems(
                options=[
                    {"label": "Sales (in Rupees)", "value": "amount"},
                    {"label": "Quantity", "value": "qty"}
                ],
                id="y-axis-selection",
                value="amount",
                inline=True,
                className="mb-3"
            )
        ], width=6)
    ]),
    dbc.Row([
        dbc.Col(dcc.Graph(id="graph-content"), width=12)
    ]),
    
    # New chat interface
    dbc.Row([
        dbc.Col([
            html.Div([
                html.Div(id="chat-history", style={
                    "height": "300px",
                    "overflow-y": "auto",
                    "border": "1px solid #ddd",
                    "padding": "10px",
                    "margin-bottom": "10px",
                    "border-radius": "5px"
                }),
                dbc.Input(id="chat-input", placeholder="Ask about your data...", type="text"),
                dbc.Button("Send", id="send-button", color="primary", className="mt-2"),
            ], className="my-4")
        ], width=12)
    ])
], fluid=True)

@callback(
    Output("graph-content", "figure"),
    Input("dropdown-selection", "value"),
    Input("y-axis-selection", "value")
)
def update_graph(selected_status, selected_y_axis):
    if selected_status is None:
        return px.line(title="Select a status to view the graph")

    # Filter data based on the selected status
    filtered_df = df[df['status'] == selected_status]
    
    # Remove specific dates (31st March and 29th June)
    excluded_dates = pd.to_datetime(['31/03/2022', '29/06/2022'], format='%d/%m/%Y')
    filtered_df = filtered_df[~filtered_df['date'].isin(excluded_dates)]
    
    # Aggregate the data by date for the selected y-axis
    aggregated_data = filtered_df.groupby('date', as_index=False)[selected_y_axis].sum()
    
    # Adjust y-axis label dynamically
    y_axis_label = "Sales (in Rupees)" if selected_y_axis == "amount" else "Quantity"
    
    # Create the line chart
    fig = px.line(
        aggregated_data,
        x="date",
        y=selected_y_axis,
        title=f"{y_axis_label} over Time for Status: {selected_status}",
        labels={selected_y_axis: y_axis_label, 'date': 'Date'}
    )
    return fig

def prepare_kpi_data(df):
    """Prepare KPI data for LLM analysis"""
    # Calculate daily aggregates
    daily_kpis = df.groupby(['date', 'status']).agg({
        'amount': ['sum', 'mean'],
        'qty': ['sum', 'mean']
    }).reset_index()
    
    # Flatten column names
    daily_kpis.columns = ['date', 'status', 
                         'total_sales', 'avg_sales',
                         'total_quantity', 'avg_quantity']
    
    # Convert date to string for JSON serialization
    daily_kpis['date'] = daily_kpis['date'].dt.strftime('%Y-%m-%d')
    
    # Calculate metrics by status with flattened column names
    metrics_by_status = df.groupby('status').agg({
        'amount': ['sum', 'mean', 'count'],
        'qty': ['sum', 'mean']
    })
    
    # Flatten the multi-index columns
    metrics_by_status.columns = [
        f"{col[0]}_{col[1]}" for col in metrics_by_status.columns
    ]
    
    # Enhanced statistics
    overall_stats = {
        'total_revenue': float(df['amount'].sum()),
        'total_orders': int(len(df)),
        'avg_order_value': float(df['amount'].mean()),
        'status_distribution': df['status'].value_counts().to_dict(),
        'date_range': {
            'start': df['date'].min().strftime('%Y-%m-%d'),
            'end': df['date'].max().strftime('%Y-%m-%d')
        },
        'metrics_by_status': metrics_by_status.round(2).to_dict('index')
    }
    
    return {
        'daily_metrics': daily_kpis.to_dict(orient='records'),
        'overall_stats': overall_stats
    }

# Modify the update_chat callback
@callback(
    Output("chat-history", "children"),
    [Input("send-button", "n_clicks")],
    [State("chat-input", "value"),
     State("chat-history", "children"),
     State("dropdown-selection", "value")],
    prevent_initial_call=True
)
def update_chat(n_clicks, user_input, chat_history, selected_status):
    if not user_input:
        raise PreventUpdate
    
    if chat_history is None:
        chat_history = []
    
    # Add user message to chat immediately
    chat_history.append(
        html.Div([
            html.Span("You: ", style={"font-weight": "bold"}),
            html.Span(user_input)
        ], style={"margin-bottom": "10px"})
    )
    
    # Add loading message
    chat_history.append(
        html.Div([
            html.Span("AI: ", style={"font-weight": "bold"}),
            html.Span("Analyzing data...", id="ai-response")
        ], style={"margin-bottom": "10px", "color": "#2E86C1"})
    )
    
    # Filter data if status is selected
    filtered_df = df[df['status'] == selected_status] if selected_status else df
    
    # Prepare KPI data with additional context
    kpi_data = prepare_kpi_data(filtered_df)
    
    # Add trend analysis
    kpi_data['trends'] = calculate_trends(filtered_df)
    
    # Convert to JSON for LLM
    selected_data = json.dumps(kpi_data)
    
    # Get AI response synchronously
    response = asyncio.run(get_llm_response(user_input, selected_data, selected_status))
    
    # Update the last message (remove loading message and add actual response)
    chat_history[-1] = html.Div([
        html.Span("AI: ", style={"font-weight": "bold"}),
        html.Span(response)
    ], style={"margin-bottom": "10px", "color": "#2E86C1"})
    
    return chat_history

def calculate_trends(df):
    """Calculate additional trend metrics for the data"""
    # Calculate daily totals first
    daily_totals = df.groupby('date').agg({
        'amount': 'sum',
        'qty': 'sum'
    })
    
    # Calculate growth rates
    daily_growth = daily_totals.pct_change()
    
    # Get top performing days
    top_days = daily_totals.nlargest(5, 'amount')
    
    # Calculate weekly averages
    weekly_avg = df.groupby(pd.Grouper(key='date', freq='W')).agg({
        'amount': 'mean',
        'qty': 'mean'
    })
    
    trends = {
        'daily_growth': {
            'amount': float(daily_growth['amount'].mean()),
            'quantity': float(daily_growth['qty'].mean())
        },
        'top_performing_days': {
            date.strftime('%Y-%m-%d'): {
                'amount': float(row['amount']),
                'quantity': float(row['qty'])
            }
            for date, row in top_days.iterrows()
        },
        'weekly_averages': {
            date.strftime('%Y-%m-%d'): {
                'amount': float(row['amount']),
                'quantity': float(row['qty'])
            }
            for date, row in weekly_avg.iterrows()
        }
    }
    return trends

async def get_llm_response(user_query, selected_data, selected_status=None):
    """Helper function to get LLM response asynchronously"""
    response = ""
    async for chunk in call_llm(user_query, selected_data, selected_status):
        response += chunk
    return response

# Add callback to clear input after sending
@callback(
    Output("chat-input", "value"),
    [Input("send-button", "n_clicks")],
    prevent_initial_call=True
)
def clear_input(n_clicks):
    return ""

if __name__ == "__main__":
    app.run(debug=True)
