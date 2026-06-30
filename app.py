import uuid
from datetime import datetime, timezone

from flask import Flask, jsonify, request
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

from auditor import read_entries, write_entry
from detector import classify_with_llm

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

    # Signal 2 and final scoring are added in Milestone 4 — placeholder for now
    stylo_score = 0.5
    confidence = round((0.6 * llm_score) + (0.4 * stylo_score), 4)

    if confidence >= 0.70:
        attribution = "likely_ai"
    elif confidence <= 0.35:
        attribution = "likely_human"
    else:
        attribution = "uncertain"

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
        },
    })


@app.route("/log", methods=["GET"])
def get_log():
    entries = read_entries(limit=50)
    return jsonify({"entries": entries})


if __name__ == "__main__":
    app.run(debug=True)