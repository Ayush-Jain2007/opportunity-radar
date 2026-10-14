# 🎯 Opportunity Radar

**An AI-powered opportunity discovery and matching platform for students.**

Opportunity Radar helps students discover internships, scholarships, hackathons, and research programs that match their interests and educational background.

## Problem Statement

Students often struggle to find relevant opportunities because information is scattered across multiple websites. They may also spend time reviewing opportunities for which they are not eligible.

## Proposed Solution

Opportunity Radar uses TinyFish to search for and retrieve opportunity information from web pages. It extracts available details, compares opportunities with a student's interests, and provides preliminary eligibility checks.

## Key Features

- **Opportunity discovery:** Search for opportunity listings using TinyFish.
- **Information extraction:** Extract available details such as title, eligibility, duration, and source URL.
- **Eligibility checks:** Flag opportunities for preliminary eligibility review.
- **Interest matching:** Calculate keyword-based match scores.
- **Opportunity filtering:** Filter results by selected opportunity type.
- **Dashboard:** Browse results and view summary metrics using Streamlit.
- **Deadline utilities:** Identify certain deadline formats when explicitly stated.

## Technology Stack

- Python
- TinyFish Search and Fetch APIs
- Streamlit
- JSON for storing extracted opportunities
- Basic keyword matching for eligibility and interest scoring

## Project Workflow

1. TinyFish searches for relevant opportunity pages.
2. TinyFish Fetch retrieves page content.
3. Python extracts supported opportunity details.
4. The extracted data is saved in `opportunities.json`.
5. The student enters their year, branch, interests, and opportunity preferences.
6. The system calculates preliminary eligibility results and interest-match scores.
7. Streamlit displays the ranked opportunities and their source links.

## Getting Started

### Prerequisites

- Python 3.11 or newer
- A TinyFish API key

### Installation

Clone this repository and enter the project folder:

```bash
git clone https://github.com/Ayush-Jain2007/opportunity-radar
cd "Azinhack Project"
```

Create and activate a virtual environment if you don't already have one.

On Windows PowerShell:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

Install the required packages:

```powershell
python -m pip install tinyfish python-dotenv streamlit
```

Create a `.env` file in the project root:

```text
TINYFISH_API_KEY=your_api_key_here
```

Replace the placeholder with your own API key. Never commit `.env` or publish your API key.

### Run the opportunity extractor

```powershell
python extract_titles.py
```

### Launch the dashboard

```powershell
python -m streamlit run app.py
```

## TinyFish Integration

TinyFish is a core part of Opportunity Radar's discovery pipeline. Its Search API finds relevant web pages, and its Fetch API retrieves page content for extraction. This enables the project to collect opportunity information from external sources rather than relying entirely on manually entered data.

## Limitations

- Extraction currently supports only certain page formats.
- Some websites may block automated retrieval.
- Eligibility and interest scores are preliminary heuristics, not guarantees.
- Deadline detection supports a limited set of date formats.
- The current system does not guarantee that every listing is open or accepting applications.

Students should verify eligibility, deadlines, and application status on the original source website.

## Future Scope

- TF-IDF and cosine-similarity-based ranking
- Improved eligibility matching
- More opportunity sources and extraction formats
- Deadline and application-status verification
- User profiles and saved opportunities
- More comprehensive filtering and recommendations

## Hackathon

Built for **AZINHACK '26**, Open Innovation track.

## License

## License

This project is licensed under the MIT License. See the `LICENSE` file for details.