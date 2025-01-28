import tkinter as tk
from tkinter import filedialog, ttk
import json
import os


def load_queue():
    try:
        with open("queue.json", "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return []


def save_queue(data):
    with open("queue.json", "w") as f:
        json.dump(data, f, indent=4)


def add_files():
    files = filedialog.askopenfilenames(filetypes=[("Video Files", "*.mp4 *.mkv *.avi")])
    for file in files:
        file_name = os.path.basename(file)
        title = os.path.splitext(file_name)[0]  # Default title as the file name without extension
        queue.append({"file_path": file, "title": title, "tags": [], "description": "", "visibility": "Public"})
    refresh_table()


def save_to_json():
    save_queue(queue)


def refresh_table():
    for item in tree.get_children():
        tree.delete(item)

    for index, item in enumerate(queue):
        tree.insert(
            "",
            "end",
            iid=index,
            values=(item["file_path"], item["title"], ",".join(item["tags"]), item["description"], item["visibility"]),
        )


def move_up():
    selected = tree.selection()
    if selected:
        index = int(selected[0])
        if index > 0:
            queue[index], queue[index - 1] = queue[index - 1], queue[index]
            refresh_table()
            tree.selection_set(index - 1)


def move_down():
    selected = tree.selection()
    if selected:
        index = int(selected[0])
        if index < len(queue) - 1:
            queue[index], queue[index + 1] = queue[index + 1], queue[index]
            refresh_table()
            tree.selection_set(index + 1)


def remove_selected():
    selected = tree.selection()
    if selected:
        index = int(selected[0])
        queue.pop(index)
        refresh_table()


def select_item(event):
    selected = tree.selection()
    if selected:
        index = int(selected[0])
        item = queue[index]

        # Populate side panel fields with selected item data
        file_path_label.config(text=item["file_path"])
        title_entry.delete(0, "end")
        title_entry.insert(0, item["title"])
        tags_entry.delete(0, "end")
        tags_entry.insert(0, ",".join(item["tags"]))
        description_text.delete("1.0", "end")
        description_text.insert("1.0", item["description"])
        visibility_combobox.set(item["visibility"])


def save_changes():
    selected = tree.selection()
    if selected:
        index = int(selected[0])
        item = queue[index]

        # Update the item with values from the side panel
        item["title"] = title_entry.get()
        item["tags"] = [tag.strip() for tag in tags_entry.get().split(",") if tag.strip()]
        item["description"] = description_text.get("1.0", "end").strip()
        item["visibility"] = visibility_combobox.get()

        refresh_table()
        tree.selection_set(index)


# Load existing queue
queue = load_queue()

# Create the GUI
root = tk.Tk()
root.title("Queue Manager")

# Main layout frames
main_frame = tk.Frame(root)
main_frame.pack(fill="both", expand=True)

table_frame = tk.Frame(main_frame)
table_frame.pack(side="left", fill="both", expand=True)

side_panel = tk.Frame(main_frame, width=300, padx=10, pady=10, bg="#f4f4f4")
side_panel.pack(side="right", fill="y")

# Table (Treeview)
columns = ("file_path", "title", "tags", "description", "visibility")
tree = ttk.Treeview(table_frame, columns=columns, show="headings", selectmode="browse")
tree.heading("file_path", text="File Path")
tree.heading("title", text="Title")
tree.heading("tags", text="Tags")
tree.heading("description", text="Description")
tree.heading("visibility", text="Visibility")
tree.pack(fill="both", expand=True)

# Populate the table with the initial queue
refresh_table()

# Buttons for table management
button_frame = tk.Frame(table_frame)
button_frame.pack(fill="x", pady=5)

add_button = tk.Button(button_frame, text="Add Files", command=add_files)
add_button.pack(side="left", padx=5)

up_button = tk.Button(button_frame, text="Move Up", command=move_up)
up_button.pack(side="left", padx=5)

down_button = tk.Button(button_frame, text="Move Down", command=move_down)
down_button.pack(side="left", padx=5)

remove_button = tk.Button(button_frame, text="Remove Selected", command=remove_selected)
remove_button.pack(side="left", padx=5)

save_button = tk.Button(button_frame, text="Save to JSON", command=save_to_json)
save_button.pack(side="left", padx=5)

# Side panel for editing
tk.Label(side_panel, text="Edit Item", bg="#f4f4f4", font=("Arial", 14, "bold")).pack(anchor="w")

# File path (read-only)
tk.Label(side_panel, text="File Path:", bg="#f4f4f4").pack(anchor="w")
file_path_label = tk.Label(side_panel, text="", bg="#f4f4f4", wraplength=280)
file_path_label.pack(anchor="w", fill="x", pady=5)

# Title
tk.Label(side_panel, text="Title:", bg="#f4f4f4").pack(anchor="w")
title_entry = tk.Entry(side_panel, width=40)
title_entry.pack(anchor="w", fill="x", pady=5)

# Tags
tk.Label(side_panel, text="Tags (comma-separated):", bg="#f4f4f4").pack(anchor="w")
tags_entry = tk.Entry(side_panel, width=40)
tags_entry.pack(anchor="w", fill="x", pady=5)

# Description
tk.Label(side_panel, text="Description:", bg="#f4f4f4").pack(anchor="w")
description_text = tk.Text(side_panel, width=40, height=5)
description_text.pack(anchor="w", fill="x", pady=5)

# Visibility
tk.Label(side_panel, text="Visibility:", bg="#f4f4f4").pack(anchor="w")
visibility_combobox = ttk.Combobox(side_panel, values=["Public", "Private", "Unlisted"], state="readonly")
visibility_combobox.pack(anchor="w", fill="x", pady=5)

# Save changes button
save_changes_button = tk.Button(side_panel, text="Save Changes", command=save_changes)
save_changes_button.pack(anchor="e", pady=10)

# Bind table row selection to the side panel
tree.bind("<<TreeviewSelect>>", select_item)

# Run the GUI
root.mainloop()
