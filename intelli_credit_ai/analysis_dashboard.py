import streamlit as st
import plotly.graph_objects as go

def render_analysis_page():
    st.markdown('<div class="header-container">', unsafe_allow_html=True)
    st.markdown("<h1>Credit Risk Analysis</h1>", unsafe_allow_html=True)
    st.markdown("<p class='subtitle'>AI-generated insights and recommendations</p>", unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
    
    results = st.session_state.get('analysis_results')
    
    if not results:
        st.info("No analysis data available. Please generate a new application from the **Upload Documents** section.")
        return
        
    company_name = results["company_name"]
    final_score = results["final_score"]
    recommendation = results["recommendation"]
    llm_results = results["llm_results"]
    key_factors = results["key_factors"]
    
    st.markdown(f"<h3>{company_name} - Credit Profile</h3>", unsafe_allow_html=True)
    
    # ------------------ TOP ROW: SCORE & RECOMMENDATION ------------------
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.markdown('<div class="card-container" style="height: 380px;">', unsafe_allow_html=True)
        st.markdown("<h4 style='text-align:center;'>Credit Risk Score</h4>", unsafe_allow_html=True)
        # Plotly Gauge Chart matching dark theme
        fig_gauge = go.Figure(go.Indicator(
            mode="gauge+number",
            value=final_score,
            domain={'x': [0, 1], 'y': [0, 1]},
            title={'text': "", 'font': {'size': 24, 'color': 'white'}},
            number={'font': {'color': 'white'}},
            gauge={
                'axis': {'range': [None, 100], 'tickwidth': 1, 'tickcolor': "darkgray"},
                'bar': {'color': "#FF5A1F", 'thickness': 0.25},
                'bgcolor': "#111827",
                'borderwidth': 0,
                'bordercolor': "#111827",
                'steps': [
                    {'range': [0, 40], 'color': "rgba(239, 68, 68, 0.2)"},   # Faded Red
                    {'range': [40, 70], 'color': "rgba(245, 158, 11, 0.2)"},  # Faded Orange
                    {'range': [70, 100], 'color': "rgba(16, 185, 129, 0.2)"}  # Faded Green
                ]
            }
        ))
        fig_gauge.update_layout(
            height=250, 
            margin=dict(l=20, r=20, t=10, b=10),
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font={'color': 'white'}
        )
        fig_gauge.update_layout(height=250, margin=dict(l=20, r=20, t=10, b=10))
        st.plotly_chart(fig_gauge, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
        
    with col2:
        st.markdown('<div class="card-container" style="height: 380px; display: flex; flex-direction: column; justify-content: center;">', unsafe_allow_html=True)
        st.markdown("<h4>Loan Recommendation</h4>", unsafe_allow_html=True)
        
        # Style based on recommendation
        if "Approved" in recommendation:
            color = "#10b981"
            bg = "rgba(16, 185, 129, 0.1)"
            icon = "✅"
        elif "Moderate" in recommendation:
            color = "#f59e0b"
            bg = "rgba(245, 158, 11, 0.1)"
            icon = "⚠️"
        else:
            color = "#ef4444"
            bg = "rgba(239, 68, 68, 0.1)"
            icon = "❌"
            
        st.markdown(f"""
        <div style="background-color: {bg}; padding: 20px; border-radius: 12px; border: 1px solid {color}; margin-top: 10px; margin-bottom: 20px;">
            <h2 style="color: {color}; margin: 0; display: flex; align-items: center; gap: 10px;">
                {icon} {recommendation}
            </h2>
        </div>
        """, unsafe_allow_html=True)
        
        # Suggested limit and rate
        st.markdown("<b>Suggested Loan Limit:</b> <span style='color: #1f4ed8; font-weight: bold;'>$1,500,000</span>", unsafe_allow_html=True)
        st.markdown("<b>Estimated Interest Rate:</b> <span style='color: #1f4ed8; font-weight: bold;'>6.5% - 8.0%</span>", unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)


    # ------------------ BOTTOM ROW: SUMMARY & RISK FACTORS ------------------
    colA, colB = st.columns([1.5, 1])

    with colA:
        st.markdown('<div class="card-container" style="height: 100%;">', unsafe_allow_html=True)
        st.markdown("<h4>AI Financial Summary</h4>", unsafe_allow_html=True)
        st.markdown(f"<p style='color: #475569; line-height: 1.6;'>{llm_results.get('summary', 'No summary available.')}</p>", unsafe_allow_html=True)
        
        # Extracted metrics
        st.markdown("<h5>Key Metrics Extracted:</h5>", unsafe_allow_html=True)
        ratios = llm_results.get("financial_ratios", {})
        if ratios:
            r1, r2, r3 = st.columns(3)
            r1.metric("Debt-to-Equity", ratios.get("debt_to_equity", "N/A"))
            r2.metric("Current Ratio", ratios.get("current_ratio", "N/A"))
            r3.metric("EBITDA Margin", ratios.get("ebitda_margin", "N/A"))
        st.markdown('</div>', unsafe_allow_html=True)
        
    with colB:
        st.markdown('<div class="card-container" style="height: 100%;">', unsafe_allow_html=True)
        st.markdown("<h4>Key Risk Factors</h4>", unsafe_allow_html=True)
        
        if key_factors:
            for factor in key_factors:
                st.markdown(f"""
                <div style="border-left: 4px solid #FF5A1F; padding-left: 10px; margin-bottom: 12px; color: #D1D5DB; background-color: rgba(255, 90, 31, 0.05); padding: 10px; border-radius: 4px;">
                    {factor}
                </div>
                """, unsafe_allow_html=True)
        else:
            st.write("No major risk factors identified.")
            
        st.markdown('</div>', unsafe_allow_html=True)

