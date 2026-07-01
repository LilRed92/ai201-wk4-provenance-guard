def calculate_confidence(llm_score, stylo_score):
    # Average (weighted) per planning.md: LLM 60%, stylometrics 40%
    return round((0.6 * llm_score) + (0.4 * stylo_score), 4)

def get_attribution(confidence):
    if confidence >= 0.70:
        return "likely_ai"
    elif confidence <= 0.35:
        return "likely_human"
    else:
        return "uncertain"