import joblib
import os

# Load model artifacts once
model_path = os.path.join(os.path.dirname(__file__), 'model.pkl')
vec_path = os.path.join(os.path.dirname(__file__), 'vectorizer.pkl')

model = joblib.load(model_path)
vectorizer = joblib.load(vec_path)

def predict_news(text):
    # Transform input
    tfidf_text = vectorizer.transform([text])
    # Predict
    prediction = model.predict(tfidf_text)[0] # 0 = Real, 1 = Fake
    # Get Confidence (Simple decision function distance for PA Classifier)
    confidence = abs(model.decision_function(tfidf_text)[0])
    
    # Normalize confidence roughly to 0-100%
    conf_score = min(confidence * 20 + 50, 99.9) 
    
    result = "Fake" if prediction == 1 else "Real"
    return result, conf_score