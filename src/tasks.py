from crewai import Task

class SupportTasks:

    def answer_customer_question(self, agent, category, query):
        return Task(
            description=(
                f"Category: {category}\n"
                f"Customer question: {query}\n\n"
                "Steps:\n"
                "- Search the FAQ database.\n"
                "- Identify the product implicitly from the results.\n"
                "- Answer ONLY using the retrieved data.\n"
                "- If no results are found, say so clearly."
            ),
            expected_output="A clear and helpful answer based strictly on the FAQ.",
            agent=agent
        )