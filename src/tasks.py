from crewai import Task

class SupportTasks:

    def answer_customer_question(self, agent, category, query):
        return Task(
            description=(
                f"Category: {category}\n"
                f"Customer question: {query}\n\n"
                "Instructions:\n"
                "You MUST rely ONLY on the tool output.\n"
                "- You MAY rewrite the answer to be more formal or clearer.\n"
                "- You MUST preserve the original meaning.\n"
                "- Do NOT add or remove information.\n"
                "- If the tool asks for clarification, return it verbatim.\n"
                "- If multiple options are presented, return them verbatim and STOP.\n"
                "- NEVER say information was not found unless the tool explicitly says so.\n"
            ),
            expected_output=(
                "A response strictly derived from the tool output."
            ),
            agent=agent
        )