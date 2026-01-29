from collections import defaultdict
from src.text_utils import tokenize

def question_matches(user_question: str, faq_question: str) -> bool:
    user_tokens = set(tokenize(user_question))
    faq_tokens = set(tokenize(faq_question))

    return len(user_tokens & faq_tokens) >= 1


def resolve_results(rows, original_question: str):
    by_product = defaultdict(list)

    for r in rows:
        product_id, question, answer, product_hint, score = r
        by_product[product_id].append(r)

    if not by_product:
        return {"type": "NO_RESULTS"}

    all_rows = [r for items in by_product.values() for r in items]
    all_rows.sort(key=lambda x: x[4], reverse=True)

    best = all_rows[0]
    second = all_rows[1] if len(all_rows) > 1 else None

    if not question_matches(original_question, best[1]):
        return {"type": "NO_RESULTS"}

    if second is None or best[4] >= second[4] + 1:
        return {
            "type": "ANSWER",
            "product_hint": best[3],
            "answer": best[2]
        }

    sorted_products = sorted(
        by_product.items(),
        key=lambda x: len(x[1]),
        reverse=True
    )

    if len(sorted_products) == 1:
        item = sorted_products[0][1][0]
        return {
            "type": "ANSWER",
            "product_hint": item[3],
            "answer": item[2]
        }

    return {
        "type": "DISAMBIGUATE",
        "options": [
            {
                "product_id": asin,
                "product_hint": items[0][3]
            }
            for asin, items in sorted_products[:3]
        ] + [
            {
                "product_id": None,
                "product_hint": "None of the above"
            }
        ]
    }