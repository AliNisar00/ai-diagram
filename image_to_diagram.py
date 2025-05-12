from diagram_builder import DiagramBuilder
from query_llava import query_llava
import re
import sys

def extract_nodes_and_edges(response_text):
    # Basic pattern-based extraction (can be replaced later with NLP (potential todo))
    node_pattern = re.findall(r"nodes?: (.+?)(?:\.|\n|$)", response_text, re.IGNORECASE)
    edge_pattern = re.findall(r"connections? are: (.+?)(?:\.|\n|$)", response_text, re.IGNORECASE)

    nodes = []
    edges = []

    if node_pattern:
        nodes = [n.strip() for n in re.split(r",| and ", node_pattern[0]) if n.strip()]

    if edge_pattern:
        raw_edges = re.split(r",|;| and ", edge_pattern[0])
        for edge in raw_edges:
            parts = re.split(r"->|→| to ", edge)
            if len(parts) == 2:
                edges.append((parts[0].strip(), parts[1].strip()))

    return nodes, edges

prompt = """
This image contains a system diagram. List the nodes and connections.

The response should be in plain text, like:

Nodes: node_a, node_b, node_c
Connections are: node_a -> node_b, node_b -> node_c

Use lowercase snake_case for node names. Do not include anything else except the node and connection lists.
"""

def image_to_diagram(image_path, prompt):
    #response = query_llava(prompt, image_path)

    response = """
Nodes: ray_sensor_truck, ray_sensor_trailer1_left, ray_sensor_trailer1_right, ray_sensor_trailer2_left, ray_sensor_trailer2_right, laser_scan_truck, laser_scan_trailer1_left, laser_scan_trailer1_right, laser_scan_trailer2_left, laser_scan_trailer2_right, tf_tree, costmap_muxer, costmap_server, amcl, nav2_behavior_tree, robot_base
Connections: ray_sensor_truck -> laser_scan_truck, ray_sensor_trailer1_left -> laser_scan_trailer1_left, ray_sensor_trailer1_right -> laser_scan_trailer1_right, ray_sensor_trailer2_left -> laser_scan_trailer2_left, ray_sensor_trailer2_right -> laser_scan_trailer2_right, laser_scan_truck -> costmap_muxer, laser_scan_trailer1_left -> costmap_muxer, laser_scan_trailer1_right -> costmap_muxer, laser_scan_trailer2_left -> costmap_muxer, laser_scan_trailer2_right -> costmap_muxer, tf_tree -> costmap_muxer, costmap_muxer -> costmap_server, costmap_server -> amcl, costmap_server -> nav2_behavior_tree, amcl -> nav2_behavior_tree, nav2_behavior_tree -> robot_base
    """

    print("📤 LLaVA Response:\n", response)

    nodes, edges = extract_nodes_and_edges(response)

    builder = DiagramBuilder()

    for node in nodes:
        builder.add_node(node)

    for from_node, to_node in edges:
        builder.add_edge(from_node, to_node)

    builder.print_state()
    builder.render("diagram_from_image.png")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python image_to_diagram.py <image_path>")
    else:
        image_path = sys.argv[1]
        image_to_diagram(image_path, prompt)
