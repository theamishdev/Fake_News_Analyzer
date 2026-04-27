from flask import Flask, request, jsonify
import logging
import joblib
import os
import random

app = Flask(__name__)

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Global variables for model and vectorizer
model = None
vectorizer = None

def load_model():
    global model, vectorizer
    model_path = 'news_model.joblib'
    vectorizer_path = 'tfidf_vectorizer.joblib'
    
    if os.path.exists(model_path) and os.path.exists(vectorizer_path):
        logger.info("Loading trained model and vectorizer...")
        model = joblib.load(model_path)
        vectorizer = joblib.load(vectorizer_path)
    else:
        logger.warning("Model or vectorizer not found. Falling back to heuristic mode.")

# Initial model load
load_model()

@app.route('/predict', methods=['POST'])
def predict():
    global model, vectorizer
    data = request.json
    if not data or 'text' not in data:
        return jsonify({'error': 'No text provided'}), 400
    
    text = data['text']
    logger.info(f"Analyzing news: {text[:50]}...")
    
    if model and vectorizer:
        # --- ML Model Prediction ---
        # Transform the input text
        text_tfidf = vectorizer.transform([text])
        # Predict
        prediction = model.predict(text_tfidf)[0]
        # Get decision function for confidence (PAC doesn't have predict_proba)
        decision = model.decision_function(text_tfidf)[0]
        # Map decision to a pseudo-confidence (0.5 to 0.99)
        confidence = min(0.99, max(0.5, 0.5 + abs(decision) / 10))
        
        result = prediction
        logger.info(f"ML Prediction: {result} | Confidence: {confidence:.2f}")
        mode = "ML Model"
    else:
        # --- Fallback to Heuristic mode if training failed ---
        score = 0.0
        # ... (reuse the simplified heuristic from before)
        high_risk_keywords = ['conspiracy', 'illuminati', 'mind-control']
        for kw in high_risk_keywords:
            if kw in text.lower(): score += 0.5
        
        is_fake = score > 0.4
        result = "Fake" if is_fake else "Real"
        confidence = 0.75
        mode = "Heuristic (Fallback)"

    return jsonify({
        'result': result,
        'confidence': float(confidence),
        'model_version': '2.0.0',
        'prediction_mode': mode
    })

@app.route('/health', methods=['GET'])
def health():
    return jsonify({'status': 'healthy'})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
