import math
import re

def _sentence_length_variance_score(text):
    sentences = re.split(r'[.!?]+', text)
    sentences = [s.strip() for s in sentences if s.strip()]

    if len(sentences) < 2:
        return 0.5

    lengths = [len(s.split()) for s in sentences]
    mean = sum(lengths) / len(lengths)
    variance = sum((l - mean) ** 2 for l in lengths) / len(lengths)
    stddev = math.sqrt(variance)

    # Human likeness = high variance = lower score
    # Capped stddev at 15 max human variance
    normalized = min(stddev / 15.0, 1.0)
    return round(1.0 - normalized, 4)

def _type_token_ratio_score(text):
    words = re.findall(r'\b[a-zA-Z]+\b', text.lower())
    if not words:
        return 0.5

    # Human likeness = diverse vocabulary = lower score
    ttr = len(set(words)) / len(words)
    return round(1.0 - ttr, 4)

def _punctuation_density_score(text):
    words = text.split()
    if not words:
        return 0.5

    punct_chars = set('.,!?;:—–-…()[]{}"\"')
    punct_count = sum(1 for char in text if char in punct_chars)
    density = punct_count / len(words)

    # Human likeness = high or varied punctuation = lower score
    # Capped at 0.5 density for human scores
    normalized = min(density / 0.5, 1.0)
    return round(1.0 - normalized, 4)

def analyze_stylometrics(text):
    slv = _sentence_length_variance_score(text)
    ttr = _type_token_ratio_score(text)
    pd = _punctuation_density_score(text)

    # Average weighted score as per planning.md: SLV 55%, TTR 20%, PD 25%
    stylo_score = round((0.55 * slv) + (0.2 * ttr) + (0.25 * pd), 4)
    return stylo_score, {"slv": slv, "ttr": ttr, "pd": pd}