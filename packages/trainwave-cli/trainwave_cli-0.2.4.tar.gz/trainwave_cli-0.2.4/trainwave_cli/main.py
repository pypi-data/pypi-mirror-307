import inspect
import sys

import typer
from loguru import logger

from trainwave_cli.cli import auth, jobs, secrets, setup

app = typer.Typer()
app.add_typer(jobs.app, name="jobs", help="Manage training jobs")
app.add_typer(auth.app, name="auth", help="Authenticate with Trainwave")
app.add_typer(setup.app, name="config")
app.add_typer(secrets.app, name="secrets", help="Manage job secrets")


def get_package_name() -> str:
    frame = inspect.currentframe()
    f_back = frame.f_back if frame is not None else None
    f_globals = f_back.f_globals if f_back is not None else None
    # break reference cycle
    # https://docs.python.org/3/library/inspect.html#the-interpreter-stack
    del frame

    package_name: str | None = None
    if f_globals is not None:
        package_name = f_globals.get("__name__")

        if package_name == "__main__":
            package_name = f_globals.get("__package__")

        if package_name:
            package_name = package_name.partition(".")[0]

    if package_name is None:
        raise RuntimeError("Could not determine the package name automatically.")

    return package_name


def get_version(*, package_name: str) -> str:
    import importlib.metadata

    version: str | None = None
    try:
        version = importlib.metadata.version(package_name)
    except importlib.metadata.PackageNotFoundError:
        raise RuntimeError(f"{package_name!r} is not installed.") from None

    if version is None:
        raise RuntimeError(
            f"Could not determine the version for {package_name!r} automatically."
        )

    return version


def version_callback(*, value: bool):
    if value:
        package_name = get_package_name()
        version = get_version(package_name=package_name)
        typer.echo(f"{package_name}, {version}")
        raise typer.Exit()


@app.callback()
def callback(
    version: bool = typer.Option(None, callback=version_callback, is_eager=True),
) -> None:
    pass


def entrypoint() -> None:
    logger.remove()
    logger.add(sys.stdout, colorize=True, format="<level>{message}</level>")
    app()


if __name__ == "__main__":
    app()
