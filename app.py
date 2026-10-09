from pathlib import Path

import joblib
from flask import Flask, jsonify, request, send_from_directory

from content import HASHTAG_LIMITS, LANGUAGES, build_options

BASE_DIR = Path(__file__).parent
MODEL_PATH = BASE_DIR / "model.pkl"
MIN_CONFIDENCE = 0.25
MODES = {"topic", "photo"}


def load_models():
    if not MODEL_PATH.exists():
        raise SystemExit("model.pkl not found. Run: python train_model.py")
    bundle = joblib.load(MODEL_PATH)
    if not isinstance(bundle, dict) or {"category", "language"} - bundle.keys():
        raise SystemExit("model.pkl is outdated. Re-run: python train_model.py")
    return bundle["category"], bundle["language"]


category_model, language_model = load_models()
app = Flask(__name__, static_folder=str(BASE_DIR / "static"), static_url_path="/static")


def detect_language(topic, requested):
    if requested in LANGUAGES:
        return requested
    return str(language_model.predict([topic])[0])


def detect_category(topic):
    probabilities = category_model.predict_proba([topic])[0]
    best = probabilities.argmax()
    confidence = float(probabilities[best])
    if confidence < MIN_CONFIDENCE:
        return "lifestyle", confidence
    return str(category_model.classes_[best]), confidence


@app.get("/")
def index():
    return send_from_directory(app.static_folder, "index.html")


@app.post("/api/generate")
def generate():
    payload = request.get_json(silent=True) or {}
    topic = str(payload.get("topic", "")).strip()[:500]
    platform = payload.get("platform", "Instagram")
    mode = payload.get("mode", "topic")
    requested_lang = payload.get("lang", "auto")

    if len(topic) < 4:
        return jsonify(error="Topic is too short"), 400
    if platform not in HASHTAG_LIMITS:
        return jsonify(error="Unknown platform"), 400
    if mode not in MODES:
        return jsonify(error="Unknown mode"), 400

    lang = detect_language(topic, requested_lang)
    category, confidence = detect_category(topic)

    return jsonify(
        platform=platform,
        mode=mode,
        language=lang,
        topic=topic,
        category=category,
        confidence=round(confidence, 2),
        options=build_options(category, topic, platform, mode, lang),
    )


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=False)