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

    # replace possibly empty values
    if "Option" in df.columns:
        df["Option"].fillna("N/A", inplace=True)

    # Clean "Item" column
    for index, row in df.iterrows():
        item = row["Item"]
        category = row["Category"]

        # update the item if in item_mapping_dict
        if item in item_mapping_dict:
            df.at[index, "Item"] = item_mapping_dict[item]
            updated_items.add(item)
            unaffected_items.discard(item)

        # update the category if in category_mapping_dict
        if category in category_mapping_dict:
            df.at[index, "Category"] = category_mapping_dict[category]
            updated_categories.add(category)
            unaffected_categories.discard(category)

    # saving the cleaned file
    month_name = os.path.basename(input_file).split("_")[0]
    output_folder = "cleaned_data"
    os.makedirs(output_folder, exist_ok=True)
    output_file = os.path.join(output_folder, f"{month_name}_cleaned.csv")
    df.to_csv(output_file, index=False)

    return output_file, len(updated_items), len(unaffected_items), updated_items, unaffected_items, len(updated_categories), len(unaffected_categories), updated_categories, unaffected_categories
