import feedparser
from newspaper import Article
import time
import pickle
from datetime import datetime

keywords = ["war", "Iran", "IRGC", "US", "Israel"]

feeds = [
    "https://www.csis.org/,
    "https://feeds.bbci.co.uk/news/world/rss.xml"
]

def contains_keywords(text, keywords):
    if text is None:
        return False

    text_lower = text.lower()
    for keyword in keywords:
        if keyword.lower() in text_lower:
            return True
    return False

def get_article_text(url, timeout=10):
    try:
        article = Article(url)
        article.download()
        article.parse()
        return {
            "title": article.title,
            "text": article.text,
            "authors": article.authors
        }
    except Exception as e:
        print(f" [ERROR] Could not extract article: {str(e)}")
        return None

def scrape_news():
    all_articles = []

    for feed_url in feeds:
        print(f"\n Parsing feed: {feed_url}")
        print(f"-" * 60)

        try:
            feed = feedparser.parse(feed_url)

            for entry in feed.entries[:50]:
                title = entry.get("title","No title")
                link = entry.get("link","No link")
                summary = entry.get("summary","")

                if contains_keywords(title, keywords) or contains_keywords(summary, keywords):
                    print(f"\n Found matching article: {title}")
                    print(f"    URL: {link}")

                    print(f"    Extracting full text ...")
                    article_data = get_article_text(link)

                    if article_data:
                        all_articles.append({
                            "title": title,
                            "url": link,
                            "full_text": article_data["text"],
                            "authors": article_data["authors"]
                        })
                        text_preview = article_data["text"][:200]+"..."
                        print(f"    Preview: {text_preview}")
                        print("     "+"-"*55)
                    time.sleep(2)
        except Exception as e:
            print(f"[ERROR] parsing feed {feed_url}:{str(e)}")
            time.sleep(1)
    return all_articles

if __name__ == "__main__":
    print("=" * 60)
    print("NEWS SCRAPER - Finding articles about:", ', '.join(keywords))
    print("=" * 60)

    # Run the scraper
    articles = scrape_news()

    # Display results
    print("\n" + "=" * 60)
    print(f"📊 RESULTS: Found {len(articles)} matching articles")
    print("=" * 60)

    for i, article in enumerate(articles, 1):
        print(f"\n{i}. {article['title']}")
        print(f"   URL: {article['url']}")
        if article['authors']:
            print(f"   By: {', '.join(article['authors'])}")
        print(f"   Text preview: {article['full_text'][:150]}...")
        print("-" * 60)

    # Save to pickle file
    timestamp = datetime.now().strftime("%Y%m%d_%H")
    pickle_filename = f"news_{timestamp}.pkl"
    try:
        with open(pickle_filename, 'wb') as f:
            pickle.dump(articles, f)
        print(f"\n✅ Successfully saved {len(articles)} articles to {pickle_filename}")
    except Exception as e:
        print(f"\n❌ Failed to save pickle file: {str(e)}")

    print("✨ Scraping complete!")
