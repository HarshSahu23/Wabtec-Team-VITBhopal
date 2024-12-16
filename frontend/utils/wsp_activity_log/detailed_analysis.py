import streamlit as st
import pandas as pd
def detailed_analysis():
    st.subheader("Detailed Event Log")
    
    filtered_dmp = st.session_state.data_handler.filtered_dmp
    
    if not filtered_dmp.empty:
        # # Add search functionality
        # search = st.text_input("Search events", "")
        
        # # Filter based on search
        # if search:
        #     mask = filtered_dmp.astype(str).apply(lambda x: x.str.contains(search, case=False)).any(axis=1)
        #     filtered_dmp = filtered_dmp[mask]
        
        # Add column selector
        selected_columns = st.multiselect(
            "Select columns to display",
            options=filtered_dmp.columns.tolist(),
            default=filtered_dmp.columns.tolist()
        )
        
        # Show filtered data
        st.dataframe(filtered_dmp[selected_columns], height=400)
        
        # Add download button
        csv = filtered_dmp.to_csv(index=False)
        st.download_button(
            label="Download filtered data as CSV",
            data=csv,
            file_name="filtered_dump_log.csv",
            mime="text/csv"
        )
        
        # Add summary statistics for filtered data
        st.subheader("Filtered Data Statistics")
        
        col3, col4 = st.columns(2)
        
        with col3:
            st.write("Numerical Columns Statistics")
            st.dataframe(filtered_dmp.describe())
            
        with col4:
            st.write("Non-Zero Events Count")
            non_zero_counts = (filtered_dmp != 0).sum()
            st.dataframe(pd.DataFrame({
                'Column': non_zero_counts.index,
                'Non-Zero Count': non_zero_counts.values
            }))
            
    else:
        st.info("No filtered data available")