import streamlit as st
def render_section_header(title, description, icon):
        """Render a consistent section header"""
        st.markdown(f"""
            <div class="section-header">
                <h1 style="display: flex; align-items: center; gap: 10px;">
                    {icon} {title}
                </h1>
                <p style="margin-top: 5px; color: #6c757d;">{description}</p>
            </div>
        """, unsafe_allow_html=True)
    