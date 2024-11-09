# azure_cli.py

import click
from .azure_blob_session import (
    get_blob_service_client,
    list_blobs_in_container
)
from .utils import process_data, liberal_format
from .click_utils import (
    save_credentials,
    save_source_configuration
)

from .rivery_session import RiverySession
from .click_utils import load_credentials, load_source_configuration
from copy import deepcopy
from . import utils  # Assuming utils.py contains generate_rivers_template
from rich.table import Table
from rich.live import Live

RETRY_MAPPING_MAX = 3

DONE_STATUS = "Done"

SAVING_THE_RIVER_STATUS = "Saving the river..."

GENERATING_MAPPING_STATUS = "Generating mapping..."

RETRYING_MAPPING_STATUS = "Retrying to generate mapping..."

MAPPING_ERRORS_STATUS = "Mapping failed with error: {errors}"


@click.group()
def cli():
    """CLI tool to interact with Azure Blob Storage."""
    pass

@cli.command()
@click.option('--account-name', required=False, help='Azure Storage account name')
@click.option('--account-key', required=False, help='Azure Storage account key')
@click.option('--connection-string', required=False, help='Azure Storage connection string')
@click.option('--sas-token', required=False, help='Shared Access Signature (SAS) token')
@click.option('--rivery-api-token', required=False, help='Rivery API token')
@click.option('--rivery-host', required=False, help='Rivery host to use. The default value is: https://console.rivery.io',
              default='https://console.rivery.io')
def configure_creds(account_name, account_key, connection_string, sas_token, rivery_api_token, rivery_host):
    """
    Configure and store Azure Storage and Rivery API credentials.
    """
    if not any([account_name, account_key, connection_string, sas_token, rivery_api_token, rivery_host]):
        click.echo("Error: Please provide at least one credential option to configure.")
        return

    save_credentials(account_name, account_key, connection_string, sas_token, rivery_api_token, rivery_host)

@cli.command()
@click.option('--container-name', required=False, help='Container name') # todo can be taken from the template river
@click.option('--prefix', required=False, help='Prefix to filter blobs')
@click.option('--template-river-id', required=False, help='The base template river to populate rivers')
@click.option('--filename-template', required=False, help='The template used in populated river')
@click.option('--group-id', required=True, help='The id of the group to attach the rivers to')
@click.option('--cron-schedule', required=False, help='The cron config to schedule new river')
def configure_source(container_name, prefix, template_river_id, filename_template, group_id, cron_schedule):
    """
    Configure and store source settings for Azure Blob Storage.
    If 'filename-template' is provided, generate river templates based on the blob names.
    """

    if not any([container_name, prefix, template_river_id, filename_template, cron_schedule]):
        click.echo("Please provide at least one config with the group.")

    source_config = {
        'container_name': container_name,
        'prefix': prefix,
        'template_river_id': template_river_id,
        'filename_template': filename_template,
        'group_id': group_id,
        'cron_schedule': cron_schedule,
    }
    save_source_configuration(**source_config)

    # If filename_template is provided, generate river templates
    if filename_template:
        # Get the BlobServiceClient
        blob_service_client = get_blob_service_client()
        if not blob_service_client:
            return

        # List blobs with the specified prefix
        source_config = load_source_configuration(group_id)
        blob_names = list_blobs_in_container(
            blob_service_client,
            source_config.get('container_name'),
            source_config.get('prefix')
        )
        if not blob_names:
            click.echo("No blobs found to generate river templates.")
            return

        # Generate river templates using utils.generate_rivers_template
        generated_templates = utils.generate_rivers_template(filename_template, blob_names)

        # Log the first 10 generated templates
        click.echo("\nGenerated River Templates (showing up to 10):")
        for i, template in enumerate(generated_templates[:10], start=1):
            click.echo(f"{i}. {template}")

        total_templates = len(generated_templates)
        if total_templates > 10:
            click.echo(f"...and {total_templates - 10} more templates.")
        click.echo(f"\nTotal number of templates generated: {total_templates}")
        save_source_configuration(**{'generated_templates': generated_templates, 'group_id': group_id})

    # Save the source configuration (including generated templates if any)

def generate_table(group_id, table_data):
    table = Table(title=f"Generating Rivers for Group ID: {group_id}")
    table.add_column("River Name", style="cyan", no_wrap=True)
    table.add_column("Target Table Name", style="green")
    table.add_column("Status", style="magenta")
    table.add_column("River URL", style="green")

    for row in table_data:
        table.add_row(row["new_river_name"], row["target_table_name"], row["status"], row["river_url"])

    return table

@cli.command()
@click.option('--group-id', required=True, help='The id of the group to attach the rivers to')
def populate_rivers(group_id):
    creds = load_credentials()
    source_config = load_source_configuration(group_id)
    if not source_config:
        click.echo(f"The source is not configured for the provided group id: {group_id}.")
        return

    rivery_token = creds.get('rivery_api_token')
    template_river_id = source_config.get('template_river_id')
    generated_templates = source_config.get('generated_templates')
    cron_schedule = source_config.get('cron_schedule')
    rivery_host = source_config.get('rivery_host')

    if not rivery_token:
        click.echo("Error: Rivery API token is missing. Please configure the credentials.")
        return

    if not template_river_id:
        click.echo("Error: Template river ID is missing. Please configure the source settings.")
        return

    if not generated_templates:
        click.echo("Error: No generated templates found. Please configure the source settings.")
        return

    if not cron_schedule:
        click.echo("Cron schedule is missing. Rivers will be created but not scheduled.")

    rivery_session = RiverySession(token=rivery_token, host=rivery_host)
    template_river = rivery_session.get_river(
        **{"river_id": template_river_id}
    )
    template_river = process_data(
        template_river,
        convert_to_oi=['connection_id', 'fz_connection', 'env_id'],
        to_delete=['river_date_updated', 'version_id', 'river_date_inserted', 'cross_id'],
        to_date=['start_date'],
    )

    table_data = []
    new_river_objects = _generate_new_rivers_objects(generated_templates, group_id,
                                                     table_data, template_river, cron_schedule)

    generate_mapping_number = len(table_data)

    with Live(generate_table(group_id, table_data), refresh_per_second=4) as live:
        initiate_mapping_objects = {}
        river_title_id_map = {}

        for table_row in table_data:
            current_river_name = table_row["new_river_name"]

            saved_river_data = rivery_session.save_river(data=new_river_objects[current_river_name])
            river_id = str(saved_river_data.get('_id'))
            new_river_objects[current_river_name] = saved_river_data

            table_row['river_url'] = '/'.join(
                [rivery_session.host, 'river', str(saved_river_data['river_definitions']['account']),
                 str(saved_river_data['river_definitions']['env_id']), 'river', river_id]
            ) + '/'

            river_title_id_map[current_river_name] = river_id

            table_row["status"] = GENERATING_MAPPING_STATUS
            live.update(generate_table(group_id, table_data))

            initiate_mapping_objects[current_river_name] = rivery_session.generate_mapping(
                river_id=river_id, data=saved_river_data
            )

        retry_count_per_river = {}
        while generate_mapping_number:
            for table_row in table_data:
                if table_row['status'] in (GENERATING_MAPPING_STATUS, RETRYING_MAPPING_STATUS):
                    current_river_name = table_row["new_river_name"]
                    mapping, errors = rivery_session.pull_river_mapping(
                        mapping_data=initiate_mapping_objects[current_river_name]
                    )
                    if errors and retry_count_per_river.get(current_river_name, 0) < RETRY_MAPPING_MAX:
                        # error happened for the first time, doing a retry
                        initiate_mapping_objects[current_river_name] = rivery_session.generate_mapping(
                            river_id=river_id, data=new_river_objects[current_river_name]
                        )
                        retry_count_per_river[current_river_name] = retry_count_per_river.get(current_river_name, 0) + 1
                        table_row["status"] = RETRYING_MAPPING_STATUS
                    elif errors:
                        table_row["status"] = MAPPING_ERRORS_STATUS.format(errors=errors)
                        generate_mapping_number -= 1
                    elif mapping:
                        table_row["status"] = SAVING_THE_RIVER_STATUS
                        _save_river_with_mapping(mapping, new_river_objects[current_river_name],
                                                 river_title_id_map, rivery_session, table_row)
                        table_row["status"] = DONE_STATUS
                        generate_mapping_number -= 1

                live.update(generate_table(group_id, table_data))

@cli.command()
@click.option('--group-id', required=True, help='The id of the group to attach the rivers to')
def delete_rivers(group_id):
    creds = load_credentials()
    source_config = load_source_configuration(group_id)
    if not source_config:
        click.echo(f"The source is not configured for the provided group id: {group_id}.")
        return

    rivery_token = creds.get('rivery_api_token')
    rivery_host = source_config.get('rivery_host')
    rivery_session = RiverySession(token=rivery_token, host=rivery_host)

    rivers_list = rivery_session.list_rivers(group_id=group_id)

    with click.progressbar(range(len(rivers_list)), label=f'Deleting rivers for the group {group_id}') as bar:
        for i in bar:
            rivery_session.delete_river(data={"_id": rivers_list[i].get('_id')})

    click.echo(f"Deleted all rivers for group id: {group_id}.")

def _save_river_with_mapping(mapping, new_river_data, river_title_id_map, rivery_session, table_row):
    new_river_data['tasks_definitions'][1]['task_config']["file_columns"] = mapping['target']
    new_river_data['tasks_definitions'][1]['task_config']["source_mapping"] = mapping['source']
    payload = {
        "river_definitions": new_river_data.get("river_definitions"),
        "tasks_definitions": new_river_data.get("tasks_definitions"),
        "cross_id": {"$oid": river_title_id_map[table_row["new_river_name"]]},
        "_id": {"$oid": river_title_id_map[table_row["new_river_name"]]}
    }
    rivery_session.save_river(
        river_id=river_title_id_map[table_row["new_river_name"]],
        data=payload
    )


def _generate_new_rivers_objects(generated_templates, group_id, table_data, template_river, cron_schedule=None):
    new_river_objects = {}

    template_target_table = template_river['tasks_definitions'][1]['task_config']['target_table']
    for i, gen_template in enumerate(generated_templates):
        new_river_name = f'new river {i} - {gen_template["template"]}'
        new_river_target_table = liberal_format(template_target_table, entity_name=gen_template["entity_name"])
        new_river_structure = process_data(
            deepcopy(template_river),
            to_replace={
                'group_id': {"_id": {"$oid":group_id}},
                'file_pattern': gen_template['template'],
                'river_name': new_river_name,
                'target_table': new_river_target_table
            }
        )
        new_river_structure['tasks_definitions'][0]['schedule']["isEnabled"] = True if cron_schedule else False
        new_river_structure['tasks_definitions'][0]['schedule']["isEnabled"] = True if cron_schedule else False
        new_river_structure['tasks_definitions'][0]['task_config']["temp_folder_to_run"] = gen_template['template']
        new_river_objects[new_river_name] = {

            'river_definitions': new_river_structure.get('river_definitions'),
            'tasks_definitions': new_river_structure.get('tasks_definitions')

        }
        table_data.append({
            "new_river_name": new_river_name,
            "target_table_name":new_river_target_table,
            "status": "Creating river...",
            "river_url": "N/A"
        })
    return new_river_objects


@cli.command()
def list_source_configs():
    """
    List all source configurations.
    """
    source_configs = load_source_configuration()
    if not source_configs:
        click.echo("No source configurations found.")
        return

    click.echo("\nSource Configurations:")
    for group_id, source_config in source_configs.items():
        click.echo(f"Group ID: {group_id}")
        for key, value in source_config.items():
            click.echo(f"  {key}: {value}")
        click.echo()



def main():
    # populate_rivers("672b8cbceffd72c69d342d18")
    cli()

if __name__ == '__main__':
    main()