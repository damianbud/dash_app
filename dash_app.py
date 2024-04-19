import pandas as pd 
import dash
from dash import Dash, dcc, html, callback
from dash.dependencies import Input, Output, State
import plotly.express as px
from dash import dash_table
import dash_bootstrap_components as dbc


df = pd.read_csv("_select_city_lon_lat_date_trunc_week_date_time_as_week_start_cou_202404181607.csv", index_col=0)
df_reset = df.reset_index()

df_berlin = df_reset[df_reset['city']=='Berlin']

df_cities =df_reset[df_reset['city'].isin(['Berlin', 'Brighton', 'Porto Alegre'])]

#table
table = dash_table.DataTable(df_berlin.to_dict('records'),
                                  [{"name": i, "id": i} for i in df_berlin.columns],
                               style_data={'color': 'white','backgroundColor': "#222222"},
                              style_header={
                                  'backgroundColor': 'rgb(210, 210, 210)',
                                  'color': 'black','fontWeight': 'bold'}, 
                                     style_table={ 
                                         'minHeight': '400px', 'height': '400px', 'maxHeight': '400px',
                                         'minWidth': '900px', 'width': '900px', 'maxWidth': '900px',
                                         'marginLeft': 'auto', 'marginRight': 'auto',
                                         'marginTop': 0, 'marginBottom': "30"}
                                     )

fig1 = px.bar(df_cities, 
             x='week_start', 
             y='number_of_hours',  
             color='city',
             color_discrete_map={'Berlin': 'red', 'Brighton': 'blue', 'Porto Alegre': 'green'}, 
             barmode='group',
             height=300, title = "Berlin vs Brighton & Porto Alegre",)

fig1 = fig1.update_layout(
        plot_bgcolor="#222222", paper_bgcolor="#222222", font_color="white", 
    #margin=dict(l=20, r=20, t=0, b=20)
)
    

graph1 = dcc.Graph(figure=fig1)

#Line graph
fig2 = px.line(df_berlin, x='week_start', y='number_of_hours', height=300, title="No. of hours with good conditions for cycling", markers=True)
fig2 = fig2.update_layout(
        plot_bgcolor="#222222", paper_bgcolor="#222222", font_color="white"
    )
graph2 = dcc.Graph(figure=fig2)


fig3 = px.scatter_geo(df_cities, 
                      lat='lat', 
                      lon='lon',
                      color='number_of_hours',
                      projection='natural earth',
                      animation_frame="week_start", # Ensure you have a year column in df_cities or remove this line
                      scope='world',
                      color_continuous_scale=px.colors.sequential.ice,
                      size='number_of_hours', # Optionally size points by some metric
                      hover_name='city') # Show city names when hovering over points

fig3 = fig3.update_layout(
    plot_bgcolor="#222222", 
    paper_bgcolor="#222222", 
    font_color="white", 
    geo_bgcolor="#222222"
)

# Using a Dash component to display the figure
graph3 = dcc.Graph(figure=fig3)

data_dict = {
    'Category': ['Yes', 'No'],
    'Values': ['100', '0']
}
df = pd.DataFrame(data_dict)

fig4 = px.pie(df, names='Category', values='Values', title='Is this a pie chart?')

fig4 = fig4.update_layout(
    plot_bgcolor="#222222", 
    paper_bgcolor="#222222", 
    font_color="white", 
    geo_bgcolor="#222222"
)
graph4 = dcc.Graph(figure=fig4)


app =dash.Dash(external_stylesheets=[dbc.themes.DARKLY])
server = app.server
app.layout = html.Div([html.H1('Good cycling conditions in Berlin', style={'textAlign': 'center', 'color': '#636EFA'}), 
                       html.Div(html.P("Using the wheater data we take a look at Berlin's hours with good cycling conditions"), 
                                style={'marginLeft': 50, 'marginRight': 25}),
                       html.Div([html.Div('Berlin', 
                                          style={'backgroundColor': '#636EFA', 'color': 'white', 
                                                 'width': '900px', 'marginLeft': 'auto', 'marginRight': 'auto'}),
                                 table, graph1,  graph2, graph3, graph4]),
                        html.Div([html.Button("Download Data", id="btn-download-txt", 
                                             style={'marginLeft': 50, 'marginRight': 25,
                                                   'marginTop': 10, 'marginBottom': "30"}),
                                 dcc.Download(id="download-text")]),                    
])

                       
@callback(
    Output("download-text", "data"),
    Input("btn-download-txt", "n_clicks"),
    prevent_initial_call=True  #you ensure that the callback isn't executed when the app first loads
)


def download_table(n_clicks):
        return dcc.send_data_frame(df.to_csv, filename="cycling_hours_in_cities.txt")

if __name__ == '__main__':
     app.run_server(port=8020)