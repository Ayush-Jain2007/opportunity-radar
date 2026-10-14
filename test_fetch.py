from dotenv import load_dotenv
from tinyfish import TinyFish

load_dotenv()
client = TinyFish()

search = client.search.query(query="internships for first year engineering students 2026")
top_urls = [r.url for r in search.results[:3]]

pages = client.fetch.get_contents(urls=top_urls, format="markdown")

print("Number of successful pages:", len(pages.results))

for page in pages.results:
    print("\nWebsite:", page.title)
    print("URL:", page.url)
    print("First 500 characters:")
    print(page.text[:500])