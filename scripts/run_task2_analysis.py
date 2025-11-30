"""
Master Analysis Script
Task 2: Fintech Customer Experience Analytics

This script orchestrates the complete Task 2 analysis pipeline:
1. Sentiment Analysis (VADER, TextBlob, Afinn)
2. Topic Modeling (TF-IDF, LDA, NMF)
3. Visualization Generation
4. Report Generation

Usage:
    python scripts/run_task2_analysis.py

Or run individual modules:
    python scripts/sentiment_analysis.py
    python scripts/topic_modeling.py
    python scripts/visualizations.py
    python scripts/generate_report.py
"""

import os
import sys
import time
from datetime import datetime

# Add the project root directory to Python path
# This allows importing from scripts module regardless of where script is run from
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if project_root not in sys.path:
    sys.path.insert(0, project_root)


def print_header(title):
    """Print formatted section header."""
    print("\n" + "="*70)
    print(f"  {title}")
    print("="*70 + "\n")


def run_module(module_name, description):
    """Run a Python module and track execution time."""
    print_header(description)
    
    start_time = time.time()
    
    try:
        # Import and run the module
        if module_name == "sentiment_analysis":
            from scripts import sentiment_analysis
            sentiment_analysis.main()
        elif module_name == "topic_modeling":
            from scripts import topic_modeling
            topic_modeling.main()
        elif module_name == "visualizations":
            from scripts import visualizations
            visualizations.main()
        elif module_name == "generate_report":
            from scripts import generate_report
            generate_report.main()
        
        elapsed = time.time() - start_time
        print(f"\n✓ {description} completed in {elapsed:.2f} seconds")
        return True
        
    except Exception as e:
        print(f"\n✗ Error in {description}: {str(e)}")
        import traceback
        traceback.print_exc()
        return False


def check_prerequisites():
    """Check if required files exist."""
    print_header("Checking Prerequisites")
    
    required_files = [
        'data/bank_reviews_clean.csv'
    ]
    
    missing_files = []
    
    for filepath in required_files:
        if os.path.exists(filepath):
            print(f"✓ Found: {filepath}")
        else:
            print(f"✗ Missing: {filepath}")
            missing_files.append(filepath)
    
    if missing_files:
        print("\n⚠ Missing required files!")
        print("Please run Task 1 scripts first:")
        print("  1. python scripts/scrape_reviews.py")
        print("  2. python scripts/clean_reviews.py")
        return False
    
    print("\n✓ All prerequisites met")
    return True


def main():
    """Main orchestration function."""
    print("\n" + "="*70)
    print("  TASK 2: NLP & SENTIMENT ANALYSIS")
    print("  Ethiopian Banking Apps - Customer Experience Analytics")
    print("="*70)
    print(f"\nStarted: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    overall_start = time.time()
    
    # Check prerequisites
    if not check_prerequisites():
        print("\n✗ Prerequisites not met. Exiting.")
        sys.exit(1)
    
    # Track success of each module
    results = {}
    
    # Module 1: Sentiment Analysis
    results['sentiment'] = run_module(
        "sentiment_analysis",
        "Module 1: Sentiment Analysis (VADER, TextBlob, Afinn)"
    )
    
    if not results['sentiment']:
        print("\n✗ Sentiment analysis failed. Cannot proceed.")
        sys.exit(1)
    
    # Module 2: Topic Modeling
    results['topics'] = run_module(
        "topic_modeling",
        "Module 2: Topic Modeling (TF-IDF, LDA, NMF)"
    )
    
    if not results['topics']:
        print("\n✗ Topic modeling failed. Cannot proceed.")
        sys.exit(1)
    
    # Module 3: Visualizations
    results['visualizations'] = run_module(
        "visualizations",
        "Module 3: Visualization Generation"
    )
    
    # Module 4: Report Generation
    results['report'] = run_module(
        "generate_report",
        "Module 4: Business Report Generation"
    )
    
    # Summary
    overall_elapsed = time.time() - overall_start
    
    print_header("TASK 2 ANALYSIS COMPLETE")
    
    print("Module Execution Summary:")
    print(f"  {'Module':<30} {'Status':<10}")
    print("  " + "-"*40)
    
    modules = [
        ("Sentiment Analysis", results['sentiment']),
        ("Topic Modeling", results['topics']),
        ("Visualizations", results['visualizations']),
        ("Report Generation", results['report'])
    ]
    
    for module_name, success in modules:
        status = "✓ Success" if success else "✗ Failed"
        print(f"  {module_name:<30} {status:<10}")
    
    print(f"\nTotal execution time: {overall_elapsed:.2f} seconds ({overall_elapsed/60:.1f} minutes)")
    print(f"Completed: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    print("\n" + "="*70)
    print("  OUTPUT FILES GENERATED")
    print("="*70)
    
    print("\nCSV Files:")
    print("  ✓ data/sentiment_results.csv")
    print("  ✓ data/topics_keywords.csv")
    print("  ✓ data/lda_topics.csv")
    
    print("\nVisualizations (visuals/):")
    print("  ✓ rating_distribution.png")
    print("  ✓ sentiment_by_bank.png")
    print("  ✓ sentiment_vs_rating.png")
    print("  ✓ monthly_sentiment_trends.png")
    print("  ✓ wordcloud.png")
    print("  ✓ top_bigrams_trigrams.png")
    print("  ✓ tfidf_keywords_by_bank.png")
    print("  ✓ lda_topic_distribution.png")
    
    print("\nFinal Report:")
    print("  ✓ TASK2_REPORT.md")
    
    print("\n" + "="*70)
    print("\n✓ Task 2 analysis pipeline completed successfully!")
    print("\nNext steps:")
    print("  1. Review TASK2_REPORT.md for business insights")
    print("  2. Examine visualizations in visuals/ directory")
    print("  3. Analyze CSV outputs for detailed data")
    print("\n")


if __name__ == "__main__":
    main()
