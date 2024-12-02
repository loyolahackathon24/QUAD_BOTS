import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
import re

class SentimentAnalyzer:
    def __init__(self):
        self.data = None
        self.model = None
        self.vectorizer = None

    def load_and_train(self):
        """Load dataset and train the model"""
        try:
            # Load the CSV file
            self.data = pd.read_csv("Tweets.csv")
            print("Dataset loaded. Total tweets:", len(self.data))
            
            # Clean the data
            self.data = self.data.dropna()
            
            # Create vectorizer
            self.vectorizer = TfidfVectorizer(max_features=5000, stop_words='english', ngram_range=(1, 2))
            
            # Prepare features and target
            X = self.vectorizer.fit_transform(self.data['text'])
            y = self.data['sentiment']
            
            # Split the data
            X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
            
            # Train the model
            self.model = MultinomialNB()
            self.model.fit(X_train, y_train)
            
            # Evaluate the model
            y_pred = self.model.predict(X_test)
            accuracy = accuracy_score(y_test, y_pred)
            print(f"\nModel Training Results:")
            print(f"Accuracy: {accuracy:.2f}")
            print("\nDetailed Performance Report:")
            print(classification_report(y_test, y_pred))
            
            return True
            
        except Exception as e:
            print(f"Error in training: {str(e)}")
            return False

    def predict_sentiment(self, text):
        """Predict sentiment for given text"""
        if self.model is None or self.vectorizer is None:
            print("Model not trained. Please train the model first.")
            return None
        
        try:
            # Transform the text
            text_vectorized = self.vectorizer.transform([text])
            
            # Predict
            prediction = self.model.predict(text_vectorized)[0]
            probabilities = self.model.predict_proba(text_vectorized)[0]
            
            # Get confidence score
            confidence = max(probabilities)
            
            return {
                'sentiment': prediction,
                'confidence': confidence,
                'probabilities': {
                    'negative': probabilities[0],
                    'neutral': probabilities[1],
                    'positive': probabilities[2]
                }
            }
            
        except Exception as e:
            print(f"Error in prediction: {str(e)}")
            return None

    def create_visualization(self, input_text=None):
        """Create visualizations for sentiment analysis with live updates"""
        if input_text is None:
            return None
        
        fig = plt.figure(figsize=(10, 5))
        
        # 1. Word Distribution for Input Text
        ax1 = plt.subplot(121)
        words = input_text.split()
        word_freq = pd.Series(words).value_counts().head(10)
        word_freq.plot(kind='barh', ax=ax1, color='#3498db')
        ax1.set_title('Top Words in Your Text')
        ax1.set_xlabel('Frequency')
        
        # 2. Live Sentiment Prediction
        ax2 = plt.subplot(122)
        result = self.predict_sentiment(input_text)
        if result:
            probs = pd.Series(result['probabilities'])
            probs.plot(kind='bar', ax=ax2, color=['#2ecc71', '#e74c3c', '#3498db'])
            ax2.set_title('Sentiment Prediction Probabilities')
            ax2.set_ylabel('Probability')
        
        plt.tight_layout()
        return fig