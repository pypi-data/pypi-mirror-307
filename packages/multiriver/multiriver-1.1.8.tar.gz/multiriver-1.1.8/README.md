# Azure Blob Storage batch rivers creation CLI Tool

A command-line interface (CLI) tool to interact with Azure Blob Storage and manage rivers in Rivery. This tool allows you to configure Azure and Rivery credentials, generate river templates based on blob names, populate rivers, delete rivers, and list source configurations.

## Table of Contents

- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Configuration](#configuration)
  - [Configure Credentials](#configure-credentials)
  - [Configure Source](#configure-source)
- [Commands](#commands)
  - [populate\-rivers](#populate-rivers)
  - [delete\-rivers](#delete-rivers)
  - [list\-source\-configs](#list-source-configs)
- [Usage Examples](#usage-examples)
  - [Example Workflow](#example-workflow)
- [License](#license)
- [Contact](#contact)

## Prerequisites

- Python 3.6 or higher
- Azure Blob Storage account
- Rivery account and API token
- **Virtual Environment**: It is recommended to use a virtual environment to manage dependencies.

## Installation

1. **Create a Virtual Environment**

   It is recommended to create a virtual environment to isolate the dependencies.

   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

2. **Install the CLI Tool**

   Install the `multiriver` package using `pip`:

   ```bash
   pip install multiriver
   ```

   *(Ensure that the package ********************************************************`multiriver`******************************************************** is available in the Python Package Index or replace this command with the appropriate installation method if installing from a local source.)*

## Configuration

Before using the CLI tool, you need to configure your Azure and Rivery credentials, as well as source settings.

### Configure Credentials

Use the `configure_creds` command to set up your Azure Storage and Rivery API credentials.

```bash
multiriver configure-creds \
    --account-name YOUR_AZURE_ACCOUNT_NAME \
    --account-key YOUR_AZURE_ACCOUNT_KEY \
    --rivery-api-token YOUR_RIVERY_API_TOKEN
```

**Options:**

- `--account-name` (optional, but mandatory for the connection): Azure Storage account name.
- `--account-key` (optional, but mandatory for the connection): Azure Storage account key.
- `--connection-string` (optional): Azure Storage connection string.
- `--sas-token` (optional): Shared Access Signature (SAS) token.
- `--rivery-api-token` (optional, but mandatory for the connection): Rivery API token.
- `--rivery-host` (optional): Rivery host URL (default: `https://console.rivery.io`).

**Note:** You must provide at least one Azure credential and the Rivery API token.

### Configure Source

Use the `configure-source` command to set up source settings for Azure Blob Storage. This command will generate river templates based on the blobs in the specified container and store them together with the config under `~/.rivery/source_config`.

```bash
multiriver configure-source \
    --container-name YOUR_CONTAINER_NAME \
    --template-river-id TEMPLATE_RIVER_ID \
    --filename-template FILENAME_TEMPLATE \
    --group-id GROUP_ID \
    --cron-schedule CRON_SCHEDULE
```

**Options:**

- `--container-name` (optional): Name of the Azure Blob Storage container.
- it  (optional): ID of the base template river in Rivery.
- `--filename-template` (optional): Template used for generating river names.
- `--group-id` (required): ID of the group to attach the rivers to in Rivery.
- `--cron-schedule` (optional): Cron expression to schedule new rivers.

**Note:** You must provide the `--group-id` option. If `--filename-template` is provided, river templates will be generated based on the blob names.

## Commands

### populate-rivers

Populate rivers in Rivery based on the generated templates.

```bash
multiriver populate-rivers --group-id GROUP_ID
```

**Options:**

- `--group-id` (required): ID of the group to attach the rivers to in Rivery.

### delete-rivers

Delete all rivers associated with a specific group in Rivery.

```bash
multiriver delete-rivers --group-id GROUP_ID
```

**Options:**

- `--group-id` (required): ID of the group whose rivers will be deleted.

### list-source-configs

List all source configurations that have been set up.

```bash
multiriver list-source-configs
```

## Usage Examples

### Example Workflow

1. **Create a Virtual Environment**

   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

2. **Install the CLI Tool**

   ```bash
   pip install multiriver
   ```

3. **Configure Credentials**

   ```bash
   multiriver configure_creds \
       --account-name myazureaccount \
       --account-key myazurekey \
       --rivery-api-token myriverytoken
   ```

4. **Configure Source**

   ```bash
   multiriver configure-source \
       --container-name mycontainer \
       --template-river-id 62b075d34c86b10010ddf473 \
       --filename-template "{entity_name}_data.csv" \
       --group-id 6720e1592f775cb9fcdbf026 \
       --cron-schedule "0 0 * * *"
   ```

5. **Populate Rivers**

   ```bash
   multiriver populate-rivers --group-id 6720e1592f775cb9fcdbf026
   ```

   This command will:

   - Create new rivers in Rivery using the templates.
   - Generate mapping for every river.
   - Schedule the rivers if a cron schedule was provided.

6. **Delete Rivers**

   If you need to delete all rivers associated with the group:

   ```bash
   multiriver delete-rivers --group-id 6720e1592f775cb9fcdbf026
   ```

7. **List Source Configurations**

   To view all source configurations:

   ```bash
   multiriver list-source-configs
   ```

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Contact

For any questions or issues, please contact Rivery support.

