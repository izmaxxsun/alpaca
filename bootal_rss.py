from rss_parser import Parser
from requests import get

rss_url = 'https://slickdeals.net/newsearch.php?mode=frontpage&searcharea=deals&searchin=first&rss=1'

xml = get(rss_url)

parser = Parser(xml=xml.content, limit=5)
feed = parser.parse()

# Iteratively print feed items
count = len(feed.feed)
print(f'RSS Count: {count}')

for item in feed.feed:
    print(f"Title: {item.title}\n")
    print(f"Description: {item.description}\n--------------")

