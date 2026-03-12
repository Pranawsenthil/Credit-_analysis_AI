import streamlit as st
import os

def render_cam_reports():
    st.markdown('<div class="header-container">', unsafe_allow_html=True)
    st.markdown("<h1>Credit Appraisal Memos (CAM)</h1>", unsafe_allow_html=True)
    st.markdown("<p class='subtitle'>Review and export generated CAM documents</p>", unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
    
    results = st.session_state.get('analysis_results')
    
    if not results:
        st.info("No CAM reports available yet. Please complete a credit application via **Upload Documents**.")
        return
        
    company_name = results["company_name"]
    final_score = results["final_score"]
    recommendation = results["recommendation"]
    cam_filepath = results.get("cam_filepath")
    cam_filename = results.get("cam_filename")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown('<div class="card-container">', unsafe_allow_html=True)
        st.markdown(f"<h3>Draft CAM Preview: {company_name}</h3>", unsafe_allow_html=True)
        st.markdown("<hr>", unsafe_allow_html=True)
        
        st.markdown(f"**Application Subject:** {company_name}")
        st.markdown(f"**Calculated Score:** {final_score}/100")
        st.markdown(f"**Recommendation:** {recommendation}")
        
        st.markdown("#### Executive Summary")
        st.write(results["llm_results"].get("summary", "No summary provided."))
        
        st.markdown("#### Key Risk Factors")
        for factor in results.get("key_factors", []):
            st.markdown(f"- {factor}")
            
        st.markdown("#### Recent News Intelligence")
        for news in results.get("news_headlines", []):
            st.markdown(f"- {news}")
            
        st.markdown('</div>', unsafe_allow_html=True)
        
    with col2:
        st.markdown('<div class="card-container" style="text-align: center;">', unsafe_allow_html=True)
        st.markdown("<h3>Export Options</h3>", unsafe_allow_html=True)
        st.markdown("<p style='color: #64748b;'>Download the official PDF format of this Credit Appraisal Memo.</p>", unsafe_allow_html=True)
        
        if cam_filepath and os.path.exists(cam_filepath):
            with open(cam_filepath, "rb") as f:
                pdf_bytes = f.read()
                
            st.download_button(
                label="📥 Download CAM PDF",
                data=pdf_bytes,
                file_name=cam_filename,
                mime="application/pdf",
                use_container_width=True
            )
        else:
            st.error("CAM PDF file not found. Please run the analysis again.")
            
        st.markdown('</div>', unsafe_allow_html=True)

