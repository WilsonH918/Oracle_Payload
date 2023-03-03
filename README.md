# Oracle Cloud Procurement Agent Uploader


# Overview
This project provides a set of Python scripts that automate the process of uploading procurement agents to Oracle Cloud using the Oracle Cloud REST API. The scripts can process multiple agents at once, saving users a significant amount of time compared to manually inputting agents through the Oracle Cloud UI.

There are two scripts included in this project:
1. deploy_input_file.py: This script reads in a document called "input.xlsx" that contains a list of usernames and business units, creates a payload for each user, and uploads the final combined payload to Oracle Cloud.
2. deploy_input_name.py: This script allows users to type in the agent name and procurement BU in the VScode and follows the same process as the deploy_input_file.py script.


# Usage
To use the scripts, follow these steps:
1. Clone this repository to your local machine using Git.
2. Install the required Python packages by running pip install -r requirements.txt.
3. Set up your Oracle Cloud credentials in a config.ini file. You can use the config_template.ini file as a starting point.
4. Run the deploy_input_file.py script or the deploy_input_name.py script, depending on your needs. The scripts will prompt you for any required inputs and guide you through the process of uploading the procurement agents.


# Requirements
The scripts require the following Python packages:
pandas
requests
json
