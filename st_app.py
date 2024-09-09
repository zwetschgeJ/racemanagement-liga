import numpy as np
import streamlit as st
import pandas as pd
from pymongo import MongoClient
import utils
from utils import BOATS, BUCHSTABEN, EVENTS

st.set_page_config(layout="wide")
st.title('Ergebnis-Manager')
st.sidebar.title('Options')

def init_connection():
    # TODO: use details from secrets.toml file
    uri = f"mongodb+srv://{st.secrets['mongo']['db_username']}:{st.secrets['mongo']['db_password']}@{st.secrets['mongo']['cluster_name']}.3rpqm.mongodb.net/dsbl?retryWrites=true&w=majority"
    return MongoClient(uri)

pymongo = True

if pymongo:
    client = init_connection()

    try:
        client.admin.command('ping')
        print("[INFO] Pinged your deployment. You successfully connected to MongoDB!")
    except Exception as e:
        print(e)

    db = client.dsbl
    collection_names = db.list_collection_names()
    collection_names.sort()
    EVENTS = len(collection_names)

# Initialize session state for data storage
if 'data' not in st.session_state:
    st.session_state.data = {f'Event {event}': {} for event in range(1, EVENTS + 1)}

# BOATS = st.sidebar.number_input('Number of Boats', value=BOATS, key='BOATS')
# EVENTS = st.sidebar.number_input('Number of Events', value=EVENTS, key='EVENTS')

st.sidebar.divider()


# Function to create pairing list and results (mimics the generate_pairing_list callback)
def initialize_pairing_result():
    for event in range(EVENTS):
        pairing_list, results = utils.create_pairing_list(event)
        st.session_state.data['Event {}'.format(event+1)]['pairing_list'] = pairing_list.reset_index().to_dict('split')
        st.session_state.data['Event {}'.format(event+1)]['results'] = results.reset_index(drop=True).to_dict('split')


def initialize_from_pymongo():
    for event in range(0, len(collection_names)):
        pairing_list, results = utils.create_pairing_list(event)
        results = pd.DataFrame(db[collection_names[event]].find())
        results.drop(columns=['_id'], inplace=True)

        st.session_state.data['Event {}'.format(event+1)]['pairing_list'] = pairing_list.reset_index().to_dict('split')
        st.session_state.data['Event {}'.format(event+1)]['results'] = results.reset_index(drop=True).to_dict('split')


def write_to_pymongo():
    for event in range(len(collection_names)):
        df = pd.DataFrame(st.session_state.data[selected_event]['results']['data'],
                              columns=st.session_state.data[selected_event]['results']['columns'],)
        print(df.head())
        collection = db[collection_names[event]]
        collection.delete_many({})

        data_dict = df.to_dict("records")
        collection.insert_many(data_dict)



if st.session_state.data['Event 1'] == {}:
    if pymongo:
        initialize_from_pymongo()
    else:
        initialize_pairing_result()


selected_event = st.sidebar.selectbox('Select Event', options=[f'Event {i}' for i in range(1, EVENTS + 1)], index=0)

pairing_list_df = pd.DataFrame(st.session_state.data[selected_event]['pairing_list']['data'],
                               columns=st.session_state.data[selected_event]['pairing_list']['columns'], )
results_df = pd.DataFrame(st.session_state.data[selected_event]['results']['data'],
                          columns=st.session_state.data[selected_event]['results']['columns'], )
st.sidebar.download_button(label="Download Pairing List", data=pairing_list_df.to_csv(), file_name='pairing_list.csv', mime='text/csv', )

if st.sidebar.button('Upload Results'):
    uploaded_file = st.sidebar.file_uploader("Choose a file")
    if uploaded_file is not None:
        uploaded_results_df = pd.read_csv(uploaded_file)
        st.text('Uploaded Results')
        st.dataframe(uploaded_results_df, height=750, use_container_width=True, hide_index=True,)
        st.session_state.data[selected_event]['results'] = uploaded_results_df.reset_index(drop=True).to_dict('split')

# Display and download pairing list
if st.session_state.data[selected_event]['pairing_list'] is not None:
    results_df = pd.DataFrame(st.session_state.data[selected_event]['results']['data'],
                              columns=st.session_state.data[selected_event]['results']['columns'], )
    results_df.reset_index(drop=True, inplace=True)
    selected_race = st.sidebar.selectbox('Select Race', options=pairing_list_df['Race'], index=0)

    # TODO: get race details based on Event information
    race_details = pairing_list_df[pairing_list_df['Race'] == selected_race]
    results = list()
    for b in range(1,utils.BOATS+1):
        team = race_details[f'Boat{b}'].values[0]

        # TODO: initialize entry with value from results
        result_options = [i for i in range(1, BOATS + 1)] + list(BUCHSTABEN.keys())
        flight = utils.get_flight(selected_race)
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
        results.append(st.sidebar.selectbox(f'Boat {b} - ' + team, options=result_options, index=index,))


    if st.sidebar.button('Update Results'):
        for b, r in zip(range(1,utils.BOATS+1),results):
            if r:
                team = race_details[f'Boat{b}'].values[0]
                flight = utils.get_flight(selected_race)
                results_df.loc[results_df['Teams'] == team, f'Flight {flight}'] = r

        st.session_state.data[selected_event]['results'] = results_df.reset_index(drop=True).to_dict('split')

    team = st.sidebar.selectbox('Select Team', options=results_df['Teams'].sort_values(), index=0)
    scp = st.sidebar.number_input('Enter SCP', value=0)
    if st.sidebar.button('Update SCP'):
        filtered_df = results_df[results_df['Teams'] == team]
        row_index = filtered_df.index[0]
        if scp == 0:
            scp = np.nan
        results_df.loc[row_index, 'SCP'] = scp
        st.session_state.data[selected_event]['results'] = results_df.reset_index(drop=True).to_dict('split')

# Display updated results
if st.session_state.data[selected_event]['results'] is not None:
    results_df = pd.DataFrame(st.session_state.data[selected_event]['results']['data'],
                              columns=st.session_state.data[selected_event]['results']['columns'],)
    results_df.reset_index(drop=True, inplace=True)

    results_df = utils.sort_results(results_df)
    try:
        results_df.drop(columns=['Rank'], inplace=True)
    except KeyError:
        pass
    results_df.insert(0, 'Rank', range(1, results_df.shape[0] + 1))
    results_df.fillna('-', inplace=True)
    st.text('Results for {}'.format(selected_event))
    st.dataframe(results_df, height=750, use_container_width=True, hide_index=True,)
    st.sidebar.download_button(label="Download Results", data=results_df.to_csv(), file_name='results.csv', mime='text/csv')

# TODO: save results to MongoDB
write_to_pymongo()


#Overall ranking
st.text('Overall Results')
overall_results = pd.DataFrame({'Teams': utils.TEAMS})
for event in range(1, EVENTS + 1):
    result_df = pd.DataFrame(st.session_state.data[f'Event {event}']['results']['data'],
                              columns=st.session_state.data[f'Event {event}']['results']['columns'],)
    result_df.reset_index(drop=True, inplace=True)
    result_df = utils.sort_results(result_df)
    result_df.insert(0, 'Rank', range(1, result_df.shape[0] + 1))
    result_df.sort_values(by='Teams', inplace=True)
    overall_results['Event {}'.format(event)] = result_df['Rank'].values

sum_columns = ['Event {}'.format(event) for event in range(1, EVENTS + 1)]
overall_results['Total'] = overall_results[sum_columns].sum(axis=1)
overall_results.sort_values(by=['Total','Event {}'.format(EVENTS)], inplace=True)
try:
    overall_results.drop(columns=['Rank'], inplace=True)
except KeyError:
    pass
overall_results.insert(0, 'Rank', range(1, overall_results.shape[0] + 1))
st.dataframe(overall_results, height=750, use_container_width=True, hide_index=True,)

