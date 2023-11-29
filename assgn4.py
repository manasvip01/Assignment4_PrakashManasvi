import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import plotly.express as px
import pandas as pd
# Data taken from- https://informationisbeautiful.net/visualizations/worlds-biggest-data-breaches-hacks/
# Load your dataset
df = pd.read_excel('IIB Data Breaches - LATEST.xlsx')

# Clean and prepare your data
df['method'] = df['method'].str.strip()
df.rename(columns={'year   ': 'year'}, inplace=True)
df['year'] = pd.to_numeric(df['year'], errors='coerce')
df['records lost'] = pd.to_numeric(df['records lost'], errors='coerce')
df['data sensitivity'] = pd.to_numeric(df['data sensitivity'], errors='coerce')

# Replace NaN values with a default value
default_size = df['records lost'].mean()
df['records lost'].fillna(default_size, inplace=True)
df['data sensitivity'].fillna(df['data sensitivity'].mean(), inplace=True)

# Initialize the Dash app
app = dash.Dash(__name__)

# Define the layout of the app
app.layout = html.Div([
    html.H1("DATA BREACH ANALYSIS", style={'text-align': 'center', 'color': '#FFFFFF', 'font-family': 'Times New Roman, serif','background': 'linear-gradient(to bottom, #333333, #555555)'}),

    html.Div([
        dcc.Graph(id='bubble-chart', style={'display': 'inline-block', 'width': '70%'}),

        html.Div([
            html.Label("Select Year Range:", style={'color': '#333333','font-family': 'Times New Roman, serif', 'font-weight': 'bold','margin-left':'-90px','font-size':'30px'}),
            dcc.RangeSlider(
                id='year-slider',
                min=df['year'].min(),
                max=df['year'].max(),
                value=[df['year'].min(), df['year'].max()],
                marks={str(year): {'label': str(year)} for year in df['year'].dropna().unique()},
                step=None
            ),
            html.Div(
                [html.Div(str(int(year)), className='year-label') 
                 for year in df['year'].dropna().unique()], className='year-labels-container'
            )
        ], style={'display': 'inline-block', 'width': '30%', 'vertical-align': 'top','margin-top':'300px','margin-left':'-70px'})
    ], style={'backgroundColor': '#FFFFFF'})
], style={'backgroundColor': '#FFFFFF'})

# Define callback to update graph
@app.callback(
    Output('bubble-chart', 'figure'),
    [Input('year-slider', 'value')]
)
def update_graph(selected_years):
    filtered_df = df[df['year'].between(selected_years[0], selected_years[1])]

    fig = px.scatter_3d(filtered_df, x='sector', y='organisation', z='records lost',
                        color='method', size='data sensitivity',
                        hover_data=['organisation', 'records lost', 'sector', 'data sensitivity','ID','source name'],
                        title="IIB Data Breaches",
                        color_continuous_scale=px.colors.sequential.Inferno)

    
    fig.update_layout(
        transition_duration=500,
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        scene=dict(
            xaxis=dict(backgroundcolor="rgb(200, 200, 230)",title=dict(text='SECTOR', font=dict(color='#1a0226',family='Times New Roman, serif')), tickfont=dict(size=10,family='Times New Roman, serif')),
            yaxis=dict(backgroundcolor="rgb(230, 200,230)", title=dict(text='ORGANISATION', font=dict(color='#1a0226',family='Times New Roman, serif')),tickfont=dict(size=10,family='Times New Roman, serif')),
            zaxis=dict(backgroundcolor="rgb(230, 230,200)", title=dict(text='RECORDS LOST', font=dict(color='#1a0226',family='Times New Roman, serif')),tickfont=dict(size=10,family='Times New Roman, serif'))
        ),
        margin=dict(l=100, r=0, b=0, t=40),
        legend=dict(font=dict(size=17,family='Times New Roman, serif'),title=dict(text='Method')),
        title=dict(text='IIB Data Breaches', font=dict(size=20, family='Times New Roman, serif', color='#333333'))
    )

    
    fig.update_layout(height=600, width=800)

    return fig

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)
