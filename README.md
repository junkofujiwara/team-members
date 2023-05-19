## GitHub team and member maintenance script

### Prerequisites
Python 3
`pip install -r requirements.txt`

### Usage: List Team Members
Purpose: To list Team Members info in specified organization.<br/>
How to Use: Execute following command-line with your organization name and token (Personal Access Token). The list of repo names and visibility information is written to a csv files `teams.csv` and `members.csv`.

- command-line: 
`python3 team_members.py list -o <org-name> -t <token>`
- Output: 
`teams.csv` and `members.csv`
- Teams Output Format: `<team slug>,<name>,<description>,<privacy>,<parent_name>`
- Members Output Format: `<team slug>,<username>,<role>`
- Log File: 
`team_members.log`


### Usage: Create Teams and Members
Purpose: To create teams and members.<br/>
How to Use: Execute following command-line with your target organization name and token (Personal Access Token). Processes teams and member creations from the files `teams.csv` and `members.csv`.<br/>
Note: When you have team synchronization set up for a team with your organization's identity provider (IdP), you will see an error if you attempt to use the API for making changes to the team's membership. [Reference](https://docs.github.com/en/rest/teams/members?apiVersion=2022-11-28#add-or-update-team-membership-for-a-user)

- command-line
`python3 team_members.py create -o <org-name> -t <token>`
- Input
`teams.csv` and `members.csv`
- Log File: 
`team_members.log`
- Note
404 error will be returned if the team already exists. In this case, you can delete the team from the GitHub UI and re-run the script.

### Additional Notes
The name of the output CSV files can be changed in settings.py
