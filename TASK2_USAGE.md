# Task 2: NLP & Sentiment Analysis - Usage Guide

## Overview

Task 2 performs comprehensive NLP and sentiment analysis on Ethiopian banking app reviews collected in Task 1.

---

## Quick Start

### Option 1: Run Complete Pipeline (Recommended)

```bash
# Run all modules in sequence
python scripts/run_task2_analysis.py
```

This will execute:
1. Sentiment Analysis
2. Topic Modeling
3. Visualization Generation
4. Report Generation

### Option 2: Run Individual Modules

```bash
# 1. Sentiment analysis
python scripts/sentiment_analysis.py

# 2. Topic modeling (requires step 1)
python scripts/topic_modeling.py

# 3. Visualizations (requires steps 1-2)
python scripts/visualizations.py

# 4. Report generation (requires steps 1-3)
python scripts/generate_report.py
```

---

## Prerequisites

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Required Input File

- `data/bank_reviews_clean.csv` (from Task 1)

If this file doesn't exist, run Task 1 first:
```bash
python scripts/scrape_reviews.py
python scripts/clean_reviews.py
```

---

## Output Files

### CSV Files (data/)

| File | Description | Columns |
|------|-------------|---------|
| `sentiment_results.csv` | Reviews with sentiment scores | review, rating, date, bank, source, vader_compound, textblob_polarity, textblob_subjectivity, afinn_score |
| `topics_keywords.csv` | Topic keywords and weights | model, topic_id, word, weight |
| `lda_topics.csv` | LDA topic assignments | review, bank, rating, lda_topic |

### Visualizations (visuals/)

| File | Description |
|------|-------------|
| `rating_distribution.png` | Rating distribution per bank |
| `sentiment_by_bank.png` | Average sentiment scores by bank |
| `sentiment_vs_rating.png` | Correlation between sentiment and rating |
| `monthly_sentiment_trends.png` | Monthly sentiment trends |
| `wordcloud.png` | Word cloud of top 200 words |
| `top_bigrams_trigrams.png` | Most common phrases |
| `tfidf_keywords_by_bank.png` | Top keywords per bank |
| `lda_topic_distribution.png` | Topic prevalence |

### Final Report

- `TASK2_REPORT.md` - Comprehensive business insights report

---

## Analysis Methods

### 1. Sentiment Analysis

**Three sentiment tools applied:**

- **VADER** (Valence Aware Dictionary and sEntiment Reasoner)
  - Compound score: -1 (negative) to +1 (positive)
  - Optimized for social media text

- **TextBlob**
  - Polarity: -1 (negative) to +1 (positive)
  - Subjectivity: 0 (objective) to 1 (subjective)

- **Afinn**
  - Lexicon-based scoring
  - Typically ranges from -5 to +5

**Aggregated Insights:**
- Overall sentiment per bank
- Sentiment by rating
- Sentiment by month
- Rating-sentiment correlation

### 2. Topic Modeling

**Text Preprocessing:**
1. Lowercase conversion
2. Stopword removal (NLTK + custom banking terms)
3. Lemmatization
4. Punctuation removal
5. Bigram/trigram detection

**Methods:**
- **TF-IDF**: Keyword extraction (overall + per bank)
- **LDA**: Latent Dirichlet Allocation (5 topics)
- **NMF**: Non-negative Matrix Factorization (5 topics)

**Outputs:**
- Top words per topic
- Topic prevalence distribution
- Bank-specific keywords
- Common phrases (bigrams/trigrams)

### 3. Visualizations

**8 professional charts:**
1. Rating distribution (stacked bar)
2. Sentiment by bank (bar with error bars)
3. Sentiment vs rating (scatter with trend line)
4. Monthly trends (multi-line chart)
5. Word cloud (top 200 words)
6. Bigrams/trigrams (horizontal bars)
7. TF-IDF keywords (grouped bars)
8. LDA topics (pie + bar charts)

All saved as high-resolution PNG (300 DPI)

### 4. Business Report

**Sections:**
1. Executive Summary
2. Sentiment Analysis Insights
3. Topic Modeling Insights
4. Business Insights & Interpretation
5. Recommendations (for developers, PMs, executives, support)
6. Methodology

---

## Expected Runtime

| Module | Estimated Time |
|--------|----------------|
| Sentiment Analysis | 30-60 seconds |
| Topic Modeling | 2-5 minutes |
| Visualizations | 30-60 seconds |
| Report Generation | 10-20 seconds |
| **Total** | **4-7 minutes** |

*Times vary based on dataset size and system performance*

---

## Troubleshooting

### Issue: "ModuleNotFoundError"

**Solution**: Install dependencies
```bash
pip install -r requirements.txt
```

### Issue: "NLTK data not found"

**Solution**: Download NLTK data
```python
import nltk
nltk.download('stopwords')
nltk.download('punkt')
nltk.download('wordnet')
```

The scripts will attempt to download automatically on first run.

### Issue: "File not found: bank_reviews_clean.csv"

**Solution**: Run Task 1 first
```bash
python scripts/scrape_reviews.py
python scripts/clean_reviews.py
```

### Issue: Visualizations not generating

**Solution**: Ensure visuals/ directory exists
```bash
mkdir visuals
```

---

## Customization

### Adjust Number of Topics

Edit the scripts:

**topic_modeling.py:**
```python
# Change n_topics parameter
lda_topics, df = perform_lda_topic_modeling(df, n_topics=7, n_words=10)
nmf_topics = perform_nmf_topic_modeling(df, n_topics=7, n_words=10)
```

### Change Visualization Style

Edit **visualizations.py:**
```python
# Change color palette
BANK_COLORS = {
    'Commercial Bank of Ethiopia': '#your_color',
    'Bank of Abyssinia': '#your_color',
    'Dashen Bank': '#your_color'
}
```

### Add Custom Stopwords

Edit **topic_modeling.py:**
```python
custom_stopwords = {
    'app', 'bank', 'your_word_here'
}
```

---

## Next Steps

After completing Task 2:

1. **Review the Report**: Read `TASK2_REPORT.md` for insights
2. **Examine Visualizations**: Check charts in `visuals/`
3. **Analyze Data**: Explore CSV files for detailed analysis
4. **Implement Recommendations**: Share findings with stakeholders
5. **Git Workflow**: Commit and push results

```bash
git checkout -b task-2
git add .
git commit -m "Task 2: Add NLP and sentiment analysis"
git checkout main
git merge task-2
git push origin main
```

---

## Support

For issues or questions:
- Check error messages in console output
- Review prerequisites section
- Verify all dependencies installed
- Ensure Task 1 completed successfully

---

**10 Academy - Week 2: Fintech Customer Experience Analytics**  
**Task 2: NLP & Sentiment Analysis**
