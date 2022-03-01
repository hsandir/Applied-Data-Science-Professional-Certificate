# Import required libraries
import pandas as pd
import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output
import plotly.express as px

# Read the airline data into pandas dataframe
spacex_df = pd.read_csv("spacex_launch_dash.csv")
max_payload = int(spacex_df['Payload Mass (kg)'].max())
min_payload = int(spacex_df['Payload Mass (kg)'].min())
launch_sites_df = spacex_df.groupby(['Launch Site'], as_index=False).first()

option_df= [{'label': i, 'value': i} for i in launch_sites_df['Launch Site']]
option_df.append({'label': 'All Sites', 'value': 'ALL'})

mark_f= {i : '%i kg' %i  for i in range(min_payload,max_payload,1000)}

# Create a dash application
app = dash.Dash(__name__)

# Create an app layout
app.layout = html.Div(children=[html.H1('SpaceX Launch Records Dashboard',
                                        style={'textAlign': 'center', 'color': '#503D36',
                                               'font-size': 40}),
                                # TASK 1: Add a dropdown list to enable Launch Site selection
                                # The default select value is for ALL sites
                                # dcc.Dropdown(id='site-dropdown',...)
                                dcc.Dropdown(id='site-dropdown', 
                                                     # Update dropdown values using list comphrehension
                                                     options=option_df,
                                                        value='ALL',
                                                     placeholder="Select a Launch Site",
                                                     searchable=True,
                                                     #style={'width':'80%', 'padding':'3px', 'font-size': '20px', 'text-align-last' : 'center'}
                                            ),


                                html.Br(),

                                # TASK 2: Add a pie chart to show the total successful launches count for all sites
                                # If a specific launch site was selected, show the Success vs. Failed counts for the site
                                html.Div(dcc.Graph(id='success-pie-chart')),
                                html.Br(),

                                html.P("Payload range (Kg):"),
                                # TASK 3: Add a slider to select payload range
                                #dcc.RangeSlider(id='payload-slider',...)
                                dcc.RangeSlider(id='payload-slider',
                                    min=0, max=10000, step=1000,
                                    marks=mark_f,
                                    value=[min_payload, max_payload]),





                                # TASK 4: Add a scatter chart to show the correlation between payload and launch success
                                html.Div(dcc.Graph(id='success-payload-scatter-chart')),
                                ])

# TASK 2:
# Add a callback function for `site-dropdown` as input, `success-pie-chart` as output
@app.callback(Output(component_id='success-pie-chart', component_property='figure'),
              Input(component_id='site-dropdown', component_property='value'))
def success_pie_chart(entered_site):
    filtered_df =spacex_df.groupby('Launch Site')['class'].mean().reset_index()
    if entered_site == 'ALL':
        title_f = 'Success Rate by Launch Sites'
        value_f= 'class'
        name_f='Launch Site'

        
    else:
        selected_df =  spacex_df[spacex_df['Launch Site']==entered_site]
        filtered_df= selected_df['Launch Site'].groupby(spacex_df['class']).count().reset_index()
        title_f = 'Success Rate by %s ' % entered_site
        value_f = 'Launch Site'
        name_f='class'
    fig = px.pie(filtered_df, values= value_f, names=name_f, title=title_f)
    return fig
        
# TASK 4:
# Add a callback function for `site-dropdown` and `payload-slider` as inputs, `success-payload-scatter-chart` as output
@app.callback(Output(component_id='success-payload-scatter-chart', component_property='figure'),
              Input(component_id='site-dropdown', component_property='value'),
              Input(component_id='payload-slider', component_property='value'))


def success_payload_scatter_chart(entered_site, range):
    low, high = range
    filtered_df =spacex_df[spacex_df['Payload Mass (kg)'].apply(lambda x : x > low and x < high)].reset_index()
    if entered_site == 'ALL':
        title_f = 'Success Rate by Launch Sites'
        value_f= 'Payload Mass (kg)'
        name_f='Launch Site'

        
    else:
        selected_df =  spacex_df[spacex_df['Launch Site']==entered_site]
        filtered_df= selected_df.groupby(['Launch Site','class', 'Booster Version'])['Payload Mass (kg)'].sum().reset_index()
        title_f = 'Success Rate by %s ' % entered_site
        value_f = 'Payload Mass (kg)'
        name_f='class'
    fig = px.scatter(filtered_df, x= value_f, y=name_f, title=title_f, color="Booster Version")   
    return fig


# Run the app
if __name__ == '__main__':
    app.run_server(port=8050)

