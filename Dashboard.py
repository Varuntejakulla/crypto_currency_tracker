from dash import Dash, dcc, html, Input, Output
from pycoingecko import CoinGeckoAPI
import pandas as pd
import plotly.express as px
import requests
from datetime import datetime

# Function to fetch cryptocurrency data
def fetch_data():
    coins = []
    for page in range(1, 6):  # Fetch data for 5 pages (100 coins total, 20 coins per page)
        coins.extend(cg.get_coins_markets(vs_currency='usd', per_page=20, page=page))
    df = pd.DataFrame(coins)
    # Convert 'last_updated' to datetime
    df['last_updated'] = pd.to_datetime(df['last_updated'])
    return df

# Function to fetch simplified price data
def fetch_simple_price(coin_id):
    url = "https://api.coingecko.com/api/v3/simple/price"
    params = {
        "ids": coin_id,
        "vs_currencies": "usd",
        "include_market_cap": "true",
        "include_24hr_vol": "true",
        "include_24hr_change": "true",
        "include_last_updated_at": "true"
    }
    response = requests.get(url, params=params).json()
    return response

# Initialize Dash App
app = Dash(__name__)

# Initialize CoinGecko API
cg = CoinGeckoAPI()

# Fetch and prepare data
data = fetch_data()

# Define application layout
app.layout = html.Div(
    style={'backgroundColor': '#1a1a1a', 'color': '#ffffff', 'padding': '10px'},
    children=[
        html.H1(
            "Cryptocurrency Dashboard",
            style={'textAlign': 'center', 'color': '#00ff99'}
        ),
        dcc.Dropdown(
            id='coin-selector',
            options=[{'label': coin, 'value': coin} for coin in data['id']],
            value=data['id'][0],
            multi=False,
            placeholder="Select a cryptocurrency",
            style={
                'backgroundColor': '',
                'color':'red',
                'border': '1px solid #00ff99'
            }
        ),
        html.Div(
            id='coin-details',
            style={
                'textAlign': 'center',
                'fontSize': '20px',
                'margin': '20px',
                'padding': '15px',
                'borderRadius': '10px',
                'backgroundColor': '#292929',
                'boxShadow': '0 4px 8px rgba(0, 0, 0, 0.2)',
                'fontFamily': 'Arial, sans-serif',
                'color': '#00ff99',
                'border': '1px solid #00ff99'
            }
        ),
        html.Div([
            dcc.Graph(id='market-cap-graph', style={'display': 'inline-block', 'width': '48%'}),
            dcc.Graph(id='volume-graph', style={'display': 'inline-block', 'width': '48%'})
        ]),
        dcc.Graph(id='24h-change-graph', style={'display': 'inline-block', 'width': '96%'}),
        dcc.Graph(id='pie-chart', style={'textAlign': 'center', 'marginTop': '20px'})
    ]
)

# Define callbacks for interactivity
@app.callback(
    [Output('coin-details', 'children'),
     Output('market-cap-graph', 'figure'),
     Output('volume-graph', 'figure'),
     Output('24h-change-graph', 'figure'),
     Output('pie-chart', 'figure')],
    [Input('coin-selector', 'value')]
)
def update_dashboard(selected_coin):
    if not selected_coin:
        return "Select a coin", {}, {}, {}, {}

    # Fetch simplified price data
    simple_price = fetch_simple_price(selected_coin)

    if selected_coin not in simple_price:
        return f"No data available for {selected_coin}", {}, {}, {}, {}

    coin_data = simple_price[selected_coin]

    # Prepare details section with clean UI
    details = html.Div(
    style={
        'display': 'flex',
        'justifyContent': 'space-between',
        'flexWrap': 'wrap',
        'gap': '10px',
        'padding': '10px',
        'backgroundColor': '#1a1a1a',
        'borderRadius': '10px',
    },
    children=[
        html.Div(
            f"Price (USD): ${coin_data['usd']}",
            style={
                'backgroundColor': '#292929',
                'padding': '20px',
                'borderRadius': '8px',
                'boxShadow': '0 4px 8px rgba(0, 0, 0, 0.2)',
                'color': '#00ff99',
                'textAlign': 'center',
                'flex': '1 1 20%',
                'fontSize': '18px',
            }
        ),
        html.Div(
            f"Market Cap (USD): ${coin_data['usd_market_cap']}",
            style={
                'backgroundColor': '#292929',
                'padding': '20px',
                'borderRadius': '8px',
                'boxShadow': '0 4px 8px rgba(0, 0, 0, 0.2)',
                'color': '#f39c12',
                'textAlign': 'center',
                'flex': '1 1 20%',
                'fontSize': '18px',
            }
        ),
        html.Div(
            f"24h Volume (USD): ${coin_data['usd_24h_vol']}",
            style={
                'backgroundColor': '#292929',
                'padding': '20px',
                'borderRadius': '8px',
                'boxShadow': '0 4px 8px rgba(0, 0, 0, 0.2)',
                'color': '#3498db',
                'textAlign': 'center',
                'flex': '1 1 20%',
                'fontSize': '18px',
            }
        ),
        html.Div(
            f"24h Change: {coin_data['usd_24h_change']}%",
            style={
                'backgroundColor': '#292929',
                'padding': '20px',
                'borderRadius': '8px',
                'boxShadow': '0 4px 8px rgba(0, 0, 0, 0.2)',
                'color': '#e74c3c' if coin_data['usd_24h_change'] < 0 else '#2ecc71',
                'textAlign': 'center',
                'flex': '1 1 20%',
                'fontSize': '18px',
            }
        ),
        html.Div(
            f"Last Updated: {datetime.utcfromtimestamp(coin_data['last_updated_at']).strftime('%Y-%m-%d %H:%M:%S')} UTC",
            style={
                'backgroundColor': '#292929',
                'padding': '20px',
                'borderRadius': '8px',
                'boxShadow': '0 4px 8px rgba(0, 0, 0, 0.2)',
                'color': '#9b59b6',
                'textAlign': 'center',
                'flex': '1 1 20%',
                'fontSize': '18px',
            }
        ),
    ]
)


    # Market Cap Graph
    fig_market_cap = px.bar(
        data,
        x='name',
        y='market_cap',
        title=f"Market Cap of {selected_coin}",
        labels={'market_cap': 'Market Cap (USD)'},
        template='plotly_dark',
        color='market_cap',
        color_continuous_scale='Viridis'
    )

    # Volume Graph
    fig_volume = px.bar(
        data,
        x='name',
        y='total_volume',
        title=f"24h Trading Volume of {selected_coin}",
        labels={'total_volume': 'Volume (USD)'},
        template='plotly_dark',
        color='total_volume',
        color_continuous_scale='Cividis'
    )

    # 24h Change Graph
    fig_change = px.bar(
        data,
        x='name',
        y='price_change_percentage_24h',
        title=f"24h Price Change of {selected_coin}",
        labels={'price_change_percentage_24h': 'Change (%)'},
        template='plotly_dark',
        color='price_change_percentage_24h',
        color_continuous_scale='Turbo'
    )

    # Pie Chart for Market Metrics
    fig_pie = px.pie(
        values=[coin_data['usd_market_cap'], coin_data['usd_24h_vol']],
        names=['Market Cap', '24h Volume'],
        title=f"Market Metrics for {selected_coin}",
        template='plotly_dark',
        color_discrete_sequence=px.colors.sequential.RdBu
    )

    return details, fig_market_cap, fig_volume, fig_change, fig_pie

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)
