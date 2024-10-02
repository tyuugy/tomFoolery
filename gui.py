import tkinter as tk
from tkinter import ttk, filedialog, messagebox

# Function to ensure only numbers are entered for cost
def validate_numeric_input(P):
    return P.isdigit() or P == ""

# Function to synchronize mod ID with mod name
def sync_mod_id(*args):
    mod_id_var.set(mod_name_var.get())

# Function to gather data and create the .lua file
def save_joker():
    # Collect all input data
    joker_data = {
        "mod_name": mod_name_var.get(),
        "mod_id": mod_id_var.get(),
        "mod_author": mod_author_entry.get(),
        "mod_description": mod_description_entry.get("1.0", tk.END).strip(),
        "joker_key": joker_key_entry.get(),
        "joker_name": joker_name_entry.get(),
        "joker_description": joker_description_entry.get("1.0", tk.END).strip(),
        "rarity": rarity_var.get(),
        "cost": int(cost_entry.get())
    }

    # Prompt user to select output directory
    output_dir = filedialog.askdirectory(title="Select Output Directory")
    if output_dir:
        # Create and save .lua file
        create_joker_lua(joker_data, output_dir)
        messagebox.showinfo("Success", f"Joker '{joker_data['joker_key']}.lua' created successfully in {output_dir}!")

# Function to create the .lua file content
def create_joker_lua(joker_data, output_dir):
    lua_content = f"""
    --- STEAMODDED HEADER
    --- MOD_NAME: "{joker_data['mod_name']}"
    --- MOD_ID: {joker_data['mod_id']}
    --- MOD_DESCRIPTION: default
    --- MOD_AUTHOR: ION: "{joker_data['mod_description']}"
    --- DEPENDENCIES: [Steamodded>=1.0.0~ALPHA-0812d]
    --- BADGE_COLOR: c7638f
    --- PREFIX: mvan

    -- Creates an atlas for cards to use
    SMODS.Atlas {{
        -- Key for code to find it with
        key = "{joker_data['joker_key']}",
        -- The name of the file, for the code to pull the atlas from
        path = "example.png",
        -- Width of each sprite in 1x size
        px = 71,
        -- Height of each sprite in 1x size
        py = 95
    }}

    SMODS.Joker {{
        key = '{joker_data['joker_key']}',
        loc_txt = {{
            name = '{joker_data['joker_name']}',
            text = {{
                "{joker_data['joker_description']}"
            }}
        }},
        config = {{}},
        loc_vars = function(self, info_queue, card)
            return {{}}
        end,
        rarity = {joker_data['rarity']},
        atlas = '{joker_data['joker_key']}',
        pos = {{ x = 0, y = 0 }},
        cost = {joker_data['cost']},
        calculate = function(self, card, context)
            if context.joker_main then
                return {{
                    joker_slots = 3,
                    mult_mod = 4,
                    message = "Joker grants +3 slots and x4 multiplier."
                }}
            end
        end
    }}
    """
    
    file_path = f"{output_dir}/{joker_data['joker_key']}.lua"
    with open(file_path, "w") as file:
        file.write(lua_content)

# Create the main window
root = tk.Tk()
root.title("Balatro Joker Creator")
root.geometry("800x600")

# Variables to sync mod ID and mod name
mod_name_var = tk.StringVar()
mod_id_var = tk.StringVar()
mod_name_var.trace_add("write", sync_mod_id)

# Header section for additional mod owner information
header_frame = tk.Frame(root)
header_frame.pack(pady=10)

header_label = tk.Label(header_frame, text="Enter Mod Owner Information", font=("Arial", 16))
header_label.pack()

mod_author_entry = tk.Entry(header_frame, width=40)
mod_author_entry.pack(pady=5)
mod_author_entry.insert(0, "Enter Mod Author Name")

# Main frame for mod and joker information
main_frame = tk.Frame(root)
main_frame.pack(pady=20)

# Mod Name and ID section
mod_name_label = tk.Label(main_frame, text="Mod Name:")
mod_name_label.grid(row=0, column=0, padx=10, pady=5)
mod_name_entry = tk.Entry(main_frame, textvariable=mod_name_var)
mod_name_entry.grid(row=0, column=1, padx=10, pady=5)

mod_id_label = tk.Label(main_frame, text="Mod ID:")
mod_id_label.grid(row=0, column=2, padx=10, pady=5)
mod_id_entry = tk.Entry(main_frame, textvariable=mod_id_var, state='readonly')
mod_id_entry.grid(row=0, column=3, padx=10, pady=5)

# Joker Name and Key
joker_name_label = tk.Label(main_frame, text="Joker Name:")
joker_name_label.grid(row=1, column=0, padx=10, pady=5)
joker_name_entry = tk.Entry(main_frame)
joker_name_entry.grid(row=1, column=1, padx=10, pady=5)

joker_key_label = tk.Label(main_frame, text="Joker Key:")
joker_key_label.grid(row=1, column=2, padx=10, pady=5)
joker_key_entry = tk.Entry(main_frame)
joker_key_entry.grid(row=1, column=3, padx=10, pady=5)

# Joker Description
joker_description_label = tk.Label(main_frame, text="Joker Description:")
joker_description_label.grid(row=2, column=0, padx=10, pady=5)
joker_description_entry = tk.Text(main_frame, height=4, width=50)
joker_description_entry.grid(row=2, column=1, columnspan=3, padx=10, pady=5)

# Rarity Dropdown
rarity_label = tk.Label(main_frame, text="Rarity:")
rarity_label.grid(row=3, column=0, padx=10, pady=5)
rarity_var = tk.IntVar()
rarity_dropdown = ttk.Combobox(main_frame, textvariable=rarity_var, values=[1, 2, 3, 4], state="readonly")
rarity_dropdown.grid(row=3, column=1, padx=10, pady=5)
rarity_dropdown.current(0)

# Cost (numeric entry only)
cost_label = tk.Label(main_frame, text="Cost:")
cost_label.grid(row=3, column=2, padx=10, pady=5)
cost_entry = tk.Entry(main_frame, validate='key', validatecommand=(root.register(validate_numeric_input), '%P'))
cost_entry.grid(row=3, column=3, padx=10, pady=5)

# Save Button
save_button = tk.Button(root, text="Save Joker", command=save_joker)
save_button.pack(pady=20)

# Run the application
root.mainloop()
