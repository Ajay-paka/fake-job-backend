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

    # ---- MATCHES ----
    matched_strong = [word for word in strong_scam if word in text]
    matched_pressure = [word for word in pressure_phrases if word in text]
    matched_mlm = [word for word in mlm_style if word in text]
    matched_domains = [domain for domain in free_domains if domain in text]

    # ---- PENALTIES WITH CAPS ----
    strong_penalty = min(25 * len(matched_strong), 50)
    pressure_penalty = min(10 * len(matched_pressure), 30)
    mlm_penalty = min(5 * len(matched_mlm), 20)
    domain_penalty = min(10 * len(matched_domains), 20)

    total_penalty = strong_penalty + pressure_penalty + mlm_penalty + domain_penalty

    score -= total_penalty

    # ---- MINIMUM SCORE LIMIT (Never below 20) ----
    score = max(score, 20)

    # ---- FLAGS ----
    if matched_strong:
        flags.append("Strong scam indicators detected 🚩")

    if matched_pressure:
        flags.append("Uses urgency / pressure tactics 🚩")

    if matched_mlm:
        flags.append("Marketing/MLM-style language detected 🚩")

    if matched_domains:
        flags.append("Uses free email domain 🚩")

    # ---- RISK CLASSIFICATION ----
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