# Jira CLI Kit

> A female rabbit is called a doe. A male rabbit is called a buck. A baby rabbit is called a kit.

This is a command-line tool to interact with Jira Cloud to create tickets and add comments to existing tickets.
It uses a configuration file (`~/.jira.cfg`) for default settings and allows command-line arguments to override these defaults.

## Setup

### Install

```bash
git clone git@gitlab.com:q-os/security.git
pip install ./security/projects/jiracli  # locally
pip install jiraclikit  # from PyPI
```

### 1. Create a Jira API Token

To interact with Jira Cloud, you need to generate an API token:

1. Go to [Jira API Token page](https://id.atlassian.com/manage-profile/security/api-tokens).
2. Log in with your Jira account.
3. Click on **Create API token**.
4. Name the token and click **Create**.
5. Copy the token and save it securely.

### 2. Set Environment Variables

Store the Jira API URL and token as environment variables for secure access:

```bash
export JC_JIRA_URL="https://yourdomain.atlassian.net"  # Replace with your Jira domain
export JC_JIRA_TOKEN="your_jira_api_token"  # Replace with the generated API token
```

### 3. Initial Run Configuration

When you run the tool for the first time, it will prompt you to enter:

- **Default Project ID**: The Jira project ID where tickets will be created.
- **Default Parent Task ID** (optional): A parent ticket ID if you often create subtasks under a specific epic or task.

These will be saved in the `~/.jira.cfg` file.

### Examples

#### Creating a Ticket

To create a new ticket in Jira:

```bash
python jira_cli.py -s "Ticket Title" -m "Detailed description of the ticket" -p "PROJECT_ID" -e "PARENT_TASK_ID" -t "tag1,tag2"
```

- This will create a ticket with the specified title, message, project, parent task, and tags.
- If `-p` or `-e` is not specified, the tool will fall back to the defaults in `~/.jira.cfg`, unless `-n` is used.

#### Adding a Comment to a Ticket

To add a comment to an existing ticket:

```bash
python jira_cli.py -c "TICKET_ID" -m "Your comment here"
```

- This will add the provided comment to the specified ticket.

#### Using "No Defaults" Mode

To ignore the `.jira.cfg` settings and use only the provided CLI arguments:

```bash
python jira_cli.py -s "New Ticket Without Defaults" -p "ANOTHER_PROJECT_ID" -n
```

## Configuration File (`~/.jira.cfg`)

The configuration file will look like this:

```ini
[DEFAULT]
project_id = YOUR_DEFAULT_PROJECT_ID
parent_task = YOUR_DEFAULT_PARENT_TASK_ID
```

The settings here are automatically created on the first run if they don't already exist.

---

### Notes

- **Environment Variables**: Ensure the `JIRA_URL` and `JIRA_API_TOKEN` are set before running the tool.
- **Command-line Override**: CLI arguments override the config file values.
- **Error Handling**: If any required parameter is missing, the script will raise an error and prompt for correction.

## Publish

```bash
python -m pip install --upgrade pip build twine
python -m build --sdist && python -m build --wheel
twine upload ./dist/* -u __token__ -p $PYPI_API_KEY
```
