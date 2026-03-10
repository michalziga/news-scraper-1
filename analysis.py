import os
import pickle
import re
from collections import Counter
import nltk
from nltk.corpus import stopwords

# Download stopwords if not installed
nltk.download("stopwords")

STOPWORDS = set(stopwords.words("english"))

def load_all_articles():
    articles = []

    for file in os.listdir():
        if file.endswith(".pkl"):
            print(f"Loading {file}")
            with open(file, "rb") as f:
                data = pickle.load(f)
                articles.extend(data)

    return articles


def combine_text(articles):
    all_text = ""

    for article in articles:
        if "full_text" in article:
            all_text += article["full_text"] + " "

    return all_text


def preprocess_text(text):
    # lowercase normalization
    text = text.lower()

    # remove punctuation
    text = re.sub(r"[^a-z\s]", "", text)

    # tokenize
    words = text.split()

    # remove stopwords
    words = [word for word in words if word not in STOPWORDS]

    return words


def analyze_words(words):
    counter = Counter(words)
    return counter.most_common(10)


def save_results(results):
    filename = "analysis_results.txt"

    with open(filename, "w") as f:
        f.write("Top 10 Most Frequent Words\n")
        f.write("=" * 30 + "\n")

        for word, count in results:
            f.write(f"{word}: {count}\n")

    print(f"Results saved to {filename}")


def main():
    print("Loading news files...")
    articles = load_all_articles()

    print(f"Loaded {len(articles)} articles")

    print("Combining text...")
    text = combine_text(articles)

    print("Processing text...")
    words = preprocess_text(text)

    print("Analyzing word frequency...")
    top_words = analyze_words(words)

    print("\nTop 10 Most Frequent Words")
    print("=" * 30)

    for word, count in top_words:
        print(f"{word}: {count}")

    save_results(top_words)


if __name__ == "__main__":
    main()
