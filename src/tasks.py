from crewai import Task

class SupportTasks:

    def answer_customer_question(self, agent, category, query):
        return Task(
            description=(
                f"A customer has submitted a question.\n"
                f"**Category:** {category}\n"
                f"**Question** {query}\n\n"
                "Steps to follow:\n"
                "1. Use the 'Search FAQ Database' tool to find relevant Q&A pairs for this category and query.\n"
                "2. Analyze the search results to match the specifc product or issue mentioned.\n"
                "3. Formulate a friendly, helpful, and direct answer based ONLY on the search results."
            ),
            expected_output=(
                "A natural language response answering the customer's question."
                "The tone shold be professional and helpful. "
                "Do not mention technical details like 'search score' or 'database'."
            ),
            agent=agent
        )