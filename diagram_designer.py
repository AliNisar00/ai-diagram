import os
import graphviz

# Global state for the diagram
diagram_state = {
    "nodes": [],
    "edges": []
}

def add_node(node_id, label):
    """
    Add a node to the diagram state.
    :param node_id: Unique identifier for the node.
    :param label: Text label for the node.
    """
    # Check if node already exists
    for node in diagram_state["nodes"]:
        if node["id"] == node_id:
            print(f"Node '{node_id}' already exists.")
            return
    diagram_state["nodes"].append({"id": node_id, "label": label})
    print(f"Added node: {node_id} -> '{label}'")

def add_edge(from_node, to_node):
    """
    Add an edge between two nodes.
    :param from_node: The node id for the edge source.
    :param to_node: The node id for the edge target.
    """
    # Verify that both nodes exist
    node_ids = [node["id"] for node in diagram_state["nodes"]]
    if from_node not in node_ids:
        print(f"Source node '{from_node}' does not exist. Please add it first.")
        return
    if to_node not in node_ids:
        print(f"Target node '{to_node}' does not exist. Please add it first.")
        return
    diagram_state["edges"].append({"from": from_node, "to": to_node})
    print(f"Added edge: {from_node} -> {to_node}")

def render_diagram(output_filename="diagram_output", output_format="png"):
    """
    Render the current diagram state to an image file.
    :param output_filename: The base name for the output file.
    :param output_format: The format for rendering (default: 'png').
    """
    dot = graphviz.Digraph(comment="Diagram")
    
    # Add nodes from state to the DOT graph
    for node in diagram_state["nodes"]:
        dot.node(node["id"], label=node["label"])
    
    # Add edges from state
    for edge in diagram_state["edges"]:
        dot.edge(edge["from"], edge["to"])
    
    # Render and save the diagram (cleanup intermediate files)
    output_filepath = dot.render(filename=output_filename, format=output_format, cleanup=True)
    print(f"Diagram rendered and saved as {output_filepath}")
    
    return output_filepath

def print_state():
    """Print the current state of the diagram."""
    print("\nCurrent Diagram State:")
    print("Nodes:")
    for node in diagram_state["nodes"]:
        print(f"  {node['id']}: '{node['label']}'")
    print("Edges:")
    for edge in diagram_state["edges"]:
        print(f"  {edge['from']} -> {edge['to']}")
    print()

def main():
    # A test case to generate two nodes and one edge. The LLM will intercept here shortly (just need to figure out a few things first)
    # These commands simulate text instructions from the user.
    
    # Example: "Add a node called 'Camera'"
    add_node("camera", "Camera")
    
    # Example: "Add a node called 'YOLO Detection Node'"
    add_node("yolo", "YOLO Detection Node")
    
    # Example: "Connect 'Camera' to 'YOLO Detection Node'"
    add_edge("camera", "yolo")
    
    # Print current state for debugging
    print_state()
    
    # Render the diagram
    rendered_file = render_diagram("diagram_output", "png")
    
    # (Future todo) Use Pillow or another tool to convert the PNG to a JPG.
    # Example from GPT:
    # from PIL import Image
    # img = Image.open(rendered_file)
    # img.convert("RGB").save("final_diagram.jpg", "JPEG")
    
if __name__ == "__main__":
    main()
