"""
Web Scraper for Ethiopian Banking Apps - Google Play Store Reviews
Task 1: Fintech Customer Experience Analytics

This script scrapes reviews from Google Play Store for three Ethiopian banking apps:
- Commercial Bank of Ethiopia (CBE Mobile Banking App)
- Bank of Abyssinia (BOA Mobile Banking App)
- Dashen Bank (Dashen Mobile App)

Target: 400+ reviews per bank (1200+ total)
"""

import os
import pandas as pd
from google_play_scraper import Sort, reviews
from datetime import datetime
import time

# Configuration
APPS_CONFIG = [
    {
        'app_id': 'com.combanketh.mobilebanking',
        'bank_name': 'Commercial Bank of Ethiopia',
        'short_name': 'cbe'
    },
    {
        'app_id': 'com.boa.boaMobileBanking',
        'bank_name': 'Bank of Abyssinia',
        'short_name': 'boa'
    },
    {
        'app_id': 'com.dashen.dashensuperapp',
        'bank_name': 'Dashen Bank',
        'short_name': 'dashen'
    }
]

# Target reviews per app
TARGET_REVIEWS_PER_APP = 400

# Output directories
RAW_DATA_DIR = 'data/raw'
OUTPUT_FILE = 'data/bank_reviews_raw.csv'


def create_directories():
    """Create necessary directories if they don't exist."""
    os.makedirs(RAW_DATA_DIR, exist_ok=True)
    os.makedirs('data', exist_ok=True)
    print(f"✓ Created directories: {RAW_DATA_DIR}")


def scrape_app_reviews(app_id, bank_name, short_name, count=TARGET_REVIEWS_PER_APP):
    """
    Scrape reviews for a single app from Google Play Store.
    
    Args:
        app_id (str): Google Play Store app package ID
        bank_name (str): Full name of the bank
        short_name (str): Short name for file naming
        count (int): Number of reviews to scrape
    
    Returns:
        pd.DataFrame: DataFrame containing scraped reviews
    """
    print(f"\n{'='*60}")
    print(f"Scraping reviews for: {bank_name}")
    print(f"App ID: {app_id}")
    print(f"Target: {count} reviews")
    print(f"{'='*60}")
    
    all_reviews = []
    continuation_token = None
    
    try:
        # Scrape reviews in batches
        while len(all_reviews) < count:
            try:
                result, continuation_token = reviews(
                    app_id,
                    lang='en',
                    country='us',
                    sort=Sort.NEWEST,
                    count=min(200, count - len(all_reviews)),
                    continuation_token=continuation_token
                )
                
                if not result:
                    print(f"⚠ No more reviews available. Collected {len(all_reviews)} reviews.")
                    break
                
                all_reviews.extend(result)
                print(f"  → Collected {len(all_reviews)}/{count} reviews...")
                
                # If no continuation token, we've reached the end
                if not continuation_token:
                    print(f"⚠ Reached end of available reviews. Collected {len(all_reviews)} reviews.")
                    break
                
                # Small delay to avoid rate limiting
                time.sleep(1)
                
            except Exception as e:
                print(f"⚠ Error during batch scraping: {str(e)}")
                break
        
        # Convert to DataFrame
        if all_reviews:
            df = pd.DataFrame(all_reviews)
            
            # Extract and rename relevant columns
            df_clean = pd.DataFrame({
                'review_text': df['content'],
                'rating': df['score'],
                'date': df['at'].apply(lambda x: x.strftime('%Y-%m-%d') if pd.notnull(x) else None),
                'bank_name': bank_name,
                'source': 'google_play'
            })
            
            # Save individual bank file
            output_path = os.path.join(RAW_DATA_DIR, f'{short_name}_reviews.csv')
            df_clean.to_csv(output_path, index=False, encoding='utf-8')
            print(f"✓ Saved {len(df_clean)} reviews to: {output_path}")
            
            return df_clean
        else:
            print(f"✗ No reviews collected for {bank_name}")
            return pd.DataFrame()
            
    except Exception as e:
        print(f"✗ Error scraping {bank_name}: {str(e)}")
        return pd.DataFrame()


def main():
    """Main function to orchestrate the scraping process."""
    print("\n" + "="*60)
    print("GOOGLE PLAY STORE REVIEW SCRAPER")
    print("Task 1: Ethiopian Banking Apps")
    print("="*60)
    
    start_time = time.time()
    
    # Create directories
    create_directories()
    
    # Scrape reviews for all apps
    all_dataframes = []
    
    for app in APPS_CONFIG:
        df = scrape_app_reviews(
            app_id=app['app_id'],
            bank_name=app['bank_name'],
            short_name=app['short_name'],
            count=TARGET_REVIEWS_PER_APP
        )
        
        if not df.empty:
            all_dataframes.append(df)
    
    # Combine all reviews
    if all_dataframes:
        combined_df = pd.concat(all_dataframes, ignore_index=True)
        
        # Save combined raw data
        combined_df.to_csv(OUTPUT_FILE, index=False, encoding='utf-8')
        
        print(f"\n{'='*60}")
        print("SCRAPING SUMMARY")
        print(f"{'='*60}")
        print(f"Total reviews collected: {len(combined_df)}")
        print(f"Reviews per bank:")
        for bank in combined_df['bank_name'].unique():
            count = len(combined_df[combined_df['bank_name'] == bank])
            print(f"  • {bank}: {count} reviews")
        print(f"\nCombined data saved to: {OUTPUT_FILE}")
        print(f"Time elapsed: {time.time() - start_time:.2f} seconds")
        print(f"{'='*60}\n")
        
        # Display sample
        print("Sample of scraped data (first 3 rows):")
        print(combined_df.head(3).to_string())
        
    else:
        print("\n✗ No reviews were collected. Please check app IDs and internet connection.")


if __name__ == "__main__":
    main()
