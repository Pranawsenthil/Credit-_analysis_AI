import streamlit as st
import os
import time

# original backend modules
from pdf_parser import extract_text_from_pdf
from research_agent import search_company_news, evaluate_news_sentiment
from risk_model import calculate_risk_score, extract_key_factors
from llm_service import analyze_document_with_llm
from cam_generator import generate_cam_pdf

UPLOAD_DIR = "uploads"
if not os.path.exists(UPLOAD_DIR):
    os.makedirs(UPLOAD_DIR)

def render_upload_section():
    st.markdown('<div class="card-container">', unsafe_allow_html=True)
    st.markdown("<h2 style='color:#FF5A1F;'>New Credit Application</h2>", unsafe_allow_html=True)
    st.markdown("<p>Upload corporate financials to run Intelli Credit AI analysis</p><br>", unsafe_allow_html=True)
    
    with st.form("credit_application_form"):
        st.markdown("<h3>Company Information</h3>", unsafe_allow_html=True)
        company_name = st.text_input("Company Name", placeholder="e.g. Acme Corporation")
        
        st.markdown("<br><h3>Financial Documents</h3>", unsafe_allow_html=True)
        uploaded_file = st.file_uploader("Upload Financial Report (PDF)", type=["pdf"], help="Drag and drop or brose files")
        
        st.markdown("<br><h3>Qualitative Data</h3>", unsafe_allow_html=True)
        site_notes = st.text_area("Site Visit Observations & Notes", 
                                  placeholder="Enter observations from site visit, qualitative market context...", 
                                  height=130)
                                  
        st.markdown("<br>", unsafe_allow_html=True)
        submitted = st.form_submit_button("Analyze Credit Risk", use_container_width=True)

    st.markdown('</div>', unsafe_allow_html=True)
    
    if submitted:
        if not company_name:
            st.error("Please enter a valid company name.")
        elif uploaded_file is None:
            st.error("Please upload a financial document.")
        else:
            with st.spinner("Processing documents & querying Intelli Credit Engine..."):
                # 1. Setup
                filepath = os.path.join(UPLOAD_DIR, uploaded_file.name)
                with open(filepath, "wb") as f:
                    f.write(uploaded_file.getbuffer())
                
                # 2. Extract Text
                progress_text = st.empty()
                progress_text.text("Extracting financial data from PDF...")
                financial_text = extract_text_from_pdf(filepath)
                if not financial_text:
                    financial_text = ""
                
                # 3. LLM Analysis (use only raw text portion if structured data returned)
                progress_text.text("Running LLM analysis on financials...")
                llm_input = financial_text.get("full_text", "") if isinstance(financial_text, dict) else str(financial_text)
                llm_results = analyze_document_with_llm(llm_input)
                
                # 4. Agentic Research
                progress_text.text("Gathering market intelligence...")
                news_headlines = search_company_news(company_name)
                news_risk_score = evaluate_news_sentiment(news_headlines)
                
                # 5. Risk Scoring
                progress_text.text("Calculating Credit Risk Score...")
                final_score, recommendation, score_breakdown = calculate_risk_score(
                    financial_text, site_notes, news_risk_score, llm_results.get("ratio_health", "Neutral")
                )
                key_factors = extract_key_factors(financial_text, site_notes, news_headlines)
                
                # 6. Generate CAM PDF payload
                cam_filename = f"CAM_{company_name.replace(' ', '_')}.pdf"
                cam_filepath = os.path.join(UPLOAD_DIR, cam_filename)
                
                generate_cam_pdf(
                    company_name, final_score, recommendation, key_factors, cam_filepath,
                    llm_summary=llm_results.get("summary", ""), 
                    financial_ratios=llm_results.get("financial_ratios", {})
                )
                
                progress_text.empty()
                
                # Save results to session state
                st.session_state['analysis_results'] = {
                    "company_name": company_name,
                    "final_score": final_score,
                    "recommendation": recommendation,
                    "score_breakdown": score_breakdown,
                    "key_factors": key_factors,
                    "llm_results": llm_results,
                    "cam_filepath": cam_filepath,
                    "cam_filename": cam_filename,
                    "news_headlines": news_headlines
                }
                
                st.success("✅ Analysis Complete!")
                st.info("Navigate to the **Credit Analysis** tab in the sidebar to view the dashboard results.")

