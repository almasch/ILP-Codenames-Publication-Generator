from invoke import task
import shutil
from pathlib import Path

from rich.console import Console

console = Console()

@task
def reset(ctx):
    """
    Resets the whole project to its initial state. All workspaces and generated aleph experiments
    are deleted.
    """

    console.print("💥 RESET the whole workspace.")

    # Determine the path to the script.
    project_root = Path(__file__).parent.absolute()

    # Construct the path to the folder to erase based on the script location to prevent deleting wrong data by mistake...
    folder_to_delete = project_root.parent / ctx.aleph_experiments_dir
    folder_to_delete.mkdir(exist_ok=True)
    if folder_to_delete.exists():
        for item in folder_to_delete.iterdir():
            if item.is_file():
                if item.name == ".gitkeep":
                    continue
                item.unlink()
            elif item.is_dir():
                shutil.rmtree(item)
