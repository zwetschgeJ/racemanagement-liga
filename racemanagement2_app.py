import streamlit as st
import numpy as np
import pandas as pd
from pymongo import MongoClient
import utils
import utils_pairing_list1 as liga1
import utils_pairing_list2 as liga2

st.set_page_config(layout="wide")
st.title('Ergebnis-Manager')
st.sidebar.title('Options')
st.sidebar.divider()


@st.cache_resource
def init_connection():
    uri = f"mongodb+srv://{st.secrets['mongo']['db_username']}:{st.secrets['mongo']['db_password']}@{st.secrets['mongo']['cluster_name']}.3rpqm.mongodb.net/dsbl?retryWrites=true&w=majority"
    client = MongoClient(uri)
    try:
        client.admin.command('ping')
    except Exception as e:
        print(e)
    return client


leagues = ['1. Liga', '2. Liga']

selected_league = st.sidebar.selectbox('Select League', options=leagues, index=0)
if selected_league == leagues[0]:
    DBNAME = liga1.DBNAME
    EVENTNAMES = liga1.EVENTNAMES
    BOATS = liga1.BOATS
    FLIGHTS = liga1.FLIGHTS
    TEAMS = liga1.TEAMS
    BUCHSTABEN = liga1.BUCHSTABEN
    PAIRINGLIST = liga1.PAIRINGLIST
elif selected_league == leagues[1]:
    DBNAME = liga2.DBNAME
    EVENTNAMES = liga2.EVENTNAMES
    BOATS = liga2.BOATS
    FLIGHTS = liga2.FLIGHTS
    TEAMS = liga2.TEAMS
    BUCHSTABEN = liga2.BUCHSTABEN
    PAIRINGLIST = liga2.PAIRINGLIST


TEAMS.sort()

client = init_connection()
db = client[DBNAME]
collection_names = db.list_collection_names()
collection_names.sort()
EVENTS = len(collection_names)

selected_event = st.sidebar.selectbox('Select Event', options=EVENTNAMES, index=EVENTS - 1)

# Initialize session state for data storage
st.session_state.data = {event: {} for event in EVENTNAMES}


# Function to create pairing list and results (mimics the generate_pairing_list callback)
def initialize_pairing_result():
    for event in range(EVENTS):
        pairing_list, results = utils.create_pairing_list(event, PAIRINGLIST, FLIGHTS, TEAMS)
        st.session_state.data[EVENTNAMES[event]]['pairing_list'] = pairing_list.reset_index().to_dict(
            'split')
        st.session_state.data[EVENTNAMES[event]]['results'] = results.reset_index(drop=True).to_dict('split')


def initialize_from_pymongo():
    for event in range(0, EVENTS):
        pairing_list, results = utils.create_pairing_list(event, PAIRINGLIST, FLIGHTS, TEAMS)
        results = pd.DataFrame(list(db[collection_names[event]].find()))

        st.session_state.data[EVENTNAMES[event]]['pairing_list'] = pairing_list.reset_index().to_dict(
            'split')
        st.session_state.data[EVENTNAMES[event]]['results'] = results.reset_index(drop=True).to_dict('split')


def write_to_pymongo(df, event):
    collection = db[collection_names[event]]
    collection.delete_many({})
    collection.insert_many(df.to_dict("records"))


initialize_from_pymongo()

pairing_list_df = pd.DataFrame(st.session_state.data[selected_event]['pairing_list']['data'],
                               columns=st.session_state.data[selected_event]['pairing_list']['columns'], )
results_df = pd.DataFrame(st.session_state.data[selected_event]['results']['data'],
                          columns=st.session_state.data[selected_event]['results']['columns'], )
st.sidebar.download_button(label="Download Pairing List", data=pairing_list_df.to_csv(), file_name='pairing_list.csv',
                           mime='text/csv', )

# Display and download pairing list
if st.session_state.data[selected_event]['pairing_list'] is not None:
    st.sidebar.divider()
    st.sidebar.text('Results')
    results_df = pd.DataFrame(st.session_state.data[selected_event]['results']['data'],
                              columns=st.session_state.data[selected_event]['results']['columns'], )
    results_df.reset_index(drop=True, inplace=True)
    selected_race = st.sidebar.selectbox('Select Race', options=pairing_list_df['Race'], index=0)

    race_details = pairing_list_df[pairing_list_df['Race'] == selected_race]
    results = list()
    for b in range(1, BOATS + 1):
        team = race_details[f'Boat{b}'].values[0]
        result_options = [i for i in range(1, BOATS + 1)] + list(BUCHSTABEN.keys())
        flight = utils.get_flight(selected_race, TEAMS, BOATS)
        team_lookup = team.replace('(', ' (')
        current_result = results_df.loc[results_df['Teams'] == team_lookup, f'Flight {flight}']
        try:
            current_result = current_result.astype(int)
        except ValueError:
            pass
        try:
            index = result_options.index(current_result.values[0])
        except:
            index = len(result_options) - 1
        results.append(st.sidebar.selectbox(f'Boat {b} - ' + team, options=result_options, index=index, ))

    if st.sidebar.button('Update Results'):
        for b, r in zip(range(1, BOATS + 1), results):
            if r:
                team = race_details[f'Boat{b}'].values[0]
                team_lookup = team.replace('(', ' (')
                flight = utils.get_flight(selected_race, TEAMS, BOATS)
                if r == "No result":
                    r = np.nan
                results_df.loc[results_df['Teams'] == team_lookup, f'Flight {flight}'] = r

        st.session_state.data[selected_event]['results'] = results_df.reset_index(drop=True).to_dict('split')
        write_to_pymongo(results_df, EVENTNAMES.index(selected_event))

    st.sidebar.divider()
    st.sidebar.text('Scoring Penalties')
    team = st.sidebar.selectbox('Select Team', options=results_df['Teams'].sort_values(), index=0)
    scp = st.sidebar.number_input('Enter SCP', value=0)

    if st.sidebar.button('Update SCP'):
        filtered_df = results_df[results_df['Teams'] == team]
        row_index = filtered_df.index[0]
        if scp == 0:
            scp = np.nan
        results_df.loc[row_index, 'SCP'] = scp
        st.session_state.data[selected_event]['results'] = results_df.reset_index(drop=True).to_dict('split')

        write_to_pymongo(results_df, EVENTNAMES.index(selected_event))

# Display updated results
if st.session_state.data[selected_event]['results'] is not None:
    results_df = pd.DataFrame(st.session_state.data[selected_event]['results']['data'],
                              columns=st.session_state.data[selected_event]['results']['columns'], )
    results_df.reset_index(drop=True, inplace=True)

    results_df = utils.sort_results(results_df, FLIGHTS, BOATS, BUCHSTABEN)
    try:
        results_df.drop(columns=['Rank'], inplace=True)
    except KeyError:
        pass
    results_df.insert(0, 'Rank', range(1, results_df.shape[0] + 1))
    results_df.infer_objects()
    #results_df.fillna('-', inplace=True) # FIXME: FutureWarning
    try:
        results_df.drop(columns=['_id'], inplace=True)
    except KeyError:
        pass
    st.text('Results for {}'.format(selected_event))
    st.dataframe(results_df, height=750, use_container_width=True, hide_index=True, ) # FIXME: produces streamlit serialization error
    st.sidebar.divider()
    st.sidebar.download_button(label="Download Results", data=results_df.to_csv(), file_name='results.csv',
                               mime='text/csv')

# Overall ranking
st.text('Overall Results')
overall_results = pd.DataFrame({'Teams': TEAMS})
sum_columns = []
max_event = 0
for event in range(EVENTS):
    result_df = pd.DataFrame(st.session_state.data[EVENTNAMES[event]]['results']['data'],
                             columns=st.session_state.data[EVENTNAMES[event]]['results']['columns'], )
    result_df.reset_index(drop=True, inplace=True)
    result_df = utils.sort_results(result_df, FLIGHTS, BOATS, BUCHSTABEN)
    if result_df['Total'].min() == 0:
        continue
    result_df.insert(0, 'Rank', range(1, result_df.shape[0] + 1))
    result_df.sort_values(by='Teams', inplace=True)
    overall_results[EVENTNAMES[event]] = result_df['Rank'].values
    sum_columns.append(EVENTNAMES[event])
    if event > max_event:
        max_event = event

if max_event > 0:
    overall_results['Total'] = overall_results[sum_columns].sum(axis=1)
    overall_results.sort_values(by=['Total', EVENTNAMES[max_event]], inplace=True)
try:
    overall_results.drop(columns=['Rank'], inplace=True)
except KeyError:
    pass
overall_results.insert(0, 'Rank', range(1, overall_results.shape[0] + 1))
st.dataframe(overall_results, height=750, use_container_width=True, hide_index=True, )
