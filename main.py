import requests
import json
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
def get_Loan(userid):
    loan_URL=Base_URL+"/users/"+userid+"/loans"
    response=requests.get(loan_URL,headers=Auth,params={"limit":50})
    if response.status_code==200:
        return response.json().get("item_loan",[])
    return[]

#gets all load information
def get_fines(userid):
    fines_URL=Base_URL+"/users/"+userid+"/fines"
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
        fines=get_fines(userid)
        user_data.append(
            {
                "userid":userid,
                "name":f_name+" "+l_name,
                "loans":loans,
                "fines":fines
            }
        )
        print(f"Name: {f_name}")
        print(f"User ID: {userid}")
        print(f"Loans: {json.dumps(loans, indent=4)}")
        print(f"Fines: {json.dumps(fines, indent=4)}")
        '''
    htmlbase=<html><head></head><body>
    <table>
    <tr>
    <th>ID</th>
    <th>Name</th>
    <th>Loans</th>
    <th>Fees</th>
    </tr>
    <tr>
    <td></td>
    </body></html>
'''

generate_html()