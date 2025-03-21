import pandas as pd
import os

def merge_cleaned_xlsx(output_file):
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

    writer = pd.ExcelWriter(output_path, engine="openpyxl")

    sheets_added = 0  # Track number of sheets added

    for file in files:
        try:
            df = pd.read_excel(file, engine="openpyxl")
            sheet_name = os.path.basename(file).replace("_cleaned.xlsx", "")[:31]  # Extract name, max 31 chars
            df.to_excel(writer, sheet_name=sheet_name, index=False)  
            sheets_added += 1
        except Exception as e:
            print(f"⚠️ Skipping {file}: {e}")  # Handle missing/invalid files

    if sheets_added > 0:
        writer.close()
        print(f"✅ Merged {sheets_added} files into {output_path}")
    else:
        print("⚠️ No valid Excel files found! Nothing to merge.")

# Example usage
merge_cleaned_xlsx("Merged_Cleaned_Data.xlsx")
