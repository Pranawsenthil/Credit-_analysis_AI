import json

def analyze_document_with_llm(text):
    """
    Mocks an LLM call to summarize the document and extract key financial metrics.
    In a real application, this would call OpenAI, Anthropic, or Gemini APIs.
    """
    
    # We use heuristics for the mock to make it dynamic based on what's in the text.
    # But fundamentally, we return a structured JSON-like response.
    
    response = {
        "summary": "This document outlines the recent financial performance of the company. It highlights operational metrics and provides an overview of current liabilities and growth trajectories.",
        "financial_ratios": {
            "debt_to_equity": 1.5,
            "current_ratio": 1.2,
            "ebitda_margin": "12%"
        },
        "ratio_health": "Moderate Risk"
    }
    
    # normalize input so we always operate on a string
    if isinstance(text, dict):
        # pdf_parser returns a dict with a "full_text" key containing the raw content
        text = text.get("full_text", "")
    elif text is None:
        text = ""
    else:
        # ensure we have a string even if something odd was passed
        text = str(text)

    text_lower = text.lower()
    
    if "profit" in text_lower or "growth" in text_lower:
        response["summary"] = "The document indicates strong financial health with noted profit margins and positive growth trajectories. Liquidity appears stable."
        response["financial_ratios"]["debt_to_equity"] = 0.8  # Healthy
        response["financial_ratios"]["current_ratio"] = 2.1   # Healthy
        response["financial_ratios"]["ebitda_margin"] = "24%"
        response["ratio_health"] = "Low Risk"
        
    elif "loss" in text_lower or "debt" in text_lower or "bankruptcy" in text_lower:
        response["summary"] = "The company's financials show significant distress, highlighting considerable debt loads and recent operating losses. Solvency is a major concern."
        response["financial_ratios"]["debt_to_equity"] = 3.5  # High risk
        response["financial_ratios"]["current_ratio"] = 0.7   # High risk
        response["financial_ratios"]["ebitda_margin"] = "-5%"
        response["ratio_health"] = "High Risk"

    return response
