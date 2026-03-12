import streamlit as st
import os
from streamlit_option_menu import option_menu

# Import routing modules
import auth
import dashboard
import upload_section
import analysis_dashboard
import cam_reports
import ui_components

# Initialize session state for auth and data
if 'authenticated' not in st.session_state:
    st.session_state['authenticated'] = False
if 'username' not in st.session_state:
    st.session_state['username'] = None
if 'analysis_results' not in st.session_state:
    st.session_state['analysis_results'] = None

st.set_page_config(page_title="Intelli Credit", page_icon="🏦", layout="wide")

# Inject Global Premium Dark CSS
ui_components.inject_custom_css()

# Application Logic
if not st.session_state['authenticated']:
    # Render login page if not authenticated
    auth.show_login_page()
else:
    # Authenticated Layout - Top Navigation Bar
    ui_components.render_custom_navbar()
    
    selected_page = option_menu(
        menu_title=None,
        options=["Dashboard", "Upload Documents", "Credit Analysis", "CAM Reports", "Logout"],
        icons=["house", "cloud-upload", "bar-chart-line", "file-earmark-text", "box-arrow-right"],
        menu_icon="cast",
        default_index=0,
        orientation="horizontal",
        styles={
            "container": {"padding": "0!important", "background-color": "transparent", "margin-top": "-10px", "margin-bottom": "30px", "border-bottom": "1px solid #1F2937"},
            "icon": {"color": "#FF5A1F", "font-size": "16px"}, 
            "nav-link": {"font-size": "15px", "text-align": "center", "margin":"0px", "--hover-color": "rgba(255,90,31,0.1)", "color": "#D1D5DB"},
            "nav-link-selected": {"background-color": "rgba(255,90,31,0.1)", "color": "#FF5A1F", "font-weight": "600", "border-bottom": "2px solid #FF5A1F", "border-radius":"0"},
        }
    )

    # Route navigation
    if selected_page == "Dashboard":
        dashboard.render_dashboard()
        
    elif selected_page == "Upload Documents":
        upload_section.render_upload_section()
        
    elif selected_page == "Credit Analysis":
        analysis_dashboard.render_analysis_page()
        
    elif selected_page == "CAM Reports":
        cam_reports.render_cam_reports()
        
    elif selected_page == "Logout":
        st.session_state['authenticated'] = False
        st.session_state['username'] = None
        st.rerun()
