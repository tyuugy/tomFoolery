import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from PIL import Image, ImageTk
import os

# Function to ensure only numbers are entered for cost
def validate_numeric_input(P):
    return P.isdigit() or P == ""

# Function to synchronize mod ID with mod name
def sync_mod_id(*args):
    mod_id_var.set(mod_name_var.get())

# Function to browse for an image file
def browse_image():
    file_path = filedialog.askopenfilename(
        title="Select Joker Image",
        filetypes=[("Image Files", "*.png;*.jpg;*.jpeg;*.gif;*.bmp")]
    )
    if file_path:
        image_path_var.set(file_path)
        image_label.config(text=os.path.basename(file_path))  # Display only the file name
        update_preview()  # Update the preview to show the selected image

# Function to update the preview section
def update_preview():
    # Update the image preview
    if image_path_var.get():
        img = Image.open(image_path_var.get())
        img = img.resize((150, 150))  # Resize the image for display
        img = ImageTk.PhotoImage(img)
        image_preview_label.config(image=img)
        image_preview_label.image = img  # Keep a reference to avoid garbage collection

# Function to show Joker information
def show_info(event):
    preview_text = f"""
    Mod Name: {mod_name_var.get()}
    Joker Name: {joker_name_entry.get()}
    Description: {joker_description_entry.get("1.0", tk.END).strip()}
    Rarity: {rarity_var.get()}
    Cost: {cost_entry.get()}
    """
    joker_info_label.config(text=preview_text)

# Function to hide Joker information
def hide_info(event):
    joker_info_label.config(text="")

# Function to gather data and create the folder structure and files
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
        "image_path": image_path_var.get()
    }

    # Prompt user to select output directory
    output_dir = filedialog.askdirectory(title="Select Output Directory")
    if output_dir:
        # Create the main folder named after the joker's key
        joker_folder_path = os.path.join(output_dir, joker_data['joker_key'])
        os.makedirs(joker_folder_path, exist_ok=True)

        # Create the assets folder with 1x and 2x subfolders
        assets_path = os.path.join(joker_folder_path, "assets")
        os.makedirs(os.path.join(assets_path, "1x"), exist_ok=True)
        os.makedirs(os.path.join(assets_path, "2x"), exist_ok=True)

        # Resize and save the image in 1x and 2x folders
        save_resized_images(joker_data['image_path'], assets_path)

        # Create and save the .lua file in the main folder
        create_joker_lua(joker_data, joker_folder_path)
        messagebox.showinfo("Success", f"Joker '{joker_data['joker_key']}' created successfully in {joker_folder_path}!")

# Function to resize and save the images
def save_resized_images(image_path, assets_path):
    try:
        # Open the original image
        img = Image.open(image_path)

        # Resize for 1x folder
        img_1x = img.resize((71, 95))
        img_1x.save(os.path.join(assets_path, "1x", "joker_image.png"))

        # Resize for 2x folder
        img_2x = img.resize((142, 190))
        img_2x.save(os.path.join(assets_path, "2x", "joker_image.png"))
    except Exception as e:
        messagebox.showerror("Error", f"Failed to resize and save images: {e}")

# Function to create the .lua file content
def create_joker_lua(joker_data, folder_path):
    # Only use the image file name without the path
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
        path = "joker_image.png",
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
        config = {{ extra = {{}} }},
        loc_vars = function(self, info_queue, card)
            return {{ vars = {{}} }}
        end,
        rarity = {joker_data['rarity']},
        atlas = '{joker_data['joker_key']}',
        pos = {{ x = 0, y = 0 }},
        cost = {joker_data['cost']}
    }}
    """
    
    file_path = os.path.join(folder_path, f"{joker_data['joker_key']}.lua")
    
    # Save the Lua file
    with open(file_path, "w") as file:
        file.write(lua_content)

# Rainbow wave effect for the save button
def rainbow_wave():
    # List of rainbow colors
    colors = ['#FF0000', '#FF7F00', '#FFFF00', '#00FF00', '#0000FF', '#4B0082', '#9400D3']
    # Update button color based on current color index
    current_color = colors[rainbow_wave.color_index]
    save_button.config(bg=current_color, activebackground=current_color)
    # Increment color index and reset if it exceeds the list length
    rainbow_wave.color_index = (rainbow_wave.color_index + 1) % len(colors)
    # Schedule the function to be called again after 1000 ms (1 second) for a slower effect
    root.after(1000, rainbow_wave)

# Initialize color index for rainbow wave
rainbow_wave.color_index = 0

# Create the main window
root = tk.Tk()
root.title("tomFoolery")
root.geometry("800x900")

# Variables to sync mod ID and mod name
mod_name_var = tk.StringVar()
mod_id_var = tk.StringVar()
image_path_var = tk.StringVar()
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

# Image Upload
image_frame = tk.Frame(root)
image_frame.pack(pady=10)

image_label = tk.Label(image_frame, text="No image selected")
image_label.pack()

browse_button = tk.Button(image_frame, text="Browse Image", command=browse_image)
browse_button.pack()

# Preview Section
preview_frame = tk.LabelFrame(root, text="Joker Preview", padx=10, pady=10)
preview_frame.pack(pady=10)

# Image Preview
image_preview_label = tk.Label(preview_frame)
image_preview_label.pack(side="left", padx=10)

# Joker Info Label (hidden until hover)
joker_info_label = tk.Label(preview_frame, text="", justify="left")
joker_info_label.pack(side="left", padx=10)

# Bind hover events to image preview
image_preview_label.bind("<Enter>", show_info)
image_preview_label.bind("<Leave>", hide_info)

# Save Button with Rainbow Effect
save_button = tk.Button(root, text="Save Joker", command=save_joker, font=("Arial", 14), width=15, height=2)
save_button.pack(side='right', padx=20, pady=20)

# Start the rainbow wave effect
rainbow_wave()

# Trigger update preview when fields are updated
mod_name_var.trace_add("write", lambda *args: update_preview())
joker_name_entry.bind("<KeyRelease>", lambda event: update_preview())
joker_description_entry.bind("<KeyRelease>", lambda event: update_preview())
rarity_dropdown.bind("<<ComboboxSelected>>", lambda event: update_preview())
cost_entry.bind("<KeyRelease>", lambda event: update_preview())

# Run the application
root.mainloop()
