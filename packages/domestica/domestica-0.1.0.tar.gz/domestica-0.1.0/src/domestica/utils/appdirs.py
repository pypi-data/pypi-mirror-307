from pathlib import Path

import typer

from ..constants import Constants


def get_app_dir() -> str:
    """
    Returns the path to the directory where the given app is installed.

    Returns:
        str: The path to the directory where the app is installed.
    """
    app_dir = typer.get_app_dir(Constants.APP_NAME)
    return app_dir


def get_config_file_path() -> str:
    """
    Returns the path to the configuration file for the given app.

    Returns:
        str: The path to the configuration file.
    """
    app_dir = get_app_dir()
    config_path: Path = Path(app_dir) / Constants.CONFIG_FILE
    return config_path.as_posix()


def delete_app_config_file() -> None:
    """
    Deletes the configuration file for the given app.

    Args:
        app_name (str): The name of the app.
    """
    config_path: Path = Path(get_config_file_path())
    if config_path.is_file():
        config_path.unlink()
