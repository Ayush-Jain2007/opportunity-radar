import streamlit as st
import subprocess
import sys

st.set_page_config(
    page_title="Opportunity Radar",
    page_icon="🎯",
    layout="wide"
)

st.title("🎯 Opportunity Radar")
st.subheader("Find opportunities that match your goals")

if st.button("🔄 Refresh opportunities from TinyFish"):
    try:
        with st.spinner("Searching for fresh opportunities..."):
            subprocess.run(
                [sys.executable, "extract_titles.py"],
                check=True
            )

        st.success("Opportunity data refreshed successfully!")
        st.rerun()

    except subprocess.CalledProcessError:
        st.error(
            "Refresh failed. Check the VS Code terminal "
            "for the error message."
        )

st.write(
    "Discover internships, scholarships, and hackathons "
    "matched to your interests and eligibility."
)

st.divider()

st.header("Tell us about yourself")

name = st.text_input("Your name")

year = st.selectbox(
    "Year of study",
    ["First Year", "Second Year", "Third Year", "Fourth Year"]
)

branch = st.selectbox(
    "Your branch",
    [
        "AI & Data Science",
        "Computer Science",
        "Information Technology",
        "Electronics",
        "Other"
    ]
)

interests = st.multiselect(
    "Choose your interests",
    [
        "Python",
        "Artificial Intelligence",
        "Machine Learning",
        "Web Development",
        "Data Science",
        "Cybersecurity",
        "Research"
    ]
)

opportunity_type = st.multiselect(
    "What opportunities are you looking for?",
    [
        "Internships",
        "Scholarships",
        "Hackathons",
        "Research Programs"
    ]
)


if st.button("Find Opportunities"):
    if not interests:
        st.warning("Please select at least one interest.")
    elif not opportunity_type:
        st.warning("Please select an opportunity type.")
    else:
        import json
        from eligibility import check_eligibility
        from ranking import calculate_interest_score

        with open("opportunities.json", "r", encoding="utf-8") as file:
            opportunities = json.load(file)

        # Convert the selected year into a number
        year_number = {
            "First Year": 1,
            "Second Year": 2,
            "Third Year": 3,
            "Fourth Year": 4
        }[year]

        # Convert interest labels to keywords
        interest_keywords = [
            "AI" if item == "Artificial Intelligence" else item
            for item in interests
        ]

        for opportunity in opportunities:
            opportunity["eligibility_result"] = check_eligibility(
                opportunity.get("eligibility", "Not specified"),
                year_number
            )

            opportunity["interest_score"] = calculate_interest_score(
                opportunity,
                interest_keywords
            )

        ranked_opportunities = sorted(
            opportunities,
            key=lambda item: item["interest_score"],
            reverse=True
        )
        
        selected_types = {
            "Internships": ["internship", "intern"],
            "Scholarships": ["scholarship", "scholar"],
            "Hackathons": ["hackathon"],
            "Research Programs": ["research", "research program"]
        }

        selected_keywords = []

        for selected_type in opportunity_type:
            selected_keywords.extend(selected_types[selected_type])

        ranked_opportunities = [
            opportunity
            for opportunity in ranked_opportunities
            if any(
                keyword in (
                    opportunity.get("title", "") + " " +
                    opportunity.get("eligibility", "")
                ).lower()
                for keyword in selected_keywords
            )
        ]

        st.subheader("Your opportunity matches")
        col1, col2, col3 = st.columns(3)

        col1.metric(
            "Opportunities found",
            len(ranked_opportunities)
        )

        col2.metric(
            "Need eligibility check",
            sum(
                1 for opportunity in ranked_opportunities
                if opportunity.get("eligibility_result") in [
                    "Unknown",
                    "Needs verification"
                ]
            )
        )

        col3.metric(
            "Good interest matches",
            sum(
                1 for opportunity in ranked_opportunities
                if opportunity.get("interest_score", 0) >= 50
            )
        )

        st.divider()

        for opportunity in ranked_opportunities:
            with st.container(border=True):
                st.markdown(f"### {opportunity.get('title', 'Unknown')}")
                st.write(
                    "Interest match:",
                    f"{opportunity['interest_score']}%"
                )
                st.write(
                    "Eligibility:",
                    opportunity["eligibility_result"]
                )
                st.write(
                    "Duration:",
                    opportunity.get("duration", "Not specified")
                )

                source_url = opportunity.get("source_url")
                if source_url:
                    st.markdown(f"[View source]({source_url})")