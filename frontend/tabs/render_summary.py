import streamlit as st
import plotly.graph_objects as go
import random
import pandas as pd  # Added import
from datetime import datetime

from backend.data_handler import DataHandler
from frontend.utils.edit_folder_metadata import edit_folder_metadata
from frontend.utils.render_section_header import render_section_header
from frontend.compute.summary_viz import create_axle_grouped_bar_chart, create_clubbed_horizontal_bar_chart, create_simple_bar_chart

def render_chart(df, table_name, axle_mode, color_seed):
    """Helper function to render chart based on mode and swap_axes state."""
    swap_axes = st.session_state.swap_axes  # Get swap_axes state
    if len(df.columns) == 2:
        fig = create_simple_bar_chart(df, table_name, color_seed, swap_axes)
    else:
        fig = (
            create_clubbed_horizontal_bar_chart(df, table_name, color_seed, swap_axes)
            if not axle_mode
            else create_axle_grouped_bar_chart(df, table_name, color_seed, swap_axes)
        )
    st.plotly_chart(fig, key=f"{table_name}_{axle_mode}_{swap_axes}", use_container_width=True)

def add_total_occurrences(df):
    """Add total occurrences row with two columns."""
    total_sum = df.select_dtypes(include=['int64', 'float64']).sum().sum()
    # Create total row with empty strings for all columns except first two
    total_row = {col: '' for col in df.columns}
    total_row[df.columns[0]] = 'Total Occurrences'
    total_row[df.columns[1]] = total_sum
    return pd.concat([df, pd.DataFrame([total_row])], ignore_index=True)

def render_summary():
    render_section_header(
        "System Summary",
        "Overview of all the csv files analysed from the folders",
        "📜"
    )
    
    edit_folder_metadata()

    # Initialize visibility states
    if 'show_tables' not in st.session_state:
        st.session_state.show_tables = True
    if 'show_charts' not in st.session_state:
        st.session_state.show_charts = True
    if 'axle_mode' not in st.session_state:
        st.session_state.axle_mode = False
    if 'swap_axes' not in st.session_state:
        st.session_state.swap_axes = False  # Initialize swap_axes state

    # Toolbar row
    col1, col2, col3, col4, col5 = st.columns([1, 1, 1, 1, 1])
    # with col1:
    #     if st.button("Toggle Tables 📋", help="Show/Hide all tables", use_container_width=True):
    #         st.session_state.show_tables = not st.session_state.show_tables
    # with col2:
    #     if st.button("Toggle Charts 📊", help="Show/Hide all charts", use_container_width=True):
    #         st.session_state.show_charts = not st.session_state.show_charts
    

    try:
        if not st.session_state.data_handler.tables:
            st.warning("No tables found. Please upload a folder first to analyze it.")
        else:
            # Create two expanders
            with st.expander("View Tables 📋", expanded=True): #expanded by default
                tables_list = list(st.session_state.data_handler.tables.items())
                for i in range(0, len(tables_list), 2):
                    # Create a new row for every 2 tables
                    cols = st.columns([1, 0.1, 1])  # Middle column for spacing
                    
                    # First table in the row
                    table_name, df = tables_list[i]
                    with cols[0]:
                        st.markdown(f"#### {table_name}")
                        df_with_total = add_total_occurrences(df)
                        st.dataframe(df_with_total, use_container_width=True, hide_index=True)
                    
                    # Add second table if it exists
                    if i + 1 < len(tables_list):
                        table_name, df = tables_list[i + 1]
                        with cols[2]:
                            st.markdown(f"#### {table_name}")
                            df_with_total = add_total_occurrences(df)
                            # Modify the last row to keep only the first two columns
                            st.dataframe(df_with_total, use_container_width=True, hide_index=True)

            with st.expander("View Charts 📊", expanded=False):
                col1, col2, col3, col4, col5 = st.columns([1, 2, 1, 1, 1])

                with col1:
                    if st.button("SWAP AXES ⚠️", help="WARNING: This will dramatically change chart visualization. Use only if you know what you're doing!", use_container_width=True):
                        st.session_state.swap_axes = not st.session_state.swap_axes

                with col4:
                    if 'axle_mode_dict' not in st.session_state:
                        st.session_state.axle_mode_dict = {}
                    if st.button("Toggle Graph Mode 🔁", help="Switch between Error/Axle grouping", use_container_width=True):
                        for table_name, df in st.session_state.data_handler.tables.items():
                            if len(df.columns) >= 3:
                                st.session_state.axle_mode_dict[table_name] = not st.session_state.axle_mode_dict.get(table_name, False)
                            else:
                                st.session_state.axle_mode_dict[table_name] = False

                with col5:
                    def update_color_seed():
                        st.session_state.color_seed = random.randint(1, 100)
                    if 'color_seed' not in st.session_state:
                        st.session_state.color_seed = random.randint(1, 100)
                    st.button("Change Color Palette 🎨", help="Randomize chart colors", on_click=update_color_seed, use_container_width=True)

                if st.session_state.swap_axes:
                    st.warning("⚠️ Charts axes are now swapped! This may make some visualizations harder to read.")


                charts_list = list(st.session_state.data_handler.tables.items())
                for i in range(0, len(charts_list), 2):
                    # Create a new row for every 2 charts
                    cols = st.columns([1, 0.1, 1])  # Middle column for spacing
                    
                    # First chart in the row
                    table_name, df = charts_list[i]
                    with cols[0]:
                        st.markdown(f"#### {table_name}")
                        axle_mode = st.session_state.axle_mode_dict.get(table_name, False)
                        render_chart(df, table_name, axle_mode, st.session_state.color_seed)
                    
                    # Add second chart if it exists
                    if i + 1 < len(charts_list):
                        table_name, df = charts_list[i + 1]
                        with cols[2]:
                            st.markdown(f"#### {table_name}")
                            axle_mode = st.session_state.axle_mode_dict.get(table_name, False)
                            render_chart(df, table_name, axle_mode, st.session_state.color_seed)

    except AttributeError:
        st.warning("Please upload a folder first to analyze it.")
