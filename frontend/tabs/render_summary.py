import streamlit as st

from frontend.utils.render_section_header import render_section_header
def render_summary():
        render_section_header(
            "System Summary",
            "Overview of system health and key metrics across all logs.",
            "📈"
        )
        
        # Enhanced summary section with interactive elements
        tabs = st.tabs(["Overview 📊", "Trends 📈", "Recommendations 💡"])
        
        with tabs[0]:
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.metric(
                    label="System Health",
                    value="98%",
                    delta="↑ 2%",
                    help="Overall system health score based on error rates"
                )
            with col2:
                st.metric(
                    label="Active Issues",
                    value="27",
                    delta="↓ 5",
                    delta_color="inverse"
                )
            with col3:
                st.metric(
                    label="MTTR",
                    value="45m",
                    delta="↓ 12m",
                    help="Mean Time To Resolution"
                )
        
        with tabs[1]:
            # Timeline selector
            timeline = st.select_slider(
                "Analysis Period",
                options=["24H", "7D", "30D", "90D", "1Y"],
                value="7D"
            )
            st.info("Select a time period and upload data to view trends")
        
        with tabs[2]:
            st.markdown("""
                ### 🤖 AI-Powered Recommendations
                
                Upload system data to receive intelligent insights and recommendations:
                - Performance optimization suggestions
                - Preventive maintenance alerts
                - Resource allocation recommendations
            """)
