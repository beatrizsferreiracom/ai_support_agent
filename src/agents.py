from crewai import Agent
from src.handlers import handle_question

class SupportAgents:

    def support_specialist(self):
        return Agent(
            role="Customer Support Specialist",
            goal=("Answer customer questions using the internal FAQ database"
                  "Ensure answers are accurate, faithful to the database, and helpful."),
            backstory=(
                "You are a customer support specialist responsible for answering "
                "questions strictly based on an internal FAQ database extracted from "
                "real customer questions and answers."
            ),
            tools=[handle_question],
            verbose=True
        )