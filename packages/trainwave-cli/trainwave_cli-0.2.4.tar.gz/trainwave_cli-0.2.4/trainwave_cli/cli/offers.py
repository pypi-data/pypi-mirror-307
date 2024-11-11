import typer
from beaupy import select
from rich.console import Console

from trainwave_cli.api import Api
from trainwave_cli.config.config import config
from trainwave_cli.utils import async_command, ensure_api_key

app = typer.Typer()


HARDWARE_OPTIONS = [
    "GPU",
    "CPU",
]
CURSOR = "➡️"


@app.command()
@async_command
@ensure_api_key
async def list():
    api_client = Api(config.api_key, config.endpoint)
    _offers = await api_client.offers()

    console = Console()
    console.print("Select Hardware")
    hw = select(HARDWARE_OPTIONS, cursor=CURSOR)

    if hw == "GPU":
        pass
    else:
        pass
