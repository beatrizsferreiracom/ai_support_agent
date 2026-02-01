from src.text_utils import is_compatible

def resolve_results(rows, user_question, is_compatible):
    if not rows:
        return {"type": "NO_RESULTS"}

    best = rows[0]
    second = rows[1] if len(rows) > 1 else None

    intent_match = is_compatible(user_question, best[2])

    if not second or best[-1] >= second[-1] + 0.15:
        return {
            "type": "ANSWER",
            "product_hint": best[1],
            "answer": best[3],
            "intent_match": intent_match,
            "matched_question": best[2]
        }

    return {
        "type": "DISAMBIGUATE",
        "options": [
            {"product_id": r[0], "product_hint": r[1], "question": r[2]}
            for r in rows[:3]
        ] + [{"product_id": None, "product_hint": "None of the above"}]
    }