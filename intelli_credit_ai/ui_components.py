import streamlit as st

def inject_custom_css():
    """Injects the custom CSS file into the Streamlit app."""
    try:
        with open("styles.css") as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
    except FileNotFoundError:
        st.error("styles.css not found.")

def render_hero_section():
    """Renders the bold premium hero header section."""
    st.markdown("""
    <div class="hero-section">
        <h1 class="hero-title">Intelli <span>Credit</span></h1>
        <p class="subtitle" style="font-size: 1.4em; color: #D1D5DB; margin-bottom: 30px;">
            AI Powered Credit Intelligence for Smarter Lending Decisions
        </p>
    </div>
    """, unsafe_allow_html=True)

def render_custom_navbar():
    """Renders the top branding for the navbar (navigation is handled via horizontal option_menu in app.py)."""
    st.markdown("""
    <div class="custom-navbar">
        <div class="nav-logo">
            <h2>Intelli<span>Credit</span></h2>
        </div>
        <div style="flex-grow: 1;"></div>
    </div>
    <div style="height: 20px;"></div>
    """, unsafe_allow_html=True)
