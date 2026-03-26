import networkx as nx
from graph_builder import G, build_graph

build_graph()

# 🔍 Query 1: Top billed products
def top_billed_products():
    product_count = {}

    for node in G.nodes:
        if str(node).startswith("BILL_"):
            for neighbor in G.successors(node):
                if str(neighbor).startswith("PROD_"):
                    product_count[neighbor] = product_count.get(neighbor, 0) + 1

    sorted_products = sorted(product_count.items(), key=lambda x: x[1], reverse=True)

    return sorted_products[:5]


# 🔍 Query 2: Orders without delivery
def orders_without_delivery():
    result = []

    for node in G.nodes:
        if str(node).startswith("SO_"):
            has_delivery = False

            for neighbor in G.successors(node):
                if str(neighbor).startswith("DEL_"):
                    has_delivery = True
                    break

            if not has_delivery:
                result.append(node)

    return result[:10]


# 🔍 Query 3: Trace full flow
def trace_order(order_id):
    order_node = f"SO_{order_id}"

    if order_node not in G:
        return "Order not found."

    trace = []

    trace.append(f"Sales Order: {order_node}")

    # Step 1: Delivery
    deliveries = []
    for neighbor in G.successors(order_node):
        if neighbor.startswith("DEL_"):
            deliveries.append(neighbor)

    if deliveries:
        for d in deliveries:
            trace.append(f"→ Delivery: {d}")
    else:
        trace.append("→ Delivery: NOT FOUND")

    # Step 2: Billing
    billings = []
    for neighbor in G.successors(order_node):
        if neighbor.startswith("BILL_"):
            billings.append(neighbor)

    if billings:
        for b in billings:
            trace.append(f"→ Billing: {b}")
    else:
        trace.append("→ Billing: NOT FOUND")

    # Step 3: Payments
    payments = []
    for b in billings:
        for neighbor in G.successors(b):
            if neighbor.startswith("PAY_"):
                payments.append(neighbor)

    if payments:
        for p in payments:
            trace.append(f"→ Payment: {p}")
    else:
        trace.append("→ Payment: NOT FOUND")

    return "\n".join(trace)

def delivered_not_billed():
    result = []

    for node in G.nodes():
        if node.startswith("SO_"):
            
            has_delivery = False
            has_billing = False

            for neighbor in G.successors(node):
                if neighbor.startswith("DEL_"):
                    has_delivery = True
                if neighbor.startswith("BILL_"):
                    has_billing = True

            if has_delivery and not has_billing:
                result.append(node)

    return result

def billed_not_delivered():
    result = []

    for node in G.nodes():
        if node.startswith("SO_"):
            
            has_delivery = False
            has_billing = False

            for neighbor in G.successors(node):
                if neighbor.startswith("DEL_"):
                    has_delivery = True
                if neighbor.startswith("BILL_"):
                    has_billing = True

            if has_billing and not has_delivery:
                result.append(node)

    return result