from crewai import Crew, Process
from src.agents import SupportAgents
from src.tasks import SupportTasks

def run_support_crew(category: str, query: str):
    agents = SupportAgents()
    tasks = SupportTasks()

    support_agent = agents.support_specialist()
    answer_task = tasks.answer_customer_question(
        agent=support_agent,
        category=category,
        query=query
    )

    crew = Crew(
        agents=[support_agent],
        tasks=[answer_task],
        process=Process.sequential,
        verbose=True
    )

    result = crew.kickoff()
    return result