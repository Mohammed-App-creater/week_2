-- ============================================================================
-- Analytical SQL Queries for Fintech Customer Experience Analytics
-- Task 3: Database Queries and Analysis
-- ============================================================================

-- ============================================================================
-- 1. Count Reviews Per Bank
-- ============================================================================

-- Total reviews per bank with bank name
SELECT 
    b.bank_name,
    b.app_name,
    COUNT(r.review_id) AS total_reviews,
    MIN(r.review_date) AS first_review_date,
    MAX(r.review_date) AS last_review_date
FROM banks b
LEFT JOIN reviews r ON b.bank_id = r.bank_id
GROUP BY b.bank_id, b.bank_name, b.app_name
ORDER BY total_reviews DESC;

-- ============================================================================
-- 2. Average Rating Per Bank
-- ============================================================================

-- Average rating with additional statistics per bank
SELECT 
    b.bank_name,
    COUNT(r.review_id) AS total_reviews,
    ROUND(AVG(r.rating)::numeric, 2) AS avg_rating,
    MIN(r.rating) AS min_rating,
    MAX(r.rating) AS max_rating,
    MODE() WITHIN GROUP (ORDER BY r.rating) AS most_common_rating,
    ROUND(STDDEV(r.rating)::numeric, 2) AS rating_stddev
FROM banks b
LEFT JOIN reviews r ON b.bank_id = r.bank_id
GROUP BY b.bank_id, b.bank_name
ORDER BY avg_rating DESC NULLS LAST;

-- ============================================================================
-- 3. Count of Positive/Negative/Neutral Reviews
-- ============================================================================

-- Overall sentiment distribution
SELECT 
    sentiment_label,
    COUNT(*) AS review_count,
    ROUND(COUNT(*) * 100.0 / SUM(COUNT(*)) OVER (), 2) AS percentage
FROM reviews
WHERE sentiment_label IS NOT NULL
GROUP BY sentiment_label
ORDER BY review_count DESC;

-- Sentiment distribution per bank
SELECT 
    b.bank_name,
    r.sentiment_label,
    COUNT(*) AS review_count,
    ROUND(COUNT(*) * 100.0 / SUM(COUNT(*)) OVER (PARTITION BY b.bank_name), 2) AS percentage_within_bank
FROM banks b
JOIN reviews r ON b.bank_id = r.bank_id
WHERE r.sentiment_label IS NOT NULL
GROUP BY b.bank_name, r.sentiment_label
ORDER BY b.bank_name, r.sentiment_label;

-- Sentiment summary per bank (pivot-style)
SELECT 
    b.bank_name,
    COUNT(r.review_id) AS total_reviews,
    SUM(CASE WHEN r.sentiment_label = 'positive' THEN 1 ELSE 0 END) AS positive_count,
    SUM(CASE WHEN r.sentiment_label = 'neutral' THEN 1 ELSE 0 END) AS neutral_count,
    SUM(CASE WHEN r.sentiment_label = 'negative' THEN 1 ELSE 0 END) AS negative_count,
    ROUND(AVG(CASE WHEN r.sentiment_label = 'positive' THEN 100.0 ELSE 0 END), 2) AS positive_percentage,
    ROUND(AVG(CASE WHEN r.sentiment_label = 'negative' THEN 100.0 ELSE 0 END), 2) AS negative_percentage
FROM banks b
LEFT JOIN reviews r ON b.bank_id = r.bank_id
GROUP BY b.bank_id, b.bank_name
ORDER BY positive_percentage DESC;

-- ============================================================================
-- 4. Duplicate Detection Query
-- ============================================================================

-- Find duplicate reviews (same text, bank, and date)
SELECT 
    b.bank_name,
    r.review_text,
    r.review_date,
    r.rating,
    COUNT(*) AS duplicate_count
FROM reviews r
JOIN banks b ON r.bank_id = b.bank_id
GROUP BY b.bank_name, r.review_text, r.review_date, r.rating
HAVING COUNT(*) > 1
ORDER BY duplicate_count DESC, b.bank_name;

-- Find potential duplicate reviews (same text across different dates)
SELECT 
    b.bank_name,
    r.review_text,
    COUNT(*) AS occurrence_count,
    STRING_AGG(DISTINCT r.review_date::TEXT, ', ' ORDER BY r.review_date::TEXT) AS dates,
    STRING_AGG(DISTINCT r.rating::TEXT, ', ') AS ratings
FROM reviews r
JOIN banks b ON r.bank_id = b.bank_id
GROUP BY b.bank_name, r.review_text
HAVING COUNT(*) > 1
ORDER BY occurrence_count DESC;

-- Find reviews with identical text but different banks
SELECT 
    r.review_text,
    COUNT(DISTINCT r.bank_id) AS bank_count,
    STRING_AGG(DISTINCT b.bank_name, ', ') AS banks,
    COUNT(*) AS total_occurrences
FROM reviews r
JOIN banks b ON r.bank_id = b.bank_id
GROUP BY r.review_text
HAVING COUNT(DISTINCT r.bank_id) > 1
ORDER BY total_occurrences DESC;

-- ============================================================================
-- 5. Null Value Check
-- ============================================================================

-- Check for NULL values in banks table
SELECT 
    'banks' AS table_name,
    SUM(CASE WHEN bank_id IS NULL THEN 1 ELSE 0 END) AS null_bank_id,
    SUM(CASE WHEN bank_name IS NULL THEN 1 ELSE 0 END) AS null_bank_name,
    SUM(CASE WHEN app_name IS NULL THEN 1 ELSE 0 END) AS null_app_name,
    COUNT(*) AS total_rows
FROM banks;

-- Check for NULL values in reviews table
SELECT 
    'reviews' AS table_name,
    SUM(CASE WHEN review_id IS NULL THEN 1 ELSE 0 END) AS null_review_id,
    SUM(CASE WHEN bank_id IS NULL THEN 1 ELSE 0 END) AS null_bank_id,
    SUM(CASE WHEN review_text IS NULL THEN 1 ELSE 0 END) AS null_review_text,
    SUM(CASE WHEN rating IS NULL THEN 1 ELSE 0 END) AS null_rating,
    SUM(CASE WHEN review_date IS NULL THEN 1 ELSE 0 END) AS null_review_date,
    SUM(CASE WHEN sentiment_label IS NULL THEN 1 ELSE 0 END) AS null_sentiment_label,
    SUM(CASE WHEN sentiment_score IS NULL THEN 1 ELSE 0 END) AS null_sentiment_score,
    SUM(CASE WHEN source IS NULL THEN 1 ELSE 0 END) AS null_source,
    COUNT(*) AS total_rows
FROM reviews;

-- Detailed NULL check with percentages
SELECT 
    'review_text' AS column_name,
    SUM(CASE WHEN review_text IS NULL THEN 1 ELSE 0 END) AS null_count,
    ROUND(SUM(CASE WHEN review_text IS NULL THEN 1 ELSE 0 END) * 100.0 / COUNT(*), 2) AS null_percentage
FROM reviews
UNION ALL
SELECT 
    'sentiment_label',
    SUM(CASE WHEN sentiment_label IS NULL THEN 1 ELSE 0 END),
    ROUND(SUM(CASE WHEN sentiment_label IS NULL THEN 1 ELSE 0 END) * 100.0 / COUNT(*), 2)
FROM reviews
UNION ALL
SELECT 
    'sentiment_score',
    SUM(CASE WHEN sentiment_score IS NULL THEN 1 ELSE 0 END),
    ROUND(SUM(CASE WHEN sentiment_score IS NULL THEN 1 ELSE 0 END) * 100.0 / COUNT(*), 2)
FROM reviews
ORDER BY null_percentage DESC;

-- ============================================================================
-- 6. Additional Analytical Queries
-- ============================================================================

-- Reviews by source platform
SELECT 
    source,
    COUNT(*) AS review_count,
    ROUND(AVG(rating)::numeric, 2) AS avg_rating,
    ROUND(COUNT(*) * 100.0 / SUM(COUNT(*)) OVER (), 2) AS percentage
FROM reviews
GROUP BY source
ORDER BY review_count DESC;

-- Time-based analysis: Reviews per month
SELECT 
    DATE_TRUNC('month', review_date) AS month,
    COUNT(*) AS review_count,
    ROUND(AVG(rating)::numeric, 2) AS avg_rating
FROM reviews
GROUP BY DATE_TRUNC('month', review_date)
ORDER BY month DESC;

-- Rating distribution
SELECT 
    rating,
    COUNT(*) AS count,
    ROUND(COUNT(*) * 100.0 / SUM(COUNT(*)) OVER (), 2) AS percentage,
    REPEAT('█', (COUNT(*) * 50 / MAX(COUNT(*)) OVER ())::INT) AS bar_chart
FROM reviews
GROUP BY rating
ORDER BY rating DESC;

-- Top 10 most recent reviews per bank
SELECT 
    b.bank_name,
    r.review_text,
    r.rating,
    r.sentiment_label,
    r.review_date
FROM (
    SELECT 
        bank_id,
        review_text,
        rating,
        sentiment_label,
        review_date,
        ROW_NUMBER() OVER (PARTITION BY bank_id ORDER BY review_date DESC) AS rn
    FROM reviews
) r
JOIN banks b ON r.bank_id = b.bank_id
WHERE r.rn <= 10
ORDER BY b.bank_name, r.review_date DESC;

-- Correlation between rating and sentiment score
SELECT 
    rating,
    COUNT(*) AS review_count,
    ROUND(AVG(sentiment_score)::numeric, 3) AS avg_sentiment_score,
    ROUND(MIN(sentiment_score)::numeric, 3) AS min_sentiment_score,
    ROUND(MAX(sentiment_score)::numeric, 3) AS max_sentiment_score
FROM reviews
WHERE sentiment_score IS NOT NULL
GROUP BY rating
ORDER BY rating DESC;
