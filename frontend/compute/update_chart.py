import streamlit as st

from frontend.utils.css_utils import get_metrics_css
from frontend.compute.visualizations import create_bar_chart, create_pie_chart, create_treemap, get_color
def update_chart(data_handler, selected_errors, chart_type):
        if not data_handler or len(selected_errors) == 0:
            st.warning("No data to display. Please select errors to visualize.")
            return
        
        filtered_data = data_handler.ecl_freq_summary[
            data_handler.ecl_freq_summary['Description'].isin(selected_errors)
        ]
        
        if not filtered_data.empty:
            # Create metrics for quick insights
            total_errors = filtered_data['Frequency'].sum()
            max_error = filtered_data.loc[filtered_data['Frequency'].idxmax()]
            
            # Inject metrics CSS
            st.markdown(get_metrics_css(), unsafe_allow_html=True)
            
            # Display metrics in columns
            metric_cols = st.columns(3)
            
            with metric_cols[0]:
                st.markdown(f"""
                    <div class="metric-container">
                        <div class="metric-title">Total Errors</div>
                        <div class="metric-value-large">{total_errors:,}</div>
                    </div>
                """, unsafe_allow_html=True)
            
            with metric_cols[1]:
                st.markdown(f"""
                    <div class="metric-container">
                        <div class="metric-title">Most Common Error</div>
                        <div class="metric-value-medium">{max_error['Description']}</div>
                    </div>
                """, unsafe_allow_html=True)
            
            with metric_cols[2]:
                st.markdown(f"""
                    <div class="metric-container">
                        <div class="metric-title">Highest Frequency</div>
                        <div class="metric-value-large">{max_error['Frequency']:,}</div>
                    </div>
                """, unsafe_allow_html=True)
            
            # Close the container card
            st.markdown("</div>", unsafe_allow_html=True)
            # Add sorting options
            sort_col1, sort_col2 = st.columns(2)
            with sort_col1:
                sort_by = st.selectbox(
                    "Sort by",
                    ["Description", "Frequency"],
                    key="sort_by_select"
                )
            with sort_col2:
                sort_order = st.selectbox(
                    "Sort order",
                    ["Ascending", "Descending"],
                    key="sort_order_select"
                )
            
            # Apply sorting based on user selection
            sort_ascending = sort_order == "Ascending"
            filtered_data = filtered_data.sort_values(
                by=sort_by,
                ascending=sort_ascending
            )
            
            # Add button columns for chart controls
            btn_col1, btn_col2 = st.columns(2)
            
            # Add axis swap button for bar chart
            if chart_type == "Bar Chart":
                with btn_col1:
                    if st.button("Swap Axes", use_container_width=True):
                        st.session_state.axes_swapped = not st.session_state.axes_swapped
                
                with btn_col2:
                    if st.button(
                        "Change Graph Annotation",
                        help="Changes the annotated value over each element in the graph from percent to respective quantity",
                        use_container_width=True
                    ):
                        st.session_state.show_percentage = not st.session_state.show_percentage
            
            # Create and display the selected chart type
            if chart_type == "Bar Chart":
                fig = create_bar_chart(filtered_data, get_color, st.session_state)
            elif chart_type == "Pie Chart":
                fig = create_pie_chart(filtered_data, get_color)
            else:  # Treemap
                fig = create_treemap(filtered_data)
            
            # Display the chart with custom config
            st.plotly_chart(
                fig,
                use_container_width=True,
                config={
                    'displayModeBar': True,
                    'displaylogo': False,
                    'modeBarButtonsToRemove': ['lasso2d', 'select2d'],
                    'toImageButtonOptions': {
                        'format': 'png',
                        'filename': 'error_analysis',
                        'height': 600,
                        'width': 1200,
                        'scale': 2
                    }
                }
            )
            
            # Remove or comment out the existing 'Detailed Data' section
            # st.subheader("Detailed Data")
            # st.dataframe(...)

            # Add the new 'Get Detailed Data' section
            st.subheader("Get Detailed Data")
            col1, col2 = st.columns([1, 3])
            with col1:
                if st.session_state.selected_errors:
                    # Convert set to list and sort for consistent display
                    all_selected_errors = sorted(list(st.session_state.selected_errors))
                    selected_error = st.selectbox(
                        "🔍 Search/Select Error",
                        options=all_selected_errors,
                        help="Type to search or select an error to view details"
                    )
                    detailed_data = st.session_state.data_handler.ecl[
                        st.session_state.data_handler.ecl['Description'] == selected_error
                    ]
                else:
                    st.write("No errors selected.")
            
            with col2:
                if st.session_state.selected_errors and not detailed_data.empty:
                    # Get all available column names (titles) from the original data
                    available_tags = st.session_state.data_handler.ecl.columns.tolist()
                    
                    # Filter out any previously selected tags that are no longer valid
                    valid_selected_tags = list(
                        tag for tag in st.session_state.selected_tags 
                        if tag in available_tags
                    )
                    
                    # Multi-select widget for titles/columns
                    new_tag = st.multiselect(
                        "🏷️ Search/Select Data Fields",
                        options=available_tags,
                        default=valid_selected_tags if valid_selected_tags else None,
                        help="Select which data fields to display"
                    )
                    st.session_state.selected_tags = set(new_tag)
                    
            # Render detailed data below the columns
            if st.session_state.selected_errors and not detailed_data.empty:
                if st.session_state.selected_tags:
                    # Filter columns instead of index
                    filtered_data = detailed_data[list(st.session_state.selected_tags)]
                    st.table(filtered_data)
                else:
                    st.info("Please select data fields to display")
            elif st.session_state.selected_errors:
                st.write("No details available for this error.")
    