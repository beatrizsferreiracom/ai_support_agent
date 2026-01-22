from crewai import Agent
from src.tools import FAQTools

class SupportAgents:

    def support_specialist(self):
        return Agent(
            role="Customer Support Specialist",
            goal="Answer questions using ONLY the FAQ search results.",
            backstory=(
                "You never guess. "
                "If the database does not return results, "
                "you clearly say the information was not found."
            ),
            tools=[FAQTools.search_faq],
            verbose=True,
            memory=False,
            allow_delegation=False
        )