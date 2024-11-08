# azure_blob_session.py

from azure.storage.blob import BlobServiceClient
from azure.identity import DefaultAzureCredential
import click
from .click_utils import load_credentials

def get_blob_service_client(account_name=None):
    """
    Authenticate and return a BlobServiceClient instance.
    """
    # Load credentials
    creds = load_credentials()
    stored_account_name = creds.get('account_name')
    account_key = creds.get('account_key')
    connection_string = creds.get('connection_string')
    sas_token = creds.get('sas_token')

    # Use provided account_name if given, else use stored account_name
    account_name = account_name or stored_account_name

    if not account_name and not connection_string:
        click.echo("Error: Account name is not configured. Please run 'configure_creds' command.")
        return None

    if connection_string:
        # Authenticate using the connection string
        blob_service_client = BlobServiceClient.from_connection_string(connection_string)
    elif account_name and sas_token:
        # Authenticate using the account name and SAS token
        blob_service_client = BlobServiceClient(
            account_url=f"https://{account_name}.blob.core.windows.net",
            credential=sas_token
        )
    elif account_name and account_key:
        # Authenticate using the account name and account key
        blob_service_client = BlobServiceClient(
            account_url=f"https://{account_name}.blob.core.windows.net",
            credential=account_key
        )
    elif account_name:
        # Authenticate using DefaultAzureCredential
        credential = DefaultAzureCredential()
        blob_service_client = BlobServiceClient(
            account_url=f"https://{account_name}.blob.core.windows.net",
            credential=credential
        )
    else:
        click.echo("Error: No valid credentials provided or found in ~/.rivery/auth")
        return None

    return blob_service_client

def list_blobs_in_container(blob_service_client, container_name, prefix=None):
    """
    List blobs in the specified container, optionally filtering by prefix.
    """
    try:
        # Get the container client
        container_client = blob_service_client.get_container_client(container_name)
        # List blobs in the container with optional prefix
        blobs = container_client.list_blobs(name_starts_with=prefix)
        blob_names = [blob.name for blob in blobs]
        return blob_names
    except Exception as e:
        click.echo(f"Error: {str(e)}")
        return None
