from collections import defaultdict

def resolve_results(rows):
    by_product = defaultdict(list)

    for r in rows:
        product_id, question, answer, product_hint, score = r
        by_product[product_id].append((product_id, question, answer, product_hint, score))

    if not by_product:
        return {"type": "NO_RESULTS"}

    all_rows = []
    for items in by_product.values():
        all_rows.extend(items)

    all_rows_sorted = sorted(all_rows, key=lambda x: x[4], reverse=True)

    best = all_rows_sorted[0]
    second = all_rows_sorted[1] if len(all_rows_sorted) > 1 else None

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

    if (
        len(sorted_products) == 1 or
        len(sorted_products[0][1]) >= 2 * len(sorted_products[1][1])
    ):
        _, items = sorted_products[0]
        return {
            "type": "ANSWER",
            "product_hint": items[0][3],
            "answer": items[0][2]
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