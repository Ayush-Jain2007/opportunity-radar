
import json

from eligibility import check_eligibility
from ranking import calculate_interest_score


# Student profile
student_year = 1
student_interests = ["Python", "AI", "Machine Learning"]


# Load opportunities
with open("opportunities.json", "r", encoding="utf-8") as file:
    opportunities = json.load(file)


# Evaluate each opportunity
for opportunity in opportunities:
    eligibility = opportunity.get(
        "eligibility", "Not specified"
    )

    opportunity["eligibility_result"] = check_eligibility(
        eligibility,
        student_year
    )

    opportunity["interest_score"] = calculate_interest_score(
        opportunity,
        student_interests
    )
    if opportunity["eligibility_result"] == "Likely not eligible":
        opportunity["recommendation"] = "Not recommended"
    elif opportunity["eligibility_result"] == "Unknown":
        opportunity["recommendation"] = "Check eligibility"
    elif opportunity["interest_score"] >= 50:
        opportunity["recommendation"] = "Good interest match"
    else:
        opportunity["recommendation"] = "Low interest match"



# Sort by interest score
ranked_opportunities = sorted(
    opportunities,
    key=lambda item: item["interest_score"],
    reverse=True
)


# Display recommendations
print("\n===== OPPORTUNITY RADAR =====\n")

for opportunity in ranked_opportunities:
    print("Title:", opportunity.get("title", "Unknown"))
    print("Eligibility:", opportunity["eligibility_result"])
    print("Recommendation:", opportunity["recommendation"])
    print("Source:", opportunity.get("source_url", "Not available"))
    print("-" * 45)
