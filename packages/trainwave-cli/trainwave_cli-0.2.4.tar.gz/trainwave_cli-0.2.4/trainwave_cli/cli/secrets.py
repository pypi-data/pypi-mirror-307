import builtins
from datetime import datetime, timezone
from operator import itemgetter
from typing import Annotated, Optional

import human_readable
import typer
from dateutil import parser
from tabulate import tabulate
from typer_config.decorators import use_toml_config

from trainwave_cli.api import Api, Secret
from trainwave_cli.config.config import config
from trainwave_cli.utils import async_command, ensure_api_key

app = typer.Typer()


@app.command()
@async_command
@use_toml_config(default_value="trainwave.toml")
@ensure_api_key
async def list(
    organization: Annotated[str, typer.Option(help="The organization ID or RID")],
) -> None:
    api_client = Api(config.api_key, config.endpoint)
    secrets = await api_client.list_secrets(organization)

    project_scoped = [secret for secret in secrets if secret.project]
    org_scoped = [secret for secret in secrets if not secret.project]
    unique: dict[str, tuple[bool, Secret]] = {}

    for org_secret in org_scoped:
        unique[org_secret.name] = (False, org_secret)

    for project_secret in project_scoped:
        if project_secret.name in unique:
            unique[project_secret.name] = (True, project_secret)
        else:
            unique[project_secret.name] = (False, project_secret)

    sorted_secrets = dict(sorted(unique.items(), key=itemgetter(0)))

    headers = ["ID", "NAME", "SCOPE", "DIGEST", "CREATED"]
    table = [
        [
            secret.rid,
            secret.name if not overridden else f"{secret.name} (*)",
            "PROJECT" if secret.project else "ORG",
            secret.digest[:16],
            human_readable.date_time(
                datetime.now(timezone.utc) - parser.parse(secret.created_at)
            ),
        ]
        for (overridden, secret) in sorted_secrets.values()
    ]
    typer.echo(tabulate(table, headers=headers, tablefmt="simple"))


@app.command()
@async_command
@use_toml_config(default_value="trainwave.toml")
@ensure_api_key
async def set(
    organization: Annotated[str, typer.Option(help="The organization ID or RID")],
    secrets: builtins.list[str],
    project: Annotated[Optional[str], typer.Option(help="Project ID or RID")] = None,
) -> None:
    secret_dict: dict[str, str] = {}

    for secret in secrets:
        _KV_PARTS = 2
        splitted = secret.split("=")

        # Validate format
        if len(splitted) != _KV_PARTS:
            typer.echo(
                f"Error: Invalid format '{secret}'. Expected format is KEY=VALUE.",
                err=True,
            )
            raise typer.Exit(code=1)

        secret_name, secret_value = splitted
        secret_dict[secret_name] = secret_value

    # Now call API and insert
    api_client = Api(config.api_key, config.endpoint)
    await api_client.set_secrets(organization, secret_dict, project)


@app.command()
@async_command
@use_toml_config(default_value="trainwave.toml")
@ensure_api_key
async def unset(
    organization: Annotated[str, typer.Option(help="The organization ID or RID")],
    secret_names: builtins.list[str],
) -> None:
    api_client = Api(config.api_key, config.endpoint)

    existing_secrets = await api_client.list_secrets(organization)
    lookup = {
        secret.name: secret.id for secret in existing_secrets
    }

    secret_ids: builtins.list[str] = []
    while secret_names:
        current = secret_names.pop()
        if current not in lookup:
            typer.echo(f"Error: Secret '{current}' not found.", err=True)
            raise typer.Exit(code=1)

        secret_ids.append(lookup[current])

    await api_client.unset_secrets(organization, secret_ids)
