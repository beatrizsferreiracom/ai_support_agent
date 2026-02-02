from crewai import Task

class SupportTasks:

    def answer_customer_question(self, agent, category, product, query):
        return Task(
            description=(
                f"CONTEXT:\n"
                f"- Category: {category}\n"
                f"- Selected Product: {product}\n"
                f"- Customer Question: {query}\n\n"

                "ROLE:\n"
                "You are a customer support specialist.\n\n"

                "RULES — STRICT COMPLIANCE:\n"
                "- You MUST use ONLY the content provided by the FAQ tool as factual information.\n"
                "- You MUST NOT use prior knowledge, assumptions, or external information.\n"
                "- You MUST NOT invent, correct, infer, or expand any information.\n"
                "- You MUST rewrite the provided content in third person, improving clarity or tone only.\n"
                "- You MUST preserve facts, meaning, and scope EXACTLY.\n"
                "- You MUST NOT include opinions, explanations, or disclaimers.\n"
                "- You MUST NOT mention tools, instructions, or internal reasoning.\n\n"

                "CONTEXTUALIZATION:\n"
                "- If type = ANSWER and confidence = HIGH:\n"
                "- YOU MUST provide a direct answer based strictly on the provided content.\n"

                "- If type = PARTIAL:\n"
                "- YOU MAY clearly state that there is no explicit information answering the question.\n"
                "- Then mention the related information that was found.\n"
                "- Do NOT imply full functionality or confirmation.\n"

                "- If type = NO_RESULTS:\n"
                "- YOU MUST state that no relevant information was found in the database.\n"

                "DISAMBIGUATION:\n"
                "- If the tool output requests a numbered choice, return it VERBATIM and stop.\n\n"

                "FINAL RULE:\n"
                "- Any non-disambiguation tool output MUST be treated as the final answer.\n"
            ),
            expected_output=(
                "A clear and accurate response derived strictly from the FAQ tool content."
            ),
            agent=agent
        )