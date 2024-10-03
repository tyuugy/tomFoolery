import tkinter as tk
from tkinter import ttk, filedialog, messagebox

# Function to ensure only numbers are entered for cost and effect values
def validate_numeric_input(P):
    return P.isdigit() or P == ""

# Function to synchronize mod ID with mod name
def sync_mod_id(*args):
    mod_id_var.set(mod_name_var.get())

# Function to gather selected contexts and effects
def get_selected_contexts_and_effects():
    selected_contexts = [context for context, var in context_vars.items() if var.get()]
    effects = {effect: effect_vars[effect].get() for effect in effect_vars if effect_vars[effect].get()}
    return selected_contexts, effects

# Function to gather data and create the .lua file
def save_joker():
    # Collect all input data
    joker_data = {
        "mod_name": mod_name_var.get(),
        "mod_id": mod_id_var.get(),
        "mod_author": "tyuugy and ggnoods",
        "joker_key": joker_key_entry.get(),
        "joker_name": joker_name_entry.get(),
        "joker_description": joker_description_entry.get("1.0", tk.END).strip(),
        "rarity": rarity_var.get(),
        "cost": int(cost_entry.get()),
        "contexts": get_selected_contexts_and_effects()[0],
        "effects": get_selected_contexts_and_effects()[1]
    }

    # Prompt user to select output directory
    output_dir = filedialog.askdirectory(title="Select Output Directory")
    if output_dir:
        create_joker_lua(joker_data, output_dir)
        messagebox.showinfo("Success", f"Joker '{joker_data['joker_key']}.lua' created successfully in {output_dir}!")

# Function to create the .lua file content
def create_joker_lua(joker_data, output_dir):
    # Create context string
    context_str = ", ".join(joker_data['contexts'])
    
    # Create effects string
    effects_str = "\n".join([f"    {key} = {value}," for key, value in joker_data['effects'].items()])

    lua_content = f"""--- STEAMODDED HEADER
--- MOD_NAME: {joker_data['mod_name']}
--- MOD_ID: {joker_data['mod_id']}
--- MOD_DESCRIPTION: default
--- MOD_AUTHOR: [{joker_data['mod_author']}]
--- DEPENDENCIES: [Steamodded>=1.0.0~ALPHA-0812d]
--- BADGE_COLOR: c7638f
----------------------------------------------
    -- Creates an atlas for cards to use
    SMODS.Atlas {{
        key = "{joker_data['joker_key']}",
        path = "example.png",
        px = 71,
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
        config = {{ extra = {{ mult = {joker_data['mult_value']} }} }},  -- Insert user-defined multiplier here
        loc_vars = function(self, info_queue, card)
            return {{ vars = {{ card.ability.extra.mult }} }}
        end,
        contexts = {{ {context_str} }},
        effects = {{
{effects_str}
        }},
        rarity = {joker_data['rarity']},
        atlas = '{joker_data['joker_key']}',
        pos = {{ x = 0, y = 0 }},
        cost = {joker_data['cost']},
        calculate = function(self, card, context)
            if context.joker_main then
                return {{
                    mult_mod = card.ability.extra.mult,
                    message = localize {{ type = 'variable', key = 'a_mult', vars = {{ card.ability.extra.mult }} }}
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
root.title("tomFoolery")
root.geometry("800x900")

# Variables to sync mod ID and mod name
mod_name_var = tk.StringVar()
mod_id_var = tk.StringVar()
mod_name_var.trace_add("write", sync_mod_id)

# Header section for additional mod information
header_frame = tk.Frame(root)
header_frame.pack(pady=10)

# Changed header label
header_label = tk.Label(header_frame, text="tomFoolery", font=("Arial", 16))
header_label.pack()

# Fixed label for the authors
mod_author_label = tk.Label(header_frame, text="Mod made by tyuugy and ggnoods", font=("Arial", 12))
mod_author_label.pack(pady=5)

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
rarity_label.grid(row=4, column=0, padx=10, pady=5)
rarity_var = tk.IntVar()
rarity_dropdown = ttk.Combobox(main_frame, textvariable=rarity_var, values=[1, 2, 3, 4], state="readonly")
rarity_dropdown.grid(row=4, column=1, padx=10, pady=5)
rarity_dropdown.current(0)

# Cost (numeric entry only)
cost_label = tk.Label(main_frame, text="Cost:")
cost_label.grid(row=4, column=2, padx=10, pady=5)
cost_entry = tk.Entry(main_frame, validate='key', validatecommand=(root.register(validate_numeric_input), '%P'))
cost_entry.grid(row=4, column=3, padx=10, pady=5)

# Context Selection
context_frame = tk.LabelFrame(root, text="Select Contexts", padx=10, pady=10)
context_frame.pack(pady=10)
contexts_list = ["end_of_round", "buying_card", "discard", "joker_main", "repetition"]
context_vars = {context: tk.BooleanVar() for context in contexts_list}
for i, context in enumerate(contexts_list):
    checkbox = tk.Checkbutton(context_frame, text=context, variable=context_vars[context])
    checkbox.grid(row=i//2, column=i%2, sticky='w', padx=5)

# Effect Configuration
effect_frame = tk.LabelFrame(root, text="Configure Effects", padx=10, pady=10)
effect_frame.pack(pady=10)
effects_list = ["mult_mod", "plus_chips", "times_mult", "extra.func"]
effect_vars = {effect: tk.Entry(effect_frame, validate='key', validatecommand=(root.register(validate_numeric_input), '%P')) for effect in effects_list}
for i, effect in enumerate(effects_list):
    label = tk.Label(effect_frame, text=f"{effect}:")
    label.grid(row=i, column=0, sticky='e')
    effect_vars[effect].grid(row=i, column=1, padx=5)

# Save Button moved to the right
save_button = tk.Button(root, text="Save Joker", command=save_joker)
save_button.pack(side='right', padx=20, pady=20)

# Run the application
root.mainloop()
