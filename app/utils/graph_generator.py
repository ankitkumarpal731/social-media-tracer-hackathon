from pyvis.network import Network
import os

def generate_graph(input_value, matches, output_html="graph.html"):
    net = Network(height="500px", width="100%", bgcolor="#222222", font_color="white")

    # Add central node
    net.add_node(input_value, label=input_value, shape="box", color="orange")

    # Add matched platform nodes
    for match in matches:
        platform = match['platform']
        confidence = match.get('confidence', 0)
        net.add_node(platform, label=f"{platform}\n{confidence}%", color="lightblue")
        net.add_edge(input_value, platform)

    # Save HTML (no browser, no notebook mode)
    net.write_html(output_html)
    return os.path.abspath(output_html)
