#!/usr/bin/env python3
# -*- coding: utf_8 -*-
"""list_repo.py"""
import logging
import settings
from util.utility import init, write_file, read_file
from util.github_query import list_org_members, create_org_members

def main():
    """main"""
    logging.basicConfig(
        level = logging.INFO,
        format = "%(asctime)s [%(levelname)s] %(message)s",
        handlers = [
            logging.FileHandler("org_members.log"),
            logging.StreamHandler()
        ])
    github_org, github_token, operation = init()
    if operation.casefold() == settings.OPERATION_LIST:
        logging.info("List org members")
        org_member_count = write_file(
            list_org_members(settings.API_ENDPOINT,
                              github_org,
                              github_token),
            settings.OUTPUT_FILE_ORG_MEMBERS)
        logging.info("Filed %s org members (%s)",
                     org_member_count,
                     settings.OUTPUT_FILE_ORG_MEMBERS)
    elif operation.casefold() == settings.OPERATION_UPDATE:
        logging.info("Update org members")
        org_member_data = read_file(settings.OUTPUT_FILE_ORG_MEMBERS)
        org_member_count = create_org_members(
            settings.API_ENDPOINT,
            github_org, github_token,
            org_member_data)
        logging.info("Created %s org members", org_member_count)

if __name__ == "__main__":
    main()
