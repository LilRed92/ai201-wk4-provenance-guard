import uuid
from datetime import datetime, timezone

from flask import Flask, jsonify, request
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

from auditor import read_entries, write_entry
from detector import classify_with_llm
from scorer import calculate_confidence, get_attribution
from stylometrics import analyze_stylometrics


app = Flask(__name__)

limiter = Limiter(
    get_remote_address,
    app=app,
    default_limits=[],
    storage_uri="memory://",
)


@app.route("/submit", methods=["POST"])
@limiter.limit("10 per minute;100 per day")
def submit():
    body = request.get_json(force=True)
    text = body.get("text", "").strip()
    creator_id = body.get("creator_id", "").strip()

    if not text or not creator_id:
        return jsonify({"error": "Both 'text' and 'creator_id' are required."}), 400

    content_id = str(uuid.uuid4())

    # Signal 1: Groq LLM classifier
    llm_score, llm_reasoning = classify_with_llm(text)

    # Signal 2: Stylometric scores
    stylo_score, stylo_breakdown = analyze_stylometrics(text)

    # Final combined score
    confidence = calculate_confidence(llm_score, stylo_score)
    attribution = get_attribution(confidence)


    # Transparency labels are implemented in Milestone 5 — placeholder for now
    label = "Transparency label coming in Milestone 5."

    entry = {
        "content_id": content_id,
        "creator_id": creator_id,
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "attribution": attribution,
        "confidence": confidence,
        "llm_score": llm_score,
        "stylo_score": stylo_score,
        "stylo_breakdown": stylo_breakdown,
        "status": "classified",
    }
    write_entry(entry)

    return jsonify({
        "content_id": content_id,
        "attribution": attribution,
        "confidence": confidence,
        "label": label,
        "signals": {
            "llm_score": llm_score,
            "llm_reasoning": llm_reasoning,
            "stylo_score": stylo_score,
            "stylo_breakdown": stylo_breakdown,
        },
    })


@app.route("/log", methods=["GET"])
def get_log():
    entries = read_entries(limit=50)
    return jsonify({"entries": entries})


if __name__ == "__main__":
    app.run(debug=True)