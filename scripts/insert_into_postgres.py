"""
PostgreSQL Data Insertion Script
Task 3: Load cleaned CSV data into PostgreSQL database

This script:
1. Connects to PostgreSQL database
2. Loads the cleaned CSV file
3. Inserts unique banks into the banks table
4. Inserts all reviews into the reviews table
5. Prints summary statistics
6. Handles errors gracefully
"""

import psycopg2
from psycopg2 import sql, extras
import pandas as pd
import sys
from datetime import datetime
from typing import Dict, Tuple
import os


class PostgreSQLInserter:
    """Handle PostgreSQL database operations for review data insertion"""
    
    def __init__(self, db_config: Dict[str, str]):
        """
        Initialize database connection
        
        Args:
            db_config: Dictionary containing database connection parameters
        """
        self.db_config = db_config
        self.conn = None
        self.cursor = None
        
    def connect(self):
        """Establish connection to PostgreSQL database"""
        try:
            self.conn = psycopg2.connect(
                host=self.db_config['host'],
                port=self.db_config['port'],
                database=self.db_config['database'],
                user=self.db_config['user'],
                password=self.db_config['password']
            )
            self.cursor = self.conn.cursor()
            print("[OK] Successfully connected to PostgreSQL database")
            return True
        except psycopg2.Error as e:
            print(f"[ERROR] Error connecting to PostgreSQL database: {e}")
            return False
    
    
    def close(self):
        """Close database connection"""
        if self.cursor:
            self.cursor.close()
        if self.conn:
            self.conn.close()
        print("[OK] Database connection closed")
    
    def insert_banks(self, df: pd.DataFrame) -> Dict[str, int]:
        """
        Insert unique banks into banks table
        
        Args:
            df: DataFrame containing review data
            
        Returns:
            Dictionary mapping bank names to bank_ids
        """
        try:
            # Get unique banks
            unique_banks = df['bank'].unique()
            bank_mapping = {}
            
            print(f"\n[INFO] Inserting {len(unique_banks)} unique banks...")
            
            for bank_name in unique_banks:
                # Insert bank and get the generated bank_id
                insert_query = """
                    INSERT INTO banks (bank_name, app_name)
                    VALUES (%s, %s)
                    ON CONFLICT (bank_name) DO UPDATE 
                    SET bank_name = EXCLUDED.bank_name
                    RETURNING bank_id;
                """
                
                # Use bank_name as app_name (can be updated later if needed)
                self.cursor.execute(insert_query, (bank_name, bank_name))
                bank_id = self.cursor.fetchone()[0]
                bank_mapping[bank_name] = bank_id
                
            self.conn.commit()
            print(f"[OK] Successfully inserted {len(unique_banks)} banks")
            
            return bank_mapping
            
        except psycopg2.Error as e:
            self.conn.rollback()
            print(f"[ERROR] Error inserting banks: {e}")
            raise
    
    def insert_reviews(self, df: pd.DataFrame, bank_mapping: Dict[str, int]) -> int:
        """
        Insert reviews into reviews table using batch insertion
        
        Args:
            df: DataFrame containing review data
            bank_mapping: Dictionary mapping bank names to bank_ids
            
        Returns:
            Number of reviews inserted
        """
        try:
            print(f"\n[INFO] Inserting {len(df)} reviews...")
            
            # Prepare data for insertion
            review_data = []
            for _, row in df.iterrows():
                bank_id = bank_mapping.get(row['bank'])
                if bank_id is None:
                    print(f"[WARNING] Warning: Bank '{row['bank']}' not found in mapping, skipping review")
                    continue
                
                # Parse date
                try:
                    review_date = pd.to_datetime(row['date']).date()
                except:
                    review_date = datetime.now().date()
                
                # Prepare review tuple
                review_tuple = (
                    bank_id,
                    row['review'],
                    int(row['rating']),
                    review_date,
                    None,  # sentiment_label (to be filled by sentiment analysis)
                    None,  # sentiment_score (to be filled by sentiment analysis)
                    row['source']
                )
                review_data.append(review_tuple)
            
            # Batch insert using execute_batch for better performance
            insert_query = """
                INSERT INTO reviews 
                (bank_id, review_text, rating, review_date, sentiment_label, sentiment_score, source)
                VALUES (%s, %s, %s, %s, %s, %s, %s);
            """
            
            # Use execute_batch for efficient batch insertion
            extras.execute_batch(self.cursor, insert_query, review_data, page_size=1000)
            self.conn.commit()
            
            print(f"[OK] Successfully inserted {len(review_data)} reviews")
            return len(review_data)
            
        except psycopg2.Error as e:
            self.conn.rollback()
            print(f"[ERROR] Error inserting reviews: {e}")
            raise
    
    def print_summary_statistics(self):
        """Print summary statistics after insertion"""
        try:
            print("\n" + "="*70)
            print("DATABASE SUMMARY STATISTICS")
            print("="*70)
            
            # Total banks
            self.cursor.execute("SELECT COUNT(*) FROM banks;")
            total_banks = self.cursor.fetchone()[0]
            print(f"\n[BANKS] Total Banks: {total_banks}")
            
            # Total reviews
            self.cursor.execute("SELECT COUNT(*) FROM reviews;")
            total_reviews = self.cursor.fetchone()[0]
            print(f"[REVIEWS] Total Reviews: {total_reviews}")
            
            # Reviews per bank
            print(f"\n[INFO] Reviews per Bank:")
            self.cursor.execute("""
                SELECT b.bank_name, COUNT(r.review_id) as review_count
                FROM banks b
                LEFT JOIN reviews r ON b.bank_id = r.bank_id
                GROUP BY b.bank_name
                ORDER BY review_count DESC;
            """)
            for bank_name, count in self.cursor.fetchall():
                print(f"   • {bank_name}: {count} reviews")
            
            # Average rating
            self.cursor.execute("SELECT ROUND(AVG(rating)::numeric, 2) FROM reviews;")
            avg_rating = self.cursor.fetchone()[0]
            print(f"\n[RATING] Average Rating: {avg_rating}/5.0")
            
            # Rating distribution
            print(f"\n[INFO] Rating Distribution:")
            self.cursor.execute("""
                SELECT rating, COUNT(*) as count,
                       ROUND(COUNT(*) * 100.0 / SUM(COUNT(*)) OVER (), 2) as percentage
                FROM reviews
                GROUP BY rating
                ORDER BY rating DESC;
            """)
            for rating, count, percentage in self.cursor.fetchall():
                bar = '=' * int(percentage / 2)
                print(f"   {rating} stars: {count:4d} ({percentage:5.2f}%) {bar}")
            
            # Source distribution
            print(f"\n[SOURCE] Reviews by Source:")
            self.cursor.execute("""
                SELECT source, COUNT(*) as count
                FROM reviews
                GROUP BY source
                ORDER BY count DESC;
            """)
            for source, count in self.cursor.fetchall():
                print(f"   • {source}: {count} reviews")
            
            # Date range
            self.cursor.execute("""
                SELECT MIN(review_date), MAX(review_date)
                FROM reviews;
            """)
            min_date, max_date = self.cursor.fetchone()
            print(f"\n[DATE] Date Range: {min_date} to {max_date}")
            
            print("\n" + "="*70)
            
        except psycopg2.Error as e:
            print(f"[ERROR] Error fetching summary statistics: {e}")


def load_csv_data(csv_path: str) -> pd.DataFrame:
    """
    Load and validate CSV data
    
    Args:
        csv_path: Path to the cleaned CSV file
        
    Returns:
        DataFrame containing the CSV data
    """
    try:
        if not os.path.exists(csv_path):
            raise FileNotFoundError(f"CSV file not found: {csv_path}")
        
        df = pd.read_csv(csv_path)
        print(f"[OK] Successfully loaded CSV file: {csv_path}")
        print(f"  Rows: {len(df)}, Columns: {len(df.columns)}")
        
        # Validate required columns
        required_columns = ['review', 'rating', 'date', 'bank', 'source']
        missing_columns = [col for col in required_columns if col not in df.columns]
        
        if missing_columns:
            raise ValueError(f"Missing required columns: {missing_columns}")
        
        print(f"[OK] All required columns present: {required_columns}")
        
        return df
        
    except Exception as e:
        print(f"[ERROR] Error loading CSV file: {e}")
        raise


def main():
    """Main execution function"""
    
    # Database configuration
    # IMPORTANT: Update these values with your PostgreSQL credentials
    db_config = {
        'host': 'localhost',
        'port': '5432',
        'database': 'fintech_reviews',
        'user': 'postgres',  # Change this to your PostgreSQL username
        'password': '199605'  # Change this to your PostgreSQL password
    }
    
    # Path to cleaned CSV file
    csv_path = r'c:\Users\yoga\code\10_Academy\week_2\data\bank_reviews_clean.csv'
    
    print("="*70)
    print("PostgreSQL Data Insertion Script")
    print("="*70)
    
    try:
        # Load CSV data
        print("\n[Step 1/6] Loading CSV data...")
        df = load_csv_data(csv_path)
        
        # Initialize database inserter
        print("\n[Step 2/6] Connecting to PostgreSQL...")
        inserter = PostgreSQLInserter(db_config)
        
        if not inserter.connect():
            print("\n[ERROR] Failed to connect to database. Please check your credentials.")
            sys.exit(1)
        
        # Insert banks
        print("\n[Step 3/6] Inserting banks...")
        bank_mapping = inserter.insert_banks(df)
        
        # Insert reviews
        print("\n[Step 4/6] Inserting reviews...")
        reviews_inserted = inserter.insert_reviews(df, bank_mapping)
        
        # Print summary statistics
        print("\n[Step 5/6] Generating summary statistics...")
        inserter.print_summary_statistics()
        
        # Close connection
        print("\n[Step 6/6] Closing database connection...")
        inserter.close()
        
        print("\n" + "="*70)
        print("[SUCCESS] DATA INSERTION COMPLETED SUCCESSFULLY!")
        print("="*70)
        
    except Exception as e:
        print(f"\n[ERROR] Error during execution: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
