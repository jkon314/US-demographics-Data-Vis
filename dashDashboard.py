# If you prefer to run the code online instead of on your computer click:
# https://github.com/Coding-with-Adam/Dash-by-Plotly#execute-code-in-browser

from dash import Dash, dcc, Input, Output

import dash_bootstrap_components as dbc  
import pandas as pd
import plotly.express as px
import plotly.graph_objects as gobj

# Build your components


df = pd.read_csv('county_demographics.csv')

stateDF = df.drop(columns='County') # i know this isn't accurate but couldnt find population distribution data to supplement

stateDF.groupby('State').mean()

app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
mytext = dcc.Markdown(children="#US Demographics Dashboard")

droptions = []

for col in df.columns:
    print(col)
    if (col != "State" and col != "County"):
        print("good col name")
        droptions.append({'label':'{}'.format(col, col), 'value':col})
        #we dont want state and County in dropdown


states = df['State'].unique()

stateDroptions = []
for state in states:
    stateDroptions.append({'label':'{}'.format(state, state), 'value':state})
#print(stateDf)

# Customize your own Layout
app.layout = dbc.Container([

    mytext,
    dbc.Alert("Hi there",color="success"),
    dcc.Dropdown(id="selectCategory", options=droptions, value="Age.Percent Under 18 Years"),

    dcc.Graph(id='usMap',figure=px.choropleth(
        data_frame = stateDF,
        locationmode='USA-states',
        locations='State',
        scope="usa",
        color= "Age.Percent Under 18 Years",
        #hover_data=['State', category],
        color_continuous_scale=px.colors.sequential.YlOrRd,
        labels={'Pct of Colonies Impacted': '% of Bee Colonies'},
        template='plotly_dark'




        )),

    dcc.Dropdown(id="selectState", options=stateDroptions, value="PA"),
    dcc.Graph(id='stateMap', figure=px.bar(
        
        df.loc[df['State'] == 'PA'],
        x='Age.Percent Under 18 Years',
        y='County'


        ))

    ])

@app.callback(
    [Output(component_id='usMap', component_property='figure')],
   # [Output(component_id='stateMap',component_property='figure')],
    [Input(component_id='selectCategory', component_property='value')],
    #[Input(component_id='selectState',component_property='value')]
)

def update_us_map(category,state):
    fig1 = px.choropleth(
        data_frame = stateDF,
        locationmode='USA-states',
        locations='State',
        scope="usa",
        color= category,
        #hover_data=['State', category],
        color_continuous_scale=px.colors.sequential.YlOrRd,
        labels={'Pct of Colonies Impacted': '% of Bee Colonies'},
        template='plotly_dark'




        )

    #dfCounty = df.loc[df['State'] == state]

   # fig2 = px.bar(
    #    
     #   dfCounty,
      #  x=category,
       # y='County'
#
#
 #       )
    return [fig1]#,[fig2]
# Run app
if __name__=='__main__':
    app.run_server(port=8051)