from crewai import Crew, Process
from src.agents import SupportAgents
from src.tasks import SupportTasks

def run_support_crew(category: str, product: str, query: str):
    """
    Orchestrates the support agent to answer a customer question
    considering category and selected product.
    """

    agents = SupportAgents()
    tasks = SupportTasks()

    agent = agents.support_specialist()

    task = tasks.answer_customer_question(
        agent=agent,
        category=category,
        product=product,
        query=query
    )

    crew = Crew(
        agents=[agent],
        tasks=[task],
        process=Process.sequential,
        verbose=True
    )

    return crew.kickoff()