def analyze_text(text):
    text = text.lower()

    score = 100
    flags = []

    strong_scam = [
        "registration fee",
        "internship fee",
        "security deposit",
        "pay amount"
    ]

    pressure_phrases = [
        "limited slots",
        "confirm your seat",
        "immediate openings",
        "interview process almost over",
        "short-listed"
    ]

    mlm_style = [
        "managerial position",
        "entrepreneurship",
        "global training module",
        "rapid promotion",
        "business development associate"
    ]

    free_domains = ["gmail.com", "yahoo.com", "outlook.com"]

    matched_strong = [word for word in strong_scam if word in text]
    if matched_strong:
        score -= 25
        flags.append("Strong scam indicator detected 🚩")

    matched_pressure = [word for word in pressure_phrases if word in text]
    if matched_pressure:
        score -= 10
        flags.append("Uses urgency / pressure tactics 🚩")

    matched_mlm = [word for word in mlm_style if word in text]
    if matched_mlm:
        score -= 5
        flags.append("Marketing/MLM-style language detected 🚩")

    matched_domains = [domain for domain in free_domains if domain in text]
    if matched_domains:
        score -= 10
        flags.append("Uses free email domain 🚩")

    score = max(score, 0)

    if score >= 80:
        risk = "Low"
    elif score >= 50:
        risk = "Medium"
    else:
        risk = "High"

    matched_words = matched_strong + matched_pressure + matched_mlm + matched_domains

    return {
        "score": score,
        "risk": risk,
        "flags": flags,
        "matched_words": matched_words
    }