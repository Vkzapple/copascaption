from pathlib import Path

import joblib
from flask import Flask, jsonify, request, send_from_directory

from content import HASHTAG_LIMITS, build_options

BASE_DIR = Path(__file__).parent
MODEL_PATH = BASE_DIR / "model.pkl"
MIN_CONFIDENCE = 0.25
MODES = {"topik", "foto"}

if not MODEL_PATH.exists():
    raise SystemExit("model.pkl belum ada. Jalankan dulu: python train_model.py")

model = joblib.load(MODEL_PATH)
app = Flask(__name__, static_folder=str(BASE_DIR / "static"), static_url_path="/static")


@app.get("/")
def index():
    return send_from_directory(app.static_folder, "index.html")


@app.post("/api/generate")
def generate():
    payload = request.get_json(silent=True) or {}
    topic = str(payload.get("topic", "")).strip()[:500]
    platform = payload.get("platform", "Instagram")
    mode = payload.get("mode", "topik")

    if len(topic) < 4:
        return jsonify(error="Topik terlalu pendek"), 400
    if platform not in HASHTAG_LIMITS:
        return jsonify(error="Platform tidak dikenal"), 400
    if mode not in MODES:
        return jsonify(error="Mode tidak dikenal"), 400

    probabilities = model.predict_proba([topic])[0]
    best = probabilities.argmax()
    category = model.classes_[best]
    confidence = float(probabilities[best])
    if confidence < MIN_CONFIDENCE:
        category = "lifestyle"

    return jsonify(
        platform=platform,
        mode=mode,
        topic=topic,
        category=category,
        confidence=round(confidence, 2),
        options=build_options(category, topic, platform, mode),
    )


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=False)
