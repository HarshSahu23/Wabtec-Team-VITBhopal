import streamlit as st

def inject_main_css():
    """Inject main CSS styles for better spacing and readability."""
    st.markdown("""
        <style>
            .stRadio > div {
                display: flex;
                justify-content: center;
                gap: 1rem;
            }
            .stCheckbox > label {
                word-wrap: break-word;
                max-width: 300px;
            }
        </style>
    """, unsafe_allow_html=True)

def inject_column_css():
    """Inject CSS styles for styling columns."""
    st.markdown("""
        <style>
            [data-testid="stHorizontalBlock"] > div:nth-child(1) {
                background-color: rgba(200, 200, 200, 0.2);
                padding: 15px;
                border-radius: 15px;
            }
        </style>
    """, unsafe_allow_html=True)

def get_metrics_css():
    """Return CSS styles for the metrics display."""
    return """
    <style>
        .metric-container {
            background-color: rgba(248,249,250,0.7);
            border: 1px solid #FF5757;
            border-radius: 10px;
            padding: 15px;
            text-align: center;
            height: 120px;
        }
        .metric-title {
            color: #495057;
            font-size: 16px;
            font-weight: bold;
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }
        .metric-value-large {
            color: #FF5757;
            font-size: 28px;
            font-weight: bold;
            margin-top: 10px;
        }
        .metric-value-medium {
            color: #FF5757;
            font-size: 20px;
            font-weight: bold;
            margin-top: 10px;
        }
    </style>
    """

def inject_tab_css():
    """Inject CSS styles for the navigation tabs."""
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