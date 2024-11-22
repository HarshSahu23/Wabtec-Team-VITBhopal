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