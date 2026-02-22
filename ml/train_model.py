import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import PassiveAggressiveClassifier
from sklearn.metrics import accuracy_score
import joblib

# 1. Load Data
print("Loading data...")
try:
    df = pd.read_csv("data/dataset.csv")
except FileNotFoundError:
    print("Error: Run setup_dataset.py first!")
    exit()

# 2. Split Data
x_train, x_test, y_train, y_test = train_test_split(df['title'], df['label'], test_size=0.2, random_state=7)

# 3. Vectorize Text (Convert text to numbers)
tfidf_vectorizer = TfidfVectorizer(stop_words='english', max_df=0.7)
tfidf_train = tfidf_vectorizer.fit_transform(x_train) 
tfidf_test = tfidf_vectorizer.transform(x_test)

# 4. Train Model
print("Training model...")
pac = PassiveAggressiveClassifier(max_iter=50)
pac.fit(tfidf_train, y_train)

# 5. Evaluate
y_pred = pac.predict(tfidf_test)
score = accuracy_score(y_test, y_pred)
print(f'Accuracy: {round(score*100,2)}%')

# 6. Save Pipeline
joblib.dump(pac, 'ml/model.pkl')
joblib.dump(tfidf_vectorizer, 'ml/vectorizer.pkl')
print("Model and Vectorizer saved in 'ml/' folder.")