import os
import pickle
import re
from collections import Counter

#import nltk
#from nltk.corpus import stopwords

# Download stopwords if not installed
#nltk.download("stopwords")

#STOPWORDS = set(stopwords.words("english"))

def simple_tokenize(text, stopwords=None):
    if not text:
        return[]
    text = text.lower()
    text = re.sub(r"[^a-z\s]", "", text)

    tokens = text.split()

    if stopwords:
        tokens = [t for t in tokens if t not in stopwords]
    return tokens



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

stopwords_set = set({ 
    "the", "in", "and", "of", "to", "a", "on", "for", "with", "is", "was", "as",
    "at", "by", "an", "from", "that", "this", "it", "be", "are", "has", "have", "we", "he", "not", "said", "her", "his", "but", "they", "my", "where"
})  

keywords_tech = [
    "rocket",
    "missile",
    "fighter",
    "jet",
    "drone",
    "uav",
    "bomb",
    "munition",
    "airdefense",
    "sam",
    "cruisemissile",
    "ballisticmissile",
    "stealthaircraft",
    "bomber",
    "interceptor",
    "armeddrone",
    "precisionmunition"
]

keywords_leaders = [
    "mojtaba", 
    "khamenei",
    "masoud", 
    "pezeshkian",
    "abbas", 
    "araghchi",
    "mohammad", 
    "pakpour",
    "donald", 
    "trump",
    "pete", 
    "hegseth",
    "lindsey", 
    "graham",
    "benjamin", 
    "netanyahu",
    "mark", 
    "carney",
    "tamim",
    "bin", 
    "hamad",
    "al",
    "thani",
    "emmanuel", 
    "macron"
]


#def preprocess_text(text):
    # lowercase normalization
#    text = text.lower()

    # remove punctuation
#    text = re.sub(r"[^a-z\s]", "", text)

    # tokenize
#    words = text.split()

    # remove stopwords
#    words = [word for word in words if word not in STOPWORDS]

#    return words

def analyze_words(words):
    counter = Counter(words)
    return counter.most_common(20)

def analyze_mult_word_keywords(text, keywords):
    text_lower = text.lower()
    counter = {k: text_lower.count(k) for k in keywords if text_lower.count(k) > 0}
    return sorted(counter.items(), key=lambda x: x[1], reverse=True)[:20]

def save_results(results):
    filename = "analysis_results.txt"

    with open(filename, "w") as f:
        f.write("Top 20 Most Frequent Words / Categories / Leaders\n")
        f.write("=" * 50 + "\n")

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
    words = simple_tokenize(text, stopwords_set)
    
    words_filtered = [w for w in words if w in keywords_tech]
    print("Filtered tech words sample:", words_filtered[:50])

    print("Analyzing word frequency for military tech...")
    top_words_tech = analyze_words(words_filtered)

    print("Analyzing political leaders mentions...")
    top_words_leaders = analyze_mult_word_keywords(text, keywords_leaders)
    
    all_results = top_words_tech + top_words_leaders

    print("\nTop 10 Most Frequent Military Tech")
    print("=" * 30)
    for word, count in top_words_tech:
        print(f"{word}: {count}")

    print("\nTop 10 Most Mentioned Leaders")
    print("=" * 30)
    for word, count in top_words_leaders:
        print(f"{word}: {count}")

    save_results(all_results)


if __name__ == "__main__":
    main()