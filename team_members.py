#!/usr/bin/env python3
# -*- coding: utf_8 -*-
"""list_repo.py"""
import logging
import settings
from util.utility import init, write_file, read_file
from util.github_query import list_teams, list_team_members, create_teams, create_team_members

def main():
    """main"""
    logging.basicConfig(
        level = logging.INFO,
        format = "%(asctime)s [%(levelname)s] %(message)s",
        handlers = [
            logging.FileHandler("team_members.log"),
            logging.StreamHandler()
        ])
    github_org, github_token, operation = init()
    if operation.casefold() == settings.OPERATION_LIST:
        logging.info("List team and members")
        teams = list_teams(settings.API_ENDPOINT,
                           github_org,
                           github_token)
        team_count = write_file(teams, settings.OUTPUT_FILE_TEAMS)
        logging.info("Filed %s teams (%s)", team_count, settings.OUTPUT_FILE_TEAMS)
        team_member_count = write_file(
            list_team_members(settings.API_ENDPOINT,
                              github_org,
                              github_token,
                              teams),
            settings.OUTPUT_FILE_TEAM_MEMBERS)
        logging.info("Filed %s team members (%s)",
                     team_member_count,
                     settings.OUTPUT_FILE_TEAM_MEMBERS)
    elif operation.casefold() == settings.OPERATION_UPDATE:
        logging.info("Update teams and members")
        team_data = read_file(settings.OUTPUT_FILE_TEAMS)
        team_count = create_teams(settings.API_ENDPOINT,
                                  github_org,
                                  github_token,
                                  team_data)
        logging.info("Created %s teams", team_count)
        team_member_data = read_file(settings.OUTPUT_FILE_TEAM_MEMBERS)
        team_member_count = create_team_members(
            settings.API_ENDPOINT,
            github_org, github_token,
            team_member_data)
        logging.info("Created %s team members", team_member_count)

if __name__ == "__main__":
    main()
