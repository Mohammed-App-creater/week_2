"""
Download required NLTK data packages
"""
import nltk

print("Downloading NLTK data packages...")

# Download required packages
packages = [
    'stopwords', 
    'punkt', 
    'punkt_tab',  # Additional punkt data
    'wordnet', 
    'averaged_perceptron_tagger',
    'averaged_perceptron_tagger_eng',  # English-specific tagger
    'omw-1.4'
]

for package in packages:
    try:
        print(f"\nDownloading {package}...")
        nltk.download(package, quiet=False)
        print(f"✓ {package} downloaded successfully")
    except Exception as e:
        print(f"⚠ Warning downloading {package}: {e}")

print("\n✓ All NLTK data packages downloaded!")

# Test if stopwords work
try:
    from nltk.corpus import stopwords
    stop_words = stopwords.words('english')
    print(f"\n✓ Stopwords test successful! Found {len(stop_words)} English stopwords")
except Exception as e:
    print(f"\n✗ Stopwords test failed: {e}")
