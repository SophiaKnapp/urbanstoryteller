# Environment used: dash1_8_0_env
from re import X
import pandas as pd     #(version 1.0.0)
import plotly           #(version 4.5.0)
import plotly.express as px

import dash             #(version 1.8.0)
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate
import json
# print(px.data.gapminder()[:15])

external_stylesheets = ["https://codepen.io/chriddyp/pen/bWLwgP.css"]

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

#---------

# GET DATA HERE

#---------------------------------------------------------------
app.layout = html.Div([

    html.Div([
        dcc.Graph(id='the_graph')
    ]),

    # I should do: type='text' https://dash.plotly.com/dash-core-components/input

    html.Div([
        dcc.Input(id='input_state', type='number', inputMode='numeric', value=2007,
                  max=2007, min=1952, step=5, required=True),
        # dcc.Input(id='selected_hashtag', type='text', value='hashtag'),
        html.Button(id='submit_button', n_clicks=0, children='Submit'),
        html.Div(id='output_state'),
    ],style={'text-align': 'center'}),



])

#---------------------------------------------------------------
@app.callback(
    [Output('output_state', 'children'),
    Output(component_id='the_graph', component_property='figure')],
    [Input(component_id='submit_button', component_property='n_clicks')],
    [State(component_id='input_state', component_property='value')]
)
# if I change state to input: callback gets called every time I change it, not just when I click the button

# number of inputs and outputs like callback
def update_output(num_clicks, val_selected):
    if val_selected is None:
        raise PreventUpdate
    else:
        # data by plotly: px.data.gapminder()
        # df = px.data.gapminder().query("year=={}".format(val_selected)) # filtering the data
        # print(df[:3])

        data={'loc':[0,1,2],'n_posts':[100,20,4]}
        df=pd.DataFrame(data)
        print(df)

        with open('test.json') as f:
            potatoes = json.load(f)

            print(potatoes)

        fig = px.choropleth(df, locations="loc",
                            color="n_posts",
                            hover_name="n_posts",
                            geojson=potatoes,
                            # projection='natural earth',
                            center={'lat': 11.581649780273438, 'lon': 48.125309497327876}, X
                            # TODO https://medium.com/analytics-vidhya/create-choropleth-maps-by-using-plotly-31771803da7
                            title='Life Expectancy by Year',
                            color_continuous_scale=px.colors.sequential.Plasma)

    

        fig.update_geos(fitbounds="locations", visible=False)

        fig.update_layout(title=dict(font=dict(size=28),x=0.5,xanchor='center'),
                        margin=dict(l=60, r=60, t=50, b=50))



        return ('The input value was "{}" and the button has been \
                clicked {} times'.format(val_selected, num_clicks), fig)

app.run_server(debug=True)