# Task 4: Insights & Recommendations - Reproduction Guide

## 📋 Overview

This guide provides step-by-step instructions to reproduce the Task 4 analysis, visualizations, and insights report for the Fintech Customer Experience Analytics project.

---

## 🎯 Deliverables

This task produces the following outputs:

### Visualizations (5 PNG files in `visuals/`)
1. `rating_distribution_by_bank.png` - Bar chart showing 1-5 star rating distribution per bank
2. `avg_sentiment_by_bank.png` - Bar chart with error bars showing average VADER sentiment scores
3. `monthly_sentiment_trend.png` - Line chart showing sentiment trends over time
4. `top_negative_keywords.png` - Bar chart of top 15 keywords from negative reviews
5. `topic_prevalence_by_bank.png` - Stacked bar chart showing topic distribution

### Output Tables (2 CSV files in `outputs/`)
1. `bank_summary.csv` - Bank-level summary statistics
2. `top_negative_keywords.csv` - Top keywords from negative reviews with frequencies

### Reports & Documentation
1. `TASK4_REPORT.md` - Comprehensive insights and recommendations report (10 pages)
2. `README_TASK4.md` - This file
3. `scripts/plot_task4.py` - Python script to generate all visualizations and tables

---

## 🔧 Prerequisites

### Required Software
- Python 3.8 or higher
- pip (Python package manager)

### Required Python Packages

Install dependencies:

```bash
pip install pandas matplotlib seaborn numpy
```

Or using the project requirements file:

```bash
pip install -r requirements_task3.txt  # If pandas is already installed
```

**Package Versions** (tested):
- pandas >= 2.0.0
- matplotlib >= 3.7.0
- seaborn >= 0.12.0
- numpy >= 1.24.0

---

## 📂 Required Input Files

Ensure the following files exist in your project directory:

```
week_2/
├── data/
│   ├── sentiment_results.csv    # 979 reviews with sentiment scores
│   └── topics_keywords.csv       # Topic modeling outputs (LDA, NMF, TF-IDF)
└── scripts/
    └── plot_task4.py             # Visualization script
```

**Data Requirements**:
- `sentiment_results.csv` must contain columns: `review`, `rating`, `date`, `bank`, `source`, `vader_compound`, `textblob_polarity`, `textblob_subjectivity`, `afinn_score`, `sentiment_category`
- `topics_keywords.csv` must contain columns: `model`, `topic_id`, `word`, `weight`

---

## 🚀 Step-by-Step Instructions

### Step 1: Navigate to Project Directory

```bash
cd c:\Users\yoga\code\10_Academy\week_2
```

### Step 2: Verify Input Files Exist

```bash
# Windows Command Prompt
dir data\sentiment_results.csv
dir data\topics_keywords.csv

# Or PowerShell
ls data/sentiment_results.csv
ls data/topics_keywords.csv
```

### Step 3: Run the Visualization Script

```bash
python scripts/plot_task4.py
```

**Expected Console Output**:

```
======================================================================
Task 4: Visualization and Analysis Script
======================================================================
[OK] Output directories ready
Loading data...
[OK] Loaded 979 reviews
[OK] Loaded 160 topic keywords

======================================================================
GENERATING VISUALIZATIONS
======================================================================

[1/5] Generating rating distribution chart...
  [OK] Saved: visuals/rating_distribution_by_bank.png

[2/5] Generating average sentiment chart...
  [OK] Saved: visuals/avg_sentiment_by_bank.png

[3/5] Generating monthly sentiment trend chart...
  [OK] Saved: visuals/monthly_sentiment_trend.png

[4/5] Generating top negative keywords chart...
  [OK] Saved: visuals/top_negative_keywords.png

[5/5] Generating topic prevalence chart...
  [OK] Saved: visuals/topic_prevalence_by_bank.png

======================================================================
GENERATING OUTPUT TABLES
======================================================================

[Output 1/2] Generating bank summary table...
  [OK] Saved: outputs/bank_summary.csv

                       bank  total_reviews  avg_rating  avg_vader  pct_negative_reviews
          Bank of Abyssinia            336        3.15      0.105                 22.62
Commercial Bank of Ethiopia            316        3.98      0.232                  9.18
                Dashen Bank            327        3.80      0.288                 14.68

[Output 2/2] Generating top negative keywords table...
  [OK] Saved: outputs/top_negative_keywords.csv

keyword  count  pct_negative_mentions
    app    115                  75.16
    not     38                  24.84
  worst     34                  22.22
   bank     28                  18.30
   very     23                  15.03

======================================================================
[SUCCESS] ALL OUTPUTS GENERATED SUCCESSFULLY!
======================================================================
```

### Step 4: Verify Output Files

```bash
# Check visualizations
dir visuals\*.png

# Check output tables
dir outputs\*.csv

# Expected files:
# visuals/rating_distribution_by_bank.png
# visuals/avg_sentiment_by_bank.png
# visuals/monthly_sentiment_trend.png
# visuals/top_negative_keywords.png
# visuals/topic_prevalence_by_bank.png
# outputs/bank_summary.csv
# outputs/top_negative_keywords.csv
```

### Step 5: Review the Insights Report

Open the comprehensive report:

```bash
# Windows
start TASK4_REPORT.md

# Or open in your preferred markdown viewer
```

---

## 📊 Expected Outputs

### Visualizations

All PNG files will be saved at **300 DPI** resolution with professional styling:
- Clear titles and axis labels
- Color-coded by bank (CBE: Blue, BOA: Purple, Dashen: Orange)
- Grid lines for readability
- Value labels on bars/points where appropriate

### Output Tables

#### `bank_summary.csv`

| bank | total_reviews | avg_rating | avg_vader | pct_negative_reviews |
|------|---------------|------------|-----------|---------------------|
| Bank of Abyssinia | 336 | 3.15 | 0.105 | 22.62 |
| Commercial Bank of Ethiopia | 316 | 3.98 | 0.232 | 9.18 |
| Dashen Bank | 327 | 3.80 | 0.288 | 14.68 |

#### `top_negative_keywords.csv`

| keyword | count | pct_negative_mentions |
|---------|-------|----------------------|
| app | 115 | 75.16 |
| not | 38 | 24.84 |
| worst | 34 | 22.22 |
| ... | ... | ... |

---

## 🔍 Troubleshooting

### Issue: ModuleNotFoundError

**Error**: `ModuleNotFoundError: No module named 'pandas'` (or matplotlib, seaborn, numpy)

**Solution**:
```bash
pip install pandas matplotlib seaborn numpy
```

### Issue: FileNotFoundError

**Error**: `FileNotFoundError: [Errno 2] No such file or directory: 'data/sentiment_results.csv'`

**Solution**:
- Verify you're in the correct directory: `c:\Users\yoga\code\10_Academy\week_2`
- Check that input files exist in `data/` folder
- Ensure file names match exactly (case-sensitive on some systems)

### Issue: Permission Denied

**Error**: `PermissionError: [Errno 13] Permission denied: 'visuals/...'`

**Solution**:
- Close any programs that might have the files open (image viewers, Excel)
- Ensure you have write permissions to the `visuals/` and `outputs/` directories
- Run command prompt as administrator (if necessary)

### Issue: UnicodeEncodeError

**Error**: `UnicodeEncodeError: 'charmap' codec can't encode character`

**Solution**: This has been fixed in the script by using ASCII-compatible characters. If you still encounter this, ensure you're using Python 3.8+.

### Issue: Empty or Incorrect Visualizations

**Symptoms**: Charts generated but appear empty or incorrect

**Solution**:
- Verify input CSV files have correct structure and data
- Check for data quality issues (missing values, incorrect date formats)
- Review console output for warnings or errors during generation

---

## 📁 File Structure

After running the script, your directory structure should look like:

```
week_2/
├── data/
│   ├── sentiment_results.csv
│   └── topics_keywords.csv
├── scripts/
│   └── plot_task4.py
├── visuals/
│   ├── rating_distribution_by_bank.png
│   ├── avg_sentiment_by_bank.png
│   ├── monthly_sentiment_trend.png
│   ├── top_negative_keywords.png
│   └── topic_prevalence_by_bank.png
├── outputs/
│   ├── bank_summary.csv
│   └── top_negative_keywords.csv
├── TASK4_REPORT.md
└── README_TASK4.md
```

---

## 🔄 Regenerating Outputs

To regenerate all outputs (e.g., after data updates):

```bash
# Simply re-run the script
python scripts/plot_task4.py
```

The script will overwrite existing files in `visuals/` and `outputs/` directories.

---

## 📖 Understanding the Outputs

### Key Metrics Explained

**VADER Compound Score**: Ranges from -1 (most negative) to +1 (most positive). Scores:
- ≥ 0.05: Positive sentiment
- -0.05 to 0.05: Neutral sentiment
- ≤ -0.05: Negative sentiment

**Rating Distribution**: Shows how many reviews fall into each star category (1-5). Helps identify:
- Polarization (high 1-star and 5-star, low middle)
- Consistency (even distribution vs. skewed)

**Sentiment Trend**: Monthly average sentiment scores reveal:
- Improvement or decline over time
- Impact of app updates or incidents
- Seasonal patterns

**Negative Keywords**: Most frequent words in negative reviews indicate:
- Primary pain points (e.g., "crash", "slow")
- Feature requests (e.g., "need", "add")
- Technical issues (e.g., "error", "bug")

---

## 🎓 Advanced Usage

### Customizing Visualizations

Edit `scripts/plot_task4.py` to customize:

**Colors**: Modify `BANK_COLORS` dictionary (line 31-35)
```python
BANK_COLORS = {
    'Commercial Bank of Ethiopia': '#YOUR_COLOR',
    'Bank of Abyssinia': '#YOUR_COLOR',
    'Dashen Bank': '#YOUR_COLOR'
}
```

**Figure Size**: Modify `plt.rcParams['figure.figsize']` (line 26)
```python
plt.rcParams['figure.figsize'] = (14, 7)  # Width, Height in inches
```

**DPI (Resolution)**: Modify `dpi` parameter in `plt.savefig()` calls
```python
plt.savefig('visuals/chart.png', dpi=600)  # Higher = better quality, larger file
```

### Filtering Data

To analyze specific time periods, add filtering before visualization:

```python
# In load_data() function, after loading sentiment_df:
sentiment_df = sentiment_df[sentiment_df['date'] >= '2025-01-01']  # Only 2025 data
```

---

## 📞 Support

For questions or issues:

1. **Check this README** for troubleshooting steps
2. **Review console output** for specific error messages
3. **Verify input data** matches expected format
4. **Check Python/package versions** meet requirements

---

## 📚 Related Documentation

- [TASK4_REPORT.md](file:///c:/Users/yoga/code/10_Academy/week_2/TASK4_REPORT.md) - Full insights and recommendations report
- [plot_task4.py](file:///c:/Users/yoga/code/10_Academy/week_2/scripts/plot_task4.py) - Visualization script source code
- [Task 3 README](file:///c:/Users/yoga/code/10_Academy/week_2/README_TASK3.md) - Database integration guide

---

## ✅ Verification Checklist

After running the script, verify:

- [ ] 5 PNG files created in `visuals/` directory
- [ ] 2 CSV files created in `outputs/` directory
- [ ] No errors in console output
- [ ] Visualizations display correctly when opened
- [ ] CSV files contain expected data
- [ ] File sizes are reasonable (PNGs: 50-500KB each)

---

**Last Updated**: December 2, 2025  
**Script Version**: 1.0  
**Compatible with**: Python 3.8+, pandas 2.0+, matplotlib 3.7+, seaborn 0.12+
