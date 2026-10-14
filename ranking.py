import json

def calculate_interest_score(opportunity, interests):
    """
    Score an opportunity using available text fields.
    """

    text_parts = [
        opportunity.get("title", ""),
        opportunity.get("description", ""),
        opportunity.get("eligibility", ""),
        opportunity.get("duration", ""),
        opportunity.get("area", ""),
    ]

    text = " ".join(text_parts).lower()

    if not interests:
        return 0

    matched_interests = set()

    for interest in interests:
        keyword = interest.strip().lower()

        if keyword and keyword in text:
            matched_interests.add(keyword)

    score = len(matched_interests) / len(interests) * 100

    return round(score, 2)

with open("opportunities.json", "r", encoding="utf-8") as file:
    opportunities = json.load(file)

student_interests = ["Python", "AI", "Machine Learning"]

for opportunity in opportunities:
    score = calculate_interest_score(
        opportunity,
        student_interests
    )

    opportunity["interest_score"] = score

ranked_opportunities = sorted(
    opportunities,
    key=lambda item: item["interest_score"],
    reverse=True
)

for opportunity in ranked_opportunities:
    print("Title:", opportunity.get("title", "Unknown"))
    print("Interest score:", opportunity["interest_score"], "%")
    print("-" * 40)
