from flask import Flask,render_template,request,redirect
import pandas as pd
from datetime import datetime
app=Flask(__name__)

ab=[]
data=pd.read_excel('Names_List.xlsx',sheet_name=None)
data_dict={}
for year,name in data.items():
    data_dict[year]=name['Name'].tolist()
@app.route('/',methods=['POST','GET'])
def main_page():
    totals = {
        "First_year": 17,
        "Second_year": 9,
        "Third_year": 20,
        "Fourth_year": 30
    }

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
    with pd.ExcelWriter('Names_List.xlsx', engine='openpyxl', mode='a', if_sheet_exists='replace') as writer:
        for sheet, df in data.items():
            df.to_excel(writer, sheet_name=sheet, index=False)

    print("✅ Attendance updated!")
    











    ab.clear()
    return redirect('/')


if __name__=="__main__":
    app.run(debug=True)