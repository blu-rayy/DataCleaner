import pandas as pd
import os
from item_config import item_mapping_dict 
from category_config import category_mapping_dict 

def clean_data(input_file):
    df = pd.read_csv(input_file)

    updated_items = set()
    unaffected_items = set(df["Item"])

    updated_categories = set()
    unaffected_categories = set(df["Category"])

    # Replace possibly empty values
    if "Option" in df.columns:
        df = df.copy()  # Ensure df is not a view
        df["Option"] = df["Option"].fillna("N/A")

    # Clean "Item" column
    for index, row in df.iterrows():
        item = str(row["Item"]).strip() if pd.notna(row["Item"]) else ""
        category = str(row["Category"]).strip() if pd.notna(row["Category"]) else ""

        # Normalize item name (strip spaces)
        cleaned_item = item_mapping_dict.get(item, item)
        if cleaned_item != item:  # Only update if there's a change
            df.at[index, "Item"] = cleaned_item
            updated_items.add(item)
            unaffected_items.discard(item)

        # Update the category if in category_mapping_dict
        cleaned_category = category_mapping_dict.get(category, category)
        if cleaned_category != category:
            df.at[index, "Category"] = cleaned_category
            updated_categories.add(category)
            unaffected_categories.discard(category)

    # Saving the cleaned file as .csv
    month_name = os.path.basename(input_file).split("_")[0]
    output_folder = "cleaned_data"
    os.makedirs(output_folder, exist_ok=True)
    output_file = os.path.join(output_folder, f"{month_name}_cleaned.csv")
    
    df.to_csv(output_file, index=False)

    return output_file, len(updated_items), len(unaffected_items), updated_items, unaffected_items, len(updated_categories), len(unaffected_categories), updated_categories, unaffected_categories
