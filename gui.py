import tkinter as tk
from tkinter import ttk

class BuildingBlock:
    def __init__(self, name, category, properties):
        self.name = name
        self.category = category
        self.properties = properties
        self.value = 0

class JokerBuilder:
    def __init__(self, root):
        self.root = root
        self.root.title("Joker Builder")
        self.root.geometry("800x600")
        self.value_entry = print("Value Entry")

        # Create block palette
        self.block_palette = ttk.Frame(self.root)
        self.block_palette.pack(side=tk.LEFT, fill=tk.Y)

        self.modifier_blocks = []
        self.condition_blocks = []
        self.effect_blocks = []

        # Create blocks
        self.create_block("Plus Mult", "Modifiers", {"mult":1})
        self.create_block("Plus Chip", "Modifiers", {"chip":1})
        self.create_block("Suit Diamonds", "Conditions", {"suit": "Diamonds"})
        self.create_block("Poker Hand", "Conditions", {"hand": "Poker Hand"})
        self.create_block("Joker Slot", "Effects", {"joker_slot": True})

        # Create workspace
        self.workspace = ttk.Frame(self.root)
        self.workspace.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Create properties panel
        self.properties_panel = ttk.Frame(self.root)
        self.properties_panel.pack(side=tk.RIGHT, fill=tk.Y)

        # Create Lua code output
        self.lua_code_output = tk.Text(self.root)
        self.lua_code_output.pack(side=tk.BOTTOM, fill=tk.X)

        # Create entry field for numerical value
        self.value_entry = tk.Entry(self.properties_panel)
        self.value_entry.pack(fill=tk.X)

        # Create button to save value
        self.save_button = tk.Button(self.properties_panel, text="Save Value", command=self.save_value)
        self.save_button.pack(fill=tk.X)

        self.value_entry_attribute = self.value_entry

        # Create attribute value_entry
        self.value_entry_attribute = self.value_entry

        # Create tag buttons
        self.tag_buttons = []
        self.tag_button_frame = ttk.Frame(self.properties_panel)
        self.tag_button_frame.pack(fill=tk.X)



    def create_block(self, name, category, properties):
        block = BuildingBlock(name, category, properties)
        if category == "Modifiers":
            self.modifier_blocks.append(block)
        elif category == "Conditions":
            self.condition_blocks.append(block)
        elif category == "Effects":
            self.effect_blocks.append(block)

        # Create block button
        block_button = ttk.Button(self.block_palette, text=name)
        block_button.pack(fill=tk.X)


        # Set current block
        self.current_block = block

    def block_clicked(self, block):

    # Clear entry field
        self.value_entry.delete(0, tk.END)

    # Set focus to entry field
        self.value_entry.focus_set()

    # Set current block
        self.current_block = block

    # Update tag buttons
        self.update_tag_buttons()

    # Update current block based on button click
    for button in self.block_palette.winfo_children():
        if button['text'] == block.name:
            button.config(relief=tk.SUNKEN)
        else:
            button.config(relief=tk.RAISED)

    # Update current block based on button click
    for b in self.modifier_blocks:
        if b.name == block.name:
            self.current_block = b
    for b in self.condition_blocks:
        if b.name == block.name:
            self.current_block = b
    for b in self.effect_blocks:
        if b.name == block.name:
            self.current_block = b

    def save_value(self):
        # Get value from entry field
        value = self.value_entry.get()

        # Try to convert value to integer
        try:
            value = int(value)
        except ValueError:
            print("Invalid value")
            return

        # Save value to current block
        self.current_block.value = value

        print(f"Block: {self.current_block.name}, Value: {self.current_block.value}")
    


def update_tag_buttons(self):
    # Clear tag buttons
    for button in self.tag_buttons:
        button.destroy()

    # Create new tag buttons
    self.tag_buttons = []
    if self.current_block:
        def update_block_property(tag):
            # Get value from entry field
            value = self.value_entry.get()

            # Try to convert value to integer
            try:
                value = int(value)
            except ValueError:
                print("Invalid value")
                return

            # Update block properties
            self.current_block.properties[tag] = value

            # Print block properties
            print(f"Block: {self.current_block.name}, Properties: {self.current_block.properties}")

        for tag in self.current_block.properties:
            button = tk.Button(self.tag_button_frame, text=tag, command=lambda tag=tag: update_block_property(tag))
            button.pack(side=tk.LEFT)
            self.tag_buttons.append(button)

def update_block_property(self, tag):
    # Get value from entry field
    value = self.value_entry.get()

    # Try to convert value to integer
    try:
        value = int(value)
    except ValueError:
        print("Invalid value")
        return

    # Update block properties
    self.current_block.properties[tag] = value

    # Print block properties
    print(f"Block: {self.current_block.name}, Properties: {self.current_block.properties}")

def tag_button_clicked(self, tag):
        # Get value from entry field
        value = self.value_entry.get()

        # Try to convert value to integer
        try:
            value = int(value)
        except ValueError:
            print("Invalid value")
            return

        # Update block properties
        self.current_block.properties[tag] = value

        # Print block properties
        print(f"Block: {self.current_block.name}, Properties: {self.current_block.properties}")


def generate_lua_code(self):
        # TO DO: implement Lua code generation based on blocks in workspace
        pass

if __name__ == "__main__":
    root = tk.Tk()
    joker_builder = JokerBuilder(root)
    print(joker_builder.value_entry_attribute)
    root.mainloop()