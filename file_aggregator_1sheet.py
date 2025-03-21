import pandas as pd
import os

def merge_cleaned_xlsx_one_sheet(output_file):
    files = [
        "files\\excel format\\january_cleaned.xlsx",
        "files\\excel format\\february_cleaned.xlsx",
        "files\\excel format\\march_cleaned.xlsx",
        "files\\excel format\\april_cleaned.xlsx",
        "files\\excel format\\may_cleaned.xlsx",
        "files\\excel format\\june_cleaned.xlsx",
        "files\\excel format\\july_cleaned.xlsx",
        "files\\excel format\\august_cleaned.xlsx",
        "files\\excel format\\september_cleaned.xlsx",
        "files\\excel format\\october_cleaned.xlsx",
        "files\\excel format\\november_cleaned.xlsx",
        "files\\excel format\\december_cleaned.xlsx"
    ]  # Manually listed files with relative paths

    output_folder = "files\\merged"
    os.makedirs(output_folder, exist_ok=True)  # Ensure output directory exists
    output_path = os.path.join(output_folder, output_file)

    merged_df = pd.DataFrame()  # Create an empty DataFrame to hold all data

    for file in files:
        try:
            df = pd.read_excel(file, engine="openpyxl")
            df["Source File"] = os.path.basename(file)  # Add a column to indicate the source
            merged_df = pd.concat([merged_df, df], ignore_index=True)  # Merge data
        except Exception as e:
            print(f"⚠️ Skipping {file}: {e}")  # Handle missing/invalid files

    if not merged_df.empty:
        merged_df.to_excel(output_path, sheet_name="Merged_Data", index=False)
        print(f"✅ Merged all files into one sheet: {output_path}")
    else:
        print("⚠️ No valid Excel files found! Nothing to merge.")

# Example usage
merge_cleaned_xlsx_one_sheet("OneFile_Cleaned_Data.xlsx")
