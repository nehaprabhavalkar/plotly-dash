import dash
from dash.dependencies import Input, Output
import dash_table
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import calendar
import flask

df = pd.read_excel('bq.xlsx')

server = flask.Flask(__name__)
app = dash.Dash(__name__, server=server)


df['year'] = pd.DatetimeIndex(df['Date']).year
df['month'] = pd.DatetimeIndex(df['Date']).month
df['month'] = df['month'].apply(lambda x: calendar.month_abbr[x])

df['year'] = df['year'].astype('str')
df['year'] = df['year'].str[2:]

df['date'] = df['month'] + ' ' +df['year']

df = df.drop(['Date','year','month'],axis=1)

new_df = pd.DataFrame(pd.pivot_table(df,index=['Item Sort Order','Item Type','Item'],columns='date'))

new_df.columns = [col[1] for col in new_df.columns]

i = 3

while i > 0:
	new_df = new_df.reset_index(level=0)
 	# run 2 times as two levels need to be dropped
	i = i-1 

fruit_df = new_df[new_df['Item Type']=='Fruit']
veg_df = new_df[new_df['Item Type']=='Vegetable']

new_df = new_df.drop(['Item Type'],axis=1)
fruit_df = fruit_df.drop(['Item Type'],axis=1)
veg_df = veg_df.drop(['Item Type'],axis=1)
available_indicators = ['Select All','Fruit','Vegetable']

app.layout = html.Div(children=[
    html.Div([
            dcc.Dropdown(
                id='column',
                options=[{'label': i, 'value': i} for i in available_indicators],
                placeholder = 'Select a Field...',
                value='',
                style={'width': '48%'}
            ),
            

            html.Br(),
html.Div([
    dash_table.DataTable(
        id='datatable-interactivity',
        columns=[
            {"name": i, "id": i, "selectable": True} for i in new_df.columns
        ],
        style_table={'height': 500,
        			'width': 600},
        style_as_list_view=True,

    	style_header={'backgroundColor': 'rgb(173, 216, 230)' ,
    				'border': '1px solid black'}, 
        style_cell={
        'backgroundColor': 'rgb(255, 255, 255)',
        'border': '1px solid black'
    	},          

    	style_data={ 'border': '1px solid black' }, 
        data=new_df.to_dict('records'),

        export_format='csv',

        sort_action="native",
        sort_mode="multi"
    ),
    html.Br(),
    html.Div(id='datatable-interactivity-container'),
    html.Br()
])
])
])



@app.callback(
    Output('datatable-interactivity','data'),
    [Input('column', 'value')]
    )

def update_table(input_value):
	if input_value =='Fruit':
		data=fruit_df.to_dict('records')
		return data
	elif input_value =='Vegetable':
		data=veg_df.to_dict('records')
		return data
	else:
		data=new_df.to_dict('records')
		return data


if __name__ == '__main__':
    app.run_server(debug=True)

