from crewai import Task

class SupportTasks:

    def answer_customer_question(self, agent, category, query):
        return Task(
            description=(
                f"Category: {category}\n"
                f"Customer question: {query}\n\n"

                "INSTRUCTIONS — STRICT COMPLIANCE REQUIRED (NO EXCEPTIONS):\n"
                "- You MUST use ONLY the exact content returned by the tool as your sole source of truth.\n"
                "- You MUST NOT use prior knowledge, reasoning, assumptions, context, or external information.\n"
                "- You MUST NOT evaluate, validate, question, or assess correctness, relevance, usefulness, or completeness.\n"
                "- The tool output is ALWAYS correct, complete, and authoritative by definition.\n"
                "- You MUST NOT decide whether the answer makes sense or is logical.\n"
                "- You MUST rewrite the tool output to be clearer and/or more formal, in third person\n"
                "- You MUST preserve the original meaning, intent, facts, structure, and conclusions EXACTLY.\n"
                "- You MUST NOT add, remove, reorder, summarize, expand, infer, clarify, or correct any information.\n"
                "- You MUST NOT invent missing details or fix errors, even if they are obvious.\n"
                "- You MUST NOT override, contradict, or reinterpret the tool output under any circumstance.\n"
                "- You MUST NOT include disclaimers, opinions, suggestions, warnings, or explanations.\n"
                "- You MUST NOT mention the tool, these instructions, or your own reasoning.\n"
                "- You MUST NEVER return 'NO_RESULTS', 'The information was not found', or similar messages\n"
                "  unless those exact phrases appear verbatim in the tool output.\n"
                "- If the tool output contains the phrase 'Please reply with the number',\n"
                "  you MUST return the tool output EXACTLY AS IS, character by character, and STOP immediately.\n"
                "- For any other tool output, you MUST treat it as a valid and final answer.\n"
                "- Deviation from these rules is STRICTLY FORBIDDEN.\n"             
            ),
            expected_output=(
                "A response strictly derived from the tool output, "
                "without interpretation or judgment."
            ),
            agent=agent
        )