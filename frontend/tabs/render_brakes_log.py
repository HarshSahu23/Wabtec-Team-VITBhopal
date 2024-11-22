import streamlit as st

from frontend.compute.update_chart import update_chart
from frontend.utils.render_section_header import render_section_header
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
            # Inject column CSS styles
            st.subheader("Error Selection")
            
            # Search filter
            search_term = st.text_input("🔍 Search Errors", "")
            
            # Error checkboxes with search filter in a tabular form
            st.markdown("### Select Errors")
            
            error_data = st.session_state.data_handler.ecl_freq_summary
            filtered_data = error_data[error_data['Description'].str.contains(search_term, case=False)]
            
            # Table headings
            col1_1, col1_2, col1_3 = st.columns([0.15, 0.6,0.25])
            
            with col1_1:
                # st.checkbox("", key="select_all_errors")
                select_all = st.checkbox("", key="select_all_errors")
            if select_all:
                st.session_state.selected_errors = set(filtered_data['Description'])
            else:
                st.session_state.selected_errors.clear()
            with col1_2:
                st.markdown("**Description**")
            with col1_3:
                st.markdown("**Frequency**")
            
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
    
    # elif not uploaded_files:
    #     st.info("👆 Please upload CSV files to begin analysis")
