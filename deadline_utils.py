
import re
from datetime import datetime


def extract_deadline(text):
    """
    Extract a recognizable date from text.
    Return None if no supported date is found.
    """

    patterns = [
        r"\b\d{4}-\d{2}-\d{2}\b",

        r"\b\d{1,2}\s+"
        r"(?:Jan(?:uary)?|Feb(?:ruary)?|Mar(?:ch)?|"
        r"Apr(?:il)?|May|Jun(?:e)?|Jul(?:y)?|"
        r"Aug(?:ust)?|Sep(?:tember)?|Oct(?:ober)?|"
        r"Nov(?:ember)?|Dec(?:ember)?)\s+\d{4}\b",

        r"\b(?:Jan(?:uary)?|Feb(?:ruary)?|Mar(?:ch)?|"
        r"Apr(?:il)?|May|Jun(?:e)?|Jul(?:y)?|"
        r"Aug(?:ust)?|Sep(?:tember)?|Oct(?:ober)?|"
        r"Nov(?:ember)?|Dec(?:ember)?)\s+"
        r"\d{1,2},?\s+\d{4}\b",
    ]

    formats = [
        ("%Y-%m-%d",),
        ("%d %B %Y", "%d %b %Y"),
        ("%B %d, %Y", "%B %d %Y", "%b %d, %Y", "%b %d %Y"),
    ]

    for pattern, possible_formats in zip(patterns, formats):
        match = re.search(pattern, text, re.IGNORECASE)

        if match:
            date_text = match.group(0)

            for date_format in possible_formats:
                try:
                    parsed_date = datetime.strptime(
                        date_text, date_format
                    )
                    return parsed_date.date().isoformat()
                except ValueError:
                    continue

    return None


def find_deadline_text(text):
    """Find text explicitly associated with a deadline."""

    pattern = (
        r"(?:application\s+)?deadline|"
        r"last\s+date\s+to\s+apply|"
        r"apply\s+by|"
        r"applications?\s+close(?:s)?|"
        r"closing\s+date"
    )

    for line in text.splitlines():
        if re.search(pattern, line, re.IGNORECASE):
            return line.strip()

    return None


if __name__ == "__main__":
    examples = [
        "Apply by 2026-10-30",
        "Last date: 30 October 2026",
        "Deadline: October 30, 2026",
        "Duration: 6 Months",
        "Application deadline: 30 October 2026",
        "Duration: 6 months",
        "Apply by 2026-10-30"
    ]

    for example in examples:
        print(example, "->", extract_deadline(example))
