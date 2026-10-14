from dotenv import load_dotenv
from tinyfish import TinyFish

load_dotenv()
client = TinyFish()   # reads TINYFISH_API_KEY from the environment

response = client.search.query(query="hackathons for students October 2026 India", location="IN")

for r in response.results:
    print(r.position, r.title)
    print("  ", r.url)