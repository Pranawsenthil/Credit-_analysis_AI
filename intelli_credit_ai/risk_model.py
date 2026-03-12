import pandas as pd
import re
try:
    from textblob import TextBlob
except ImportError:
    TextBlob = None

# Advanced Dynamic Severity Weights
RISK_WEIGHTS = {
    "fraud": -40,
    "investigation": -40,
    "litigation": -30,
    "lawsuit": -30,
    "bankruptcy": -50,
    "loss": -25,
    "negative cash flow": -25,
    "high debt": -20,
    "below 50% capacity": -20,
    "40% capacity": -20,
    "revenue decline": -15
}

POSITIVE_WEIGHTS = {
    "revenue growth": 20,
    "strong profit": 20,
    "positive cash flow": 15,
    "stable revenue": 10
}

def analyze_sentiment(text):
    """Returns a polarity score between -1 (negative) and 1 (positive)."""
    if not text or TextBlob is None:
        return 0
    return TextBlob(text).sentiment.polarity

def calculate_risk_score(structured_financial_data, site_notes, news_risk_score, ratio_health="Moderate Risk"):
    """
    Calculates credit risk using structured section data, NLP sentiment, and strict combination logic.
    structured_financial_data is now expected to be a dict from pdf_parser.
    """
    base_score = 80
    financial_adj = 0
    notes_adj = 0
    ratios_adj = 0
    
    triggered_risks = set()
    triggered_positives = set()

    # Handle if strings are passed by legacy tests instead of the new dict
    if isinstance(structured_financial_data, str):
        full_text = structured_financial_data.lower()
        sections = {"full_text": full_text}
    else:
        sections = structured_financial_data
        full_text = sections.get("full_text", "").lower()

    notes_lower = (site_notes or "").lower()
    combined_context = full_text + " " + notes_lower
    
    # 1. Evaluate Dynamic Weights (Negative & Positive)
    for trigger, penalty in RISK_WEIGHTS.items():
        if trigger in combined_context:
            financial_adj += penalty
            triggered_risks.add(trigger)
            
    for trigger, bonus in POSITIVE_WEIGHTS.items():
        if trigger in combined_context:
            financial_adj += bonus
            triggered_positives.add(trigger)
            
    # Fallback legacy checks if explicit positive phrases aren't used but generic ones are
    if not triggered_positives:
        if "profit" in combined_context or "growth" in combined_context:
            financial_adj += 10
            
    # 2. Section-specific Sentiment Analysis
    docs_sentiment = 0
    if sections.get("legal_section"):
        leg_sens = analyze_sentiment(sections["legal_section"])
        if leg_sens < -0.2:
            financial_adj -= 10 # Extra penalty for verifiably negative legal text
            
    if sections.get("revenue_section"):
        rev_sens = analyze_sentiment(sections["revenue_section"])
        if rev_sens > 0.3:
            financial_adj += 10 # Bonus for highly positive earnings calls
            
    # 3. Apply ratio health from LLM
    if ratio_health == "High Risk":
        ratios_adj -= 20
        triggered_risks.add("high debt ratio")
    elif ratio_health == "Low Risk":
        ratios_adj += 10
        
    # 4. Apply news risk modifier
    news_adj = -int(news_risk_score * 0.5)
    if news_risk_score >= 50:
        triggered_risks.add("negative news cycle")
    
    # 5. Final Calculation
    raw_score = base_score + financial_adj + notes_adj + ratios_adj + news_adj
    final_score = max(0, min(100, int(raw_score)))
    
    # Context Validation / Hard Combinations
    is_high_risk_combo = False
    if "loss" in triggered_risks and ("high debt" in triggered_risks or "litigation" in triggered_risks):
        is_high_risk_combo = True
        
    if len(triggered_risks) >= 2 and final_score >= 40:
        is_high_risk_combo = True

    # HARD CAP: Enforce Rejection
    if is_high_risk_combo:
        final_score = min(final_score, 39)  # Force High Risk
        # Balance waterfall chart 
        financial_adj = final_score - (base_score + notes_adj + ratios_adj + news_adj) 
        
    # Determine recommendation
    if final_score >= 70:
        recommendation = "Loan Approved"
    elif final_score >= 40:
        recommendation = "Moderate Risk (Needs Manual Review)"
    else:
        recommendation = "Loan Rejected - High Risk"
        
    breakdown = {
        "Base Score": base_score,
        "Financial Text Factors": financial_adj,
        "Ratio Analysis Factors": ratios_adj,
        "Site Visit Notes": notes_adj,
        "News Sentiment Risk": news_adj
    }
        
    return final_score, recommendation, breakdown

def extract_key_factors(structured_financial_data, site_notes, news_headlines):
    """Contextual explainability mapping to the dynamically triggered NLP signals."""
    factors = []
    
    # Handle backward compatibility
    if isinstance(structured_financial_data, str):
        full_text = structured_financial_data.lower()
    else:
        full_text = structured_financial_data.get("full_text", "").lower()
        
    notes_lower = (site_notes or "").lower()
    combined_context = full_text + " " + notes_lower
    
    # Map back to English sentences
    if "loss" in combined_context or "negative cash flow" in combined_context:
        factors.append("Financial losses or negative cash flow detected (-25).")
    if "litigation" in combined_context or "lawsuit" in combined_context:
        factors.append("Litigation or legal disputes mentioned in report (-30).")
    if "fraud" in combined_context or "investigation" in combined_context:
        factors.append("Fraud or investigation flagged in materials (-40).")
    if "high debt" in combined_context or "bankruptcy" in combined_context:
        factors.append("Severe debt obligations or bankruptcy risk identified (-20 to -50).")
    if "below 50% capacity" in combined_context or "40% capacity" in combined_context:
        factors.append("Factory operating at critical low capacity (<50%) (-20).")
    if "revenue decline" in combined_context:
        factors.append("Revenue decline detected (-15).")
        
    # Positive Maps
    if "revenue growth" in combined_context:
        factors.append("Stable revenue growth detected (+20).")
    if "strong profit" in combined_context:
        factors.append("Strong profit margins identified (+20).")
        
    # Standard outputs
    if news_headlines and any(bad in news_headlines[0].lower() for bad in ["fraud", "lawsuit", "investigation", "loss", "bankrupt"]):
        factors.append(f"Negative External News Signal: {news_headlines[0][:60]}...")
        
    if not factors:
        factors.append("Standard evaluation based on nominal inputs. No severe risks detected.")
        
    return factors
