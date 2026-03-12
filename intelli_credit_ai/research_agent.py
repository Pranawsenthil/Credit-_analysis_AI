import requests

def search_company_news(company_name):
    """
    Searches for latest headlines related to the company.
    In a real scenario, this would use NewsAPI, Google Search API, etc.
    For this prototype, we simulate the search or use a public free endpoint.
    """
    # Mocking standard news response for the prototype demonstration.
    # We will simulate "negative" news if the company name contains certain trigger words for demo purposes.
    trigger_words = ["fraud", "bankrupt", "sued", "scandal"]
    
    is_negative = any(word in company_name.lower() for word in trigger_words)
    
    if is_negative:
        return [
            f"Breaking: {company_name} faces new lawsuit over alleged financial discrepancies.",
            f"Investors worry as {company_name} reports sudden loss in Q3.",
            f"Regulatory authorities investigating {company_name} for compliance issues."
        ]
    else:
        # standard positive or neutral news
        return [
            f"{company_name} announces new strategic partnership to expand market reach.",
            f"Quarterly earnings for {company_name} show steady growth.",
            f"CEO of {company_name} speaks at industry conference about future innovations."
        ]

def evaluate_news_sentiment(news_headlines):
    """
    Evaluates the sentiment of the news headlines.
    Returns a score 0-100 where higher means higher risk (negative news).
    """
    negative_keywords = ["fraud", "lawsuit", "investigation", "loss", "bankrupt", "debt", "scandal", "decline"]
    
    risk_score = 0
    for headline in news_headlines:
        lower_headline = headline.lower()
        for word in negative_keywords:
            if word in lower_headline:
                risk_score += 15 # Add 15 points of risk for each negative keyword found
                
    return min(risk_score, 100) # Cap at 100
