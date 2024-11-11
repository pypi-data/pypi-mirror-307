from pathlib import Path

import click
import yaml
from click_default_group import DefaultGroup
from config import Config
from locations import config_file, database_file, set_custom_root
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
    
@click.group(invoke_without_command=True)
@click.option('--at', type=click.Path(exists=True, file_okay=True, dir_okay=True, path_type=Path), help='Specify the path.')
@click.pass_context
def cli(ctx, at: click.Path | None):
    """Tuiet CLI."""
    if at:
        set_custom_root(at)
    if ctx.invoked_subcommand is None:
        create_config_file()
        init_db()
        from app import App
        app = App()
        app.run()

@cli.command()
@click.argument(
    "thing_to_locate",
    type=click.Choice(["config", "database"])
)
def locate(thing_to_locate: str) -> None:
    if thing_to_locate == "config":
        print("Config file:")
        print(config_file())
    elif thing_to_locate == "database":
        print("Database file:")
        print(database_file())

if __name__ == "__main__":
    cli()