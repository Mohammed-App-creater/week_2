"""
Topic Modeling Module
Task 2: Fintech Customer Experience Analytics

This script performs comprehensive topic modeling on Ethiopian banking app reviews:
- Text preprocessing (lowercase, stopwords, lemmatization, bigrams/trigrams)
- TF-IDF keyword extraction
- LDA topic modeling (5 topics)
- NMF topic modeling (5 topics)

Outputs:
- topics_keywords.csv: Top words per topic
- lda_topics.csv: Document-topic assignments
"""

import pandas as pd
import numpy as np
import re
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer
from sklearn.decomposition import NMF, LatentDirichletAllocation
from gensim import corpora
from gensim.models import LdaModel, Phrases
from gensim.models.phrases import Phraser
import warnings
warnings.filterwarnings('ignore')

# Download required NLTK data
try:
    nltk.data.find('corpora/stopwords')
except LookupError:
    print("Downloading NLTK stopwords...")
    nltk.download('stopwords', quiet=True)

try:
    nltk.data.find('tokenizers/punkt')
except LookupError:
    print("Downloading NLTK punkt...")
    nltk.download('punkt', quiet=True)

try:
    nltk.data.find('corpora/wordnet')
except LookupError:
    print("Downloading NLTK wordnet...")
    nltk.download('wordnet', quiet=True)

# File paths
INPUT_FILE = 'data/sentiment_results.csv'
TOPICS_OUTPUT = 'data/topics_keywords.csv'
LDA_OUTPUT = 'data/lda_topics.csv'


def load_data(filepath):
    """Load sentiment results data."""
    print(f"Loading data from: {filepath}")
    df = pd.read_csv(filepath, encoding='utf-8')
    print(f"✓ Loaded {len(df)} reviews")
    return df


def preprocess_text(df):
    """
    Comprehensive text preprocessing pipeline.
    
    Steps:
    1. Lowercase
    2. Remove punctuation and special characters
    3. Tokenization
    4. Remove stopwords
    5. Lemmatization
    6. Bigram/trigram detection
    """
    print("\nPreprocessing text...")
    
    # Initialize tools
    lemmatizer = WordNetLemmatizer()
    stop_words = set(stopwords.words('english'))
    
    # Add custom stopwords specific to app reviews
    custom_stopwords = {
        'app', 'bank', 'banking', 'mobile', 'application', 'apps',
        'use', 'using', 'used', 'one', 'get', 'make', 'also', 'would',
        'could', 'even', 'really', 'much', 'well', 'good', 'bad'
    }
    stop_words.update(custom_stopwords)
    
    def clean_text(text):
        """Clean and preprocess a single text."""
        if pd.isnull(text):
            return []
        
        # Lowercase
        text = str(text).lower()
        
        # Remove URLs
        text = re.sub(r'http\S+|www\S+', '', text)
        
        # Remove email addresses
        text = re.sub(r'\S+@\S+', '', text)
        
        # Remove punctuation and special characters (keep only letters and spaces)
        text = re.sub(r'[^a-z\s]', ' ', text)
        
        # Tokenize
        tokens = word_tokenize(text)
        
        # Remove stopwords and short words (< 3 characters)
        tokens = [word for word in tokens if word not in stop_words and len(word) >= 3]
        
        # Lemmatize
        tokens = [lemmatizer.lemmatize(word) for word in tokens]
        
        return tokens
    
    # Apply preprocessing
    df['tokens'] = df['review'].apply(clean_text)
    
    # Remove empty token lists
    df = df[df['tokens'].apply(len) > 0]
    
    print(f"✓ Preprocessing complete")
    print(f"  Reviews after filtering: {len(df)}")
    print(f"  Average tokens per review: {df['tokens'].apply(len).mean():.1f}")
    
    return df


def create_bigrams_trigrams(df):
    """Detect and create bigrams and trigrams."""
    print("\nDetecting bigrams and trigrams...")
    
    # Get all token lists
    sentences = df['tokens'].tolist()
    
    # Build bigram model
    bigram = Phrases(sentences, min_count=5, threshold=10)
    bigram_mod = Phraser(bigram)
    
    # Build trigram model
    trigram = Phrases(bigram_mod[sentences], min_count=5, threshold=10)
    trigram_mod = Phraser(trigram)
    
    # Apply bigrams and trigrams
    df['tokens_with_phrases'] = df['tokens'].apply(lambda x: trigram_mod[bigram_mod[x]])
    
    # Get top bigrams and trigrams for reporting
    bigram_counter = {}
    trigram_counter = {}
    
    for tokens in df['tokens_with_phrases']:
        for token in tokens:
            if '_' in token:
                if token.count('_') == 1:
                    bigram_counter[token] = bigram_counter.get(token, 0) + 1
                elif token.count('_') == 2:
                    trigram_counter[token] = trigram_counter.get(token, 0) + 1
    
    # Sort and get top phrases
    top_bigrams = sorted(bigram_counter.items(), key=lambda x: x[1], reverse=True)[:15]
    top_trigrams = sorted(trigram_counter.items(), key=lambda x: x[1], reverse=True)[:15]
    
    print(f"✓ Phrase detection complete")
    print(f"  Unique bigrams found: {len(bigram_counter)}")
    print(f"  Unique trigrams found: {len(trigram_counter)}")
    
    print(f"\n  Top 10 bigrams:")
    for phrase, count in top_bigrams[:10]:
        print(f"    {phrase.replace('_', ' ')}: {count}")
    
    if top_trigrams:
        print(f"\n  Top 5 trigrams:")
        for phrase, count in top_trigrams[:5]:
            print(f"    {phrase.replace('_', ' ')}: {count}")
    
    return df, top_bigrams, top_trigrams


def extract_tfidf_keywords(df, top_n=20):
    """Extract top TF-IDF keywords per bank."""
    print("\nExtracting TF-IDF keywords...")
    
    # Prepare documents (join tokens back to strings)
    df['processed_text'] = df['tokens_with_phrases'].apply(lambda x: ' '.join(x))
    
    # Overall TF-IDF
    tfidf = TfidfVectorizer(max_features=100, ngram_range=(1, 2))
    tfidf_matrix = tfidf.fit_transform(df['processed_text'])
    
    feature_names = tfidf.get_feature_names_out()
    
    # Get top keywords overall
    tfidf_scores = tfidf_matrix.sum(axis=0).A1
    top_indices = tfidf_scores.argsort()[-top_n:][::-1]
    top_keywords_overall = [(feature_names[i], tfidf_scores[i]) for i in top_indices]
    
    print(f"\n  Top {top_n} TF-IDF keywords (overall):")
    for keyword, score in top_keywords_overall[:10]:
        print(f"    {keyword}: {score:.2f}")
    
    # TF-IDF per bank
    bank_keywords = {}
    
    for bank in df['bank'].unique():
        bank_docs = df[df['bank'] == bank]['processed_text']
        
        if len(bank_docs) > 0:
            bank_tfidf = TfidfVectorizer(max_features=50, ngram_range=(1, 2))
            bank_matrix = bank_tfidf.fit_transform(bank_docs)
            
            bank_features = bank_tfidf.get_feature_names_out()
            bank_scores = bank_matrix.sum(axis=0).A1
            bank_top_indices = bank_scores.argsort()[-top_n:][::-1]
            
            bank_keywords[bank] = [(bank_features[i], bank_scores[i]) for i in bank_top_indices]
    
    print(f"\n✓ TF-IDF extraction complete")
    print(f"  Keywords extracted for {len(bank_keywords)} banks")
    
    return top_keywords_overall, bank_keywords


def perform_lda_topic_modeling(df, n_topics=5, n_words=10):
    """Perform LDA topic modeling using Gensim."""
    print(f"\nPerforming LDA topic modeling ({n_topics} topics)...")
    
    # Prepare documents
    documents = df['tokens_with_phrases'].tolist()
    
    # Create dictionary and corpus
    dictionary = corpora.Dictionary(documents)
    
    # Filter extremes
    dictionary.filter_extremes(no_below=5, no_above=0.5)
    
    # Create corpus
    corpus = [dictionary.doc2bow(doc) for doc in documents]
    
    # Train LDA model
    lda_model = LdaModel(
        corpus=corpus,
        id2word=dictionary,
        num_topics=n_topics,
        random_state=42,
        passes=10,
        alpha='auto',
        per_word_topics=True
    )
    
    # Extract topics
    topics = []
    for idx in range(n_topics):
        topic_words = lda_model.show_topic(idx, topn=n_words)
        topics.append({
            'topic_id': idx,
            'words': [word for word, _ in topic_words],
            'weights': [weight for _, weight in topic_words]
        })
    
    print(f"✓ LDA modeling complete")
    print(f"\n  LDA Topics:")
    for topic in topics:
        words_str = ', '.join(topic['words'][:8])
        print(f"    Topic {topic['topic_id']}: {words_str}")
    
    # Get topic assignments for documents
    topic_assignments = []
    for doc_bow in corpus:
        topic_dist = lda_model.get_document_topics(doc_bow)
        # Get dominant topic
        if topic_dist:
            dominant_topic = max(topic_dist, key=lambda x: x[1])
            topic_assignments.append(dominant_topic[0])
        else:
            topic_assignments.append(-1)
    
    df['lda_topic'] = topic_assignments
    
    # Calculate topic prevalence
    topic_prevalence = df['lda_topic'].value_counts().sort_index()
    print(f"\n  Topic prevalence:")
    for topic_id, count in topic_prevalence.items():
        pct = (count / len(df)) * 100
        print(f"    Topic {topic_id}: {count} reviews ({pct:.1f}%)")
    
    return topics, df


def perform_nmf_topic_modeling(df, n_topics=5, n_words=10):
    """Perform NMF topic modeling using scikit-learn."""
    print(f"\nPerforming NMF topic modeling ({n_topics} topics)...")
    
    # Prepare documents
    df['processed_text'] = df['tokens_with_phrases'].apply(lambda x: ' '.join(x))
    
    # Create TF-IDF matrix
    tfidf = TfidfVectorizer(max_features=1000, max_df=0.5, min_df=5)
    tfidf_matrix = tfidf.fit_transform(df['processed_text'])
    
    # Train NMF model
    nmf_model = NMF(n_components=n_topics, random_state=42, max_iter=200)
    nmf_model.fit(tfidf_matrix)
    
    # Extract topics
    feature_names = tfidf.get_feature_names_out()
    topics = []
    
    for idx, topic in enumerate(nmf_model.components_):
        top_indices = topic.argsort()[-n_words:][::-1]
        top_words = [feature_names[i] for i in top_indices]
        top_weights = [topic[i] for i in top_indices]
        
        topics.append({
            'topic_id': idx,
            'words': top_words,
            'weights': top_weights
        })
    
    print(f"✓ NMF modeling complete")
    print(f"\n  NMF Topics:")
    for topic in topics:
        words_str = ', '.join(topic['words'][:8])
        print(f"    Topic {topic['topic_id']}: {words_str}")
    
    return topics


def interpret_topics(lda_topics, nmf_topics):
    """Generate human-readable topic descriptions."""
    print("\nGenerating topic interpretations...")
    
    # Manual interpretation based on common patterns
    topic_descriptions = {
        'LDA': [],
        'NMF': []
    }
    
    for i, topic in enumerate(lda_topics):
        words = topic['words'][:5]
        # Simple heuristic-based interpretation
        description = f"Topic {i}: {', '.join(words)}"
        topic_descriptions['LDA'].append(description)
    
    for i, topic in enumerate(nmf_topics):
        words = topic['words'][:5]
        description = f"Topic {i}: {', '.join(words)}"
        topic_descriptions['NMF'].append(description)
    
    print(f"✓ Topic interpretations generated")
    
    return topic_descriptions


def save_topic_results(lda_topics, nmf_topics, tfidf_keywords, bank_keywords, top_bigrams, top_trigrams):
    """Save topic modeling results to CSV."""
    print("\nSaving topic results...")
    
    # Prepare topics keywords CSV
    topics_data = []
    
    # LDA topics
    for topic in lda_topics:
        for word, weight in zip(topic['words'], topic['weights']):
            topics_data.append({
                'model': 'LDA',
                'topic_id': topic['topic_id'],
                'word': word,
                'weight': weight
            })
    
    # NMF topics
    for topic in nmf_topics:
        for word, weight in zip(topic['words'], topic['weights']):
            topics_data.append({
                'model': 'NMF',
                'topic_id': topic['topic_id'],
                'word': word,
                'weight': weight
            })
    
    # TF-IDF keywords
    for word, score in tfidf_keywords:
        topics_data.append({
            'model': 'TF-IDF',
            'topic_id': 'overall',
            'word': word,
            'weight': score
        })
    
    # Bank-specific TF-IDF
    for bank, keywords in bank_keywords.items():
        for word, score in keywords[:10]:  # Top 10 per bank
            topics_data.append({
                'model': 'TF-IDF',
                'topic_id': bank,
                'word': word,
                'weight': score
            })
    
    # Bigrams
    for phrase, count in top_bigrams:
        topics_data.append({
            'model': 'Bigram',
            'topic_id': 'phrases',
            'word': phrase,
            'weight': count
        })
    
    # Trigrams
    for phrase, count in top_trigrams:
        topics_data.append({
            'model': 'Trigram',
            'topic_id': 'phrases',
            'word': phrase,
            'weight': count
        })
    
    topics_df = pd.DataFrame(topics_data)
    topics_df.to_csv(TOPICS_OUTPUT, index=False, encoding='utf-8')
    
    print(f"✓ Topics saved to: {TOPICS_OUTPUT}")
    print(f"  Total entries: {len(topics_df)}")


def save_lda_assignments(df):
    """Save LDA topic assignments."""
    # Select relevant columns
    lda_df = df[['review', 'bank', 'rating', 'lda_topic']].copy()
    lda_df.to_csv(LDA_OUTPUT, index=False, encoding='utf-8')
    
    print(f"✓ LDA assignments saved to: {LDA_OUTPUT}")
    print(f"  Total documents: {len(lda_df)}")


def main():
    """Main function to orchestrate topic modeling."""
    print("\n" + "="*60)
    print("TOPIC MODELING")
    print("Task 2: Ethiopian Banking Apps")
    print("="*60 + "\n")
    
    # Load data
    df = load_data(INPUT_FILE)
    
    # Preprocess text
    df = preprocess_text(df)
    
    # Create bigrams and trigrams
    df, top_bigrams, top_trigrams = create_bigrams_trigrams(df)
    
    # Extract TF-IDF keywords
    tfidf_keywords, bank_keywords = extract_tfidf_keywords(df)
    
    # Perform LDA topic modeling
    lda_topics, df = perform_lda_topic_modeling(df, n_topics=5, n_words=10)
    
    # Perform NMF topic modeling
    nmf_topics = perform_nmf_topic_modeling(df, n_topics=5, n_words=10)
    
    # Interpret topics
    topic_descriptions = interpret_topics(lda_topics, nmf_topics)
    
    # Save results
    save_topic_results(lda_topics, nmf_topics, tfidf_keywords, bank_keywords, top_bigrams, top_trigrams)
    save_lda_assignments(df)
    
    print("\n✓ Topic modeling complete!")
    print(f"  Output files:")
    print(f"    - {TOPICS_OUTPUT}")
    print(f"    - {LDA_OUTPUT}\n")


if __name__ == "__main__":
    main()
