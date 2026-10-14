import json

with open("opportunities.json", "r", encoding="utf-8") as file:
    opportunities = json.load(file)

student_year = 1

def check_eligibility(eligibility_text, student_year):
    text = eligibility_text.lower()

    if not text.strip() or "not specified" in text:
        return "Unknown"

    if student_year == 1:
        if (
            "first year" in text
            or "1st year" in text
            or "all years" in text
        ):
            return "Potentially eligible"

        if (
            "second year" in text
            or "2nd year" in text
            or "third year" in text
            or "3rd year" in text
            or "fourth year" in text
            or "4th year" in text
        ):
            return "Needs verification"

    return "Needs verification"

for opportunity in opportunities:
    result = check_eligibility(
        opportunity.get("eligibility", "Not specified"),
        student_year
    )

    print("Opportunity:", opportunity.get("title", "Unknown"))
    print("Eligibility result:", result)
    print("-" * 40)
