import streamlit as st
from frontend.compute.update_chart import update_chart
from frontend.utils.render_section_header import render_section_header
from backend.data_processors.ecl_error_grouper import ECLErrorGrouper

def render_brakes_log():
    # Title and description
    render_section_header(
        "Brakes Log Analysis",
        "Analyze and visualize error frequencies from your brake system logs.",
        "🔍"
    )

    # Main content
    if st.session_state.data_handler and len(st.session_state.data_handler.ecl_freq_summary) > 0:
        
        col1, col2 = st.columns([1, 3])
        with col1:
            
            st.subheader("Error Selection")    
            error_view_mode = st.toggle(
                    "Group Errors",
                    value=False,
                    help="Toggle between individual errors and error groups",
                )
            error_view_mode = "Error Groups" if error_view_mode else "Individual Errors"
            # Search filter
            search_term = st.text_input("🔍 Search", "")
            
            # Reset selected errors when switching modes
            if 'last_view_mode' not in st.session_state or st.session_state.last_view_mode != error_view_mode:
                st.session_state.selected_errors = set()
                st.session_state.last_view_mode = error_view_mode
            
            # Table headings
            col1_1, col1_2, col1_3 = st.columns([0.15, 0.6, 0.25])
            
            with col1_1:
                select_all = st.checkbox("", key="select_all_items")
            
            with col1_2:
                st.markdown("**Description**")
            with col1_3:
                st.markdown("**Frequency**")
            
            # Handling Individual Errors
            if error_view_mode == "Individual Errors":
                error_data = st.session_state.data_handler.ecl_freq_summary
                filtered_data = error_data[error_data['Description'].str.contains(search_term, case=False)]
                
                if select_all:
                    st.session_state.selected_errors = set(filtered_data['Description'])
                else:
                    st.session_state.selected_errors.clear()
                
                # Display errors in a table format
                for _, row in filtered_data.iterrows():
                    error_desc = row['Description']
                    frequency = row['Frequency']
                    col1_1, col1_2, col1_3 = st.columns([0.1, 0.7, 0.2])
                    with col1_1:
                        if st.checkbox(
                            "", key=f"cb_{error_desc}",
                            value=error_desc in st.session_state.selected_errors
                        ):
                            st.session_state.selected_errors.add(error_desc)
                        else:
                            st.session_state.selected_errors.discard(error_desc)
                    with col1_2:
                        st.write(error_desc)
                    with col1_3:
                        st.write(frequency)
            
            # Handling Error Groups
            else:
                # Get error groups from the grouped_ecl dataframe
                groups_data = st.session_state.data_handler.grouped_ecl['Error Group'].value_counts()
                
                # Initialize selected_error_groups if not exists
                if 'selected_error_groups' not in st.session_state:
                    st.session_state.selected_error_groups = set()
                
                # Prepare error group data
                group_summary = []
                for group, count in groups_data.items():
                    group_errors = st.session_state.data_handler.grouped_ecl[
                        st.session_state.data_handler.grouped_ecl['Error Group'] == group
                    ]['Description'].unique()
                    group_summary.append({
                        'Group': group, 
                        'Frequency': count, 
                        'Errors': group_errors
                    })
                
                if select_all:
                    # Select all groups and their errors
                    st.session_state.selected_error_groups = set(group['Group'] for group in group_summary)
                    st.session_state.selected_errors = set(
                        error for group in group_summary 
                        for error in group['Errors']
                    )
                else:
                    st.session_state.selected_error_groups.clear()
                    st.session_state.selected_errors.clear()
                
                # Display error groups in a table format
                for group_info in group_summary:
                    group = group_info['Group']
                    frequency = group_info['Frequency']
                    col1_1, col1_2, col1_3 = st.columns([0.1, 0.7, 0.2])
                    
                    with col1_1:
                        # Check if group is selected
                        is_selected = group in st.session_state.selected_error_groups
                        if st.checkbox(
                            "", key=f"cb_{group}",
                            value=is_selected
                        ):
                            # Add group and its errors
                            st.session_state.selected_error_groups.add(group)
                            st.session_state.selected_errors.update(group_info['Errors'])
                        else:
                            # Remove group and its errors
                            st.session_state.selected_error_groups.discard(group)
                            st.session_state.selected_errors.difference_update(group_info['Errors'])
                    
                    with col1_2:
                        st.write(group)
                        # Optional: Show tooltips with errors in the group
                        with st.expander("View Errors"):
                            for error in group_info['Errors']:
                                st.write(error)
                    
                    with col1_3:
                        st.write(frequency)

        with col2:
            st.subheader("Visualization")
            chart_type = st.radio(
                "Select Chart Type",
                ["Bar Chart", "Pie Chart", "Treemap"],
                horizontal=True
            )
            update_chart(
                st.session_state.data_handler,
                st.session_state.selected_errors,
                chart_type
            )
    
    else:
        st.info("👆 Please upload CSV files to begin analysis")