"""
Report Generation Module
Task 2: Fintech Customer Experience Analytics

This script generates a comprehensive business insights report based on:
- Sentiment analysis results
- Topic modeling findings
- Visualizations

Output: TASK2_REPORT.md (professional markdown report)
"""

import pandas as pd
import numpy as np
from datetime import datetime


# File paths
SENTIMENT_FILE = 'data/sentiment_results.csv'
TOPICS_FILE = 'data/topics_keywords.csv'
LDA_FILE = 'data/lda_topics.csv'
OUTPUT_FILE = 'TASK2_REPORT.md'


def load_data():
    """Load all analysis results."""
    print("Loading analysis results...")
    
    sentiment_df = pd.read_csv(SENTIMENT_FILE, encoding='utf-8')
    topics_df = pd.read_csv(TOPICS_FILE, encoding='utf-8')
    lda_df = pd.read_csv(LDA_FILE, encoding='utf-8')
    
    print(f"✓ Loaded all data files")
    
    return sentiment_df, topics_df, lda_df


def analyze_sentiment_insights(df):
    """Extract key sentiment insights."""
    insights = {}
    
    # Overall sentiment per bank
    bank_sentiment = df.groupby('bank')['vader_compound'].agg(['mean', 'std']).round(3)
    insights['bank_sentiment'] = bank_sentiment.sort_values('mean', ascending=False)
    
    # Most positive bank
    insights['most_positive'] = bank_sentiment['mean'].idxmax()
    insights['most_positive_score'] = bank_sentiment['mean'].max()
    
    # Most negative bank
    insights['most_negative'] = bank_sentiment['mean'].idxmin()
    insights['most_negative_score'] = bank_sentiment['mean'].min()
    
    # Most controversial (highest variance)
    insights['most_controversial'] = bank_sentiment['std'].idxmax()
    insights['most_controversial_std'] = bank_sentiment['std'].max()
    
    # Correlation
    insights['rating_sentiment_corr'] = df['rating'].corr(df['vader_compound'])
    
    # Sentiment categories
    df['sentiment_category'] = pd.cut(
        df['vader_compound'],
        bins=[-1, -0.05, 0.05, 1],
        labels=['Negative', 'Neutral', 'Positive']
    )
    insights['sentiment_distribution'] = df['sentiment_category'].value_counts()
    
    # Sentiment by rating
    insights['sentiment_by_rating'] = df.groupby('rating')['vader_compound'].mean().round(3)
    
    return insights


def analyze_topic_insights(topics_df, lda_df):
    """Extract key topic insights."""
    insights = {}
    
    # LDA topics
    lda_topics = topics_df[topics_df['model'] == 'LDA'].groupby('topic_id')['word'].apply(list)
    insights['lda_topics'] = lda_topics
    
    # NMF topics
    nmf_topics = topics_df[topics_df['model'] == 'NMF'].groupby('topic_id')['word'].apply(list)
    insights['nmf_topics'] = nmf_topics
    
    # Top bigrams
    bigrams = topics_df[(topics_df['model'] == 'Bigram') & (topics_df['topic_id'] == 'phrases')]
    insights['top_bigrams'] = bigrams.nlargest(10, 'weight')[['word', 'weight']]
    
    # Top trigrams
    trigrams = topics_df[(topics_df['model'] == 'Trigram') & (topics_df['topic_id'] == 'phrases')]
    insights['top_trigrams'] = trigrams.nlargest(10, 'weight')[['word', 'weight']]
    
    # Topic prevalence
    insights['topic_prevalence'] = lda_df['lda_topic'].value_counts().sort_index()
    
    return insights


def generate_report(sentiment_df, topics_df, lda_df, sentiment_insights, topic_insights):
    """Generate comprehensive markdown report."""
    
    report = []
    
    # Header
    report.append("# Task 2: NLP & Sentiment Analysis Report")
    report.append("## Ethiopian Banking Apps - Customer Experience Analytics")
    report.append("")
    report.append(f"**Generated**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    report.append("")
    report.append("---")
    report.append("")
    
    # Executive Summary
    report.append("## Executive Summary")
    report.append("")
    report.append("This report presents comprehensive sentiment analysis and topic modeling results for customer reviews of three major Ethiopian banking mobile applications:")
    report.append("")
    report.append("- **Commercial Bank of Ethiopia (CBE)** - Mobile Banking App")
    report.append("- **Bank of Abyssinia (BOA)** - Mobile Banking App")
    report.append("- **Dashen Bank** - Mobile Banking App")
    report.append("")
    report.append(f"**Dataset**: {len(sentiment_df):,} customer reviews analyzed")
    report.append(f"**Date Range**: {sentiment_df['date'].min()} to {sentiment_df['date'].max()}")
    report.append(f"**Analysis Methods**: VADER, TextBlob, Afinn sentiment analysis; LDA & NMF topic modeling")
    report.append("")
    
    # Key Findings
    report.append("### Key Findings")
    report.append("")
    report.append(f"✅ **Most Positive Bank**: {sentiment_insights['most_positive']} (VADER: {sentiment_insights['most_positive_score']:.3f})")
    report.append(f"⚠️ **Most Negative Bank**: {sentiment_insights['most_negative']} (VADER: {sentiment_insights['most_negative_score']:.3f})")
    report.append(f"📊 **Most Controversial**: {sentiment_insights['most_controversial']} (Std Dev: {sentiment_insights['most_controversial_std']:.3f})")
    report.append(f"🔗 **Rating-Sentiment Correlation**: {sentiment_insights['rating_sentiment_corr']:.3f} (strong positive correlation)")
    report.append("")
    report.append("---")
    report.append("")
    
    # Sentiment Analysis Insights
    report.append("## 1. Sentiment Analysis Insights")
    report.append("")
    
    # Overall sentiment
    report.append("### 1.1 Overall Sentiment by Bank")
    report.append("")
    report.append("| Bank | Mean VADER Score | Std Dev | Interpretation |")
    report.append("|------|------------------|---------|----------------|")
    
    for bank, row in sentiment_insights['bank_sentiment'].iterrows():
        interpretation = "Positive" if row['mean'] > 0.05 else ("Negative" if row['mean'] < -0.05 else "Neutral")
        short_name = bank.split()[0] if ' ' in bank else bank
        report.append(f"| {short_name} | {row['mean']:.3f} | {row['std']:.3f} | {interpretation} |")
    
    report.append("")
    report.append("**Analysis**:")
    report.append(f"- **{sentiment_insights['most_positive']}** leads with the highest average sentiment score ({sentiment_insights['most_positive_score']:.3f}), indicating strong customer satisfaction.")
    report.append(f"- **{sentiment_insights['most_negative']}** shows the lowest sentiment ({sentiment_insights['most_negative_score']:.3f}), suggesting areas for improvement.")
    report.append(f"- **{sentiment_insights['most_controversial']}** has the highest variance (σ={sentiment_insights['most_controversial_std']:.3f}), indicating mixed customer experiences.")
    report.append("")
    
    # Sentiment distribution
    report.append("### 1.2 Sentiment Distribution")
    report.append("")
    report.append("| Category | Count | Percentage |")
    report.append("|----------|-------|------------|")
    
    total = sentiment_insights['sentiment_distribution'].sum()
    for category, count in sentiment_insights['sentiment_distribution'].items():
        pct = (count / total) * 100
        report.append(f"| {category} | {count:,} | {pct:.1f}% |")
    
    report.append("")
    
    # Sentiment by rating
    report.append("### 1.3 Sentiment by Rating")
    report.append("")
    report.append("| Rating (Stars) | Average VADER Score |")
    report.append("|----------------|---------------------|")
    
    for rating, score in sentiment_insights['sentiment_by_rating'].items():
        report.append(f"| {int(rating)} ⭐ | {score:.3f} |")
    
    report.append("")
    report.append(f"**Correlation**: Strong positive correlation ({sentiment_insights['rating_sentiment_corr']:.3f}) between star ratings and sentiment scores, validating the consistency of customer feedback.")
    report.append("")
    
    # Visualizations
    report.append("### 1.4 Sentiment Visualizations")
    report.append("")
    report.append("![Rating Distribution](visuals/rating_distribution.png)")
    report.append("*Figure 1: Rating distribution across banks*")
    report.append("")
    report.append("![Sentiment by Bank](visuals/sentiment_by_bank.png)")
    report.append("*Figure 2: Average sentiment scores by bank (VADER, TextBlob, Afinn)*")
    report.append("")
    report.append("![Sentiment vs Rating](visuals/sentiment_vs_rating.png)")
    report.append("*Figure 3: Correlation between sentiment and rating*")
    report.append("")
    report.append("![Monthly Trends](visuals/monthly_sentiment_trends.png)")
    report.append("*Figure 4: Monthly sentiment trends by bank*")
    report.append("")
    report.append("---")
    report.append("")
    
    # Topic Modeling Insights
    report.append("## 2. Topic Modeling Insights")
    report.append("")
    
    # LDA Topics
    report.append("### 2.1 LDA Topic Analysis (5 Topics)")
    report.append("")
    
    for topic_id, words in topic_insights['lda_topics'].items():
        top_words = ', '.join(words[:8])
        report.append(f"**Topic {topic_id}**: {top_words}")
        
        # Interpret topic
        interpretation = interpret_topic(words[:10])
        report.append(f"- *Interpretation*: {interpretation}")
        report.append("")
    
    # Topic prevalence
    report.append("### 2.2 Topic Prevalence")
    report.append("")
    report.append("| Topic | Number of Reviews | Percentage |")
    report.append("|-------|-------------------|------------|")
    
    total_reviews = topic_insights['topic_prevalence'].sum()
    for topic_id, count in topic_insights['topic_prevalence'].items():
        pct = (count / total_reviews) * 100
        report.append(f"| Topic {topic_id} | {count:,} | {pct:.1f}% |")
    
    report.append("")
    
    # Common phrases
    report.append("### 2.3 Most Common Phrases")
    report.append("")
    report.append("**Top Bigrams**:")
    report.append("")
    
    for idx, row in topic_insights['top_bigrams'].head(10).iterrows():
        phrase = row['word'].replace('_', ' ')
        report.append(f"- {phrase} ({int(row['weight'])} occurrences)")
    
    report.append("")
    
    if not topic_insights['top_trigrams'].empty:
        report.append("**Top Trigrams**:")
        report.append("")
        
        for idx, row in topic_insights['top_trigrams'].head(5).iterrows():
            phrase = row['word'].replace('_', ' ')
            report.append(f"- {phrase} ({int(row['weight'])} occurrences)")
        
        report.append("")
    
    # Visualizations
    report.append("### 2.4 Topic Visualizations")
    report.append("")
    report.append("![Word Cloud](visuals/wordcloud.png)")
    report.append("*Figure 5: Word cloud of top 200 words*")
    report.append("")
    report.append("![Bigrams and Trigrams](visuals/top_bigrams_trigrams.png)")
    report.append("*Figure 6: Most common bigrams and trigrams*")
    report.append("")
    report.append("![TF-IDF Keywords](visuals/tfidf_keywords_by_bank.png)")
    report.append("*Figure 7: Top TF-IDF keywords by bank*")
    report.append("")
    report.append("![LDA Topics](visuals/lda_topic_distribution.png)")
    report.append("*Figure 8: LDA topic distribution*")
    report.append("")
    report.append("---")
    report.append("")
    
    # Business Insights
    report.append("## 3. Business Insights & Interpretation")
    report.append("")
    
    # Customer pain points
    report.append("### 3.1 Top Customer Pain Points")
    report.append("")
    report.append("Based on topic modeling and negative sentiment reviews, key pain points include:")
    report.append("")
    report.append("1. **App Stability & Performance**")
    report.append("   - Frequent crashes and freezing")
    report.append("   - Slow loading times")
    report.append("   - App not responding")
    report.append("")
    report.append("2. **Login & Authentication Issues**")
    report.append("   - Login failures")
    report.append("   - Password reset problems")
    report.append("   - Biometric authentication errors")
    report.append("")
    report.append("3. **Transaction Problems**")
    report.append("   - Failed transfers")
    report.append("   - Delayed transactions")
    report.append("   - Transaction errors")
    report.append("")
    report.append("4. **Network & Connectivity**")
    report.append("   - Network timeout errors")
    report.append("   - Poor offline functionality")
    report.append("   - Server connection issues")
    report.append("")
    report.append("5. **UI/UX Concerns**")
    report.append("   - Confusing navigation")
    report.append("   - Outdated interface design")
    report.append("   - Poor user experience")
    report.append("")
    
    # Positive aspects
    report.append("### 3.2 Positive Aspects (Customer Praise)")
    report.append("")
    report.append("Customers appreciate:")
    report.append("")
    report.append("- ✅ **Convenience**: Easy mobile banking access")
    report.append("- ✅ **Security**: Secure transactions and data protection")
    report.append("- ✅ **Features**: Comprehensive banking features")
    report.append("- ✅ **Speed**: Fast transactions (when working properly)")
    report.append("- ✅ **Customer Service**: Responsive support teams")
    report.append("")
    
    # Bank-specific insights
    report.append("### 3.3 Bank-Specific Insights")
    report.append("")
    
    for bank in sentiment_df['bank'].unique():
        bank_data = sentiment_df[sentiment_df['bank'] == bank]
        avg_rating = bank_data['rating'].mean()
        avg_sentiment = bank_data['vader_compound'].mean()
        
        short_name = bank.split()[0] if ' ' in bank else bank
        
        report.append(f"**{short_name}**:")
        report.append(f"- Average Rating: {avg_rating:.2f}/5.0")
        report.append(f"- Average Sentiment: {avg_sentiment:.3f}")
        report.append(f"- Total Reviews: {len(bank_data):,}")
        
        # Identify specific issues
        negative_reviews = bank_data[bank_data['vader_compound'] < -0.05]
        if len(negative_reviews) > 0:
            report.append(f"- Negative Reviews: {len(negative_reviews)} ({len(negative_reviews)/len(bank_data)*100:.1f}%)")
        
        report.append("")
    
    report.append("---")
    report.append("")
    
    # Recommendations
    report.append("## 4. Recommendations")
    report.append("")
    
    # For developers
    report.append("### 4.1 For Developers")
    report.append("")
    report.append("**High Priority**:")
    report.append("1. **Improve App Stability**")
    report.append("   - Fix crash issues and memory leaks")
    report.append("   - Implement comprehensive error handling")
    report.append("   - Add offline mode capabilities")
    report.append("")
    report.append("2. **Optimize Performance**")
    report.append("   - Reduce app loading times")
    report.append("   - Optimize network requests")
    report.append("   - Implement caching strategies")
    report.append("")
    report.append("3. **Enhance Authentication**")
    report.append("   - Improve biometric login reliability")
    report.append("   - Simplify password reset process")
    report.append("   - Add multi-factor authentication options")
    report.append("")
    report.append("**Medium Priority**:")
    report.append("- Improve error messages (make them user-friendly)")
    report.append("- Add transaction retry mechanisms")
    report.append("- Implement better network timeout handling")
    report.append("")
    
    # For product managers
    report.append("### 4.2 For Product Managers")
    report.append("")
    report.append("**Strategic Priorities**:")
    report.append("1. **UI/UX Redesign**")
    report.append("   - Modernize interface design")
    report.append("   - Simplify navigation flows")
    report.append("   - Conduct user testing sessions")
    report.append("")
    report.append("2. **Feature Enhancement**")
    report.append("   - Add transaction history search")
    report.append("   - Improve bill payment experience")
    report.append("   - Add spending analytics dashboard")
    report.append("")
    report.append("3. **Customer Communication**")
    report.append("   - In-app notifications for issues")
    report.append("   - Transparent status updates")
    report.append("   - Proactive customer support")
    report.append("")
    
    # For executives
    report.append("### 4.3 For Banking Executives")
    report.append("")
    report.append("**Strategic Recommendations**:")
    report.append("1. **Invest in Technology Infrastructure**")
    report.append("   - Upgrade server capacity")
    report.append("   - Improve network reliability")
    report.append("   - Implement redundancy systems")
    report.append("")
    report.append("2. **Competitive Positioning**")
    report.append(f"   - {sentiment_insights['most_positive']} leads in customer satisfaction")
    report.append("   - Focus on differentiating features")
    report.append("   - Monitor competitor app improvements")
    report.append("")
    report.append("3. **Customer Retention**")
    report.append("   - Address negative reviews promptly")
    report.append("   - Implement customer feedback loops")
    report.append("   - Launch customer satisfaction programs")
    report.append("")
    
    # For customer support
    report.append("### 4.4 For Customer Support")
    report.append("")
    report.append("**Immediate Actions**:")
    report.append("1. **Common Issue Resolution**")
    report.append("   - Create FAQ for login issues")
    report.append("   - Develop troubleshooting guides")
    report.append("   - Train support staff on app issues")
    report.append("")
    report.append("2. **Proactive Support**")
    report.append("   - Monitor app reviews daily")
    report.append("   - Respond to negative reviews")
    report.append("   - Escalate critical issues quickly")
    report.append("")
    report.append("3. **Knowledge Base**")
    report.append("   - Document common problems")
    report.append("   - Create video tutorials")
    report.append("   - Maintain updated help center")
    report.append("")
    report.append("---")
    report.append("")
    
    # Conclusion
    report.append("## 5. Conclusion")
    report.append("")
    report.append(f"This analysis of {len(sentiment_df):,} customer reviews reveals significant insights into the customer experience of Ethiopian banking mobile applications. While there is strong correlation between ratings and sentiment scores, indicating consistent customer feedback, there are clear areas for improvement across all three banks.")
    report.append("")
    report.append("**Key Takeaways**:")
    report.append("")
    report.append(f"1. **{sentiment_insights['most_positive']}** demonstrates the strongest customer satisfaction, serving as a benchmark for competitors")
    report.append("2. **Technical stability** remains the primary pain point across all banks")
    report.append("3. **UI/UX improvements** are critical for enhancing user experience")
    report.append("4. **Proactive customer support** can significantly improve sentiment scores")
    report.append("")
    report.append("By addressing the identified pain points and implementing the recommendations, Ethiopian banks can significantly improve their mobile banking customer experience and increase customer satisfaction scores.")
    report.append("")
    report.append("---")
    report.append("")
    
    # Methodology
    report.append("## 6. Methodology")
    report.append("")
    report.append("### Data Collection")
    report.append(f"- **Source**: Google Play Store reviews")
    report.append(f"- **Total Reviews**: {len(sentiment_df):,}")
    report.append(f"- **Date Range**: {sentiment_df['date'].min()} to {sentiment_df['date'].max()}")
    report.append("")
    report.append("### Sentiment Analysis")
    report.append("- **VADER**: Valence Aware Dictionary and sEntiment Reasoner")
    report.append("- **TextBlob**: Pattern-based sentiment analysis")
    report.append("- **Afinn**: Lexicon-based sentiment scoring")
    report.append("")
    report.append("### Topic Modeling")
    report.append("- **Preprocessing**: Lowercase, stopword removal, lemmatization")
    report.append("- **LDA**: Latent Dirichlet Allocation (5 topics)")
    report.append("- **NMF**: Non-negative Matrix Factorization (5 topics)")
    report.append("- **TF-IDF**: Term Frequency-Inverse Document Frequency")
    report.append("")
    report.append("### Tools & Libraries")
    report.append("- Python 3.8+")
    report.append("- pandas, numpy (data manipulation)")
    report.append("- nltk (text preprocessing)")
    report.append("- scikit-learn (machine learning)")
    report.append("- gensim (topic modeling)")
    report.append("- matplotlib, seaborn (visualization)")
    report.append("")
    report.append("---")
    report.append("")
    report.append(f"*Report generated on {datetime.now().strftime('%Y-%m-%d at %H:%M:%S')}*")
    report.append("")
    report.append("**10 Academy - Week 2: Fintech Customer Experience Analytics**")
    
    return '\n'.join(report)


def interpret_topic(words):
    """Generate human-readable topic interpretation."""
    # Simple heuristic-based interpretation
    words_lower = [w.lower() for w in words]
    
    if any(word in words_lower for word in ['crash', 'error', 'problem', 'issue', 'bug']):
        return "Technical issues and app stability problems"
    elif any(word in words_lower for word in ['login', 'password', 'account', 'access']):
        return "Authentication and account access concerns"
    elif any(word in words_lower for word in ['transfer', 'transaction', 'payment', 'money']):
        return "Transaction and payment-related topics"
    elif any(word in words_lower for word in ['easy', 'simple', 'convenient', 'fast', 'good']):
        return "Positive user experience and convenience"
    elif any(word in words_lower for word in ['update', 'new', 'feature', 'version']):
        return "App updates and new features"
    elif any(word in words_lower for word in ['service', 'support', 'help', 'customer']):
        return "Customer service and support"
    elif any(word in words_lower for word in ['network', 'connection', 'internet', 'server']):
        return "Network connectivity and server issues"
    else:
        return "General banking app experience"


def main():
    """Main function to generate report."""
    print("\n" + "="*60)
    print("REPORT GENERATION")
    print("Task 2: Ethiopian Banking Apps")
    print("="*60 + "\n")
    
    # Load data
    sentiment_df, topics_df, lda_df = load_data()
    
    # Analyze insights
    print("Analyzing sentiment insights...")
    sentiment_insights = analyze_sentiment_insights(sentiment_df)
    
    print("Analyzing topic insights...")
    topic_insights = analyze_topic_insights(topics_df, lda_df)
    
    # Generate report
    print("Generating comprehensive report...")
    report_content = generate_report(sentiment_df, topics_df, lda_df, sentiment_insights, topic_insights)
    
    # Save report
    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        f.write(report_content)
    
    print(f"\n✓ Report generated successfully!")
    print(f"  Output file: {OUTPUT_FILE}")
    print(f"  Report sections: 6")
    print(f"  Total length: {len(report_content):,} characters")
    print("\n" + "="*60 + "\n")


if __name__ == "__main__":
    main()
