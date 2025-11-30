# Task 1: Web Scraping & Data Preprocessing - Ethiopian Banking Apps

## Project Overview

This project scrapes and analyzes customer reviews from Google Play Store for three major Ethiopian banking mobile applications:

- **Commercial Bank of Ethiopia (CBE)** - Mobile Banking App
- **Bank of Abyssinia (BOA)** - Mobile Banking App  
- **Dashen Bank** - Mobile Banking App

**Objective**: Collect and preprocess 1200+ customer reviews to enable sentiment analysis and customer experience insights.

---

## Project Structure

```
week_2/
├── data/
│   ├── raw/                          # Raw scraped data per bank
│   │   ├── cbe_reviews.csv
│   │   ├── boa_reviews.csv
│   │   └── dashen_reviews.csv
│   ├── bank_reviews_raw.csv          # Combined raw data
│   └── bank_reviews_clean.csv        # Final cleaned dataset
├── scripts/
│   ├── scrape_reviews.py             # Web scraping script
│   └── clean_reviews.py              # Data cleaning script
├── requirements.txt                   # Python dependencies
└── README.md                          # This file
```

---

## Installation

### Prerequisites
- Python 3.8 or higher
- pip package manager
- Internet connection for scraping

### Setup Instructions

1. **Clone or navigate to the project directory**:
   ```bash
   cd week_2
   ```

2. **Install required dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

---

## Usage

### Step 1: Scrape Reviews

Run the scraping script to collect reviews from Google Play Store:

```bash
python scripts/scrape_reviews.py
```

**What it does**:
- Scrapes 400+ reviews per banking app (1200+ total)
- Saves individual bank data to `data/raw/`
- Creates combined dataset at `data/bank_reviews_raw.csv`
- Displays progress and summary statistics

**Expected output**:
```
SCRAPING SUMMARY
Total reviews collected: 1200+
Reviews per bank:
  • Commercial Bank of Ethiopia: 400+
  • Bank of Abyssinia: 400+
  • Dashen Bank: 400+
```

### Step 2: Clean and Preprocess Data

Run the cleaning script to preprocess the scraped data:

```bash
python scripts/clean_reviews.py
```

**What it does**:
- Removes duplicate reviews
- Handles missing values
- Normalizes dates to YYYY-MM-DD format
- Cleans and trims text data
- Validates data quality
- Generates quality report
- Saves cleaned data to `data/bank_reviews_clean.csv`

**Expected output**:
```
DATA QUALITY REPORT
Dataset Statistics:
  • Initial reviews: 1200+
  • Duplicates removed: X
  • Final reviews: 1200+
  • Data retention rate: XX%
```

---

## Output Schema

The final cleaned dataset (`data/bank_reviews_clean.csv`) contains the following columns:

| Column   | Type   | Description                                    |
|----------|--------|------------------------------------------------|
| review   | string | Customer review text                           |
| rating   | int    | Star rating (1-5)                              |
| date     | string | Review date in YYYY-MM-DD format               |
| bank     | string | Bank name (CBE, BOA, or Dashen)                |
| source   | string | Data source (always "google_play")             |

---

## Data Preprocessing Logic

### 1. Duplicate Removal
- Identifies duplicates based on `review_text` and `bank_name`
- Keeps first occurrence, removes subsequent duplicates

### 2. Missing Value Handling
- **Review text**: Drops rows with missing review text (critical field)
- **Ratings**: Fills missing values with median rating
- **Dates**: Drops rows with missing or invalid dates

### 3. Date Normalization
- Converts all date formats to standard YYYY-MM-DD
- Drops rows where date parsing fails

### 4. Text Cleaning
- Trims leading/trailing whitespace
- Removes extra spaces (multiple spaces → single space)
- Removes non-printable characters
- Drops reviews with empty text after cleaning

### 5. Schema Standardization
- Renames columns to final schema
- Ensures consistent column order

### 6. Validation
- Checks for remaining duplicates
- Validates rating range (1-5)
- Confirms no missing values
- Verifies no empty reviews

---

## Dataset Summary

### Expected Statistics
- **Total Reviews**: 1200+ (400+ per bank)
- **Date Range**: Recent reviews from Google Play Store
- **Rating Distribution**: 1-5 stars
- **Average Review Length**: ~100-300 characters
- **Data Quality**: >95% retention rate after cleaning

### Quality Metrics
- ✓ No duplicates
- ✓ No missing values
- ✓ All ratings in valid range (1-5)
- ✓ All dates in YYYY-MM-DD format
- ✓ No empty review texts

---

## Git Workflow Instructions

### Initial Setup

1. **Initialize Git repository** (if not already done):
   ```bash
   git init
   ```

2. **Create `.gitignore`** to exclude unnecessary files:
   ```bash
   echo "*.pyc" >> .gitignore
   echo "__pycache__/" >> .gitignore
   echo ".ipynb_checkpoints/" >> .gitignore
   echo "*.log" >> .gitignore
   ```

3. **Create and switch to task-1 branch**:
   ```bash
   git checkout -b task-1
   ```

### Committing Your Work

4. **Add all project files**:
   ```bash
   git add .
   ```

5. **Commit with descriptive message**:
   ```bash
   git commit -m "Task 1: Add web scraping and data preprocessing scripts

   - Implemented scrape_reviews.py to collect 1200+ reviews from Google Play
   - Created clean_reviews.py for data preprocessing and validation
   - Added requirements.txt with project dependencies
   - Generated clean dataset: data/bank_reviews_clean.csv
   - Documented project setup and usage in README.md"
   ```

### Merging to Main

6. **Switch to main branch**:
   ```bash
   git checkout main
   ```

7. **Merge task-1 branch**:
   ```bash
   git merge task-1
   ```

8. **Push to remote repository** (if using GitHub):
   ```bash
   git remote add origin <your-repository-url>
   git push -u origin main
   ```

### GitHub Repository Setup

If you haven't created a GitHub repository yet:

1. **Create repository on GitHub**:
   - Go to https://github.com/new
   - Repository name: `fintech-customer-analytics` (or your preferred name)
   - Description: "Week 2: Fintech Customer Experience Analytics"
   - Choose Public or Private
   - Click "Create repository"

2. **Link local repository to GitHub**:
   ```bash
   git remote add origin https://github.com/YOUR_USERNAME/fintech-customer-analytics.git
   git branch -M main
   git push -u origin main
   ```

3. **Push task-1 branch** (optional, for review):
   ```bash
   git push -u origin task-1
   ```

---

## Troubleshooting

### Scraping Issues

**Problem**: "No reviews collected"
- **Solution**: Check internet connection and verify app IDs are correct

**Problem**: "Fewer than 400 reviews per app"
- **Solution**: Some apps may have fewer available reviews. The script collects as many as available.

### Cleaning Issues

**Problem**: "Input file not found"
- **Solution**: Run `scrape_reviews.py` first to generate raw data

**Problem**: "High data loss during cleaning"
- **Solution**: Review the quality report to identify which cleaning step removed data

---

## Next Steps

After completing Task 1, you can:
1. Perform exploratory data analysis (EDA) on the cleaned dataset
2. Conduct sentiment analysis on customer reviews
3. Identify common themes and pain points
4. Compare customer satisfaction across banks
5. Generate insights for business recommendations

---

## Author

**10 Academy - Week 2 Project**  
Fintech Customer Experience Analytics

---

## License

This project is for educational purposes as part of the 10 Academy training program.
