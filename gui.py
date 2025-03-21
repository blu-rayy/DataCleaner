import tkinter as tk
from tkinter import messagebox, filedialog, scrolledtext
import pandas as pd
import os

from item_config import item_mapping_dict 
from category_config import category_mapping_dict 
from cleaning import clean_data 

def select_file():
    try:
        selected_file = file_listbox.get(file_listbox.curselection())
        file_path = os.path.join("files", selected_file)
        clean_and_display(file_path)
    except tk.TclError:
        messagebox.showerror("Error", "Please select a file before proceeding.")

# code for renaming the file name with a proper naming convention
def clean_and_display(file_path):
    month = os.path.basename(file_path).split("_")[0]  
    output_file = os.path.join("cleaned_data", f"{month}_cleaned.csv")
    
    # run cleaning function
    (
        output_file, updated_item_count, unaffected_item_count, updated_items, unaffected_items,
        updated_category_count, unaffected_category_count, updated_categories, unaffected_categories
    ) = clean_data(file_path)

    # Identify new entries (items not in item_mapping_dict)
    all_items = set(updated_items).union(unaffected_items)
    new_entries = sorted([item for item in all_items if item not in item_mapping_dict])
    
    # covert sets to sorted lists
    updated_items_list = sorted(updated_items)
    unaffected_items_list = sorted(str(item) for item in unaffected_items)
    updated_categories_list = sorted(updated_categories)
    unaffected_categories_list = sorted(unaffected_categories)

    # creating a windows for item cleaning results
    result_window = tk.Toplevel(root)
    result_window.title("Item Cleaning Results")
    result_window.geometry("600x500")  # adjust if necessary

    # header for item
    tk.Label(result_window, text=f"Item Cleaning Results ({output_file})", font=("Arial", 12, "bold")).pack(pady=5)

    # Scrollable text box for detailed output
    text_area = scrolledtext.ScrolledText(result_window, wrap=tk.WORD, width=80, height=20)
    text_area.pack(padx=10, pady=5, fill=tk.BOTH, expand=True)

    text_area.tag_configure("bold", font=("Arial", 10, "bold"))

    # Insert item results with bold headers
    text_area.insert(tk.END, f"Updated Items ({updated_item_count}):\n", "bold")
    text_area.insert(tk.END, "\n".join(updated_items_list) + "\n\n")
    
    text_area.insert(tk.END, f"Unaffected Items ({unaffected_item_count}):\n", "bold")
    text_area.insert(tk.END, "\n".join(unaffected_items_list) + "\n\n")
    
    text_area.insert(tk.END, f"New Entries ({len(new_entries)}):\n", "bold")
    text_area.insert(tk.END, "\n".join(new_entries))

    # Disable editing of text area
    text_area.config(state=tk.DISABLED)

    # creating another windows for category cleaning results
    category_window = tk.Toplevel(root)
    category_window.title("Category Cleaning Results")
    category_window.geometry("600x400")  # adjust size

    # header for category
    tk.Label(category_window, text="Category Cleaning Results", font=("Arial", 12, "bold")).pack(pady=5)

    category_text_area = scrolledtext.ScrolledText(category_window, wrap=tk.WORD, width=80, height=15)
    category_text_area.pack(padx=10, pady=5, fill=tk.BOTH, expand=True)
    category_text_area.tag_configure("bold", font=("Arial", 10, "bold"))

    category_text_area.insert(tk.END, f"Updated Categories ({updated_category_count}):\n", "bold")
    category_text_area.insert(tk.END, "\n".join(updated_categories_list) + "\n\n")

    category_text_area.insert(tk.END, f"Unaffected Categories ({unaffected_category_count}):\n", "bold")
    category_text_area.insert(tk.END, "\n".join(unaffected_categories_list))

    category_text_area.config(state=tk.DISABLED)

def list_files():
    files = [f for f in os.listdir("files") if f.endswith(".csv")]
    file_listbox.delete(0, tk.END)  # clears listbox
    for file in files:
        file_listbox.insert(tk.END, file)

# GUI Setup
root = tk.Tk()
root.title("CSV Cleaning Tool")
root.geometry("400x300")
root.resizable(False, False)  # fixed window size

tk.Label(root, text="Select a CSV File to Clean:").pack(pady=5)

file_listbox = tk.Listbox(root, height=10)
file_listbox.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)

list_files()

tk.Button(root, text="Clean Selected File", command=select_file).pack(pady=5)

root.mainloop()