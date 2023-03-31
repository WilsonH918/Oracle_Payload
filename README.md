# Oracle Cloud Procurement Agent Uploader  
This project provides Python scripts that automate the process of uploading procurement agents to Oracle Cloud using the Oracle Cloud REST API. This saves users a significant amount of time compared to manually inputting agents through the Oracle Cloud UI.  

## Overview  
The project includes 3 Python scripts and 1 SQL script: 

- AgenttoAgentId.sql: Run this SQL script on your Oracle Cloud instance to return a report. Name the report "AgenttoAgentId_Report" to fit the code.  
- deploy_auto.py: This script reads in a file called "input.xlsx" that contains a list of usernames and business units. It creates a payload for each user and uploads the final combined payload to Oracle Cloud.  
- deploy_ui.py: This script provides a user-friendly interface for running the same process as deploy_auto.py. It allows you to select and load the necessary files from different locations.  
- deploy_manual.py: This script allows users to type in the agent name and procurement BU in the VScode and follows the same process as deploy_auto.py.  

## Usage  
To use the scripts, follow these steps:
1. Clone this repository to your local machine using Git.  
2. Install the required Python packages by running pip install -r requirements.txt.  
3. Set up your Oracle Cloud credentials in a .env file.  
4. Run the deploy_auto.py, deploy_ui.py or the deploy_manual.py script, depending on your needs. The scripts will prompt you for any required inputs and guide you through the process of uploading the procurement agents.  
Note: Please make sure that .env, AgenttoAgentId_Report.xlsx, input.xlsx, deploy_auto.py, deploy_manual.py and deploy_ui.py are all essential and should be placed in the same folder.  

## Discussion    
This Python script updates user accounts in Oracle Procurement using data from two input files. The agent_df DataFrame contains the current user account information, while the input_df DataFrame contains the updated information.  

The script first retrieves the Oracle username and password from environment variables using the load_dotenv() function from the dotenv package. It then prompts the user to select the input files using a file dialog.  

The deploy_update() function is the main function that handles the update process. If there is only one user to update, the function updates the user using the single upload endpoint. If there are multiple users to update, the function updates them using the bulk upload endpoint.  

The function constructs the payload for each user using the agent_id and bu values from the input DataFrame. It then sends a PATCH request to the Oracle Procurement API with the payload using the requests package. The function also shows a message box with the result of the update.  

The select_file() function opens a file dialog to prompt the user to select a file and returns the path of the selected file.  

To use this script, the user should set the required environment variables and provide the input files in the CSV and Excel formats. The user should then run the script and follow the prompts.  

The payload for each user contains the following settings:  

- Status: "Active"
- DefaultRequisitioningBU: None
- DefaultRequisitioningBUId: None
- DefaultPrinter: None
- ManageRequisitionsAllowedFlag: True
- AccessLevelToOtherAgentsRequisitions: "Full"
- ManageOrdersAllowedFlag: True
- AccessLevelToOtherAgentsOrders: "Full"
- ManageAgreementsAllowedFlag: True
- AccessLevelToOtherAgentsAgreements: "Full"
- ManageNegotiationsAllowedFlag: False
- AccessLevelToOtherAgentsNegotiations: "None"
- ManageSourcingProgramsAllowedFlag: False
- AccessLevelToOtherAgentsSourcingPrograms: "None"
- ManageCatalogContentAllowedFlag: True
- ManageSuppliersAllowedFlag: True
- ManageQualificationsAllowedFlag: True
- AccessLevelToOtherAgentsQualifications: "Full"
- ManageAslAllowedFlag: True
- AnalyzeSpendAllowedFlag: True

## Requirements  
The scripts require the following Python packages:  
pandas, json, requests, os, dotenv  
