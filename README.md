# QUAD_BOTS

# Twitter Sentiment Analyzer

A Python application that performs sentiment analysis on text input using machine learning. The application provides a graphical user interface for real-time sentiment prediction and visualization.

## Features
- Real-time sentiment analysis of text input
- Visual representation of sentiment probabilities
- Word frequency analysis
- User-friendly GUI interface

## Installation

1. Clone the repository:
2. Install required packages:

3. Ensure you have the dataset file `Tweets.csv` in the project directory.

## Usage

1. Run the application:


2. The application will:
   - Load and train the model using the Twitter dataset
   - Open a GUI window for text input and analysis

3. To analyze text:
   - Enter text in the input box
   - Click "Analyze Sentiment"
   - View results and visualizations

## Project Structure

- `main.py`: GUI implementation and application entry point
- `sentiment_analyzer.py`: Core sentiment analysis functionality
- `Tweets.csv`: Training dataset

## Code References

### Main Application (main.py)

### Sentiment Analyzer (sentiment_analyzer.py)


## Model Details

The sentiment analyzer uses:
- TF-IDF Vectorization for text feature extraction
- Multinomial Naive Bayes classifier
- Training-test split ratio: 80:20

## Output Format

The analyzer provides:
- Sentiment prediction (Positive/Negative/Neutral)
- Confidence scores
- Word frequency visualization
- Sentiment probability distribution

## Error Handling

The application includes error handling for:
- Missing dataset file
- Model training failures
- Invalid input text
- Prediction errors

## Dependencies
- pandas
- numpy
- scikit-learn
- matplotlib
- seaborn
- tkinter
