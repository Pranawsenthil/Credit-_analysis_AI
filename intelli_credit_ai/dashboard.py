import streamlit as st
from ui_components import render_hero_section

def render_dashboard():
    # Hero Section
    render_hero_section()
    
    # Action Buttons under Hero
    colA, colB, colEmpty = st.columns([1, 1, 4])
    with colA:
        if st.button("Analyze Credit Risk", use_container_width=True):
            st.info("Please navigate to 'Upload Documents' to begin analysis.")
    with colB:
        st.markdown('<div class="btn-outline">', unsafe_allow_html=True)
        if st.button("Upload Documents", use_container_width=True):
            st.info("Navigation shortcuts require session updates, please map through the top bar.")
        st.markdown('</div>', unsafe_allow_html=True)
        
    st.markdown("<br><hr style='border-color: #1F2937;'><br>", unsafe_allow_html=True)

    # Welcome Section
    st.markdown(f"""
    <div class="card-container">
        <h2>Welcome back, <span style="color:#FF5A1F;">{st.session_state.get('username', 'User')}</span></h2>
        <p>This is your corporate credit decisioning workspace. The dashboard gives you an overview of your agency's credit application pipeline.</p>
    </div>
    """, unsafe_allow_html=True)

    # Statistics
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div class="card-container" style="text-align: center;">
            <p style="color: #9CA3AF; font-size: 1.1em; margin-bottom: 5px; text-transform: uppercase; letter-spacing: 1px;">Total Applications</p>
            <h2 style="color: #FFFFFF; font-size: 3em; margin: 0; font-weight: 800;">1,284</h2>
        </div>
        """, unsafe_allow_html=True)
        
    with col2:
        st.markdown("""
        <div class="card-container" style="text-align: center;">
            <p style="color: #9CA3AF; font-size: 1.1em; margin-bottom: 5px; text-transform: uppercase; letter-spacing: 1px;">Approval Rate</p>
            <h2 style="color: #FF5A1F; font-size: 3em; margin: 0; font-weight: 800;">76%</h2>
        </div>
        """, unsafe_allow_html=True)
        
    with col3:
        st.markdown("""
        <div class="card-container" style="text-align: center;">
            <p style="color: #9CA3AF; font-size: 1.1em; margin-bottom: 5px; text-transform: uppercase; letter-spacing: 1px;">Pending Reviews</p>
            <h2 style="color: #FBBF24; font-size: 3em; margin: 0; font-weight: 800;">42</h2>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("""
    <div class="card-container" style="margin-top: 20px;">
        <h3>Recent Activity</h3>
        <table style="width: 100%; border-collapse: collapse; text-align: left;">
            <tr style="border-bottom: 1px solid #374151;">
                <th style="padding: 15px 10px; color: #9CA3AF;">Company</th>
                <th style="padding: 15px 10px; color: #9CA3AF;">Status</th>
                <th style="padding: 15px 10px; color: #9CA3AF;">Date</th>
            </tr>
            <tr style="border-bottom: 1px solid #374151;">
                <td style="padding: 15px 10px; font-weight: 600; color: #FFFFFF;">Stark Industries</td>
                <td style="padding: 15px 10px; color: #10B981; font-weight: 500;">Approved</td>
                <td style="padding: 15px 10px; color: #D1D5DB;">Oct 24, 2023</td>
            </tr>
            <tr style="border-bottom: 1px solid #374151;">
                <td style="padding: 15px 10px; font-weight: 600; color: #FFFFFF;">Wayne Enterprises</td>
                <td style="padding: 15px 10px; color: #FBBF24; font-weight: 500;">Moderate Risk</td>
                <td style="padding: 15px 10px; color: #D1D5DB;">Oct 23, 2023</td>
            </tr>
            <tr>
                <td style="padding: 15px 10px; font-weight: 600; color: #FFFFFF;">Oscorp</td>
                <td style="padding: 15px 10px; color: #EF4444; font-weight: 500;">Rejected</td>
                <td style="padding: 15px 10px; color: #D1D5DB;">Oct 21, 2023</td>
            </tr>
        </table>
    </div>
    """, unsafe_allow_html=True)
