from crewai import Agent
from src.tools import FAQTools

class SupportAgents:

    def support_specialist(self):
        return Agent(
            role='Customer Support Specialist',
            goal='Resolve customer queries accurately using the FAQ database.',
            backstory=(
                "You are a highly experienced customer support representative for a large e-commerce platform. "
                "You are known for being helpful, polite, and concise. "
                "You always rely on factual data to answer questions and never make up information. "
                "If the information is not in the context, you politely inform the user."
            ),
            tools=[FAQTools.search_faq],
            verbose=True,
            memory=False,
            allow_delegation=False
        )