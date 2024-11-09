#!/bin/homebrew/anaconda3/bin/python
import argparse
import base64
import configparser
import os
import sys
from typing import Optional

import dotenv
import requests

dotenv.load_dotenv()

# Define config file path and environment variables
CONFIG_FILE_PATH = os.path.expanduser("~/.jira.cfg")
JIRA_URL = os.environ["JC_JIRA_URL"]
JIRA_EMAIL = os.environ["JC_JIRA_EMAIL"]
JIRA_API_TOKEN = os.environ["JC_JIRA_TOKEN"]


# Function to read or create default settings
def load_config():
    config = configparser.ConfigParser()
    if os.path.exists(CONFIG_FILE_PATH):
        config.read(CONFIG_FILE_PATH)
    else:
        # Prompt user for default settings if config file doesn't exist
        config["DEFAULT"] = {
            "project_key": input("Enter default project key: "),
            "parent_task_key": input("Enter default parent task key (optional): "),
        }
        with open(CONFIG_FILE_PATH, "w") as configfile:
            config.write(configfile)
    return config


# Function to create a Jira ticket
def create_ticket(
    title: str,
    message: Optional[str],
    project_key: str,
    parent_task_key: Optional[str] = None,
    tags: Optional[str] = None,
    no_defaults: bool = False,
    self_assign: bool = False,
):
    config = load_config() if not no_defaults else None
    if config:
        if p_key := config["DEFAULT"].get("project_key"):
            project_key = p_key
        if p_task_key := config["DEFAULT"].get("parent_task_key"):
            parent_task_key = p_task_key

    if tags is None:
        split_tags = []
    elif "," in tags:
        split_tags = tags.split(",")
    elif isinstance(tags, str) and len(tags) > 0:
        split_tags = [tags]
    else:
        raise ValueError(f"Unsupported tags format: {tags!r}.")

    split_tags: list[str] = tags.split(",") if tags else []

    if not project_key:
        raise ValueError("Project key is required.")

    # Prepare Basic Auth header
    auth_string = f"{JIRA_EMAIL}:{JIRA_API_TOKEN}"
    auth_encoded = base64.b64encode(auth_string.encode()).decode()
    headers = {
        "Authorization": f"Basic {auth_encoded}",
        "Content-Type": "application/json",
    }

    # Convert the plain text message to Atlassian Document Format
    if not message:
        message = ""
    description_content = {
        "type": "doc",
        "version": 1,
        "content": [
            {"type": "paragraph", "content": [{"type": "text", "text": message}]}
        ],
    }

    payload = {
        "fields": {
            "project": {"key": project_key},
            "summary": title,
            "description": description_content,
            "issuetype": {"name": "Task"},
            "labels": split_tags,
        }
    }
    if self_assign:
        response = requests.get(f"{JIRA_URL}/rest/api/3/myself", headers=headers)
        my_jira_user_id = response.json()["accountId"]
        payload["fields"]["assignee"] = {"id": my_jira_user_id}
    if parent_task_key:
        payload["fields"]["parent"] = {"key": parent_task_key}

    response = requests.post(
        f"{JIRA_URL}/rest/api/3/issue", json=payload, headers=headers
    )
    if response.status_code == 201:
        ticket_key = response.json()["key"]
        print(f"Ticket created successfully: {ticket_key}")
        print(f"Link to ticket: {JIRA_URL}/browse/{ticket_key}")
    else:
        print(f"Failed to create ticket: {response.status_code} - {response.text}")


# Function to add a comment to an existing ticket by task key
def add_comment(task_key, comment):
    # Prepare Basic Auth header
    auth_string = f"{JIRA_EMAIL}:{JIRA_API_TOKEN}"
    auth_encoded = base64.b64encode(auth_string.encode()).decode()
    headers = {
        "Authorization": f"Basic {auth_encoded}",
        "Content-Type": "application/json",
    }
    payload = {"body": comment}

    response = requests.post(
        f"{JIRA_URL}/rest/api/3/issue/{task_key}/comment", json=payload, headers=headers
    )
    if response.status_code == 201:
        print(f"Comment added successfully to task {task_key}.")
    else:
        print(
            f"Failed to add comment to task {task_key}: {response.status_code} - {response.text}"
        )


# Main function to handle CLI arguments
def main():
    parser = argparse.ArgumentParser(description="CLI tool for creating Jira tickets")
    parser.add_argument("-s", "--summary", help="Title of the ticket")
    parser.add_argument("-m", "--message", help="Content/message of the ticket")
    parser.add_argument(
        "-c", "--comment", help="Add comment to a specific ticket by task key"
    )
    parser.add_argument("-e", "--epic", help="Parent task key for the new ticket")
    parser.add_argument("-p", "--project", help="Project key to create the ticket in")
    parser.add_argument("-t", "--tags", help="Comma-separated list of tags to apply")
    parser.add_argument(
        "-n",
        "--no-defaults",
        action="store_true",
        help="Ignore default config settings",
    )
    parser.add_argument(
        "-sa",
        "--self-assign",
        action="store_true",
        help="Assign the ticket to yourself",
    )
    args = parser.parse_args()

    # Check if no arguments were provided
    if len(sys.argv) == 1:
        parser.print_help()
        sys.exit(1)

    if args.comment:
        if not args.summary:
            print("Task key is required to add a comment")
        else:
            add_comment(args.summary, args.comment)
    else:
        create_ticket(
            args.summary,
            args.message,
            args.project,
            args.epic,
            args.tags,
            args.no_defaults,
            self_assign=args.self_assign,
        )


if __name__ == "__main__":
    main()
