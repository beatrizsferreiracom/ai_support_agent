from collections import defaultdict

def resolve_results(rows):
    if not rows:
        return {"type": "NO_RESULTS"}

    best = rows[0]
    second = rows[1] if len(rows) > 1 else None

    if not second or best[-1] >= second[-1] + 0.15:
        return {
            "type": "ANSWER",
            "product_hint": best[1],
            "answer": best[3]
        }

    return {
        "type": "DISAMBIGUATE",
        "options": [
            {"product_id": r[0], "product_hint": r[1], "question": r[2]}
            for r in rows[:3]
        ] + [{"product_id": None, "product_hint": "None of the above"}]
    }