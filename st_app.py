import streamlit as st
import pandas as pd
import utils
from utils import BOATS, BUCHSTABEN

# Initialize session state for data storage
if 'data' not in st.session_state:
    st.session_state.data = {'pairing_list': None, 'results': None}

# Function to create pairing list and results (mimics the generate_pairing_list callback)
def create_pairing_list():
    pairing_list, results = utils.create_pairing_list()
    st.session_state.data['pairing_list'] = pairing_list.reset_index().to_dict('split')
    st.session_state.data['results'] = results.reset_index(drop=True).to_dict('split')

# UI for generating pairing list
if st.sidebar.button('Generate Pairing List'):
    create_pairing_list()

# Display and download pairing list
if st.session_state.data['pairing_list'] is not None:
    pairing_list_df = pd.DataFrame(st.session_state.data['pairing_list']['data'],
                                   columns=st.session_state.data['pairing_list']['columns'],
                                   index=st.session_state.data['pairing_list']['index'])
    results_df = pd.DataFrame(st.session_state.data['results']['data'],
                             columns=st.session_state.data['results']['columns'],)

    #st.dataframe(pairing_list_df)
    st.sidebar.download_button(label="Download Pairing List", data=pairing_list_df.to_csv(), file_name='pairing_list.csv', mime='text/csv')
    selected_race = st.sidebar.selectbox('Select Race', options=pairing_list_df['Race'], index=0)

    race_details = pairing_list_df[pairing_list_df['Race'] == selected_race]
    results = list()
    for b in range(1,utils.BOATS+1):
        team = race_details[f'Boat{b}'].values[0]
        results.append(st.sidebar.selectbox(f'Boat {b} - ' + team, options=[i for i in range(1, BOATS + 1)] + list(BUCHSTABEN.keys()), index=0,))


    if st.sidebar.button('Update Results'):
        for b, r in zip(range(1,utils.BOATS+1),results):
            if r:
                team = race_details[f'Boat{b}'].values[0]
                filtered_df = results_df[results_df['Teams'] == team]
                row_index = filtered_df.index[0]
                flight = utils.get_flight(selected_race)
                results_df.loc[row_index, f'Flight {flight}'] = r
        # Assuming results_df is modified and needs to be stored back in session_state
        results_df = utils.sort_results(results_df)
        st.session_state.data['results'] = results_df.reset_index(drop=True).to_dict('split')

# Display updated results
if st.session_state.data['results'] is not None:
    # if st.sidebar.button('Add SCP'):
    team = st.sidebar.selectbox('Select Team', options=results_df['Teams'].sort_values(), index=0)
    scp = st.sidebar.number_input('Enter SCP', value=0)
    if st.sidebar.button('Update SCP'):
        filtered_df = results_df[results_df['Teams'] == team]
        row_index = filtered_df.index[0]
        results_df.loc[row_index, 'SCP'] = scp
        results_df = utils.sort_results(results_df)
        st.session_state.data['results'] = results_df.reset_index(drop=True).to_dict('split')
    results_df = pd.DataFrame(st.session_state.data['results']['data'],
                              columns=st.session_state.data['results']['columns'],)
    results_df.reset_index(drop=True, inplace=True)
    try:
        results_df.drop(columns=['Rank'], inplace=True)
    except KeyError:
        pass
    results_df.insert(0, 'Rank', range(1, results_df.shape[0] + 1))
    results_df.fillna('-', inplace=True)
    st.dataframe(results_df, height=800, use_container_width=True, hide_index=True)
    st.sidebar.download_button(label="Download Results", data=results_df.to_csv(), file_name='results.csv', mime='text/csv')

# Additional functionality like modifying SCP, displaying results, etc., would follow a similar pattern of interaction and update.
