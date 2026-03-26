import networkx as nx
import pandas as pd
import os

G = nx.DiGraph()
DATA_PATH = "data"

# 🔥 Normalize IDs
def clean_id(value):
    if pd.isna(value):
        return None
    return str(value).strip().lstrip("0")

def load_json(folder):
    path = os.path.join(DATA_PATH, folder)
    files = [f for f in os.listdir(path) if f.endswith(".jsonl")]
    
    df_list = []
    for file in files[:5]:
        df = pd.read_json(os.path.join(path, file), lines=True)
        df_list.append(df)
    
    return pd.concat(df_list, ignore_index=True)

def build_graph():
    
    # Load datasets
    customers = load_json("business_partners")
    orders = load_json("sales_order_headers")
    order_items = load_json("sales_order_items")
    products = load_json("products")
    
    deliveries = load_json("outbound_delivery_headers")
    delivery_items = load_json("outbound_delivery_items")
    
    billing = load_json("billing_document_headers")
    billing_items = load_json("billing_document_items")
    
    payments = load_json("payments_accounts_receivable")

    # DEBUG
    print("\n--- DELIVERY ITEMS SAMPLE ---")
    print(delivery_items[['referenceSdDocument', 'referenceSdDocumentItem']].head(5))

    print("\n--- ORDER ITEMS SAMPLE ---")
    print(order_items[['salesOrder', 'salesOrderItem']].head(5))

    # -------------------------------
    # 🧑 Customers
    # -------------------------------
    for _, row in customers.iterrows():
        cust_id = f"CUST_{clean_id(row['businessPartner'])}"
        G.add_node(cust_id, type="Customer")

    # -------------------------------
    # 📦 Products
    # -------------------------------
    for _, row in products.iterrows():
        prod_id = f"PROD_{clean_id(row['product'])}"
        G.add_node(prod_id, type="Product")

    # -------------------------------
    # 📄 Sales Orders
    # -------------------------------
    for _, row in orders.iterrows():
        order_id = f"SO_{clean_id(row['salesOrder'])}"
        cust_id = f"CUST_{clean_id(row['soldToParty'])}"
        
        G.add_node(order_id, type="SalesOrder")
        G.add_edge(cust_id, order_id, relation="places")

    # -------------------------------
    # 📑 Order Items
    # -------------------------------
    for _, row in order_items.iterrows():
        order_id = f"SO_{clean_id(row['salesOrder'])}"
        item_id = f"SOI_{clean_id(row['salesOrder'])}_{clean_id(row['salesOrderItem'])}"
        prod_id = f"PROD_{clean_id(row['material'])}"
        
        G.add_node(item_id, type="OrderItem")
        G.add_edge(order_id, item_id, relation="contains")
        G.add_edge(item_id, prod_id, relation="refers_to")

    # -------------------------------
    # 🚚 Deliveries
    # -------------------------------
    for _, row in deliveries.iterrows():
        del_id = f"DEL_{clean_id(row['deliveryDocument'])}"
        G.add_node(del_id, type="Delivery")

    for _, row in delivery_items.iterrows():
        del_id = f"DEL_{clean_id(row['deliveryDocument'])}"
        order_id = f"SO_{clean_id(row['referenceSdDocument'])}"
        
        # 🔥 FIXED: removed condition
        G.add_edge(order_id, del_id, relation="fulfilled_by")

    # -------------------------------
    # 💰 Billing (FIXED)
    # -------------------------------
    for _, row in billing.iterrows():
        bill_id = f"BILL_{clean_id(row['billingDocument'])}"
        G.add_node(bill_id, type="Billing")

    for _, row in billing_items.iterrows():
        order_id = f"SO_{clean_id(row['referenceSdDocument'])}"
        bill_id = f"BILL_{clean_id(row['billingDocument'])}"

        G.add_node(bill_id, type="Billing")
        G.add_edge(order_id, bill_id, relation="billed_by")

    # -------------------------------
    # 💳 Payments (FIXED)
    # -------------------------------
    for _, row in payments.iterrows():
        pay_id = f"PAY_{clean_id(row['accountingDocument'])}"
        G.add_node(pay_id, type="Payment")

        ref = clean_id(row['invoiceReference'])

        if ref:
            bill_id = f"BILL_{ref}"
            G.add_edge(bill_id, pay_id, relation="paid_by")

    # ===============================
    # 🔥 ADVANCED RELATIONSHIPS
    # ===============================

    delivery_product_edges = 0
    billing_product_edges = 0
    delivery_billing_edges = 0

    # ✅ Delivery → Product
    for _, d_row in delivery_items.iterrows():
        del_id = f"DEL_{clean_id(d_row['deliveryDocument'])}"
    
        ref_order = clean_id(d_row['referenceSdDocument'])
        ref_item = clean_id(d_row['referenceSdDocumentItem'])
    
        if ref_order and ref_item:
            soi_id = f"SOI_{ref_order}_{ref_item}"
        
            if G.has_node(soi_id):
                for prod in G.successors(soi_id):
                    G.add_edge(del_id, prod, relation="contains_product")
                    delivery_product_edges += 1

    # ✅ Billing → Product
    for _, row in billing_items.iterrows():
        bill_id = f"BILL_{clean_id(row['billingDocument'])}"
        
        if 'material' in row:
            prod_id = f"PROD_{clean_id(row['material'])}"
            
            if G.has_node(prod_id):
                G.add_edge(bill_id, prod_id, relation="billed_product")
                billing_product_edges += 1

    # ✅ Delivery → Billing
    for _, row in billing_items.iterrows():
        order_id = f"SO_{clean_id(row['referenceSdDocument'])}"
        bill_id = f"BILL_{clean_id(row['billingDocument'])}"

        for neighbor in G.successors(order_id):
            if neighbor.startswith("DEL_"):
                G.add_edge(neighbor, bill_id, relation="leads_to")
                delivery_billing_edges += 1

    # -------------------------------
    # 📊 SUMMARY
    # -------------------------------
    print("\nGraph Built Successfully!")
    print("Total Nodes:", G.number_of_nodes())
    print("Total Edges:", G.number_of_edges())

    print("\nDEBUG INFO:")
    print("Delivery → Product edges:", delivery_product_edges)
    print("Billing → Product edges:", billing_product_edges)
    print("Delivery → Billing edges:", delivery_billing_edges)


if __name__ == "__main__":
    build_graph()