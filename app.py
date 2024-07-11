import dash
from dash import dash_table, dcc, html, Input, State, Output, ALL
from dash.exceptions import PreventUpdate
import pandas as pd
import webbrowser

import utils
from utils import BOATS, BUCHSTABEN


def create_pairing_list():
    return utils.create_pairing_list()


app = dash.Dash(__name__, use_pages=False)

server = app.server

app.layout = html.Div(id='all',
                      children=[
                          html.Div(className='input-container', children=[
                              dcc.Store('data'),
                              html.H1('Scoring Dashboard'),
                              html.Button(id='download-result-button', children='Download Results'),
                              html.Br(),
                              html.Button(id='generate-pairing-list-button', children='Generate Pairing List'),
                              html.Br(),
                              html.Button(id='download-pairing-list-button', children='Download Pairing List'),
                              dcc.Download(id="download-pairing-list"),
                              dcc.Download(id="download-result-list"),
                              html.Hr(),
                              html.Div('Enter results:'),
                              dcc.Dropdown(id='race-select', disabled=True, placeholder='Select race'),
                              html.Div(id='result-entering', children=[]),
                              html.Hr(),
                              html.Div('Enter SCP:'),
                              dcc.Dropdown(id='team-scp', disabled=True),
                              dcc.Input(id='scp-value', disabled=True, type='number', min=0),
                              html.Button(id='save-scp-button', children='Save SCP'), ],
                                   style={'display': 'inline-block', 'width': '20%', 'font-family': 'sans-serif', 'margin': '10px'}),
                          html.Div(className='main-container',
                                   children=[dash_table.DataTable(id='result-table'), ],
                                   style={"display": "inline-block"}),
                      ],
                      style={'font-family': 'sans-serif', })


@app.callback(
    Output('data', 'data', allow_duplicate=True),
    Output('race-select', 'options'),
    Output('race-select', 'disabled'),
    Output('team-scp', 'options'),
    Output('team-scp', 'disabled'),
    Output('scp-value', 'disabled'),

    Input('generate-pairing-list-button', 'n_clicks'),
    prevent_initial_call=True
)
def generate_pairing_list(n_clicks):
    pairing_list, results = create_pairing_list()

    data_dict = {'pairing_list': pairing_list.reset_index().to_dict('split'),
                 'results': results.reset_index().to_dict('split')}
    return data_dict, pairing_list['Race'], False, results['Teams'], False, False


@app.callback(
    Output('result-table', 'data'),
    Output('result-table', 'columns'),

    Input('data', 'data'),
    prevent_initial_call=True
)
def update_result_table(data):
    results = pd.DataFrame(data['results']['data'], data['results']['index'], data['results']['columns']).set_index(
        'index')
    results = utils.sort_results(results)
    results.insert(0, 'Rank', range(1, results.shape[0] + 1))
    results.fillna('-', inplace=True)
    # TODO: highlight results by race assignment per flight
    return results.to_dict('records'), [{"name": i, "id": i} for i in results.columns]


@app.callback(
    Output('download-pairing-list', 'data'),

    Input('download-pairing-list-button', 'n_clicks'),
    State('data', 'data'),
    prevent_initial_call=True
)
def download_pairing_list(n_clicks, data):
    pairing_list = pd.DataFrame(data['pairing_list']['data'], data['pairing_list']['index'],
                                data['pairing_list']['columns']).set_index('index')
    return dcc.send_data_frame(pairing_list.to_csv, 'pairing_list.csv')


@app.callback(
    Output('download-result-list', 'data'),

    Input('download-result-button', 'n_clicks'),
    State('data', 'data'),
    prevent_initial_call=True
)
def download_results(n_clicks, data):
    result_df = pd.DataFrame(data['results']['data'], data['results']['index'], data['results']['columns']).set_index(
        'index')
    return dcc.send_data_frame(result_df.to_csv, 'results.csv')


@app.callback(
    Output('result-entering', 'children'),
    # Output('result-text', 'children'),
    # Output('result-input', 'children'),

    Input('data', 'data'),
    Input('race-select', 'value'),
    prevent_initial_call=True
)
def display_results_enter(data, race, ):
    if not race:
        return [], []

    patched_elements = []

    # TODO: Get number of boats from pairing list
    pairing_list = pd.DataFrame(data['pairing_list']['data'], data['pairing_list']['index'],
                                data['pairing_list']['columns']).set_index('index')
    result_df = pd.DataFrame(data['results']['data'], data['results']['index'], data['results']['columns']).set_index(
        'index')

    # get row of selected race for team -> boat assignment
    race_details = pairing_list[pairing_list['Race'] == race]

    flight = utils.get_flight(race)

    for b in range(1, BOATS + 1):
        team = race_details[f'Boat{b}'].values[0]
        value_from_results = result_df[result_df['Teams'] == team][f'Flight {flight}'].values[0]

        html_element = html.Div(children=[
            html.Div(f'Boat {b} ' + team + ':'),
            dcc.Dropdown(id={"type": "boat-result-input", "index": b}, value=value_from_results,
                         options=[i for i in range(1, BOATS + 1)] + list(BUCHSTABEN.keys()),
                         placeholder='Boat {}'.format(b))
        ],
            style={'margin': '10px', 'display': 'inline-block'})
        patched_elements.append(html_element)

    return patched_elements


@app.callback(
    Output('data', 'data', allow_duplicate=True),

    Input({"type": "boat-result-input", "index": ALL}, "value"),

    State('race-select', 'value'),
    State('data', 'data'),
    prevent_initial_call=True,
)
def add_results(values, race, data):
    result_df = pd.DataFrame(data['results']['data'], data['results']['index'], data['results']['columns']).set_index(
        'index')
    pairing_list = pd.DataFrame(data['pairing_list']['data'], data['pairing_list']['index'],
                                data['pairing_list']['columns']).set_index('index')
    if not race:
        return data

    # select club for result by race and boat number
    # values is list with vals from all inputs in order boat 1 to boat 6

    # Get club from pairing
    race_details = pairing_list[pairing_list['Race'] == race]

    for b, value in zip(range(1, BOATS + 1), values):
        if value:
            try:
                value = int(value)
                if value < 1 or value > 6:
                    raise PreventUpdate
            except ValueError:
                if value not in BUCHSTABEN.keys():
                    raise PreventUpdate
            team = race_details[f'Boat{b}'].values[0]
            filtered_df = result_df[result_df['Teams'] == team]
            row_index = filtered_df.index[0]
            flight = utils.get_flight(race)
            result_df.loc[row_index, f'Flight {flight}'] = value

    data['results'] = result_df.reset_index().to_dict('split')
    return data


@app.callback(
    Output('data', 'data'),
    Output('team-scp', 'value'),
    Output('scp-value', 'value'),

    Input('save-scp-button', 'n_clicks'),

    State('data', 'data'),
    State('scp-value', 'value'),
    State('team-scp', 'value'),
    prevent_initial_call=True,
)
def modify_scp(n_clicks, data, scp, team):
    result_df = pd.DataFrame(data['results']['data'], data['results']['index'], data['results']['columns']).set_index(
        'index')
    if not team:
        return data

    result_df.loc[result_df['Teams'] == team, 'SCP'] = scp
    data['results'] = result_df.reset_index().to_dict('split')

    return data, None, None


def open_browser():
    port = 8050
    webbrowser.open_new("http://localhost:{}".format(port))


if __name__ == '__main__':
    debug = True
    if not debug:
        open_browser()
    app.run_server(debug=debug)
