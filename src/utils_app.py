import pandas as pd
import numpy as np
import streamlit as st
import plotly.graph_objects as go

from src.utils_sorting import sort_results, create_pairing_list

# Load confing
from config import *


def get_data_excel() -> None:
    df_ = pd.read_excel("./data/liga3.xlsx")

    df = pd.DataFrame(index=range(len(TEAMS)), columns=race_columns)
    df.index = TEAMS

    for _, row in df_.iterrows():
        values = row.values

        for index, _ in df.iterrows():

            if values[0] == index:
                df.loc[index] = values[1:]

    print("[INFO] Data loaded from Excel.")
    return df


@st.cache_data(ttl=REFRESH_TIME)
def get_data_google(link_id: str, stupid_formatting: bool = False) -> pd.DataFrame:
    if stupid_formatting:
        df = pd.read_csv(
            'https://docs.google.com/spreadsheets/d/' +
            link_id  +
            '/export?gid=0&format=csv',
            skiprows=2,
        )
        df.drop(["Unnamed: 0", "Overall"], axis=1, inplace=True)

    else:
        df = pd.read_csv(
            'https://docs.google.com/spreadsheets/d/' +
            link_id  +
            '/export?gid=0&format=csv',
            skiprows=1,
        )
        df.drop(["1.", "Overall"], axis=1, inplace=True)
    
    columns = ["Teams", "SCP"]
    columns.extend([f'Flight {i}' for i in range(1, FLIGHTS + 1)])

    df.columns = columns

    print("[INFO] Data loaded from Google Docs.")
    return df


def initialize_states() -> None:
   df = get_data_google(link_id=link_event_01, stupid_formatting=True)
   st.session_state["data_event_01"] = sort_results(result_df=df)

   df = get_data_google(link_id=link_event_02)
   st.session_state["data_event_02"] = sort_results(result_df=df)
   
   df = get_data_google(link_id=link_event_03)
   st.session_state["data_event_03"] = sort_results(result_df=df)
   
   df = get_data_google(link_id=link_test)
   st.session_state["data_event_04"] = sort_results(result_df=df)

def calculate_place_flow(result_df: pd.DataFrame) -> pd.DataFrame:
    df_sorted_index = pd.DataFrame()

    for i, name in enumerate(race_columns):
        
        df_buffer = result_df.copy()
        df_buffer.iloc[:, (i+3):] = 0 #np.nan

        indices = sort_results(df_buffer)["Teams"].values

        df_sorted_index[name] = indices

    result_df_ = pd.DataFrame(index=range(len(TEAMS)), columns=race_columns)
    result_df_.index = TEAMS

    for club in TEAMS:
        res = []
        for col in df_sorted_index.columns:
                        
            s = (df_sorted_index[col] == club)

            place = s[s].index.values[0] + 1

            res.append(place)
        
        result_df_.loc[club] = res
        
    return result_df_


def create_flow_plot(result_df_: pd.DataFrame):
    # Create a figure
    fig = go.Figure()

    # Plot each row of result_df_ as a separate trace
    for index, row in result_df_.iterrows():
        fig.add_trace(go.Scatter(
            x=row.index,
            y=row.values,
            mode='lines',
            name=f'{index}',
            # hovertemplate=f'Index: {row.index}<br>Value: %{y:.2f}<extra></extra>'
        ))

    # Update the layout of the figure
    fig.update_layout(
        height=800,
        width=1200,
        yaxis_title='Platz',
        yaxis=dict(autorange='reversed'),  # Reverse y-axis
        #xaxis_tickangle=-90,  # Rotate x-axis labels
        xaxis_title_font=dict(size=14),
        yaxis_title_font=dict(size=14),
    )

    # Show the plot
    return fig


def compute_overall():
    overall_results = pd.DataFrame({'Teams': TEAMS})

    for event in range(1, EVENTS+1):
        result_df = st.session_state["data_event_0" + str(event)]
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

    st.dataframe(
        overall_results,
        height=665,
        use_container_width=True,
        hide_index=True,
    )


def highlight_fleet(_, team_in_fleet: list[bool], color: str):
    return ['color:'+color + '; font-weight:bold' if team else '' for team in team_in_fleet]


def add_pairinglist_font(df: pd.DataFrame, event: int) -> pd.DataFrame:

    pairing_list, _ = create_pairing_list(event=event)
    pairing_list = pairing_list.drop(["flight", "Race"], axis=1)

    pairing_list = pairing_list.replace("BYC(BA)", "BYC (BA)")
    pairing_list = pairing_list.replace("BYC(BE)", "BYC (BE)")

    pairing_list = pairing_list.replace("KYC(SH)", "KYC (SH)")
    pairing_list = pairing_list.replace("KYC(BW)", "KYC (BW)")
    
    teams = df["Teams"].values

    flight = 1
    style_df = df.style

    colors = ["red", "blue", "green"]
    # colors = ["#FFCCCB", "#ADD8E6", "#90EE90"]

    for i in range(pairing_list.shape[0]):
        team_in_fleet = np.isin(teams, pairing_list.iloc[i, :].values)
        
        column_name = 'Flight ' + str(flight)
        
        color = colors[i % len(colors)]
        
        style_df = style_df.apply(highlight_fleet, subset=[column_name], team_in_fleet=team_in_fleet, color=color)

        if (i + 1) % 3 == 0:
            flight += 1
    
    return style_df


def display_event(title: str, data_event: str) -> None:
    st.write("### Ergebnisse " + title)

    data = st.session_state[data_event].astype(str)
    data = data.replace("nan","0")

    # Replace 0 with "" in columns that only contain 0
    data_to_show = data.copy()
    
    for column in race_columns:
        try:
            if data_to_show[column].astype(float).sum() == 0:
               data_to_show[column] = data_to_show[column].str.replace("0", "")  
        except:
            pass

    if DISPLAY_COLORCODING:
        st.dataframe(
            add_pairinglist_font(df=data_to_show,event=int(data_event[-1])),
            height=665,
            use_container_width=True,
            hide_index=True
        )
    else:
        st.dataframe(
            data_to_show,
            height=665,
            use_container_width=True,
            hide_index=True
        )

    df_ = calculate_place_flow(data)

    plot_flow = create_flow_plot(df_)

    st.write("### Flow")
    st.plotly_chart(plot_flow)