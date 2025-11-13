from invoke import task
from pathlib import Path

from rich.console import Console

console = Console()

@task
def clean(ctx):
    """
    Clean up protocol and error files from workspaces but do not delete generated aleph experiments.
    """

    console.print("🧹 Clean up Aleph experiments.")

    # Determine the path to the script.
    project_root = Path(__file__).parent.absolute()

    # Construct the path to the folder to erase based on the script location to prevent deleting wrong data by mistake...
    folder_to_delete = project_root.parent / ctx.aleph_experiments_dir

    # Find and delete protocol and error files in all subdirectories
    for filename in [ctx.protocol_filename, ctx.error_filename]:
        for filepath in folder_to_delete.rglob(filename):
            case = filepath.parent.parent.name
            seed = filepath.parent.name
            if filepath.exists():
                console.log(f" Deleting [green]{filename}[/] file [green]{case}[/] for seed [green]{seed}[/]")
                filepath.unlink()
            else:
                console.log(f"No [green]{filename}[/] file in [green]{case}[/] for [green]{seed}[/]")

    console.log(f"Deleted all protocol and error files in [green]{ctx.aleph_experiments_dir}[/]")