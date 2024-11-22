import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
from backend.data_handler import DataHandler
import tempfile
import os
from pathlib import Path
from functools import lru_cache
from frontend.compute.visualizations import create_bar_chart, create_pie_chart, create_treemap, get_color
from frontend.utils.css_utils import inject_main_css, inject_column_css, get_metrics_css
from frontend.utils.sidebar_utils import show_help, show_credits

class StreamlitGUI:
    def __init__(self):
        self.init_page_config()
        self.init_session_state()
        self.get_color = get_color
    
    def init_page_config(self):
        st.set_page_config(
            page_title="Error Analyzer",
            page_icon="📊",
            layout="wide"
        )
        inject_main_css()
        
        # Enhanced CSS for modern, interactive tabs
        st.markdown("""
        <style>
        /* Tab container styling */
        .stTabs {
            background-color: #f8f9fa;
            padding: 10px 20px 0 20px;
            border-radius: 15px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
            margin-bottom: 20px;
        }
        
        /* Tab list styling */
        .stTabs [data-baseweb="tab-list"] {
            gap: 20px;
            background-color: transparent;
            border-bottom: 2px solid #e9ecef;
            padding: 0 20px;
        }
        
        /* Individual tab styling */
        .stTabs [data-baseweb="tab"] {
            height: 50px;
            padding: 10px 25px;
            margin-bottom: -2px;
            border-radius: 10px 10px 0 0;
            background-color: transparent;
            border: none;
            color: #6c757d;
            font-weight: 600;
            transition: all 0.3s ease;
        }
        
        /* Active tab styling */
        .stTabs [aria-selected="true"] {
            background-color: #ffffff !important;
            color: #0366d6 !important;
            border-bottom: 3px solid #0366d6;
            padding-bottom: 8px;
        }
        
        /* Hover effect for tabs */
        .stTabs [data-baseweb="tab"]:hover {
            background-color: #f1f3f5;
            color: #0366d6;
        }
        
        /* Tab panel styling */
        .stTabs [data-baseweb="tab-panel"] {
            padding: 20px 0;
            background-color: transparent;
        }

        /* Custom badges for tabs */
        .tab-badge {
            background-color: #e9ecef;
            padding: 2px 8px;
            border-radius: 12px;
            font-size: 12px;
            margin-left: 8px;
        }

        /* Animation for tab transitions */
        .stTabs [data-baseweb="tab-panel"] > div:first-child {
            animation: fadeIn 0.3s ease-in;
        }

        @keyframes fadeIn {
            from { opacity: 0; transform: translateY(10px); }
            to { opacity: 1; transform: translateY(0); }
        }

        /* Custom styling for section headers */
        .section-header {
            background: linear-gradient(90deg, #f8f9fa 0%, transparent 100%);
            padding: 15px;
            border-radius: 10px;
            margin-bottom: 20px;
        }
        </style>
        """, unsafe_allow_html=True)

    def init_session_state(self):
        # ... [previous init_session_state code remains the same]
        if 'tab_badges' not in st.session_state:
            st.session_state.tab_badges = {
                'Brakes Log': {'count': 0, 'color': '#dc3545'},
                'Dump Log': {'count': 0, 'color': '#fd7e14'},
                'Summary': {'count': 0, 'color': '#198754'}
            }

    def create_tab_label(self, title, icon, badge_count=None):
        """Create a formatted tab label with icon and optional badge"""
        badge_html = f'<span class="tab-badge">{badge_count}</span>' if badge_count is not None else ''
        return f"""
            <div style="display: flex; align-items: center; gap: 8px;">
                {icon} {title} {badge_html}
            </div>
        """

    def render_section_header(self, title, description, icon):
        """Render a consistent section header"""
        st.markdown(f"""
            <div class="section-header">
                <h1 style="display: flex; align-items: center; gap: 10px;">
                    {icon} {title}
                </h1>
                <p style="margin-top: 5px; color: #6c757d;">{description}</p>
            </div>
        """, unsafe_allow_html=True)

    def render_brakes_log(self):
        self.render_section_header(
            "Brakes Log Analysis",
            "Analyze and visualize error frequencies from your brake system logs.",
            "🔍"
        )
        # ... [rest of the brakes_log rendering code remains the same]

    def render_dump_log(self):
        self.render_section_header(
            "Dump Log Analysis",
            "Review and analyze system dump logs for critical issues.",
            "📋"
        )
        
        # Enhanced placeholder content with animations and interactivity
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("🔄 Data Upload")
            uploaded_dumps = st.file_uploader(
                "Upload Dump Log Files", 
                type=['log', 'txt'], 
                accept_multiple_files=True
            )
            
            st.subheader("🎯 Filters")
            selected_date = st.date_input("Date Range", value=None)
            error_types = st.multiselect(
                "Error Types",
                ["Critical", "Warning", "Info", "Debug"],
                default=["Critical", "Warning"]
            )
            
            # Interactive severity slider
            severity_level = st.slider(
                "Minimum Severity Level",
                min_value=1,
                max_value=5,
                value=3,
                help="Filter issues based on severity (1: Low, 5: Critical)"
            )
        
        with col2:
            st.subheader("📊 Quick Statistics")
            metric_cols = st.columns(2)
            
            # Animated metrics with dummy data
            with metric_cols[0]:
                st.metric(
                    label="Total Dumps",
                    value="1,234",
                    delta="↑ 23 from last week",
                    delta_color="inverse"
                )
            with metric_cols[1]:
                st.metric(
                    label="Critical Errors",
                    value="42",
                    delta="↓ 15%",
                    delta_color="inverse"
                )
            
            # Interactive chart selection
            chart_type = st.radio(
                "Select Visualization",
                ["Timeline", "Distribution", "Severity Breakdown"],
                horizontal=True
            )
            
            if not uploaded_dumps:
                st.info("📤 Upload dump files to view detailed analysis")

    def render_summary(self):
        self.render_section_header(
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

    def render(self):
        # Create tabs with enhanced labels and icons
        tab_labels = {
            "Brakes Log": {"icon": "🔍", "badge": 5},
            "Dump Log": {"icon": "📋", "badge": 2},
            "Summary": {"icon": "📈", "badge": None}
        }
        
        tabs = st.tabs([
            self.create_tab_label(title, info["icon"], info["badge"])
            for title, info in tab_labels.items()
        ])
        
        # Sidebar with enhanced styling
        with st.sidebar:
            st.header("⚙️ Settings")
            # ... [rest of the sidebar code remains the same]
        
        # Render content based on active tab
        with tabs[0]:
            self.render_brakes_log()
        with tabs[1]:
            self.render_dump_log()
        with tabs[2]:
            self.render_summary()

    # ... [rest of the class methods remain the same]

def main():
    gui = StreamlitGUI()
    gui.render()

if __name__ == "__main__":
    main()