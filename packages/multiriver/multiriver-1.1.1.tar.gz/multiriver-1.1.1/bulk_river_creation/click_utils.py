# click_utils.py

import os
import json
import click

AUTH_FILE_PATH = os.path.expanduser('~/.rivery/auth')
SOURCE_FILE_PATH = os.path.expanduser('~/.rivery/source')

def save_credentials(account_name=None, account_key=None, connection_string=None, sas_token=None, rivery_api_token=None, rivery_host=None):
    # Load existing credentials
    if os.path.exists(AUTH_FILE_PATH):
        with open(AUTH_FILE_PATH, 'r') as f:
            creds = json.load(f)
    else:
        creds = {}

    # Update only the provided arguments
    if account_name is not None:
        creds['account_name'] = account_name
    if account_key is not None:
        creds['account_key'] = account_key
    if connection_string is not None:
        creds['connection_string'] = connection_string
    if sas_token is not None:
        creds['sas_token'] = sas_token
    if rivery_api_token is not None:
        creds['rivery_api_token'] = rivery_api_token
    if rivery_host is not None:
        creds['rivery_host'] = rivery_host

    # Ensure the directory exists
    os.makedirs(os.path.dirname(AUTH_FILE_PATH), exist_ok=True)
    with open(AUTH_FILE_PATH, 'w') as f:
        json.dump(creds, f)

    # Log saved arguments
    saved_args = [key for key, value in {
        'account_name': account_name,
        'account_key': account_key,
        'connection_string': connection_string,
        'sas_token': sas_token,
        'rivery_api_token': rivery_api_token,
        'rivery_host': rivery_host,
    }.items() if value is not None]
    if saved_args:
        click.echo(f"Credentials saved successfully for: {', '.join(saved_args)}.")
    else:
        click.echo("No credentials were provided to save.")

    click.echo(f"Credentials are saved in {AUTH_FILE_PATH}. They will be used in future commands unless reconfigured.")


def load_credentials():
    if os.path.exists(AUTH_FILE_PATH):
        with open(AUTH_FILE_PATH, 'r') as f:
            creds = json.load(f)
        return creds
    else:
        return {}

def save_source_configuration(group_id: str, container_name=None, prefix=None, template_river_id=None,
                              filename_template=None, generated_templates=None, cron_schedule=None):
    # Load existing source configuration
    if os.path.exists(SOURCE_FILE_PATH):
        with open(SOURCE_FILE_PATH, 'r') as f:
            all_groups_source_config = json.load(f)
    else:
        all_groups_source_config = {}

    source_config = all_groups_source_config.get(group_id) or {}

    # Update only the provided arguments
    if container_name is not None:
        source_config['container_name'] = container_name
    if prefix is not None:
        source_config['prefix'] = prefix
    if template_river_id is not None:
        source_config['template_river_id'] = template_river_id
    if filename_template is not None:
        source_config['filename_template'] = filename_template
    if generated_templates is not None:
        source_config['generated_templates'] = generated_templates
    if cron_schedule is not None:
        source_config['cron_schedule'] = cron_schedule

    all_groups_source_config[group_id] = source_config
    # Ensure the directory exists
    os.makedirs(os.path.dirname(SOURCE_FILE_PATH), exist_ok=True)
    with open(SOURCE_FILE_PATH, 'w') as f:
        json.dump(obj=all_groups_source_config, fp=f)

    # Log saved arguments
    saved_args = [key for key, value in {
        'container_name': container_name,
        'prefix': prefix,
        'template_river_id': template_river_id,
        'filename_template': filename_template,
        'generated_templates': generated_templates,
        'cron_schedule': cron_schedule
    }.items() if value is not None and key != 'generated_templates']

    if saved_args:
        click.echo(f"Group {group_id} source configuration: {group_id} saved successfully for: {', '.join(saved_args)}."
                   f" Location: {SOURCE_FILE_PATH}.")
        click.echo(f"It will be used in future commands unless reconfigured.")
    else:
        click.echo("No source configuration parameters were provided to save.")


def load_source_configuration(group_id: str=None):
    if os.path.exists(SOURCE_FILE_PATH):
        with open(SOURCE_FILE_PATH, 'r') as f:
            all_groups_source_config = json.load(f)
            if not group_id:
                return all_groups_source_config
            source_config = all_groups_source_config.get(group_id)
        return source_config
    else:
        return {}
