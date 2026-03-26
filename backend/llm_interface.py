from query_engine import *

def handle_query(user_input):
    query = user_input.lower()

    # 🔒 Guardrail
    allowed_keywords = ["order", "product", "delivery", "billing", "payment"]

    if not any(word in query for word in allowed_keywords):
        return "This system is designed to answer questions related to the provided dataset only."

    # -------------------------------
    # 🧠 INTENT-BASED QUERY HANDLING
    # -------------------------------

    # ✅ 1. Top / Highest Products
    if any(word in query for word in ["top", "highest", "most", "best"]):
        if "product" in query:
            return format_products(top_billed_products())

    # ✅ 2. Orders WITHOUT delivery
    if any(phrase in query for phrase in ["no delivery", "without delivery", "not delivered"]):
        # ⚠️ Avoid clash with "billed but not delivered"
        if "billed" not in query:
            return format_orders(orders_without_delivery())

    # ✅ 3. Delivered but NOT billed
    if "delivered" in query and "not billed" in query:
        return format_orders(delivered_not_billed())

    # ✅ 4. Billed but NOT delivered
    if "billed" in query and "not delivered" in query:
        return format_orders(billed_not_delivered())

    # ✅ 5. Trace Order Flow
    if "trace" in query or "flow" in query:
        words = query.split()
        for w in words:
            if w.isdigit():
                return trace_order(w)   # already formatted nicely
        return "Please provide a valid order ID."

    # ❌ fallback
    return "Query not understood. Try rephrasing."


# -------------------------------
# 🎨 FORMATTERS (UI FRIENDLY)
# -------------------------------

def format_orders(orders):
    if not orders:
        return "No matching orders found."

    text = "Orders:\n\n"
    for o in orders:
        text += f"- {o}\n"
    return text


def format_products(products):
    if not products:
        return "No product data found."

    text = "Top 5 Billed Products:\n\n"
    for p, count in products:
        text += f"- Product {p.replace('PROD_', '')} → {count} bills\n"
    return text


def format_trace(trace_text):
    return trace_text  # already formatted nicely from query_engine