import pandas as pd
import numpy as np
import joblib
import os
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import PassiveAggressiveClassifier
from sklearn.metrics import accuracy_score, confusion_matrix
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def train():
    try:
        # 1. Load the dataset
        logger.info("Loading datasets...")
        fake_path = 'dataset/Fake.csv'
        true_path = 'dataset/True.csv'
        
        if not os.path.exists(fake_path) or not os.path.exists(true_path):
            logger.error("Dataset files not found in dataset/ folder.")
            return

        fake_df = pd.read_csv(fake_path)
        true_df = pd.read_csv(true_path)

        # 2. Add labels
        fake_df['label'] = 'Fake'
        true_df['label'] = 'Real'

        # 3. Combine and shuffle
        df = pd.concat([fake_df, true_df]).sample(frac=1).reset_index(drop=True)
        
        # Use a subset if the dataset is too large (optimization for speed)
        # For this demo, let's use 20,000 samples if it's much larger
        if len(df) > 20000:
            logger.info("Using a subset of 20,000 samples for faster training.")
            df = df.head(20000)

        logger.info(f"Dataset loaded. Total samples: {len(df)}")

        # 4. Extract features and labels
        # We'll combine title and text for better performance
        x = df['title'] + " " + df['text']
        y = df['label']

        # 5. Split the dataset
        x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2, random_state=42)

        # 6. Initialize TfidfVectorizer
        logger.info("Vectorizing text...")
        tfidf_vectorizer = TfidfVectorizer(stop_words='english', max_df=0.7)

        # Fit and transform the training set
        tfidf_train = tfidf_vectorizer.fit_transform(x_train)
        tfidf_test = tfidf_vectorizer.transform(x_test)

        # 7. Initialize and train PassiveAggressiveClassifier
        # This is great for large text datasets
        logger.info("Training model...")
        pac = PassiveAggressiveClassifier(max_iter=50)
        pac.fit(tfidf_train, y_train)

        # 8. Evaluate
        y_pred = pac.predict(tfidf_test)
        score = accuracy_score(y_test, y_pred)
        logger.info(f"Training complete. Accuracy: {score*100:.2f}%")

        # 9. Save the model and vectorizer
        logger.info("Saving model and vectorizer...")
        joblib.dump(pac, 'news_model.joblib')
        joblib.dump(tfidf_vectorizer, 'tfidf_vectorizer.joblib')
        
        logger.info("Model saved as news_model.joblib and tfidf_vectorizer.joblib")

    except Exception as e:
        logger.error(f"An error occurred during training: {str(e)}")

if __name__ == "__main__":
    train()
