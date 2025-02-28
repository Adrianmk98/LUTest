from jinja2 import Template
import requests
import json

API_Key="l7xx2af7939c63424511946e0fcdc35fe22a"
Base_URL="https://api-eu.hosted.exlibrisgroup.com/almaws/v1"
Auth={
    "Authorization": f"apikey {API_Key}",
    "Accept": "application/json"
}

#Uses base url specifically pointed at users to get users
#grabs the user information from JSON along with all user details
def get_users():
    User_URL=Base_URL+"/users"
    response=requests.get(User_URL,headers=Auth,params={"limit":50})
    if response.status_code==200:
        return response.json().get("user",[])
    return[]


#gets all load information
def get_Loan(userid):
    loan_URL=Base_URL+"/users/"+userid+"/loans"
    response=requests.get(loan_URL,headers=Auth,params={"limit":50})
    if response.status_code==200:
        return response.json().get("item_loan",[])
    return[]

#gets all load information
def get_fines(userid):
    fines_URL=Base_URL+"/users/"+userid+"/fees"
    response=requests.get(fines_URL,headers=Auth,params={"limit":50})
    if response.status_code==200:
        fines= response.json().get("fee",[])
        return fines,sum(float(fine.get("balance",0)) for fine in fines)
    return[],0



def generate_html():
    user=get_users()
    user_data = []

    for user in user:
        userid=(user.get("primary_id"))
        f_name=user.get("first_name","X")
        l_name=user.get("last_name","X")
        loans=get_Loan(userid)
        fines, total_fines=get_fines(userid)
        user_data.append(
            {
                "userid":userid,
                "name":f_name+" "+l_name,
                "loans": loans,
            "fines": fines,
            "total_fines": total_fines
            }
        )
        #print(f"Name: {f_name}")
        #print(f"User ID: {userid}")
        #print(f"Loans: {json.dumps(loans, indent=4)}")
        #print(f"Fines: {json.dumps(fines, indent=4)}")

        user_data.sort(key=lambda x: x["total_fines"], reverse=True)

        html_template = Template('''
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Alma Users Report</title>
        <style>
            body { font-family: Arial, sans-serif; }
            table { width: 100%; border-collapse: collapse; }
            th, td { border: 1px solid #ddd; padding: 8px; text-align: left; }
            th { background-color: #f4f4f4; }
        </style>
    </head>
    <body>
        <h2>Library Users with Loans and Fines</h2>
        <table>
            <tr>
                <th>Name</th>
                <th>User ID</th>
                <th>Number of Loans</th>
                <th>Total Fines ($)</th>
            </tr>
            {% for user in users %}
            <tr>
                <td>{{ user.name }}</td>
                <td>{{ user.userid }}</td>
                <td>{{ user.loans | length }}</td>
                <td>{{ "%.2f" | format(user.total_fines) }}</td>
            </tr>
            {% endfor %}
        </table>
    </body>
    </html>
    ''')

    html_content = html_template.render(users=user_data)

    with open("alma_users_report.html", "w", encoding="utf-8") as file:
            file.write(html_content)

    print("Report generated: alma_users_report.html")

generate_html()