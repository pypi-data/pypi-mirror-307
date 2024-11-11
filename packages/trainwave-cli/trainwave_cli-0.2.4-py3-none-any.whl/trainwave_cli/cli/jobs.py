
from typing import Optional

import json
import os
import sys
import traceback
from dataclasses import asdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Annotated
from urllib.parse import urlparse

import human_readable
import pytimeparse
import typer
import websockets
from dateutil import parser
from loguru import logger
from tabulate import tabulate
from typer_config.decorators import use_toml_config

from trainwave_cli.api import Api
from trainwave_cli.config.config import config
from trainwave_cli.format_utils import cents_to_dollars_str
from trainwave_cli.io import create_tarball
from trainwave_cli.utils import async_command, ensure_api_key, truncate_string

app = typer.Typer()


@app.command()
@async_command
@use_toml_config(default_value="trainwave.toml")
@ensure_api_key
async def launch(  # noqa
    # Basic job parameters
    name: Annotated[str, typer.Option(help="The name of the job")],
    project: Annotated[str, typer.Option(help="The project ID or RID")],
    setup_command: Annotated[
        str, typer.Option(help="The command to run before the job")
    ],
    run_command: Annotated[str, typer.Option(help="The command to run the job")],
    # Optional params
    organization: Annotated[
        Optional[str], typer.Option(help="ID or RID of organization")
    ] = None,
    expires: Annotated[
        str,
        typer.Option(
            help="Time til' the job will be automatically terminated. Example `1d`, `2h`` etc."
        ),
    ] = "",
    env_vars={},  # dict[str, str]  not supported by typer yet
    exclude_gitignore: Annotated[
        bool,
        typer.Option(
            help="If set the gitignore file will be used to ignore files when packaging the job"
        ),
    ] = True,
    exclude_regex: Annotated[
        Optional[str],
        typer.Option(
            help="Files matching this pattern will be ignored when packaging up the job"
        ),
    ] = None,
    # Harware parameters
    image: Annotated[
        str, typer.Option(help="The docker image to use as base for the job")
    ] = "",
    hdd_size_mb: Annotated[int, typer.Option(help="Hard drive size in MB")] = 20,
    memory_mb: Annotated[int, typer.Option(help="Memory in MB")] = 0,
    cpus: Annotated[int, typer.Option(help="Number of CPUs")] = 0,
    gpus: Annotated[
        int, typer.Option(help="Number of GPUs to allocate of the `gpu_type`")
    ] = 0,
    gpu_type: Annotated[
        str, typer.Option(help="Canonical name of the GPU to use")
    ] = "",
    compliance_soc2: Annotated[
        bool | None, typer.Option(help="Only use SOC2 compliant machines")
    ] = None,
) -> None:
    """Launch a job on Trainwave using the current configuration."""
    api_client = Api(config.api_key, config.endpoint, project)
    # Interpolate environe variables
    env_vars = eval(env_vars)
    for k, v in env_vars.items():
        if v.startswith("${"):
            interpolated = os.getenv(v[2:-1])
            if interpolated is None:
                logger.warning(f"Environment variable {v} not found")
            else:
                env_vars[k] = interpolated

    conf = {
        "name": name,
        "image": image,
        "setup_command": setup_command,
        "run_command": run_command,
        "hdd_size_mb": hdd_size_mb,
        "memory_mb": memory_mb,
        "cpus": cpus,
        "gpus": gpus,
        "gpu_type": gpu_type,
        "env_vars": env_vars,
    }
    if compliance_soc2 is not None:
        conf["compliance_soc2"] = compliance_soc2

    if conf["gpu_type"] != "" and conf["gpus"] == 0:
        conf["gpus"] = 1  # default to 1 gpu if gpu_type is set

    if expires != "":
        expires_time = pytimeparse.parse(expires)
        if expires_time is None:
            logger.warning(f"Expires cannot be used, defaulting to nothing")
        else:
            expires_at = int(datetime.now(timezone.utc).timestamp()) + int(expires_time)
            conf["expires_at"] = expires_at

    def render(k, v) -> str:
        match k:
            case "env_vars":
                return ",".join(v.keys())
            case "expires_at":
                return datetime.fromtimestamp(v).strftime("%Y-%m-%d %H:%M:%S")
            case _:
                return truncate_string(str(conf[k]), 50)

    tab_keys = list(conf.keys())
    tab_values = {
        "name": tab_keys,
        "value": [render(k, conf[k]) for k in tab_keys],
    }
    typer.echo(tabulate(tab_values, headers="keys"))
    typer.echo("\n")

    tarball = None
    try:
        job = await api_client.create_job(conf)
        tarball = create_tarball(Path().cwd(), exclude_gitignore, exclude_regex)
        await api_client.upload_code(Path(tarball.name), job.upload_url)
        await api_client.code_submission(job)

        co = asdict(job.cloud_offer)
        tab_keys = list(co.keys())
        tab_values = {
            "name": tab_keys,
            "value": [truncate_string(str(co[k]), 50) for k in tab_keys],
        }
        typer.echo("\nMatched machine\n" + tabulate(tab_values, headers="keys") + "\n")
        typer.echo(f"Cost per hour for this job: ${job.cost_per_hour:.2f}")
        typer.echo(f"Job created: {job.rid} ({job.id}) -> {job.url}")
    except Exception as e:
        traceback.print_exc()
        logger.error(f"An error occurred: {e}")
    finally:
        if tarball:
            tarball.close()


@app.command(name="list")
@async_command
@use_toml_config(default_value="trainwave.toml")
@ensure_api_key
async def list_jobs(
    organization: Annotated[str, typer.Option(help="Organization ID or RID")],
    project: Annotated[str, typer.Option(help="Project ID or RID")] = "",
) -> None:
    """List all jobs in the current project."""
    api_client = Api(
        config.api_key, config.endpoint, project=project, organization=organization
    )
    jobs = await api_client.list_jobs()

    headers = ["ID", "NAME", "STATUS", "CREATED", "GPUS", "COST"]
    table = [
        [
            j.rid,
            j.config.name,
            j.state,
            human_readable.date_time(
                datetime.now(timezone.utc) - parser.parse(j.created_at)
            ),
            f"{j.config.gpus} ({j.cloud_offer.gpu_type})",
            f"{cents_to_dollars_str(j.total_cost)} (${j.cost_per_hour}/h)",
        ]
        for j in jobs
    ]
    typer.echo(tabulate(table, headers=headers, tablefmt="simple"))


@app.command()
@async_command
@use_toml_config(default_value="trainwave.toml")
@ensure_api_key
async def status(
    project: Annotated[str, typer.Option(help="Project ID or RID")],
    job_id: str,
) -> None:
    """Get the status of a job."""
    api_client = Api(config.api_key, config.endpoint, project)
    typer.echo(await api_client.job_status(job_id))


@app.command()
@async_command
@use_toml_config(default_value="trainwave.toml")
@ensure_api_key
async def cancel(
    project: Annotated[str, typer.Option(help="Project ID or RID")],
    job_id: str,
):
    """Cancel a job."""
    api_client = Api(config.api_key, config.endpoint, project)
    await api_client.cancel_job(job_id)
    typer.echo(f"Cancelled job: {job_id}")


@app.command()
@async_command
@ensure_api_key
async def logs(
    job_id: str,
) -> None:
    """Get the logs of a job."""
    logger.remove()
    logger.add(
        sys.stdout,
        format="<green>{extra[log_time]}</green> | <white>{message}</white>",
        colorize=True,
        serialize=False,
        level="DEBUG",
        enqueue=True,
        catch=True,
    )
    parsed = urlparse(config.endpoint)
    scheme = "wss" if parsed.scheme == "https" else "ws"
    port = ""
    if parsed.port:
        port = f":{parsed.port}"
    uri = (
        f"{scheme}://{parsed.hostname}{port}/ws/logs/{job_id}/?api_key={config.api_key}"
    )

    def format_ts(ts: str | None) -> str:
        if ts is None:
            return ""
        timestamp = int(ts) / 1e9
        dt = datetime.fromtimestamp(timestamp)
        return dt.strftime("%Y-%m-%d %H:%M:%S.%f")

    ssl_context = None
    if "trainwave.dev" in uri:
        import ssl

        ssl_context = ssl.SSLContext()
        ssl_context.verify_mode = ssl.CERT_NONE
    opts = {"ssl": ssl_context} if ssl_context else {}

    async with websockets.connect(uri, **opts) as websocket:
        try:
            while response := await websocket.recv():
                data = json.loads(response)
                logger.info(data["message"], log_time=format_ts(data.get("ts")))
        except websockets.exceptions.ConnectionClosedOK:
            pass
