"""
Visualization Module
Task 2: Fintech Customer Experience Analytics

This script generates comprehensive EDA visualizations:
- Rating distribution per bank
- Average sentiment per bank
- Sentiment vs rating scatter plot
- Monthly sentiment trends
- Word cloud
- Top bigrams and trigrams
- TF-IDF keywords by bank
- LDA topic distribution

All visualizations saved to visuals/ directory as high-resolution PNG files.
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from wordcloud import WordCloud
from collections import Counter
import warnings
warnings.filterwarnings('ignore')

# Set style
sns.set_style("whitegrid")
plt.rcParams['figure.figsize'] = (12, 6)
plt.rcParams['figure.dpi'] = 300

# File paths
SENTIMENT_FILE = 'data/sentiment_results.csv'
TOPICS_FILE = 'data/topics_keywords.csv'
LDA_FILE = 'data/lda_topics.csv'
OUTPUT_DIR = 'visuals/'

# Color palette for banks
BANK_COLORS = {
    'Commercial Bank of Ethiopia': '#1f77b4',
    'Bank of Abyssinia': '#ff7f0e',
    'Dashen Bank': '#2ca02c'
}


def load_data():
    """Load all required data files."""
    print("Loading data files...")
    
    sentiment_df = pd.read_csv(SENTIMENT_FILE, encoding='utf-8')
    topics_df = pd.read_csv(TOPICS_FILE, encoding='utf-8')
    lda_df = pd.read_csv(LDA_FILE, encoding='utf-8')
    
    print(f"✓ Loaded {len(sentiment_df)} reviews with sentiment scores")
    print(f"✓ Loaded {len(topics_df)} topic keywords")
    print(f"✓ Loaded {len(lda_df)} LDA topic assignments")
    
    return sentiment_df, topics_df, lda_df


def plot_rating_distribution(df):
    """Generate rating distribution per bank."""
    print("\nGenerating rating distribution chart...")
    
    fig, ax = plt.subplots(figsize=(12, 6))
    
    # Prepare data for stacked bar chart
    rating_counts = df.groupby(['bank', 'rating']).size().unstack(fill_value=0)
    
    # Create stacked bar chart
    rating_counts.plot(
        kind='bar',
        stacked=True,
        ax=ax,
        color=['#d62728', '#ff7f0e', '#ffbb78', '#98df8a', '#2ca02c'],
        edgecolor='black',
        linewidth=0.5
    )
    
    ax.set_title('Rating Distribution by Bank', fontsize=16, fontweight='bold', pad=20)
    ax.set_xlabel('Bank', fontsize=12, fontweight='bold')
    ax.set_ylabel('Number of Reviews', fontsize=12, fontweight='bold')
    ax.legend(title='Rating (Stars)', bbox_to_anchor=(1.05, 1), loc='upper left')
    ax.set_xticklabels(ax.get_xticklabels(), rotation=45, ha='right')
    
    plt.tight_layout()
    plt.savefig(f'{OUTPUT_DIR}rating_distribution.png', dpi=300, bbox_inches='tight')
    plt.close()
    
    print(f"✓ Saved: {OUTPUT_DIR}rating_distribution.png")


def plot_sentiment_by_bank(df):
    """Generate average sentiment per bank bar chart."""
    print("\nGenerating sentiment by bank chart...")
    
    fig, axes = plt.subplots(1, 3, figsize=(16, 5))
    
    sentiment_metrics = ['vader_compound', 'textblob_polarity', 'afinn_score']
    titles = ['VADER Compound Score', 'TextBlob Polarity', 'Afinn Score']
    
    for idx, (metric, title) in enumerate(zip(sentiment_metrics, titles)):
        ax = axes[idx]
        
        # Calculate mean and std for each bank
        bank_stats = df.groupby('bank')[metric].agg(['mean', 'std']).reset_index()
        
        # Create bar chart
        bars = ax.bar(
            range(len(bank_stats)),
            bank_stats['mean'],
            yerr=bank_stats['std'],
            capsize=5,
            color=[BANK_COLORS.get(bank, '#gray') for bank in bank_stats['bank']],
            edgecolor='black',
            linewidth=1.5,
            alpha=0.8
        )
        
        ax.set_title(title, fontsize=12, fontweight='bold')
        ax.set_ylabel('Average Score', fontsize=10, fontweight='bold')
        ax.set_xticks(range(len(bank_stats)))
        ax.set_xticklabels([b.split()[0] for b in bank_stats['bank']], rotation=0)
        ax.axhline(y=0, color='black', linestyle='--', linewidth=0.8, alpha=0.5)
        ax.grid(axis='y', alpha=0.3)
    
    plt.suptitle('Average Sentiment Scores by Bank', fontsize=16, fontweight='bold', y=1.02)
    plt.tight_layout()
    plt.savefig(f'{OUTPUT_DIR}sentiment_by_bank.png', dpi=300, bbox_inches='tight')
    plt.close()
    
    print(f"✓ Saved: {OUTPUT_DIR}sentiment_by_bank.png")


def plot_sentiment_vs_rating(df):
    """Generate sentiment vs rating scatter plot."""
    print("\nGenerating sentiment vs rating scatter plot...")
    
    fig, ax = plt.subplots(figsize=(12, 7))
    
    # Create scatter plot for each bank
    for bank in df['bank'].unique():
        bank_data = df[df['bank'] == bank]
        ax.scatter(
            bank_data['rating'],
            bank_data['vader_compound'],
            label=bank.split()[0],  # Use short name
            alpha=0.5,
            s=30,
            color=BANK_COLORS.get(bank, '#gray')
        )
    
    # Add trend line (overall)
    z = np.polyfit(df['rating'], df['vader_compound'], 1)
    p = np.poly1d(z)
    x_trend = np.linspace(df['rating'].min(), df['rating'].max(), 100)
    ax.plot(x_trend, p(x_trend), "r--", linewidth=2, label='Trend Line', alpha=0.8)
    
    # Calculate correlation
    corr = df['rating'].corr(df['vader_compound'])
    
    ax.set_title(f'Sentiment vs Rating (Correlation: {corr:.3f})', 
                 fontsize=16, fontweight='bold', pad=20)
    ax.set_xlabel('Rating (Stars)', fontsize=12, fontweight='bold')
    ax.set_ylabel('VADER Sentiment Score', fontsize=12, fontweight='bold')
    ax.legend(loc='lower right', framealpha=0.9)
    ax.grid(alpha=0.3)
    ax.set_xticks([1, 2, 3, 4, 5])
    
    plt.tight_layout()
    plt.savefig(f'{OUTPUT_DIR}sentiment_vs_rating.png', dpi=300, bbox_inches='tight')
    plt.close()
    
    print(f"✓ Saved: {OUTPUT_DIR}sentiment_vs_rating.png")


def plot_monthly_sentiment_trends(df):
    """Generate monthly sentiment trends line chart."""
    print("\nGenerating monthly sentiment trends...")
    
    # Convert date to datetime and extract month
    df['date'] = pd.to_datetime(df['date'])
    df['month'] = df['date'].dt.to_period('M')
    
    # Calculate monthly average sentiment per bank
    monthly_data = df.groupby(['month', 'bank'])['vader_compound'].mean().reset_index()
    monthly_data['month'] = monthly_data['month'].astype(str)
    
    fig, ax = plt.subplots(figsize=(14, 6))
    
    # Plot line for each bank
    for bank in df['bank'].unique():
        bank_data = monthly_data[monthly_data['bank'] == bank]
        ax.plot(
            bank_data['month'],
            bank_data['vader_compound'],
            marker='o',
            label=bank.split()[0],
            linewidth=2.5,
            markersize=6,
            color=BANK_COLORS.get(bank, '#gray')
        )
    
    ax.set_title('Monthly Sentiment Trends by Bank', fontsize=16, fontweight='bold', pad=20)
    ax.set_xlabel('Month', fontsize=12, fontweight='bold')
    ax.set_ylabel('Average VADER Sentiment', fontsize=12, fontweight='bold')
    ax.legend(loc='best', framealpha=0.9)
    ax.grid(alpha=0.3)
    ax.axhline(y=0, color='black', linestyle='--', linewidth=0.8, alpha=0.5)
    
    # Rotate x-axis labels
    plt.xticks(rotation=45, ha='right')
    
    plt.tight_layout()
    plt.savefig(f'{OUTPUT_DIR}monthly_sentiment_trends.png', dpi=300, bbox_inches='tight')
    plt.close()
    
    print(f"✓ Saved: {OUTPUT_DIR}monthly_sentiment_trends.png")


def plot_wordcloud(df):
    """Generate word cloud from top 200 words."""
    print("\nGenerating word cloud...")
    
    # Combine all reviews
    all_text = ' '.join(df['review'].astype(str))
    
    # Create word cloud
    wordcloud = WordCloud(
        width=1600,
        height=800,
        background_color='white',
        colormap='viridis',
        max_words=200,
        relative_scaling=0.5,
        min_font_size=10
    ).generate(all_text)
    
    fig, ax = plt.subplots(figsize=(16, 8))
    ax.imshow(wordcloud, interpolation='bilinear')
    ax.axis('off')
    ax.set_title('Word Cloud - Top 200 Words', fontsize=18, fontweight='bold', pad=20)
    
    plt.tight_layout()
    plt.savefig(f'{OUTPUT_DIR}wordcloud.png', dpi=300, bbox_inches='tight')
    plt.close()
    
    print(f"✓ Saved: {OUTPUT_DIR}wordcloud.png")


def plot_top_bigrams_trigrams(topics_df):
    """Generate top bigrams and trigrams bar charts."""
    print("\nGenerating bigrams and trigrams charts...")
    
    # Extract bigrams and trigrams
    bigrams = topics_df[(topics_df['model'] == 'Bigram') & (topics_df['topic_id'] == 'phrases')]
    trigrams = topics_df[(topics_df['model'] == 'Trigram') & (topics_df['topic_id'] == 'phrases')]
    
    # Sort and get top 15
    bigrams = bigrams.nlargest(15, 'weight')
    trigrams = trigrams.nlargest(15, 'weight')
    
    # Create subplots
    fig, axes = plt.subplots(1, 2, figsize=(16, 6))
    
    # Plot bigrams
    if not bigrams.empty:
        ax = axes[0]
        bigrams_sorted = bigrams.sort_values('weight')
        ax.barh(
            range(len(bigrams_sorted)),
            bigrams_sorted['weight'],
            color='steelblue',
            edgecolor='black',
            linewidth=0.5
        )
        ax.set_yticks(range(len(bigrams_sorted)))
        ax.set_yticklabels([w.replace('_', ' ') for w in bigrams_sorted['word']])
        ax.set_xlabel('Frequency', fontsize=11, fontweight='bold')
        ax.set_title('Top 15 Bigrams', fontsize=13, fontweight='bold')
        ax.grid(axis='x', alpha=0.3)
    
    # Plot trigrams
    if not trigrams.empty:
        ax = axes[1]
        trigrams_sorted = trigrams.sort_values('weight')
        ax.barh(
            range(len(trigrams_sorted)),
            trigrams_sorted['weight'],
            color='coral',
            edgecolor='black',
            linewidth=0.5
        )
        ax.set_yticks(range(len(trigrams_sorted)))
        ax.set_yticklabels([w.replace('_', ' ') for w in trigrams_sorted['word']])
        ax.set_xlabel('Frequency', fontsize=11, fontweight='bold')
        ax.set_title('Top 15 Trigrams', fontsize=13, fontweight='bold')
        ax.grid(axis='x', alpha=0.3)
    
    plt.suptitle('Most Common Phrases in Reviews', fontsize=16, fontweight='bold', y=1.02)
    plt.tight_layout()
    plt.savefig(f'{OUTPUT_DIR}top_bigrams_trigrams.png', dpi=300, bbox_inches='tight')
    plt.close()
    
    print(f"✓ Saved: {OUTPUT_DIR}top_bigrams_trigrams.png")


def plot_tfidf_keywords_by_bank(topics_df, sentiment_df):
    """Generate TF-IDF keywords by bank."""
    print("\nGenerating TF-IDF keywords by bank chart...")
    
    # Get bank names
    banks = sentiment_df['bank'].unique()
    
    fig, axes = plt.subplots(1, 3, figsize=(18, 6))
    
    for idx, bank in enumerate(banks):
        ax = axes[idx]
        
        # Get top keywords for this bank
        bank_keywords = topics_df[
            (topics_df['model'] == 'TF-IDF') & 
            (topics_df['topic_id'] == bank)
        ].nlargest(10, 'weight')
        
        if not bank_keywords.empty:
            bank_keywords_sorted = bank_keywords.sort_values('weight')
            
            ax.barh(
                range(len(bank_keywords_sorted)),
                bank_keywords_sorted['weight'],
                color=BANK_COLORS.get(bank, '#gray'),
                edgecolor='black',
                linewidth=0.5,
                alpha=0.8
            )
            ax.set_yticks(range(len(bank_keywords_sorted)))
            ax.set_yticklabels(bank_keywords_sorted['word'])
            ax.set_xlabel('TF-IDF Score', fontsize=10, fontweight='bold')
            ax.set_title(bank.split()[0], fontsize=12, fontweight='bold')
            ax.grid(axis='x', alpha=0.3)
    
    plt.suptitle('Top TF-IDF Keywords by Bank', fontsize=16, fontweight='bold', y=1.02)
    plt.tight_layout()
    plt.savefig(f'{OUTPUT_DIR}tfidf_keywords_by_bank.png', dpi=300, bbox_inches='tight')
    plt.close()
    
    print(f"✓ Saved: {OUTPUT_DIR}tfidf_keywords_by_bank.png")


def plot_lda_topic_distribution(lda_df):
    """Generate LDA topic distribution chart."""
    print("\nGenerating LDA topic distribution...")
    
    # Calculate topic distribution
    topic_counts = lda_df['lda_topic'].value_counts().sort_index()
    
    fig, axes = plt.subplots(1, 2, figsize=(16, 6))
    
    # Pie chart
    ax = axes[0]
    colors = plt.cm.Set3(range(len(topic_counts)))
    ax.pie(
        topic_counts,
        labels=[f'Topic {i}' for i in topic_counts.index],
        autopct='%1.1f%%',
        startangle=90,
        colors=colors,
        textprops={'fontsize': 11, 'fontweight': 'bold'}
    )
    ax.set_title('Topic Distribution (LDA)', fontsize=14, fontweight='bold')
    
    # Bar chart
    ax = axes[1]
    ax.bar(
        [f'Topic {i}' for i in topic_counts.index],
        topic_counts.values,
        color=colors,
        edgecolor='black',
        linewidth=1.5,
        alpha=0.8
    )
    ax.set_ylabel('Number of Reviews', fontsize=11, fontweight='bold')
    ax.set_title('Topic Prevalence', fontsize=14, fontweight='bold')
    ax.grid(axis='y', alpha=0.3)
    
    plt.suptitle('LDA Topic Analysis', fontsize=16, fontweight='bold', y=1.02)
    plt.tight_layout()
    plt.savefig(f'{OUTPUT_DIR}lda_topic_distribution.png', dpi=300, bbox_inches='tight')
    plt.close()
    
    print(f"✓ Saved: {OUTPUT_DIR}lda_topic_distribution.png")


def main():
    """Main function to generate all visualizations."""
    print("\n" + "="*60)
    print("VISUALIZATION GENERATION")
    print("Task 2: Ethiopian Banking Apps")
    print("="*60 + "\n")
    
    # Load data
    sentiment_df, topics_df, lda_df = load_data()
    
    # Generate visualizations
    plot_rating_distribution(sentiment_df)
    plot_sentiment_by_bank(sentiment_df)
    plot_sentiment_vs_rating(sentiment_df)
    plot_monthly_sentiment_trends(sentiment_df)
    plot_wordcloud(sentiment_df)
    plot_top_bigrams_trigrams(topics_df)
    plot_tfidf_keywords_by_bank(topics_df, sentiment_df)
    plot_lda_topic_distribution(lda_df)
    
    print("\n" + "="*60)
    print("✓ All visualizations generated successfully!")
    print(f"  Output directory: {OUTPUT_DIR}")
    print(f"  Total charts: 8")
    print("="*60 + "\n")


if __name__ == "__main__":
    main()
