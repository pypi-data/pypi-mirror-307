import time
import webbrowser
from typing import Annotated, Optional

import typer
from loguru import logger
from rich.progress import Progress, SpinnerColumn, TextColumn

from trainwave_cli.api import Api, CLIAuthStatus
from trainwave_cli.config.config import config, config_manager
from trainwave_cli.utils import async_command, ensure_api_key

app = typer.Typer()

_BOLD = "\033[1m"
_RESET = "\033[0;0m"

LOGIN_POLLING_TIME: Annotated[int, "minutes"] = 5
LOGIN_POLLING_SLEEP_TIME: Annotated[int, "seconds"] = 5


@app.command()
@async_command
async def login() -> None:
    """
    Login to Trainwave.

    This will open a browser window for you to authenticate.
    """
    api_client = Api(None, config.endpoint)
    session_url, session_token = await api_client.create_cli_auth_session()

    typer.echo("Opening your browser to complete the login.\n")
    typer.echo(f"{_BOLD}URL:{_RESET} {session_url} \n")

    webbrowser.open_new_tab(session_url)

    api_token: Optional[str] = None
    end_polling_at = time.time() + 60 * LOGIN_POLLING_TIME

    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        transient=True,
    ) as progress:
        progress.add_task(description="Awaiting login...", total=None)

        while time.time() < end_polling_at:
            status, api_token = await api_client.check_cli_auth_session_status(
                session_token
            )
            if status == CLIAuthStatus.SUCCESS:
                break

            time.sleep(LOGIN_POLLING_SLEEP_TIME)

        if api_token:
            # Test the token
            api = Api(api_token, config.endpoint)
            user = await api.get_myself()

            typer.echo("\n")
            typer.echo("✅ Success!\n")
            typer.echo(f"Logged in as: {_BOLD}{user.email}{_RESET}")

            config.api_key = api_token
            config_manager.save()
        else:
            typer.echo("❌ Something went wrong. Try again.")


@app.command()
@async_command
@ensure_api_key
async def logout() -> None:
    """
    Logout from Trainwave.

    This will remove the API key from the configuration.
    """
    config_manager.delete()
    logger.info("Logged out")


@app.command()
@async_command
@ensure_api_key
async def whoami() -> None:
    """Get the current user's information."""
    api = Api(config.api_key, config.endpoint)
    res = await api.get_myself()
    typer.echo(res.email)


@app.command()
@async_command
async def set_token(api_key: str):
    """Manually set the API key for Trainwave."""
    api = Api(api_key, config.endpoint)
    logger.info("Checking API key...")
    if await api.check_api_key():
        logger.info("API key is valid!")
        config.api_key = api_key
        config_manager.save()
        logger.info("Done!")
    else:
        logger.error("API key is invalid")


@app.command()
@async_command
@ensure_api_key
async def token() -> None:
    """Print the current API key."""
    typer.echo(config.api_key)


@app.command()
@async_command
async def set_endpoint(endpoint: str) -> None:
    """Set the endpoint for Trainwave."""
    config.endpoint = endpoint
    config_manager.save()
