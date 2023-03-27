import pandas as pd
import json
import requests
from dotenv import load_dotenv
import os
import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox

def deploy_update(agent_df, input_df, oracle_user, oracle_pass):
    
    # Load the variables from .env
    load_dotenv()

    # Get the input from the user
    usernames = list(input_df['USERNAME'])
    procurement_BU = list(input_df['procurement_BU'])

    # Check if there is only one user
    if len(usernames) == 1:
        # If there is only one user, change the payload and the URL_bulk link
        username = str(usernames[0]).strip()
        bu = str(procurement_BU[0]).strip()
        
        try:
            filtered_df = agent_df[agent_df['USERNAME'].str.lower() == username.lower()]
        except KeyError:
            print("Column not found! Please make sure the column name is spelled correctly.")
            exit()

        if filtered_df.empty:
            print(f"Username '{username}' not found!")
            exit()
        else:
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

            # Combine the payloads into a single payload with commas between them
            combined_payload = json.dumps(payload)

            # Replace single quotes with double quotes
            combined_payload = combined_payload.replace("'", "\"")
            request_payload = combined_payload.replace('"true"', 'true').replace('"false"', 'false')

            # Update the URL to the single upload endpoint
            URL = os.getenv("URL_single")
            # Update the Content-Type to the bulk upload one
            headers = {"Content-Type": "application/vnd.oracle.adf.resourceitem+json"}

    # If there are multiple users, proceed as usual
    else:
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
                exit()
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
        request_payload = combined_payload.replace('"true"', 'true').replace('"false"', 'false')
        # Update the URL to the bulk upload endpoint
        URL = os.getenv("URL_bulk")
        # Update the Content-Type to the bulk upload one
        headers = {"Content-Type": "application/vnd.oracle.adf.batch+json"}

    # Print the request payload
    print("\nThe request payload is: \n")
    print(request_payload)

    # Save the combined payload as a formatted json file
    with open('request_payload.json', 'w') as f:
        json.dump(json.loads(request_payload), f, indent=4)

    print("\nThe request payload has been saved as a formatted json file 'request_payload.json'.\n")

    ACCOUNT = oracle_user_entry.get()
    PASSWORD = oracle_pass_entry.get()
        
    try:
        response = requests.post(URL,
                                auth=(ACCOUNT, PASSWORD),
                                headers = headers,
                                data = request_payload)
        # If you like to put your account and password in the .env file instead, please use the below code
        # response = requests.post(os.getenv("URL"), auth=(os.getenv("ACCOUNT"), os.getenv("PASSWORD")), headers = headers, data = request_payload)
        response.raise_for_status() # Raise an exception if status code indicates an error
        # If no exception was raised, print success message and response data
        print("\nThe payload was uploaded successfully!! \n")
        print("\nBelow is the response payload: \n")
        print(response.json())
        print("\nBelow is the status code: \n")
        print(response.status_code)

    except requests.exceptions.RequestException as e:
        # Handle all exceptions and print error message
        print("\nERROR: Failed to upload the payload. Please verify that the input Business Unit (BU) is correct and that the user specified in the input already has access to the BU. If the issue persists, please contact the system administrator for assistance.\n")
        print(response.raise_for_status())  


def run_deploy_update(agent_path, input_path, oracle_user, oracle_pass):
    # read the Agent to AgentId Report and Input Excel files into data frames
    agent_df = pd.read_excel(agent_path, skiprows=1)
    input_df = pd.read_excel(input_path)

    # run the deploy_update function with the selected data frames and credentials
    if oracle_user and oracle_pass:
        deploy_update(agent_df, input_df, oracle_user, oracle_pass)
    else:
        messagebox.showerror(title="Error", message="Please enter your Oracle username and password.")


def select_agent_report():
    # open a file dialog to allow the user to select the Agent to AgentId Report Excel file
    agent_report_path = filedialog.askopenfilename(title="Select Agent to AgentId Report", filetypes=[("Excel files", "*.xlsx")])
    agent_report_entry.delete(0, tk.END)
    agent_report_entry.insert(0, agent_report_path)

def select_input():
    # open a file dialog to allow the user to select the Input Excel file
    input_path = filedialog.askopenfilename(title="Select Input File", filetypes=[("Excel files", "*.xlsx")])
    input_entry.delete(0, tk.END)
    input_entry.insert(0, input_path)

def submit():
    # get the file paths and credentials from the user
    agent_report_path = agent_report_entry.get()
    input_path = input_entry.get()
    oracle_user = oracle_user_entry.get()
    oracle_pass = oracle_pass_entry.get()

    # run the deploy_update script
    run_deploy_update(agent_report_path, input_path, oracle_user, oracle_pass)

# create the main window
root = tk.Tk()

# Set the window title and size
root.title("Procurement Agent Upload")
root.geometry("500x500")

# create buttons to allow the user to select the Excel files to upload
agent_report_button = tk.Button(root, text="Select Agent to AgentId Report", command=select_agent_report)
agent_report_button.pack()
agent_report_entry = tk.Entry(root)
agent_report_entry.pack()

input_button = tk.Button(root, text="Select Input File", command=select_input)
input_button.pack()
input_entry = tk.Entry(root)
input_entry.pack()

oracle_user_label = tk.Label(root, text="Oracle Username:")
oracle_user_label.pack()
oracle_user_entry = tk.Entry(root)
oracle_user_entry.pack()

oracle_pass_label = tk.Label(root, text="Oracle Password:")
oracle_pass_label.pack()
oracle_pass_entry = tk.Entry(root, show="*")
oracle_pass_entry.pack()

# create a button to submit the form and run the script
submit_button = tk.Button(root, text="Upload Payload", command=submit)
submit_button.pack()

# run the main event loop
root.mainloop()
