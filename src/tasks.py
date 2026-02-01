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
                "- If intent_match is false, you MAY add ONE short sentence explaining that the information\n"
                "  refers to a specific aspect of the product.\n"
                "- You MUST NOT claim that this fully answers the customer question.\n"
                "- You MUST NOT imply additional functionality.\n\n"

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