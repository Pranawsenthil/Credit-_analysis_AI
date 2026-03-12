import sqlite3
import hashlib
import os
import streamlit as st

DB_PATH = 'users.db'

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def init_db():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE,
            email TEXT UNIQUE,
            password_hash TEXT
        )
    ''')
    conn.commit()
    conn.close()

def create_user(username, email, password):
    init_db()
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    try:
        # Check empty fields
        if not username or not email or not password:
            return False, "All fields are required!"
            
        c.execute("INSERT INTO users (username, email, password_hash) VALUES (?, ?, ?)",
                  (username, email, hash_password(password)))
        conn.commit()
        return True, "Account created! Please login."
    except sqlite3.IntegrityError:
        return False, "Username or Email already exists."
    finally:
        conn.close()

def verify_user(username, password):
    init_db()
    if not username or not password:
        return False
        
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT password_hash FROM users WHERE username=? OR email=?", (username, username))
    result = c.fetchone()
    conn.close()
    
    if result and result[0] == hash_password(password):
        return True
    return False

def show_login_page():
    # Inject Login specific CSS
    st.markdown("""
    <style>
    /* Full page gradient background */
    .stApp {
        background: linear-gradient(135deg, #0f172a 0%, #1e3a8a 100%) !important;
    }
    
    /* Center the title */
    .login-header {
        text-align: center;
        margin-bottom: 30px;
    }
    .login-header h1 {
        color: white;
        font-size: 3.5em;
        font-weight: 700;
        margin-bottom: 0;
    }
    .login-header p {
        color: #cbd5e1;
        font-size: 1.2em;
        margin-top: -10px;
    }

    /* Glassmorphism Card */
    .login-card-container {
        background: rgba(255, 255, 255, 0.05); /* very subtle white */
        backdrop-filter: blur(16px);
        -webkit-backdrop-filter: blur(16px);
        border-radius: 20px;
        border: 1px solid rgba(255, 255, 255, 0.1);
        padding: 40px;
        box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.3);
    }
    
    /* Text overrides for login page */
    .login-card-container *, .stTabs [data-baseweb="tab-list"] * {
        color: white !important;
    }
    .stTabs [data-baseweb="tab"] {
        color: #cbd5e1 !important;
    }
    .stTabs [aria-selected="true"] {
        color: white !important;
        border-bottom-color: #3b82f6 !important;
    }
    
    /* Modern inputs */
    .stTextInput>div>div>input {
        background-color: rgba(255, 255, 255, 0.1) !important;
        border: 1px solid rgba(255, 255, 255, 0.2) !important;
        color: white !important;
        border-radius: 12px !important;
        padding: 12px !important;
    }
    .stTextInput>div>div>input:focus {
        background-color: rgba(255, 255, 255, 0.15) !important;
        border-color: #3b82f6 !important;
        box-shadow: 0 0 0 2px rgba(59, 130, 246, 0.3) !important;
    }

    /* Primary Login Button */
    .stButton>button {
        width: 100%;
        background: linear-gradient(135deg, #3b82f6 0%, #1d4ed8 100%);
        box-shadow: 0 4px 15px rgba(37, 99, 235, 0.4);
        padding: 12px;
        border-radius: 12px;
        font-size: 16px;
        font-weight: 600;
        margin-top: 10px;
        border: none;
        color: white;
    }
    .stCheckbox { margin-top: -10px; margin-bottom: 10px; }
    </style>
    """, unsafe_allow_html=True)

    st.markdown("<div class='login-header'><h1>Intelli Credit</h1><p>AI Driven Credit Intelligence</p></div>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 1.5, 1])
    
    with col2:
        st.markdown('<div class="login-card-container">', unsafe_allow_html=True)
        tab1, tab2 = st.tabs(["Login", "Sign Up"])
        
        with tab1:
            st.markdown("### Welcome Back")
            username = st.text_input("Username / Email", key="login_user")
            
            show_login_pass = st.checkbox("Show password", key="show_login_pass")
            password = st.text_input("Password", type="default" if show_login_pass else "password", key="login_pass")
            
            if st.button("Login", use_container_width=True):
                if verify_user(username, password):
                    st.session_state['authenticated'] = True
                    st.session_state['username'] = username
                    st.rerun()
                else:
                    st.error("Incorrect username or password")
                    
        with tab2:
            st.markdown("### Create an Account")
            new_username = st.text_input("Username", key="reg_user")
            new_email = st.text_input("Email", key="reg_email")
            
            show_reg_pass = st.checkbox("Show password", key="show_reg_pass")
            new_password = st.text_input("Password", type="default" if show_reg_pass else "password", key="reg_pass")
            
            if st.button("Sign Up", use_container_width=True):
                success, msg = create_user(new_username, new_email, new_password)
                if success:
                    st.success(msg)
                else:
                    st.error(msg)
        st.markdown('</div>', unsafe_allow_html=True)
