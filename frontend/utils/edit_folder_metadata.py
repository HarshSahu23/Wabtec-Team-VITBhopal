from datetime import datetime
import streamlit as st

def edit_folder_metadata():
    # Settings to edit and save folder metadata moved from settings panel to here
    # Add inputs for Date, Depot Name, and Coach Name
    col1, col2, col3 = st.columns(3)
    with col1:
        # Date input
        date_value = None
        if 'folder_date' not in st.session_state:
            st.session_state.folder_date = datetime.now().strftime("%d-%m-%Y")
        else:
            try:
                date_value = datetime.strptime(st.session_state.folder_date, "%d-%m-%Y")
            except:
                pass
        new_date = st.date_input(
            "Date",
            value=date_value or datetime.now(),
            format="DD-MM-YYYY",
        )
        st.session_state.folder_date = new_date.strftime("%d-%m-%Y")
    with col2:
        # Depot Name input
        new_depot = st.text_input(
            "Depot Name",
            value=st.session_state.get('depot_name', ""),
        )
        st.session_state.depot_name = new_depot
    with col3:
        # Coach Name input
        new_coach = st.text_input(
            "Coach Name",
            value=st.session_state.get('coach_name', ""),
        )
        st.session_state.coach_name = new_coach