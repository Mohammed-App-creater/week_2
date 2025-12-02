-- ============================================================================
-- PostgreSQL Database Schema for Fintech Customer Experience Analytics
-- Task 3: Database Design and Implementation
-- ============================================================================

-- Create database
CREATE DATABASE fintech_reviews;

-- Connect to the database
\c fintech_reviews;

-- ============================================================================
-- Table 1: banks
-- Stores unique bank information and their associated app names
-- ============================================================================

CREATE TABLE banks (
    bank_id SERIAL PRIMARY KEY,
    bank_name TEXT NOT NULL UNIQUE,
    app_name TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Add comment to table
COMMENT ON TABLE banks IS 'Stores information about banks and their mobile applications';

-- Add comments to columns
COMMENT ON COLUMN banks.bank_id IS 'Unique identifier for each bank';
COMMENT ON COLUMN banks.bank_name IS 'Official name of the bank';
COMMENT ON COLUMN banks.app_name IS 'Name of the bank mobile application';

-- ============================================================================
-- Table 2: reviews
-- Stores customer reviews with sentiment analysis results
-- ============================================================================

CREATE TABLE reviews (
    review_id SERIAL PRIMARY KEY,
    bank_id INTEGER NOT NULL,
    review_text TEXT NOT NULL,
    rating INTEGER NOT NULL CHECK (rating >= 1 AND rating <= 5),
    review_date DATE NOT NULL,
    sentiment_label TEXT CHECK (sentiment_label IN ('positive', 'negative', 'neutral')),
    sentiment_score FLOAT CHECK (sentiment_score >= -1.0 AND sentiment_score <= 1.0),
    source TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    -- Foreign key constraint
    CONSTRAINT fk_bank
        FOREIGN KEY (bank_id)
        REFERENCES banks(bank_id)
        ON DELETE CASCADE
        ON UPDATE CASCADE
);

-- Add comment to table
COMMENT ON TABLE reviews IS 'Stores customer reviews with ratings and sentiment analysis';

-- Add comments to columns
COMMENT ON COLUMN reviews.review_id IS 'Unique identifier for each review';
COMMENT ON COLUMN reviews.bank_id IS 'Foreign key reference to banks table';
COMMENT ON COLUMN reviews.review_text IS 'The actual review text from customer';
COMMENT ON COLUMN reviews.rating IS 'Customer rating (1-5 stars)';
COMMENT ON COLUMN reviews.review_date IS 'Date when the review was posted';
COMMENT ON COLUMN reviews.sentiment_label IS 'Sentiment classification: positive, negative, or neutral';
COMMENT ON COLUMN reviews.sentiment_score IS 'Numerical sentiment score (-1.0 to 1.0)';
COMMENT ON COLUMN reviews.source IS 'Platform where review was posted (e.g., google_play, app_store)';

-- ============================================================================
-- Indexes for Performance Optimization
-- ============================================================================

-- Index on bank_id for faster joins
CREATE INDEX idx_reviews_bank_id ON reviews(bank_id);

-- Index on review_date for time-based queries
CREATE INDEX idx_reviews_date ON reviews(review_date DESC);

-- Index on rating for filtering and aggregation
CREATE INDEX idx_reviews_rating ON reviews(rating);

-- Index on sentiment_label for sentiment analysis queries
CREATE INDEX idx_reviews_sentiment ON reviews(sentiment_label);

-- Index on source for platform-specific analysis
CREATE INDEX idx_reviews_source ON reviews(source);

-- Composite index for common query patterns
CREATE INDEX idx_reviews_bank_date ON reviews(bank_id, review_date DESC);

-- Index on bank_name for search operations
CREATE INDEX idx_banks_name ON banks(bank_name);

-- ============================================================================
-- Additional Constraints and Triggers
-- ============================================================================

-- Trigger to update updated_at timestamp for banks table
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER update_banks_updated_at
    BEFORE UPDATE ON banks
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();

-- ============================================================================
-- Verification Queries
-- ============================================================================

-- Verify tables were created
SELECT table_name 
FROM information_schema.tables 
WHERE table_schema = 'public' 
ORDER BY table_name;

-- Verify indexes were created
SELECT indexname, tablename 
FROM pg_indexes 
WHERE schemaname = 'public' 
ORDER BY tablename, indexname;

-- Verify constraints
SELECT 
    tc.table_name, 
    tc.constraint_name, 
    tc.constraint_type
FROM information_schema.table_constraints tc
WHERE tc.table_schema = 'public'
ORDER BY tc.table_name, tc.constraint_type;
