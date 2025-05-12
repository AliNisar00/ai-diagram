import os
import graphviz

class DiagramBuilder:
    def __init__(self):
        self.nodes = []  # list of dicts: {id, label}
        self.edges = []  # list of dicts: {from, to}

    def _label_to_id(self, label):
        return label.strip().lower().replace(" ", "_")

    def _get_node_by_label(self, label):
        for node in self.nodes:
            if node["label"].lower() == label.lower():
                return node
        return None

    def add_node(self, label):
        node_id = self._label_to_id(label)
        if any(node["id"] == node_id for node in self.nodes):
            print(f"⚠️ Node '{label}' already exists.")
            return
        self.nodes.append({"id": node_id, "label": label})
        print(f"✔ Added node: '{label}'")

    def add_edge(self, from_label, to_label):
        src_node = self._get_node_by_label(from_label)
        tgt_node = self._get_node_by_label(to_label)
        if not src_node:
            print(f"⚠️ Source node '{from_label}' not found.")
            return
        if not tgt_node:
            print(f"⚠️ Target node '{to_label}' not found.")
            return
        self.edges.append({"from": src_node["id"], "to": tgt_node["id"]})
        print(f"✔ Connected '{from_label}' → '{to_label}'")

    def rename_node(self, old_label, new_label):
        node = self._get_node_by_label(old_label)
        if not node:
            print(f"⚠️ Node '{old_label}' not found.")
            return
        node["label"] = new_label
        print(f"✔ Renamed node '{old_label}' → '{new_label}'")

    def remove_node(self, label):
        node = self._get_node_by_label(label)
        if not node:
            print(f"⚠️ Node '{label}' not found.")
            return
        self.nodes = [n for n in self.nodes if n["id"] != node["id"]]
        self.edges = [e for e in self.edges if e["from"] != node["id"] and e["to"] != node["id"]]
        print(f"✔ Removed node '{label}'")

    def remove_edge(self, from_label, to_label):
        src_node = self._get_node_by_label(from_label)
        tgt_node = self._get_node_by_label(to_label)
        if not src_node or not tgt_node:
            print(f"⚠️ One or both nodes not found.")
            return
        before_count = len(self.edges)
        self.edges = [e for e in self.edges if not (e["from"] == src_node["id"] and e["to"] == tgt_node["id"])]
        after_count = len(self.edges)
        if before_count == after_count:
            print(f"⚠️ No such connection from '{from_label}' to '{to_label}'.")
        else:
            print(f"✔ Removed connection from '{from_label}' → '{to_label}'")

    def render(self, output_path="diagram_output.png"):
        dot = graphviz.Digraph(comment="Diagram")

        for node in self.nodes:
            dot.node(node["id"], label=node["label"])
        for edge in self.edges:
            dot.edge(edge["from"], edge["to"])

        output_filename = os.path.splitext(output_path)[0]
        file_path = dot.render(filename=output_filename, format="png", cleanup=True)
        print(f"🖼️ Diagram rendered at {file_path}")
        return file_path

    def print_state(self):
        print("\n📊 Current Diagram State:")
        print("Nodes:")
        for node in self.nodes:
            print(f"  {node['id']} : '{node['label']}'")
        print("Edges:")
        for edge in self.edges:
            print(f"  {edge['from']} -> {edge['to']}")
        print()
