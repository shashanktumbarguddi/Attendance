import pandas as pd
from datetime import datetime
import calendar

# === CONFIG ===
input_file = 'Names_List.xlsx'   # Replace with your file name
output_file = 'Names_List.xlsx'

# === GET CURRENT MONTH DATES ===
today = datetime.today()
year = today.year
month = today.month
num_days = calendar.monthrange(year, month)[1]
date_list = [datetime(year, month, day).strftime('%Y-%m-%d') for day in range(1, num_days + 1)]

# === LOAD ALL SHEETS ===
sheets = pd.read_excel(input_file, sheet_name=None)  # Returns a dict of {sheet_name: DataFrame}

updated_sheets = {}

for sheet_name, df in sheets.items():
    
    # Add empty columns for each date
    for date_str in date_list:
        df[date_str] = ""
    
    updated_sheets[sheet_name] = df

# === SAVE TO NEW FILE ===
with pd.ExcelWriter(output_file, engine='openpyxl') as writer:
    for sheet_name, df in updated_sheets.items():
        df.to_excel(writer, sheet_name=sheet_name, index=False)

print(f"Updated all sheets with date columns and saved to {output_file}")
