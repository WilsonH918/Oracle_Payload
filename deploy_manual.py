import pandas as pd
import json
import requests
from dotenv import load_dotenv
import os

# Read the excel file
try:
    df = pd.read_excel('AgenttoAgentId_Report.xlsx')
except FileNotFoundError:
    print("File not found! Please make sure the file exists in the current directory.")
    exit()

# Get the input from the user
usernames = input("Enter the USERNAME(s) separated by commas: ").split(',')

# Get procurement BU
procurement_BU = input ("Enter the BU: ")

# Loop through each username and retrieve the corresponding agent ID and payload
payloads = []
for i, username in enumerate(usernames):
    # Strip any leading/trailing whitespace from the username
    username = username.strip()

    # Filter the dataframe based on the input username
    try:
        filtered_df = df[df['USERNAME'].str.lower() == username.lower()]
    except KeyError:
        print("Column not found! Please make sure the column name is spelled correctly.")
        continue

    # Check if the username exists in the dataframe
    if filtered_df.empty:
        print(f"Username '{username}' not found!")
    else:
        # Retrieve the AGENT_ID for the input username
        agent_id = int(filtered_df.iloc[0]['AGENT_ID'])

        # Construct the payload
        payload = {
            "AgentId": agent_id,
            "ProcurementBU": procurement_BU,
            "Status": "Active",
            "DefaultRequisitioningBU": None,
            "DefaultRequisitioningBUId": None,
            "DefaultPrinter": None,
            "ManageRequisitionsAllowedFlag": True,
            "AccessLevelToOtherAgentsRequisitions": "View",
            "ManageOrdersAllowedFlag": True,
            "AccessLevelToOtherAgentsOrders": "Full",
            "ManageAgreementsAllowedFlag": False,
            "AccessLevelToOtherAgentsAgreements": "None",
            "ManageNegotiationsAllowedFlag": False,
            "AccessLevelToOtherAgentsNegotiations": "None",
            "ManageSourcingProgramsAllowedFlag": False,
            "AccessLevelToOtherAgentsSourcingPrograms": "None",
            "ManageCatalogContentAllowedFlag": False,
            "ManageSuppliersAllowedFlag": False,
            "ManageQualificationsAllowedFlag": False,
            "AccessLevelToOtherAgentsQualifications": "None",
            "ManageAslAllowedFlag": False,
            "AnalyzeSpendAllowedFlag": False
        }

        # Replace None with null
        payload = {k: (v if v is not None else None) for k, v in payload.items()}

        # Convert boolean values to lowercase string values
        payload = {k: (str(v).lower() if isinstance(v, bool) else v) for k, v in payload.items()}

        # Add ID and path information to the payload
        payload = {
            "id": f"part{i+1}",
            "path": "/procurementAgents",
            "operation": "create",
            "payload": payload
        }

        # Add the payload to the list of payloads
        payloads.append(payload)

# Combine the payloads into a single payload with commas between them
combined_payload = json.dumps({"parts": payloads})

# Replace single quotes with double quotes
combined_payload = combined_payload.replace("'", "\"")
combined_payload = combined_payload.replace('"true"', 'true').replace('"false"', 'false')

# Print the combined payload
print("The combined payload is:")
print(combined_payload)

check = input("Please check if the payload looks alright: (enter Y/N)")

if check == "Y":
    load_dotenv()
    headers = {"Content-Type": "application/vnd.oracle.adf.batch+json"}
    response = requests.post(os.getenv("URL"), auth=(os.getenv("ACCOUNT"), os.getenv("PASSWORD")), headers = headers, data = combined_payload)
    print(response.json())
    print(response.status_code)

else:
    print("Please double-check with your input document.")
    exit()




