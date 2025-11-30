"""
Data Cleaning and Preprocessing Script
Task 1: Fintech Customer Experience Analytics

This script cleans and preprocesses scraped Google Play Store reviews:
- Removes duplicates
- Handles missing values
- Normalizes date formats
- Cleans text data
- Generates quality report
"""

import pandas as pd
import numpy as np
import re
import os
from datetime import datetime

# File paths
INPUT_FILE = 'data/bank_reviews_raw.csv'
OUTPUT_FILE = 'data/bank_reviews_clean.csv'


def load_data(filepath):
    """Load raw review data."""
    print(f"Loading data from: {filepath}")
    df = pd.read_csv(filepath, encoding='utf-8')
    print(f"✓ Loaded {len(df)} reviews")
    return df


def remove_duplicates(df):
    """Remove duplicate reviews."""
    initial_count = len(df)
    df_clean = df.drop_duplicates(subset=['review_text', 'bank_name'], keep='first')
    duplicates_removed = initial_count - len(df_clean)
    print(f"✓ Removed {duplicates_removed} duplicate reviews")
    return df_clean, duplicates_removed


def handle_missing_values(df):
    """Handle missing values in the dataset."""
    print("\nHandling missing values:")
    
    # Report missing values
    missing_report = {}
    for col in df.columns:
        missing_count = df[col].isnull().sum()
        missing_pct = (missing_count / len(df)) * 100
        missing_report[col] = {'count': missing_count, 'percentage': missing_pct}
        if missing_count > 0:
            print(f"  • {col}: {missing_count} missing ({missing_pct:.2f}%)")
    
    initial_count = len(df)
    
    # Drop rows with missing review_text (critical field)
    df = df.dropna(subset=['review_text'])
    print(f"  → Dropped {initial_count - len(df)} rows with missing review_text")
    
    # Fill missing ratings with median (if any)
    if df['rating'].isnull().sum() > 0:
        median_rating = df['rating'].median()
        df['rating'] = df['rating'].fillna(median_rating)
        print(f"  → Filled missing ratings with median: {median_rating}")
    
    # Drop rows with missing dates
    initial_count = len(df)
    df = df.dropna(subset=['date'])
    print(f"  → Dropped {initial_count - len(df)} rows with missing dates")
    
    return df, missing_report


def normalize_dates(df):
    """Normalize date format to YYYY-MM-DD."""
    print("\nNormalizing dates to YYYY-MM-DD format:")
    
    def parse_date(date_str):
        """Parse various date formats to YYYY-MM-DD."""
        if pd.isnull(date_str):
            return None
        
        try:
            # Try parsing as datetime
            if isinstance(date_str, str):
                dt = pd.to_datetime(date_str)
            else:
                dt = date_str
            return dt.strftime('%Y-%m-%d')
        except:
            return None
    
    df['date'] = df['date'].apply(parse_date)
    
    # Drop any rows where date parsing failed
    initial_count = len(df)
    df = df.dropna(subset=['date'])
    print(f"✓ Normalized {len(df)} dates")
    if initial_count > len(df):
        print(f"  → Dropped {initial_count - len(df)} rows with invalid dates")
    
    return df


def clean_text(df):
    """Clean review text data."""
    print("\nCleaning review text:")
    
    def clean_review_text(text):
        """Clean individual review text."""
        if pd.isnull(text):
            return ""
        
        # Convert to string
        text = str(text)
        
        # Trim whitespace
        text = text.strip()
        
        # Remove extra spaces
        text = re.sub(r'\s+', ' ', text)
        
        # Remove non-printable characters
        text = re.sub(r'[^\x20-\x7E\n]', '', text)
        
        return text
    
    df['review_text'] = df['review_text'].apply(clean_review_text)
    
    # Drop reviews with empty text after cleaning
    initial_count = len(df)
    df = df[df['review_text'].str.len() > 0]
    empty_removed = initial_count - len(df)
    print(f"✓ Cleaned text data")
    print(f"  → Removed {empty_removed} reviews with empty text after cleaning")
    
    return df, empty_removed


def standardize_schema(df):
    """Rename columns to final schema."""
    print("\nStandardizing column names:")
    
    column_mapping = {
        'review_text': 'review',
        'rating': 'rating',
        'date': 'date',
        'bank_name': 'bank',
        'source': 'source'
    }
    
    df = df.rename(columns=column_mapping)
    
    # Ensure correct column order
    df = df[['review', 'rating', 'date', 'bank', 'source']]
    
    print(f"✓ Standardized schema: {list(df.columns)}")
    
    return df


def validate_data(df):
    """Validate cleaned data."""
    print("\nValidating cleaned data:")
    
    issues = []
    
    # Check for duplicates
    duplicates = df.duplicated(subset=['review', 'bank']).sum()
    if duplicates > 0:
        issues.append(f"Found {duplicates} duplicates")
    else:
        print("✓ No duplicates found")
    
    # Check rating range
    invalid_ratings = df[(df['rating'] < 1) | (df['rating'] > 5)].shape[0]
    if invalid_ratings > 0:
        issues.append(f"Found {invalid_ratings} invalid ratings")
    else:
        print("✓ All ratings in valid range (1-5)")
    
    # Check for missing values
    missing = df.isnull().sum().sum()
    if missing > 0:
        issues.append(f"Found {missing} missing values")
    else:
        print("✓ No missing values")
    
    # Check for empty reviews
    empty_reviews = df[df['review'].str.len() == 0].shape[0]
    if empty_reviews > 0:
        issues.append(f"Found {empty_reviews} empty reviews")
    else:
        print("✓ No empty reviews")
    
    if issues:
        print("\n⚠ Validation issues found:")
        for issue in issues:
            print(f"  • {issue}")
    else:
        print("\n✓ All validation checks passed")
    
    return len(issues) == 0


def generate_quality_report(df, initial_count, duplicates_removed, empty_removed, missing_report):
    """Generate data quality report."""
    print("\n" + "="*60)
    print("DATA QUALITY REPORT")
    print("="*60)
    
    print(f"\nDataset Statistics:")
    print(f"  • Initial reviews: {initial_count}")
    print(f"  • Duplicates removed: {duplicates_removed}")
    print(f"  • Empty reviews removed: {empty_removed}")
    print(f"  • Final reviews: {len(df)}")
    print(f"  • Data retention rate: {(len(df)/initial_count)*100:.2f}%")
    
    print(f"\nMissing Values (before cleaning):")
    for col, stats in missing_report.items():
        if stats['count'] > 0:
            print(f"  • {col}: {stats['count']} ({stats['percentage']:.2f}%)")
    
    print(f"\nDate Range:")
    print(f"  • Earliest: {df['date'].min()}")
    print(f"  • Latest: {df['date'].max()}")
    
    print(f"\nReviews per Bank:")
    for bank in df['bank'].unique():
        count = len(df[df['bank'] == bank])
        pct = (count / len(df)) * 100
        print(f"  • {bank}: {count} ({pct:.2f}%)")
    
    print(f"\nRating Distribution:")
    rating_dist = df['rating'].value_counts().sort_index()
    for rating, count in rating_dist.items():
        pct = (count / len(df)) * 100
        print(f"  • {int(rating)} stars: {count} ({pct:.2f}%)")
    
    print(f"\nAverage Rating: {df['rating'].mean():.2f}")
    print(f"Median Rating: {df['rating'].median():.1f}")
    
    print(f"\nText Statistics:")
    df['review_length'] = df['review'].str.len()
    print(f"  • Average review length: {df['review_length'].mean():.0f} characters")
    print(f"  • Median review length: {df['review_length'].median():.0f} characters")
    print(f"  • Shortest review: {df['review_length'].min()} characters")
    print(f"  • Longest review: {df['review_length'].max()} characters")
    
    print("="*60 + "\n")


def main():
    """Main function to orchestrate the cleaning process."""
    print("\n" + "="*60)
    print("DATA CLEANING & PREPROCESSING")
    print("Task 1: Ethiopian Banking Apps")
    print("="*60 + "\n")
    
    # Check if input file exists
    if not os.path.exists(INPUT_FILE):
        print(f"✗ Error: Input file not found: {INPUT_FILE}")
        print("Please run scrape_reviews.py first to collect data.")
        return
    
    # Load data
    df = load_data(INPUT_FILE)
    initial_count = len(df)
    
    # Step 1: Remove duplicates
    df, duplicates_removed = remove_duplicates(df)
    
    # Step 2: Handle missing values
    df, missing_report = handle_missing_values(df)
    
    # Step 3: Normalize dates
    df = normalize_dates(df)
    
    # Step 4: Clean text
    df, empty_removed = clean_text(df)
    
    # Step 5: Standardize schema
    df = standardize_schema(df)
    
    # Step 6: Validate data
    is_valid = validate_data(df)
    
    # Save cleaned data
    df.to_csv(OUTPUT_FILE, index=False, encoding='utf-8')
    print(f"\n✓ Cleaned data saved to: {OUTPUT_FILE}")
    
    # Generate quality report
    generate_quality_report(df, initial_count, duplicates_removed, empty_removed, missing_report)
    
    # Display sample
    print("Sample of cleaned data (first 5 rows):")
    print(df.head(5).to_string())
    print("\n")


if __name__ == "__main__":
    main()
