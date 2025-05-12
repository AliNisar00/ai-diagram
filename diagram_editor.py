import re

class DiagramEditor:
    def __init__(self, builder):
        self.builder = builder

    def process(self, command):
        command = command.strip().lower()

        # Add node
        match = re.match(r"add a node(?: called| named)? ['\"]?(.+?)['\"]?$", command)
        if match:
            label = match.group(1)
            self.builder.add_node(label)
            print(f"✔ Node '{label}' added.")
            return

        # Add edge / connect nodes
        match = re.match(r"(connect|link) ['\"]?(.+?)['\"]? (?:to|with) ['\"]?(.+?)['\"]?$", command)
        if match:
            src = match.group(2)
            dest = match.group(3)
            self.builder.add_edge(src, dest)
            print(f"✔ Connected '{src}' → '{dest}'.")
            return

        # Rename node
        match = re.match(r"rename ['\"]?(.+?)['\"]? to ['\"]?(.+?)['\"]?$", command)
        if match:
            old_label = match.group(1)
            new_label = match.group(2)
            self.builder.rename_node(old_label, new_label)
            print(f"✔ Renamed '{old_label}' to '{new_label}'.")
            return

        # Remove node
        match = re.match(r"remove node ['\"]?(.+?)['\"]?$", command)
        if match:
            label = match.group(1)
            self.builder.remove_node(label)
            print(f"✔ Removed node '{label}'.")
            return

        # Remove edge
        match = re.match(r"remove connection from ['\"]?(.+?)['\"]? to ['\"]?(.+?)['\"]?$", command)
        if match:
            src = match.group(1)
            dest = match.group(2)
            self.builder.remove_edge(src, dest)
            print(f"✔ Removed connection from '{src}' to '{dest}'.")
            return

        # Render
        if command in ["render", "draw", "show"]:
            self.builder.render()
            print("🖼️ Diagram rendered.")
            return

        # Save
        match = re.match(r"save as ['\"]?(.+?)['\"]?$", command)
        if match:
            filename = match.group(1)
            self.builder.render(output_path=filename)
            print(f"💾 Diagram saved as {filename}.")
            return

        print("⚠️ Sorry, I didn't understand that command.")

# Main CLI loop
if __name__ == "__main__":
    from diagram_builder import DiagramBuilder

    builder = DiagramBuilder()
    editor = DiagramEditor(builder)

    print("📐 Diagram Editor CLI - Type your instructions. Type 'exit' to quit.\n")

    while True:
        cmd = input(">>> ")
        if cmd.strip().lower() in ["exit", "quit"]:
            print("👋 Goodbye!")
            break
        editor.process(cmd)
