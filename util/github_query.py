#!/usr/bin/env python3
# -*- coding: utf_8 -*-
"""github_query.py"""
import logging
import requests

def list_teams(endpoint, org, token):
    """list teams"""
    data = []
    logging.info("Executing list teams query. org=%s", org)
    url = f'{endpoint}/orgs/{org}/teams?per_page=100'
    result = run_get(url, token)
    for item in result:
        if item["parent"]:
            data.append([item["slug"],
                         item["name"],
                         item["description"],
                         item["privacy"],
                         item["parent"]["name"]])
        else:
            data.append([item["slug"],
                         item["name"],
                         item["description"],
                         item["privacy"], ''])
    return data

def get_team(endpoint, org, token, team_slug, exist_check=False):
    """get team"""
    logging.info("Executing get team query. org=%s", org)
    url = f'{endpoint}/orgs/{org}/teams/{team_slug}'
    result = run_get(url, token, exist_check=exist_check)
    if result is not None:
        return result["id"]
    return None

def list_team_members(endpoint, org, token, teams):
    """list team members"""
    data = []
    for team in teams:
        team_slug = team[0] #slug of team
        logging.info("Executing list teams members query. org=%s, team=%s", org, team_slug)
        url = f'{endpoint}/orgs/{org}/teams/{team_slug}/members?per_page=100'
        result = run_get(url, token)
        for item in result:
            username = item["login"]
            url_user = f'{endpoint}/orgs/{org}/teams/{team_slug}/memberships/{username}'
            result_user = run_get(url_user, token)
            data.append([team_slug, username, result_user["role"]])
    return data

def list_org_members(endpoint, org, token):
    """list org members"""
    data = []
    logging.info("Executing list org members query. org=%s", org)
    url = f'{endpoint}/orgs/{org}/members?per_page=100'
    result = run_get(url, token)
    for item in result:
        username = item["login"]
        url_user = f'{endpoint}/orgs/{org}/memberships/{username}'
        result_user = run_get(url_user, token)
        data.append([username, result_user["role"]])
    return data

def get_team_member(url, token, exist_check=False):
    """get team member"""
    logging.info("Executing get team member query")
    result = run_get(url, token, exist_check=exist_check)
    if result is not None:
        return result["url"]
    return None

def get_org_member(url, token, exist_check=False):
    """get org member"""
    logging.info("Executing get org member query")
    result = run_get(url, token, exist_check=exist_check)
    if result is not None:
        return result["url"]
    return None

def create_teams(endpoint, org, token, teams):
    """create teams"""
    counter = 0
    for team in teams:
        name = team[1] # name
        description = team[2] # description
        privacy = team[3] # privacy
        parent_team = team[4] # parent
        team_id = get_team(endpoint, org, token, team[0], exist_check=True)
        if team_id is not None:
            logging.info("Skip creating team org=%s, team=%s", org, name)
            continue
        logging.info("Create team org=%s, team=%s", org, name)
        url = f'{endpoint}/orgs/{org}/teams'
        if len(parent_team) == 0:
            value = {'org' : org, 'name' : name, 'description' : description, 'privacy' : privacy}
        else:
            parent_team_id = get_team(endpoint, org, token, parent_team.lower().replace(' ', '_'))
            value = {'org' : org,
                     'name' : name,
                     'description' : description,
                     'privacy' : privacy,
                     'parent_team_id' : parent_team_id}
        result = run_post(url, value, token)
        if result is not None:
            counter += 1
            logging.info("Created team org=%s, team=%s", org, team[0])
    return counter

def create_team_members(endpoint, org, token, members):
    """create team members"""
    counter = 0
    for member in members:
        team_slug = member[0] # slug of team
        username = member[1] # username
        role = member[2] # role
        url = f'{endpoint}/orgs/{org}/teams/{team_slug}/memberships/{username}'
        if get_team_member(url, token, exist_check=True) is not None:
            logging.info("Skip creating members to org=%s, team=%s, member=%s",
                         org, team_slug, username)
            continue
        logging.info("Create members to org=%s, team=%s, member=%s, role=%s",
                     org, team_slug, username, role)
        value = {'role' : role}
        result = run_put(url, value, token)
        if result is not None:
            counter += 1
            logging.info("Created members to org=%s, team=%s, member=%s", org, team_slug, username)
    return counter

def create_org_members(endpoint, org, token, members):
    """create org members"""
    counter = 0
    for member in members:
        username = member[0] # username
        role = member[1] # role
        url = f'{endpoint}/orgs/{org}/memberships/{username}'
        if get_org_member(url, token, exist_check=True) is not None:
            logging.info("Skip creating members to org=%s, member=%s", org, username)
            continue
        logging.info("Create members to org=%s, member=%s, role=%s", org, username, role)
        value = {'role' : role}
        result = run_put(url, value, token)
        if result is not None:
            counter += 1
            logging.info("Created members to org=%s, member=%s", org, username)
    return counter

def run_get(url, token, throw_exception=False, exist_check=False):
    """run get (REST)"""
    try:
        headers = {"Authorization": f"bearer {token}"}
        request = requests.get(url,
          headers=headers)
        if exist_check and request.status_code == 404:
            return None
        request.raise_for_status()
        return request.json()
    except (requests.exceptions.ConnectionError,
      requests.exceptions.Timeout,
      requests.exceptions.HTTPError) as exception:
        logging.error("Request failed. %s", exception)
        logging.debug("Failed Url: %s", url)
        if throw_exception:
            raise SystemExit(exception) from exception
    return None

def run_post(url, value, token, throw_exception=False):
    """run post (REST)"""
    try:
        headers = {"Authorization": f"bearer {token}"}
        request = requests.post(url,
          json=value,
          headers=headers)
        request.raise_for_status()
        return request.json()
    except (requests.exceptions.ConnectionError,
      requests.exceptions.Timeout,
      requests.exceptions.HTTPError) as exception:
        logging.error("Request failed. %s", exception)
        logging.debug("Failed Url: %s, Value: %s", url, value)
        if throw_exception:
            raise SystemExit(exception) from exception
    return None

def run_put(url, value, token, throw_exception=False):
    """run post (REST)"""
    try:
        headers = {"Authorization": f"bearer {token}"}
        request = requests.put(url,
          json=value,
          headers=headers)
        request.raise_for_status()
        return request.json()
    except (requests.exceptions.ConnectionError,
      requests.exceptions.Timeout,
      requests.exceptions.HTTPError) as exception:
        logging.error("Request failed. %s", exception)
        logging.debug("Failed Url: %s, Value: %s", url, value)
        if throw_exception:
            raise SystemExit(exception) from exception
    return None
