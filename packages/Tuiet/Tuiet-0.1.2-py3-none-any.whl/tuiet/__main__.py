import click
import yaml
from click_default_group import DefaultGroup

from app import App
from config import Config
from locations import config_file, database_file
from models.database.app import init_db


def create_config_file() -> None:
    f = config_file()
    if f.exists():
        return

    try:
        f.touch()
        with open(f, "w") as f:
            yaml.dump(Config.get_default().model_dump(), f)
    except OSError:
        pass

@click.group(cls=DefaultGroup, default="default", default_if_no_args=True)
def cli() -> None:
    """..."""

@cli.command()
def default() -> None:
    create_config_file()
    init_db() # fix
    app = App()
    app.run()

@cli.command()
@click.argument(
    "thing_to_locate",
)
def locate(thing_to_locate: str) -> None:
    if thing_to_locate == "config":
        print("Config file:")
        print(config_file())
    elif thing_to_locate == "database":
        print("Database file:")
        print(database_file())
    else:
        # This shouldn't happen because the type annotation should enforce that
        # the only valid options are "config" and "collection".
        print(f"Unknown thing to locate: {thing_to_locate!r}")

if __name__ == "__main__":
    cli()
