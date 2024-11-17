# src/frontend/streamlit_gui.py
# [Previous imports remain the same]

class StreamlitGUI:
    # [Previous methods remain the same until update_chart]
    
    def update_chart(self, data_handler, selected_errors, chart_type):
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
            
            # Display metrics in columns
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Total Errors", f"{total_errors:,}")
            with col2:
                st.metric("Most Common Error", max_error['Description'])
            with col3:
                st.metric("Highest Frequency", f"{max_error['Frequency']:,}")
            
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
            
            # Add axis swap button for bar chart
            if chart_type == "Bar Chart":
                if st.button("Swap Axes", use_container_width=True):
                    st.session_state.axes_swapped = not st.session_state.axes_swapped
            
            # Create and display the selected chart type
            if chart_type == "Bar Chart":
                fig = self.create_bar_chart(filtered_data)
            elif chart_type == "Pie Chart":
                fig = self.create_pie_chart(filtered_data)
            else:  # Treemap
                fig = self.create_treemap(filtered_data)
            
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
            
            # Display data table
            st.subheader("Detailed Data")
            st.dataframe(
                filtered_data,
                hide_index=True,
                use_container_width=True,
                column_config={
                    "Description": st.column_config.TextColumn("Description", width="medium"),
                    "Frequency": st.column_config.NumberColumn("Frequency", format="%d")
                }
            )

    # [Rest of the class implementation remains the same]