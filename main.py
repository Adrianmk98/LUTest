import requests
import json
from jinja2 import Template

#I know I shouldnt make the API key public but its the demo
#I didnt want to leave the code unfinished. Please look at the older version
API_Key="l7xx2af7939c63424511946e0fcdc35fe22a"
Base_URL="https://api-eu.hosted.exlibrisgroup.com/almaws/v1"
Auth={
    "Authorization": f"apikey {API_Key}",
    "Accept": "application/json"
}

#Uses base url specifically pointed at users to get users
def get_users():
    User_URL=Base_URL+"/users"
    response=requests.get(User_URL,headers=Auth,params={"limit":50})
    if response.status_code==200:
        return response.json().get("user",[])
    return[]


#gets all load information
def get_loan(userid):
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
        loans=get_loan(userid)
        fines,total_fines=get_fines(userid)
        user_data.append(
            {
                "userid":userid,
                "name":f_name+" "+l_name,
                "loans":loans,
                "fines": fines,
                "total_fines": total_fines
            }
        )

        #print(f"Name: {f_name}")
        #print(f"User ID: {userid}")
        #print(f"Loans: {json.dumps(loans, indent=4)}")
        #print(f"Fines: {json.dumps(fines, indent=4)}")
    user_data.sort(key=lambda x: x["total_fines"], reverse=True)
    htmlbase=Template('''<html><body>
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
    </body></html>
''')
    html_content = htmlbase.render(users=user_data)

    # Save to file
    with open("report.html", "w", encoding="utf-8") as file:
        file.write(html_content)

    print("Report generated: alma_users_report.html")

generate_html()
