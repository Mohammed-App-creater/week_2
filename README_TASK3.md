# Task 3: PostgreSQL Database Integration

## 📋 Overview

This task involves designing and implementing a PostgreSQL relational database for the Fintech Customer Experience Analytics project. The database stores bank information and customer reviews with sentiment analysis results.

---

## 🗄️ Database Schema

### Entity Relationship Diagram (ERD)

```
┌─────────────────────────────┐
│         banks               │
├─────────────────────────────┤
│ PK  bank_id (SERIAL)        │
│     bank_name (TEXT) UNIQUE │
│     app_name (TEXT)         │
│     created_at (TIMESTAMP)  │
│     updated_at (TIMESTAMP)  │
└─────────────────────────────┘
              │
              │ 1
              │
              │
              │ N
              ▼
┌─────────────────────────────┐
│        reviews              │
├─────────────────────────────┤
│ PK  review_id (SERIAL)      │
│ FK  bank_id (INTEGER)       │
│     review_text (TEXT)      │
│     rating (INTEGER 1-5)    │
│     review_date (DATE)      │
│     sentiment_label (TEXT)  │
│     sentiment_score (FLOAT) │
│     source (TEXT)           │
│     created_at (TIMESTAMP)  │
└─────────────────────────────┘
```

### Table Descriptions

#### **Table 1: banks**

Stores unique bank information and their associated mobile applications.

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| `bank_id` | SERIAL | PRIMARY KEY | Unique identifier for each bank |
| `bank_name` | TEXT | NOT NULL, UNIQUE | Official name of the bank |
| `app_name` | TEXT | - | Name of the bank's mobile application |
| `created_at` | TIMESTAMP | DEFAULT CURRENT_TIMESTAMP | Record creation timestamp |
| `updated_at` | TIMESTAMP | DEFAULT CURRENT_TIMESTAMP | Record update timestamp |

#### **Table 2: reviews**

Stores customer reviews with ratings and sentiment analysis results.

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| `review_id` | SERIAL | PRIMARY KEY | Unique identifier for each review |
| `bank_id` | INTEGER | FOREIGN KEY → banks.bank_id, NOT NULL | Reference to the bank |
| `review_text` | TEXT | NOT NULL | The actual review text from customer |
| `rating` | INTEGER | NOT NULL, CHECK (1-5) | Customer rating (1-5 stars) |
| `review_date` | DATE | NOT NULL | Date when review was posted |
| `sentiment_label` | TEXT | CHECK (positive/negative/neutral) | Sentiment classification |
| `sentiment_score` | FLOAT | CHECK (-1.0 to 1.0) | Numerical sentiment score |
| `source` | TEXT | NOT NULL | Platform (e.g., google_play, app_store) |
| `created_at` | TIMESTAMP | DEFAULT CURRENT_TIMESTAMP | Record creation timestamp |

### Key Features

- **Foreign Key Constraint**: `reviews.bank_id` references `banks.bank_id` with CASCADE on DELETE/UPDATE
- **Check Constraints**: 
  - Rating must be between 1 and 5
  - Sentiment score must be between -1.0 and 1.0
  - Sentiment label must be 'positive', 'negative', or 'neutral'
- **Indexes**: Optimized for common query patterns (bank_id, review_date, rating, sentiment_label, source)
- **Triggers**: Automatic update of `updated_at` timestamp for banks table

---

## 🚀 Setup Instructions

### Prerequisites

1. **PostgreSQL Installation**
   - Download and install PostgreSQL from [postgresql.org](https://www.postgresql.org/download/)
   - Ensure PostgreSQL service is running
   - Default port: 5432

2. **Python Dependencies**
   ```bash
   pip install psycopg2-binary pandas
   ```

### Step 1: Create Database and Schema

```bash
# Connect to PostgreSQL
psql -U postgres

# Run the schema file
\i c:/Users/yoga/code/10_Academy/week_2/sql/schema.sql
```

Or using command line:

```bash
psql -U postgres -f c:/Users/yoga/code/10_Academy/week_2/sql/schema.sql
```

### Step 2: Configure Database Credentials

Edit [insert_into_postgres.py](file:///c:/Users/yoga/code/10_Academy/week_2/scripts/insert_into_postgres.py) and update the database configuration:

```python
db_config = {
    'host': 'localhost',
    'port': '5432',
    'database': 'fintech_reviews',
    'user': 'your_username',      # ← Change this
    'password': 'your_password'   # ← Change this
}
```

### Step 3: Run the Insertion Script

```bash
cd c:\Users\yoga\code\10_Academy\week_2
python scripts/insert_into_postgres.py
```

### Expected Output

```
======================================================================
🚀 PostgreSQL Data Insertion Script
======================================================================

📂 Step 1: Loading CSV data...
✓ Successfully loaded CSV file: c:\Users\yoga\code\10_Academy\week_2\data\bank_reviews_clean.csv
  Rows: 5, Columns: 5
✓ All required columns present: ['review', 'rating', 'date', 'bank', 'source']

🔌 Step 2: Connecting to PostgreSQL...
✓ Successfully connected to PostgreSQL database

🏦 Step 3: Inserting banks...
📊 Inserting 1 unique banks...
✓ Successfully inserted 1 banks

📝 Step 4: Inserting reviews...
📊 Inserting 5 reviews...
✓ Successfully inserted 5 reviews

📊 Step 5: Generating summary statistics...
======================================================================
📈 DATABASE SUMMARY STATISTICS
======================================================================

🏦 Total Banks: 1
📝 Total Reviews: 5

📊 Reviews per Bank:
   • Commercial Bank of Ethiopia: 5 reviews

⭐ Average Rating: 4.00/5.0

📊 Rating Distribution:
   5⭐:    3 (60.00%) ██████████████████████████████
   3⭐:    1 (20.00%) ██████████
   2⭐:    1 (20.00%) ██████████

📱 Reviews by Source:
   • google_play: 5 reviews

📅 Date Range: 2025-11-28 to 2025-11-29

======================================================================

✅ DATA INSERTION COMPLETED SUCCESSFULLY!
======================================================================
```

---

## 📊 Example SQL Queries

### 1. Count Reviews Per Bank

```sql
SELECT 
    b.bank_name,
    COUNT(r.review_id) AS total_reviews,
    MIN(r.review_date) AS first_review_date,
    MAX(r.review_date) AS last_review_date
FROM banks b
LEFT JOIN reviews r ON b.bank_id = r.bank_id
GROUP BY b.bank_id, b.bank_name
ORDER BY total_reviews DESC;
```

### 2. Average Rating Per Bank

```sql
SELECT 
    b.bank_name,
    COUNT(r.review_id) AS total_reviews,
    ROUND(AVG(r.rating)::numeric, 2) AS avg_rating,
    MIN(r.rating) AS min_rating,
    MAX(r.rating) AS max_rating
FROM banks b
LEFT JOIN reviews r ON b.bank_id = r.bank_id
GROUP BY b.bank_id, b.bank_name
ORDER BY avg_rating DESC;
```

### 3. Sentiment Distribution

```sql
SELECT 
    b.bank_name,
    COUNT(r.review_id) AS total_reviews,
    SUM(CASE WHEN r.sentiment_label = 'positive' THEN 1 ELSE 0 END) AS positive_count,
    SUM(CASE WHEN r.sentiment_label = 'neutral' THEN 1 ELSE 0 END) AS neutral_count,
    SUM(CASE WHEN r.sentiment_label = 'negative' THEN 1 ELSE 0 END) AS negative_count
FROM banks b
LEFT JOIN reviews r ON b.bank_id = r.bank_id
GROUP BY b.bank_id, b.bank_name;
```

### 4. Detect Duplicate Reviews

```sql
SELECT 
    b.bank_name,
    r.review_text,
    r.review_date,
    COUNT(*) AS duplicate_count
FROM reviews r
JOIN banks b ON r.bank_id = b.bank_id
GROUP BY b.bank_name, r.review_text, r.review_date
HAVING COUNT(*) > 1
ORDER BY duplicate_count DESC;
```

### 5. Check for NULL Values

```sql
SELECT 
    'reviews' AS table_name,
    SUM(CASE WHEN review_text IS NULL THEN 1 ELSE 0 END) AS null_review_text,
    SUM(CASE WHEN sentiment_label IS NULL THEN 1 ELSE 0 END) AS null_sentiment_label,
    SUM(CASE WHEN sentiment_score IS NULL THEN 1 ELSE 0 END) AS null_sentiment_score,
    COUNT(*) AS total_rows
FROM reviews;
```

> [!TIP]
> More comprehensive queries are available in [queries.sql](file:///c:/Users/yoga/code/10_Academy/week_2/sql/queries.sql)

---

## 📁 File Structure

```
week_2/
├── sql/
│   ├── schema.sql              # Database schema definition
│   └── queries.sql             # Analytical SQL queries
├── scripts/
│   └── insert_into_postgres.py # Python insertion script
├── data/
│   └── bank_reviews_clean.csv  # Cleaned review data
└── README_TASK3.md             # This file
```

---

## 🔧 Troubleshooting

### Connection Issues

**Problem**: `psycopg2.OperationalError: could not connect to server`

**Solutions**:
- Verify PostgreSQL service is running
- Check host and port in `db_config`
- Verify username and password
- Check firewall settings

### Permission Issues

**Problem**: `permission denied for database`

**Solutions**:
```sql
-- Grant necessary permissions
GRANT ALL PRIVILEGES ON DATABASE fintech_reviews TO your_username;
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO your_username;
GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA public TO your_username;
```

### CSV Loading Issues

**Problem**: `FileNotFoundError: CSV file not found`

**Solution**: Update the `csv_path` variable in [insert_into_postgres.py](file:///c:/Users/yoga/code/10_Academy/week_2/scripts/insert_into_postgres.py#L227) with the correct absolute path.

---

## 🎯 Next Steps

After successful insertion, you can:

1. **Add Sentiment Analysis**: Update `sentiment_label` and `sentiment_score` columns using NLP techniques
2. **Create Views**: Build materialized views for common analytical queries
3. **Add Indexes**: Optimize query performance based on usage patterns
4. **Implement Backup**: Set up automated database backups
5. **Create Dashboard**: Connect to visualization tools (Tableau, Power BI, Grafana)

---

## 📚 Additional Resources

- [PostgreSQL Documentation](https://www.postgresql.org/docs/)
- [psycopg2 Documentation](https://www.psycopg.org/docs/)
- [SQL Best Practices](https://www.postgresql.org/docs/current/sql.html)

---

## ✅ Quality Checklist

- [x] Proper data types used
- [x] Meaningful constraints (NOT NULL, FK, CHECK)
- [x] Indexes for performance optimization
- [x] Parameterized SQL (prevents SQL injection)
- [x] Error handling and graceful failures
- [x] Summary statistics after insertion
- [x] No invented data - schema matches actual CSV
- [x] Professional code formatting
- [x] Consistent naming conventions

---

**Author**: Task 3 - PostgreSQL Database Integration  
**Date**: 2025-12-02  
**Version**: 1.0
