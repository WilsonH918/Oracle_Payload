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


## Requirements  
The scripts require the following Python packages:  
pandas, json, requests, os, dotenv  
