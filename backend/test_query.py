from query_engine import *
from graph_builder import G

print("Running test...")

print("Top Products:", top_billed_products())
print("Orders without delivery:", orders_without_delivery())
print("Trace Order:", trace_order("740506"))
print("Delivered but not billed:", delivered_not_billed()[:10])
print("Billed but not delivered:", billed_not_delivered()[:10])

print("\n--- CHECKING GRAPH RELATIONSHIPS ---")

# Check SO → Delivery
for u, v, data in G.edges(data=True):
    if data.get("relation") == "fulfilled_by":
        print("SO → DEL exists:", u, "→", v)
        break

# Check SO → Billing
for u, v, data in G.edges(data=True):
    if data.get("relation") == "billed_by":
        print("SO → BILL exists:", u, "→", v)
        break

# Check BILL → Payment
for u, v, data in G.edges(data=True):
    if data.get("relation") == "paid_by":
        print("BILL → PAY exists:", u, "→", v)
        break