## GitHub team and member maintenance script

### Prerequisites
Python 3
`pip install -r requirements.txt`

### Usage: List Team Members
Purpose: List team member information within a specified organization.<br/>
How to Use: Execute following command-line with your organization name and token (Personal Access Token). The list of team member information is written to a csv files `teams.csv` and `team_members.csv`. 

- Command-line: 
`python3 team_members.py list -o <org-name> -t <token>`
- Output: 
`teams.csv` and `team_members.csv`
- Teams Output Format: `<team slug>,<name>,<description>,<privacy>,<parent_name>`
- Members Output Format: `<team slug>,<username>,<role>`
- Log File: 
`team_members.log`


### Usage: Create Teams and Members
Purpose: Create teams and team members.<br/>
How to Use: Execute following command-line with your target organization name and token (Personal Access Token). Processes teams and member creations from the files `teams.csv` and `team_members.csv`.<br/>
Note: When you have team synchronization set up for a team with your organization's identity provider (IdP), you will see an error if you attempt to use the API for making changes to the team's membership. [Reference](https://docs.github.com/en/rest/teams/members?apiVersion=2022-11-28#add-or-update-team-membership-for-a-user)

- Command-line
`python3 team_members.py create -o <org-name> -t <token>`
- Input
`teams.csv` and `team_members.csv`
- Log File: 
`team_members.log`

### Usage: List Org Members
Purpose: List organization members information within a specified organization.<br/>
How to Use: Execute following command-line with your organization name and token (Personal Access Token). The list of org member information is written to a csv file `org_members.csv`.

- Command-line: 
`python3 org_members.py list -o <org-name> -t <token>`
- Output: 
`org_members.csv`
- Members Output Format: `<username>,<role>`
- Log File: 
`org_members.log`

### Usage: Set Organization Members
Purpose: Set organization membership for a user.<br/>
How to Use: Execute following command-line with your target organization name and token (Personal Access Token). Processes set organization membership from the file `org_members.csv`.<br/>
Note: Organization needs to be created manually. [Reference](https://docs.github.com/ja/enterprise-cloud@latest/rest/orgs/members?apiVersion=2022-11-28#set-organization-membership-for-a-user)

- Command-line
`python3 org_members.py create -o <org-name> -t <token>`
- Input
`org_members.csv`
- Log File: 
`org_members.log`

### Additional Notes
- The name of the output CSV files can be changed in settings.py
- API endpoint can be changed in settings.py for GitHub Enterprise Server
