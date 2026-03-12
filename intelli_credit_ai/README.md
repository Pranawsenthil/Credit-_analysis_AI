# Intelli-Credit: AI Powered Corporate Credit Decisioning System

A prototype application built for validating automated credit underwriting. It digests uploaded financial documents, site visit notes, and external web intelligence to formulate a rapid "Approve/Moderate/Reject" recommendation.

## Features
1. **Frontend**: Streamlit-based UI for loan officers.
2. **Document Processing**: `pdfplumber` for PDF text extraction.
3. **Research Agent**: Scans simulated external news for positive or negative signals.
4. **Risk Engine**: Rule-based scoring engine weighing financials, field notes, and news sentiment.
5. **CAM Generator**: Generates a downloadable PDF Credit Appraisal Memo via `reportlab`.

## Structure
```text
intelli_credit_ai/
├── app.py               # Streamlit application entry point
├── pdf_parser.py        # PDF text extraction
├── research_agent.py    # News and sentiment simulation
├── risk_model.py        # Logic to compute final 0-100 score + recommendation 
├── cam_generator.py     # PDF generation code
├── requirements.txt     # Python dependencies
└── uploads/             # Temp directory for processing files
```

## How to Run

1. **Install dependencies:**
```bash
pip install -r requirements.txt
```

2. **Run the Streamlit app:**
```bash
streamlit run app.py
```

## Example Test Workflow

1. Start the app using `streamlit run app.py`.
2. In the "**Company Name**" field, type "Acme Corp".
3. Upload a sample PDF with financial metrics (e.g., a dummy PDF stating "Company profit has grown by 15%").
4. In the "**Qualitative Notes**" box, type "Factory operating at 40% capacity".
5. Click **Analyze Credit Risk**.
6. Review the generated risk score, recommendation, and external news factors.
7. Click **Download Credit Appraisal Memo (CAM)** to get the auto-generated PDF.
8. _Edge Case Testing:_ Try entering "fraud" or "bankrupt" in the company name or notes to see the score aggressively decrease.

## Future AI / LLM Improvements
While this prototype uses rule-based extraction and scoring, an actual production system would:
* **LLM Document Extraction**: Use an LLM (e.g., GPT-4 / Gemini) directly on the PDF text to intelligently extract Debt-to-Equity ratios, EBITDA, and nuanced risks rather than using static keyword matches.
* **Agentic News Searching**: Connect the Research Agent to a verified SERP API / News API and use an LLM to accurately summarize the financial risks posed by current headlines.
* **GenAI CAM Writing**: Use LLMs to narratively write the explanation of the risk factors within the CAM PDF, making it read exactly like a memo authored by a seasoned credit analyst.
