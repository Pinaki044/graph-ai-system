from pyvis.network import Network
from graph_builder import G

def generate_graph_html():
    net = Network(height="600px", width="100%", directed=True)

    # Add nodes
    for node, data in G.nodes(data=True):
        label = node
        node_type = data.get("type", "Unknown")

        color_map = {
            "Customer": "blue",
            "SalesOrder": "green",
            "OrderItem": "orange",
            "Product": "purple",
            "Delivery": "red",
            "Billing": "brown",
            "Payment": "black"
        }

        net.add_node(node, label=label, color=color_map.get(node_type, "gray"))

    # Add edges
    for source, target, data in G.edges(data=True):
        relation = data.get("relation", "")
        net.add_edge(source, target, label=relation)

    net.save_graph("graph.html")

    return "graph.html"