
from dotenv import load_dotenv
from tinyfish import TinyFish
from deadline_utils import extract_deadline, find_deadline_text
import json

load_dotenv()
client = TinyFish()

search = client.search.query(
    query="internships for first year engineering students 2026",
    location="IN"
)

top_urls = [r.url for r in search.results[:3]]

pages = client.fetch.get_contents(
    urls=top_urls,
    format="markdown"
)

all_opportunities = []

for page in pages.results:
    print("\nWebsite:", page.title)

    lines = page.text.splitlines()
    headers = None

    for line in lines:
        if "|" not in line:
            headers = None
            continue

        columns = [
            cell.strip()
            for cell in line.strip().strip("|").split("|")
        ]

        # Identify a table header
        if any(
            "title" in cell.lower()
            for cell in columns
        ):
            headers = [cell.lower() for cell in columns]
            continue

        # Skip Markdown's separator row
        if all(
            cell and set(cell) <= {"-", ":"}
            for cell in columns
        ):
            continue

        # Ignore rows if we haven't found a header
        if headers is None or len(columns) != len(headers):
            continue

        row = dict(zip(headers, columns))

        # Find the title column
        title = next(
            (
                value for key, value in row.items()
                if "title" in key
            ),
            ""
        )

        if not title:
            continue

        # Find eligibility and duration columns
        eligibility = next(
            (
                value for key, value in row.items()
                if "eligibility" in key
            ),
            "Not specified"
        )

        duration = next(
            (
                value for key, value in row.items()
                if "duration" in key
            ),
            "Not specified"
        )

        # Look for a line that explicitly mentions a deadline
        deadline_line = find_deadline_text(page.text)

        # Extract a date only if we found a deadline-related line
        deadline = (
            extract_deadline(deadline_line)
            if deadline_line
            else None
        )

        opportunity = {
            "title": title,
            "eligibility": eligibility or "Not specified",
            "duration": duration or "Not specified",
            "deadline": deadline,
            "deadline_status": (
                "unverified" if deadline else "unknown"
            ),
            "source_url": page.url
        }

        all_opportunities.append(opportunity)
        print(json.dumps(opportunity, indent=2))

with open("opportunities.json", "w", encoding="utf-8") as file:
    json.dump(
        all_opportunities,
        file,
        indent=2,
        ensure_ascii=False
    )

print(
    f"\nTotal opportunities extracted: "
    f"{len(all_opportunities)}"
)
print("Saved results to opportunities.json")
