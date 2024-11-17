def render_table(self):
        if self.data_handler:
            df = self.error_summary.copy()
            # Apply search filter
            if st.session_state.search_query:
                df = df[df['Description'].str.contains(st.session_state.search_query, case=False, na=False)]
            # Add checkbox column
            df.insert(0, "Select", False)
            # Create a checkbox for select/deselect all
            select_all = st.checkbox("Select/Deselect All", key="select_all")
            if select_all:
                df["Select"] = True
                st.session_state.selected_errors = df["Description"].tolist()
            else:
                df["Select"] = df["Description"].isin(st.session_state.selected_errors)
            # Display the table
            table_height = int(st.sidebar.window_size.height * 0.8)
            errors = []
            for idx, row in df.iterrows():
                col1, col2, col3 = st.columns([1, 5, 2])
                with col1:
                    selected = st.checkbox("", key=f"checkbox_{idx}", value=row["Select"])
                    if selected:
                        errors.append(row["Description"])
                with col2:
                    st.write(row["Description"])
                with col3:
                    st.write(row["Frequency"])
            st.session_state.selected_errors = errors
        else:
            st.info("No data to display. Please load data.")