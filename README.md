# CopasCaptionPop🌸✨

A cute pink and yellow yups yups **caption & hashtag generator**.
Enter a topic or a photo description, pick a platform (Instagram, LinkedIn, or X), and get **3 caption options with hashtags** as JSON. No API key, no internet, just a local (traditional) AI model `model.pkl` LMAO.

## Features

- Topic or photo-description input
- Platform-aware output for Instagram, LinkedIn, and X
- 3 options per request: playful, storytelling, and punchy
- Hashtags built from your keywords plus a category pool
- Raw JSON view and one-click copy
- Light and dark mode

## How it works

1. `model.pkl` is a scikit-learn pipeline (TF-IDF + Logistic Regression) that classifies the input into a category: food, travel, fashion, career, tech, fitness, business, or lifestyle.
2. `content.py` fills caption templates for that category and adapts them to the chosen platform:
   - **Instagram**: emojis, up to 10 hashtags, photo-style openers in photo mode
   - **LinkedIn**: no emojis, a discussion closer, 5 hashtags
   - **X**: caption plus hashtags kept under 280 characters, 2 hashtags
3. `app.py` exposes the result through a small Flask API.

> The model classifies the topic and the captions come from templates, so output is consistent but not freely generated like an LLM. The training data and captions are in Indonesian, so write your input in Indonesian for the best results.

