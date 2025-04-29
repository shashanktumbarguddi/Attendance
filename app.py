from flask import Flask,render_template,request,redirect
import pandas as pd
from datetime import datetime
import os
import calendar
app=Flask(__name__)

ab=[]
data=pd.read_excel('Names_List.xlsx',sheet_name=None)
data_dict={}
totals = {
    "First_year": 17,
    "Second_year": 9,
    "Third_year": 20,
    "Fourth_year": 30
}
absents = {}
presents = {}
names = {}
for year,name in data.items():
    data_dict[year]=name['Name'].tolist()
@app.route('/',methods=['POST','GET'])
def main_page():
    global absents, presents
    if request.method=="POST":
        #Getting the absent 
        absents = {
            "First_year": int(request.form.get("1st_year_absent", 0)),
            "Second_year": int(request.form.get("2nd_year_absent", 0)),
            "Third_year": int(request.form.get("3rd_year_absent", 0)),
            "Fourth_year": int(request.form.get("4th_year_absent", 0))
        }
        for y,c in absents.items():
            if c!=0:
                ab.append(y)
        #The total count 
        presents = {}
        for year, total in totals.items():
            absent_count = absents.get(year, 0)
            present_count = total - absent_count
            presents[year] = present_count if present_count >= 0 else 0 
        return render_template('Select.html',dict=data_dict,absent=absents)
    return render_template('index.html')

@app.route("/absent",methods=["POST"])
def absent():
    global names
    names={}
    print(ab)
    for year in ab:
        y="{}_absent_names".format(year)
        print(y)
        names[y]=[name.strip() for name in request.form.get(y, '').split(',') if name.strip()]
    print("Printing the absent names ")
    print(names)
    sheet_names = list(data.keys())
    today_str = datetime.today().strftime('%Y-%m-%d')
    for sheet in sheet_names:
        df = data[sheet]
        absent_list = names.get(f"{sheet}_absent_names", [])

        # Add today's column if not present
        if today_str not in df.columns:
            df[today_str] = 'P'

        # Mark attendance
        df[today_str] = df['Name'].apply(lambda name: 'A' if name in absent_list else 'P')
        data[sheet] = df
    # Write back

    input_file = 'Names_List.xlsx'
    new_file = f"{datetime.today().strftime('%B')}.xlsx"
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
    with pd.ExcelWriter(new_file, engine='openpyxl') as writer:
        for sheet_name, df in updated_sheets.items():
            df.to_excel(writer, sheet_name=sheet_name, index=False)

    print(f"Updated all sheets with date columns and saved to {new_file}")
    # Check if file exists
    file_exists = os.path.exists(new_file)
    # Set ExcelWriter options
    if file_exists:
        writer_options = {'mode': 'a', 'if_sheet_exists': 'replace'}
    else:
        writer_options = {'mode': 'w'}  # no need for if_sheet_exists
    # Write to the Excel file
    with pd.ExcelWriter(new_file, engine='openpyxl', **writer_options) as writer:
        for sheet, df in data.items():
            df.to_excel(writer, sheet_name=sheet, index=False)

    print(f"✅ Attendance {'updated' if file_exists else 'saved to new file'}: {new_file}")
    






    
    return render_template('text_box.html',totals=totals,absents=absents,presents=presents,names=names,ab=ab)
    ab.clear()



if __name__=="__main__":
    app.run(debug=True)