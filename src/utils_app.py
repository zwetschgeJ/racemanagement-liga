import pandas as pd
import streamlit as st
# import matplotlib.pyplot as plt
import plotly.graph_objects as go
import numpy as np

from src.utils_sorting import sort_results

BOATS = 6
FLIGHTS = 16
EVENTS = 2
TEAMS = ['ASVW', 'BYC (BA)', 'BYC (BE)', 'BYCÜ', 'DYC', 'FSC', 'JSC', 'KYC (BW)', 'KYC (SH)', 'MSC', 'MYC', 'NRV', 'RSN', 'SMCÜ', 'SV03', 'SVI', 'VSaW', 'WYC']

BUCHSTABEN = {'OCS': BOATS+1,
              'DSQ': BOATS+1,
              'DNF': BOATS+1,
              'DNC': BOATS+1,}

max_race_columns = 16
race_columns = ['Flight {}'.format(i) for i in range(1,max_race_columns+1)]


def get_data() -> None:
    df = pd.read_excel("./data/liga3.xlsx")

    result_df = pd.DataFrame(index=range(len(TEAMS)), columns=race_columns)
    result_df.index = TEAMS

    for _, row in df.iterrows():
        values = row.values

        for index, _ in result_df.iterrows():

            if values[0] == index:
                result_df.loc[index] = values[1:]

    return sort_results(result_df)

def initialize_states() -> None:
    if "data" not in st.session_state:
        st.session_state["data"] = get_data()


def calculate_place_flow(result_df: pd.DataFrame) -> pd.DataFrame:
    df_sorted = pd.DataFrame()

    for i, name in enumerate(race_columns):
        
        df_buffer = result_df.copy()
        df_buffer.iloc[:, (i+1):] = np.nan

        indices = sort_results(df_buffer).index
        df_sorted[name] = indices

    result_df_ = pd.DataFrame(index=range(len(TEAMS)), columns=race_columns)
    result_df_.index = TEAMS

    for club in TEAMS:
        res = []
        for col in df_sorted.columns:

            s = df_sorted[col] == club
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


def create_cumulative_points(result_df_: pd.DataFrame):
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
        #yaxis=dict(autorange='reversed'),  # Reverse y-axis
        #xaxis_tickangle=-90,  # Rotate x-axis labels
        xaxis_title_font=dict(size=14),
        yaxis_title_font=dict(size=14),
    )

    # Show the plot
    return fig