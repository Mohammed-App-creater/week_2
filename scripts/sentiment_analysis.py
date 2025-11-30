"""
Sentiment Analysis Module
Task 2: Fintech Customer Experience Analytics

This script performs comprehensive sentiment analysis on Ethiopian banking app reviews using:
- VADER (Valence Aware Dictionary and sEntiment Reasoner)
- TextBlob
- Afinn

Outputs:
- sentiment_results.csv: Reviews with sentiment scores
- Aggregated insights by bank, rating, and month
"""

import pandas as pd
import numpy as np
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from textblob import TextBlob
from afinn import Afinn
from datetime import datetime
import warnings
warnings.filterwarnings('ignore')

# File paths
INPUT_FILE = 'data/bank_reviews_clean.csv'
OUTPUT_FILE = 'data/sentiment_results.csv'


def load_data(filepath):
    """Load cleaned review data."""
    print(f"Loading data from: {filepath}")
    df = pd.read_csv(filepath, encoding='utf-8')
    print(f"✓ Loaded {len(df)} reviews")
    print(f"  Columns: {list(df.columns)}")
    return df


def apply_vader_sentiment(df):
    """
    Apply VADER sentiment analysis.
    
    VADER is specifically designed for social media text and works well with
    short reviews. Returns compound score (-1 to 1).
    """
    print("\nApplying VADER sentiment analysis...")
    
    analyzer = SentimentIntensityAnalyzer()
    
    def get_vader_scores(text):
        """Get VADER sentiment scores for a single text."""
        if pd.isnull(text) or text == "":
            return 0.0
        
        scores = analyzer.polarity_scores(str(text))
        return scores['compound']
    
    df['vader_compound'] = df['review'].apply(get_vader_scores)
    
    print(f"✓ VADER analysis complete")
    print(f"  Mean compound score: {df['vader_compound'].mean():.3f}")
    print(f"  Score range: [{df['vader_compound'].min():.3f}, {df['vader_compound'].max():.3f}]")
    
    return df


def apply_textblob_sentiment(df):
    """
    Apply TextBlob sentiment analysis.
    
    TextBlob provides polarity (-1 to 1) and subjectivity (0 to 1).
    Polarity: negative to positive
    Subjectivity: objective to subjective
    """
    print("\nApplying TextBlob sentiment analysis...")
    
    def get_textblob_scores(text):
        """Get TextBlob sentiment scores for a single text."""
        if pd.isnull(text) or text == "":
            return 0.0, 0.0
        
        blob = TextBlob(str(text))
        return blob.sentiment.polarity, blob.sentiment.subjectivity
    
    # Apply TextBlob and split into two columns
    textblob_scores = df['review'].apply(get_textblob_scores)
    df['textblob_polarity'] = textblob_scores.apply(lambda x: x[0])
    df['textblob_subjectivity'] = textblob_scores.apply(lambda x: x[1])
    
    print(f"✓ TextBlob analysis complete")
    print(f"  Mean polarity: {df['textblob_polarity'].mean():.3f}")
    print(f"  Mean subjectivity: {df['textblob_subjectivity'].mean():.3f}")
    
    return df


def apply_afinn_sentiment(df):
    """
    Apply Afinn sentiment analysis.
    
    Afinn uses a lexicon-based approach with scores typically ranging from -5 to 5.
    """
    print("\nApplying Afinn sentiment analysis...")
    
    afinn = Afinn()
    
    def get_afinn_score(text):
        """Get Afinn sentiment score for a single text."""
        if pd.isnull(text) or text == "":
            return 0.0
        
        return afinn.score(str(text))
    
    df['afinn_score'] = df['review'].apply(get_afinn_score)
    
    print(f"✓ Afinn analysis complete")
    print(f"  Mean score: {df['afinn_score'].mean():.3f}")
    print(f"  Score range: [{df['afinn_score'].min():.3f}, {df['afinn_score'].max():.3f}]")
    
    return df


def compute_aggregated_insights(df):
    """Compute aggregated sentiment insights."""
    print("\n" + "="*60)
    print("AGGREGATED SENTIMENT INSIGHTS")
    print("="*60)
    
    # 1. Overall sentiment per bank
    print("\n1. OVERALL SENTIMENT PER BANK")
    print("-" * 60)
    
    bank_sentiment = df.groupby('bank').agg({
        'vader_compound': ['mean', 'std', 'min', 'max'],
        'textblob_polarity': ['mean', 'std'],
        'afinn_score': ['mean', 'std'],
        'rating': ['mean', 'count']
    }).round(3)
    
    print(bank_sentiment)
    
    # Identify most positive and negative banks
    vader_by_bank = df.groupby('bank')['vader_compound'].mean().sort_values(ascending=False)
    print(f"\n✓ Most positive bank (VADER): {vader_by_bank.index[0]} ({vader_by_bank.iloc[0]:.3f})")
    print(f"✓ Most negative bank (VADER): {vader_by_bank.index[-1]} ({vader_by_bank.iloc[-1]:.3f})")
    
    # Most controversial (highest variance)
    vader_std = df.groupby('bank')['vader_compound'].std().sort_values(ascending=False)
    print(f"✓ Most controversial bank (highest variance): {vader_std.index[0]} (std: {vader_std.iloc[0]:.3f})")
    
    # 2. Sentiment by rating
    print("\n2. SENTIMENT BY RATING")
    print("-" * 60)
    
    rating_sentiment = df.groupby('rating').agg({
        'vader_compound': 'mean',
        'textblob_polarity': 'mean',
        'afinn_score': 'mean',
        'review': 'count'
    }).round(3)
    rating_sentiment.columns = ['VADER', 'TextBlob', 'Afinn', 'Count']
    
    print(rating_sentiment)
    
    # 3. Correlation between rating and sentiment
    print("\n3. CORRELATION: RATING vs SENTIMENT")
    print("-" * 60)
    
    correlations = {
        'VADER Compound': df['rating'].corr(df['vader_compound']),
        'TextBlob Polarity': df['rating'].corr(df['textblob_polarity']),
        'Afinn Score': df['rating'].corr(df['afinn_score'])
    }
    
    for metric, corr in correlations.items():
        print(f"  {metric}: {corr:.3f}")
    
    # 4. Sentiment by month
    print("\n4. SENTIMENT BY MONTH")
    print("-" * 60)
    
    # Extract month from date
    df['month'] = pd.to_datetime(df['date']).dt.to_period('M')
    
    monthly_sentiment = df.groupby('month').agg({
        'vader_compound': 'mean',
        'textblob_polarity': 'mean',
        'afinn_score': 'mean',
        'review': 'count'
    }).round(3)
    monthly_sentiment.columns = ['VADER', 'TextBlob', 'Afinn', 'Count']
    
    print(monthly_sentiment.tail(10))  # Show last 10 months
    
    # 5. Sentiment by bank and rating
    print("\n5. SENTIMENT BY BANK AND RATING")
    print("-" * 60)
    
    bank_rating_sentiment = df.groupby(['bank', 'rating'])['vader_compound'].mean().round(3)
    print(bank_rating_sentiment)
    
    print("\n" + "="*60)
    
    return df


def save_results(df, filepath):
    """Save sentiment results to CSV."""
    # Drop the temporary month column if it exists
    if 'month' in df.columns:
        df_output = df.drop('month', axis=1)
    else:
        df_output = df.copy()
    
    df_output.to_csv(filepath, index=False, encoding='utf-8')
    print(f"\n✓ Sentiment results saved to: {filepath}")
    print(f"  Total rows: {len(df_output)}")
    print(f"  Columns: {list(df_output.columns)}")


def generate_summary_statistics(df):
    """Generate summary statistics for the report."""
    print("\n" + "="*60)
    print("SUMMARY STATISTICS")
    print("="*60)
    
    print(f"\nDataset Overview:")
    print(f"  Total reviews: {len(df)}")
    print(f"  Date range: {df['date'].min()} to {df['date'].max()}")
    print(f"  Banks: {df['bank'].nunique()}")
    
    print(f"\nSentiment Score Distributions:")
    print(f"  VADER Compound:")
    print(f"    Mean: {df['vader_compound'].mean():.3f}")
    print(f"    Median: {df['vader_compound'].median():.3f}")
    print(f"    Std Dev: {df['vader_compound'].std():.3f}")
    
    print(f"  TextBlob Polarity:")
    print(f"    Mean: {df['textblob_polarity'].mean():.3f}")
    print(f"    Median: {df['textblob_polarity'].median():.3f}")
    print(f"    Std Dev: {df['textblob_polarity'].std():.3f}")
    
    print(f"  Afinn Score:")
    print(f"    Mean: {df['afinn_score'].mean():.3f}")
    print(f"    Median: {df['afinn_score'].median():.3f}")
    print(f"    Std Dev: {df['afinn_score'].std():.3f}")
    
    # Sentiment categories (based on VADER)
    df['sentiment_category'] = pd.cut(
        df['vader_compound'],
        bins=[-1, -0.05, 0.05, 1],
        labels=['Negative', 'Neutral', 'Positive']
    )
    
    print(f"\nSentiment Categories (VADER-based):")
    sentiment_dist = df['sentiment_category'].value_counts()
    for category, count in sentiment_dist.items():
        pct = (count / len(df)) * 100
        print(f"  {category}: {count} ({pct:.1f}%)")
    
    print("="*60 + "\n")


def main():
    """Main function to orchestrate sentiment analysis."""
    print("\n" + "="*60)
    print("SENTIMENT ANALYSIS")
    print("Task 2: Ethiopian Banking Apps")
    print("="*60 + "\n")
    
    # Load data
    df = load_data(INPUT_FILE)
    
    # Apply sentiment analysis tools
    df = apply_vader_sentiment(df)
    df = apply_textblob_sentiment(df)
    df = apply_afinn_sentiment(df)
    
    # Compute aggregated insights
    df = compute_aggregated_insights(df)
    
    # Generate summary statistics
    generate_summary_statistics(df)
    
    # Save results
    save_results(df, OUTPUT_FILE)
    
    print("\n✓ Sentiment analysis complete!")
    print(f"  Output file: {OUTPUT_FILE}")
    print(f"  New columns added: vader_compound, textblob_polarity, textblob_subjectivity, afinn_score\n")


if __name__ == "__main__":
    main()
