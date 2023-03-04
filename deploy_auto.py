import pandas as pd
import json
import requests
from dotenv import load_dotenv
import os

# Read the excel files
try:
    agent_df = pd.read_excel('AgenttoAgentId_Report.xlsx')
    input_df = pd.read_excel('input.xlsx')
except FileNotFoundError:
    print("File not found! Please make sure the files exist in the current directory.")
    exit()

# Get the input from the user
usernames = list(input_df['USERNAME'])
procurement_BU = list(input_df['procurement_BU'])

# Loop through each username and retrieve the corresponding agent ID and payload
payloads = []
for i, (username, bu) in enumerate(zip(usernames, procurement_BU)):
    # Strip any leading/trailing whitespace from the username and bu
    username = str(username).strip()
    bu = str(bu).strip()

    # Filter the dataframe based on the input username
    try:
        filtered_df = agent_df[agent_df['USERNAME'].str.lower() == username.lower()]
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
            "ProcurementBU": bu,
            "Status": "Active",
            "DefaultRequisitioningBU": None,
            "DefaultRequisitioningBUId": None,
            "DefaultPrinter": None,
            "ManageRequisitionsAllowedFlag": True,
            "AccessLevelToOtherAgentsRequisitions": "Full",
            "ManageOrdersAllowedFlag": True,
            "AccessLevelToOtherAgentsOrders": "Full",
            "ManageAgreementsAllowedFlag": True,
            "AccessLevelToOtherAgentsAgreements": "Full",
            "ManageNegotiationsAllowedFlag": False,
            "AccessLevelToOtherAgentsNegotiations": "None",
            "ManageSourcingProgramsAllowedFlag": False,
            "AccessLevelToOtherAgentsSourcingPrograms": "None",
            "ManageCatalogContentAllowedFlag": True,
            "ManageSuppliersAllowedFlag": True,
            "ManageQualificationsAllowedFlag": True,
            "AccessLevelToOtherAgentsQualifications": "Full",
            "ManageAslAllowedFlag": True,
            "AnalyzeSpendAllowedFlag": True
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

# Save the combined payload as a formatted json file
with open('request_payload.json', 'w') as f:
    json.dump(json.loads(combined_payload), f, indent=4)

print("The combined payload has been saved as a formatted json file 'request_payload.json'.")

check = input("Please check if the payload looks alright: (enter Y/N)")

if check == "Y":
    load_dotenv()
    headers = {"Content-Type": "application/vnd.oracle.adf.batch+json"}
    response = requests.post(os.getenv("URL"), auth=(os.getenv("ACCOUNT"), os.getenv("PASSWORD")), headers = headers, data = combined_payload)
    print(response.json())
    print(response.status_code)

else:
    print("Please double-check with you input document.")
    exit()
