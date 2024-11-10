from pathlib import Path

from xdg_base_dirs import xdg_config_home, xdg_data_home


def _app_directory(root: Path) -> Path:
    directory = root / "tuiet"
    directory.mkdir(exist_ok=True, parents=True)
    return directory

def data_directory() -> Path:
    """Return (possibly creating) the application data directory."""
    return _app_directory(xdg_data_home())

def config_directory() -> Path:
    """Return (possibly creating) the application config directory."""
    return _app_directory(xdg_config_home())

def config_file() -> Path:
    return config_directory() / "config.yaml"

def database_file() -> Path:
    return data_directory() / "db.db"
