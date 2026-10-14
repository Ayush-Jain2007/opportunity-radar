
import re
import json
from datetime import date


def clean_text(text):
    """Remove extra whitespace and Markdown formatting."""
    text = re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", text)
    text = re.sub(r"[*_`]", "", text)
    return re.sub(r"\s+", " ", text).strip()


def split_markdown_row(line):
    """Split a Markdown table row into cells."""
    return [
        cell.strip()
        for cell in line.strip().strip("|").split("|")
    ]


def extract_tables(markdown):
    """Extract rows from Markdown tables."""
    lines = markdown.splitlines()
    tables = []
    i = 0

    while i < len(lines) - 1:
        header = lines[i].strip()
        separator = lines[i + 1].strip()

        is_table = (
            "|" in header
            and "|" in separator
            and re.fullmatch(
                r"\|?[\s:|-]+\|?",
                separator
            )
        )

        if not is_table:
            i += 1
            continue

        headers = [
            clean_text(cell).lower()
            for cell in split_markdown_row(header)
        ]

        i += 2
        rows = []

        while i < len(lines) and "|" in lines[i]:
            cells = split_markdown_row(lines[i])

            if len(cells) == len(headers):
                rows.append(dict(zip(headers, cells)))

            i += 1

        tables.append((headers, rows))

    return tables


def find_column(row, *keywords):
    """Find a column whose name contains one of the keywords."""
    for column, value in row.items():
        if any(word in column for word in keywords):
            return clean_text(value)
    return None


def extract_deadline(text):
    """
    Find a recognizable date.
    Return None if no supported date pattern is found.
    """
    patterns = [
        r"\b\d{4}-\d{2}-\d{2}\b",
        r"\b\d{1,2}\s+"
        r"(?:Jan(?:uary)?|Feb(?:ruary)?|Mar(?:ch)?|"
        r"Apr(?:il)?|May|Jun(?:e)?|Jul(?:y)?|"
        r"Aug(?:ust)?|Sep(?:tember)?|Oct(?:ober)?|"
        r"Nov(?:ember)?|Dec(?:ember)?)"
        r"\s+\d{4}\b",
        r"\b(?:Jan(?:uary)?|Feb(?:ruary)?|Mar(?:ch)?|"
        r"Apr(?:il)?|May|Jun(?:e)?|Jul(?:y)?|"
        r"Aug(?:ust)?|Sep(?:tember)?|Oct(?:ober)?|"
        r"Nov(?:ember)?|Dec(?:ember)?)\s+"
        r"\d{1,2},?\s+\d{4}\b",
    ]

    for pattern in patterns:
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            return match.group(0)

    return None


def extract_opportunities(page):
    """Convert a fetched page into structured opportunity records."""
    markdown = page.text or ""
    page_title = page.title or ""
    source_url = page.url

    tables = extract_tables(markdown)
    opportunities = []

    for headers, rows in tables:
        # Only treat a table as an opportunity table if
        # it has a title-like column and useful opportunity fields.
        has_title = any(
            word in header
            for header in headers
            for word in ("title", "opportunity", "program", "programme")
        )

        has_details = any(
            word in header
            for header in headers
            for word in (
                "eligibility", "deadline", "application",
                "institution", "organization", "organisation"
            )
        )

        if not (has_title and has_details):
            continue

        for row in rows:
            title = find_column(
                row, "title", "opportunity", "program", "programme"
            )

            if not title:
                continue

            eligibility = find_column(row, "eligibility", "qualification")
            explicit_deadline = find_column(
                row, "deadline", "last date", "closing date",
                "application deadline"
            )

            # Don't mistake durations such as "6 months"
            # or a program year such as "2026" for a deadline.
            deadline = (
                extract_deadline(explicit_deadline)
                if explicit_deadline
                else None
            )

            institution = find_column(
                row, "institution", "organization", "organisation"
            )
            area = find_column(row, "area", "field", "discipline")
            duration = find_column(row, "duration")

            opportunities.append({
                "title": title,
                "institution": institution,
                "eligibility": eligibility,
                "area": area,
                "duration": duration,
                "deadline": deadline,
                "opportunity_type": "internship",
                "source_url": source_url,
                "registration_url": None,
                "deadline_status": (
                    "unverified" if deadline else "unknown"
                ),
            })

    return {
        "source_title": page_title,
        "source_url": source_url,
        "opportunities": opportunities,
        "page_type": (
            "opportunity_listing" if opportunities
            else "category_or_unrecognized_page"
        ),
    }


if __name__ == "__main__":
    print(
        "Import extract_opportunities(page) into your "
        "TinyFish test script to process fetched pages."
    )