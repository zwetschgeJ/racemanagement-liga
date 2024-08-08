import streamlit as st

from src.utils_app import initialize_states, calculate_place_flow, create_flow_plot

st.set_page_config(layout="wide")

initialize_states()

tab_event1, tab_event2, tab_event3, tab_overall = st.tabs(["Event 1", "Event 2", "Event 3", "Saison"])


with tab_event1:
    st.write("### Ergebnisse Event 1 Kiel")

    st.dataframe(
        st.session_state.data,
        width=1300,
        height=670
    )

    results_df = calculate_place_flow(st.session_state.data)

    plot_flow = create_flow_plot(results_df)

    st.write("### Flow")
    st.plotly_chart(plot_flow)