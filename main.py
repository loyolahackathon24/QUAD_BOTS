import tkinter as tk
from tkinter import ttk, messagebox
from sentiment_analyzer import SentimentAnalyzer
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import os

class SentimentAnalyzerUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Twitter Sentiment Analyzer")
        self.root.geometry("800x600")
        
        # Initialize analyzer and train model
        self.analyzer = SentimentAnalyzer()
        self.load_and_train_model()
        
        # Create UI elements
        self.create_widgets()
    
    def load_and_train_model(self):
        """Load dataset and train the model"""
        try:
            if not os.path.exists("Tweets.csv"):
                messagebox.showerror("Error", "Tweets.csv file not found!")
                self.root.quit()
                return
            
            if not self.analyzer.load_and_train():
                messagebox.showerror("Error", "Failed to train model!")
                self.root.quit()
        except Exception as e:
            messagebox.showerror("Error", f"Error in training: {str(e)}")
            self.root.quit()
    
    def create_widgets(self):
        # Input Frame
        input_frame = ttk.LabelFrame(self.root, text="Enter Text to Analyze", padding="10")
        input_frame.pack(fill=tk.X, padx=10, pady=5)
        
        # Text input
        self.text_input = tk.Text(input_frame, height=4, width=50)
        self.text_input.pack(padx=5, pady=5)
        
        # Analyze button
        analyze_btn = ttk.Button(input_frame, text="Analyze Sentiment", command=self.analyze_text)
        analyze_btn.pack(pady=5)
        
        # Results Frame
        self.results_frame = ttk.LabelFrame(self.root, text="Analysis Results", padding="10")
        self.results_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        # Results display
        self.result_label = ttk.Label(self.results_frame, text="Enter text and click Analyze")
        self.result_label.pack(pady=10)
        
        # Confidence bars frame
        self.confidence_frame = ttk.Frame(self.results_frame)
        self.confidence_frame.pack(fill=tk.X, padx=5, pady=5)
        
        # Create progress bars for each sentiment
        self.create_confidence_bars()
        
        # Visualization frame
        self.viz_frame = ttk.LabelFrame(self.root, text="Sentiment Analysis Visualization")
        self.viz_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        # Create visualization button
        viz_btn = ttk.Button(self.root, text="Show Visualization", command=self.show_visualization)
        viz_btn.pack(pady=5)

    def create_confidence_bars(self):
        """Create progress bars for confidence scores"""
        self.confidence_bars = {}
        self.confidence_labels = {}
        
        for sentiment in ['positive', 'neutral', 'negative']:
            frame = ttk.Frame(self.confidence_frame)
            frame.pack(fill=tk.X, pady=2)
            
            # Label
            label = ttk.Label(frame, text=f"{sentiment.capitalize()}: ")
            label.pack(side=tk.LEFT, padx=5)
            
            # Progress bar
            bar = ttk.Progressbar(frame, length=300, mode='determinate')
            bar.pack(side=tk.LEFT, padx=5)
            
            # Percentage label
            pct_label = ttk.Label(frame, text="0%")
            pct_label.pack(side=tk.LEFT, padx=5)
            
            self.confidence_bars[sentiment] = bar
            self.confidence_labels[sentiment] = pct_label
    
    def analyze_text(self):
        """Analyze the input text and update visualizations"""
        text = self.text_input.get("1.0", tk.END).strip()
        
        if not text:
            messagebox.showwarning("Warning", "Please enter some text!")
            return
        
        result = self.analyzer.predict_sentiment(text)
        
        if result:
            # Update main result label
            sentiment = result['sentiment']
            confidence = result['confidence']
            self.result_label.config(
                text=f"Predicted Sentiment: {sentiment.upper()}\n"
                     f"Confidence: {confidence:.2%}"
            )
            
            # Update confidence bars
            for sentiment, prob in result['probabilities'].items():
                self.confidence_bars[sentiment]['value'] = prob * 100
                self.confidence_labels[sentiment].config(
                    text=f"{prob:.1%}"
                )
            
            # Update visualization
            self.show_visualization(text)
        else:
            messagebox.showerror("Error", "Failed to analyze text!")

    def show_visualization(self, text=None):
        """Display sentiment analysis visualizations"""
        # Clear previous visualization
        for widget in self.viz_frame.winfo_children():
            widget.destroy()
        
        # Create new visualization with input text
        fig = self.analyzer.create_visualization(text)
        if fig:
            canvas = FigureCanvasTkAgg(fig, master=self.viz_frame)
            canvas.draw()
            canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

def main():
    root = tk.Tk()
    app = SentimentAnalyzerUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()