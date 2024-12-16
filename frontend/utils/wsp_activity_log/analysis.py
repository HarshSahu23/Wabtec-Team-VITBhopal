import streamlit as st
import pandas as pd
def analysis():
    st.subheader("FILL ↔ VENT Analysis", divider="gray")
    fill_vent_events = st.session_state.data_handler.fill_vent_events

    if not fill_vent_events:
        st.warning("No FILL/VENT events to display.")
    else:
        # Prepare data for combo table
        fill_vent_data = {}
        empty_events = []
        max_length = 0
        for i in range(1, 5):
            key = f'FILL_{i}_VENT_{i}'
            events = fill_vent_events.get(key, [])
            if not events:
                empty_events.append(key)
                continue
            fill_instances = [j + 1 for j in range(len(events))]
            vent_counts = [event['vent_transition_count'] for event in events]
            fill_vent_data[f'FILL_{i} (instance)'] = fill_instances
            fill_vent_data[f'VENT_{i} (count)'] = vent_counts
            if len(events) > max_length:
                max_length = len(events)
        if fill_vent_data:
            # Pad shorter lists with empty strings
            for key in fill_vent_data:
                fill_vent_data[key] += [''] * (max_length - len(fill_vent_data[key]))
            # Create DataFrame
            table_df = pd.DataFrame(fill_vent_data)
            # Display table and empty events side by side
            col1, col2 = st.columns([3, 1])
            with col1:
                st.table(table_df.style.set_properties(**{'text-align': 'center'}).set_table_styles([{'selector': 'th', 'props': [('text-align', 'center')]}]))
            with col2:
                if empty_events:
                    st.markdown("#### Empty FILL/VENT Events")
                    st.markdown(
                        '<ul style="list-style-type:none; padding-left: 0;">' +
                        ''.join([
                            f'<li style="margin-bottom: 10px; padding: 10px; background-color: #f8f9fa; text-align: center; border-radius: 5px; box-shadow: 0 2px 5px rgba(0,0,0,0.1);">{event}</li>'
                            for event in empty_events
                        ]) +
                        '</ul>',
                        unsafe_allow_html=True
                    )
        else:
            st.warning("No FILL/VENT events with data to display.")