from crewai import Crew, Process
from src.agents import SupportAgents
from src.tasks import SupportTasks

def run_support_crew(category: str, query: str):
    agents = SupportAgents()
    tasks = SupportTasks()

    agent = agents.support_specialist()
    task = tasks.answer_customer_question(agent, category, query)

    crew = Crew(
        agents=[agent],
        tasks=[task],
        process=Process.sequential,
        verbose=True
    )

    return crew.kickoff()