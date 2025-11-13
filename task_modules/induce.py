from invoke import task
import os

import subprocess
import concurrent.futures
from rich.console import Console

console = Console()

@task
def induce(ctx):
    """
    Runs swipl action.pl for each directory under experiments and
    saves the output to a protocol if this file does not already exist.
    """

    console.print("🚀 Start the induction for all aleph experiments.")

    current_dir = os.getcwd()

    try:
        # Check if the directory exists before trying to change to it
        if not os.path.exists(ctx.aleph_experiments_dir):
            console.log(f"[red]Error: Directory '{ctx.aleph_experiments_dir}' does not exist![/]")
            console.log(f"[yellow]Please create the workspaces with [green]invoke normal allow-noise combined[/] first.[/]")
            return

        os.chdir(ctx.aleph_experiments_dir)

        for configuration_dir in [dir_entry for dir_entry in os.listdir() if os.path.isdir(dir_entry)]:
            os.chdir(configuration_dir)

            console.rule(f"Processing: {configuration_dir.title()}")

            with concurrent.futures.ThreadPoolExecutor(max_workers=ctx.max_workers) as executor:
                futures = []

                for seed_dir in [d for d in os.listdir() if os.path.isdir(d)]:

                    def process_seed(seed_dir=seed_dir):
                        seed_path = os.path.join(os.getcwd(), seed_dir)

                        protocol_file = os.path.join(seed_path, ctx.protocol_filename)
                        error_file = os.path.join(seed_path, ctx.error_filename)

                        if not os.path.exists(protocol_file):
                            console.log(f"🛫  Start executing [green]{configuration_dir}[/] seed [green]{seed_dir}[/]...")

                            subprocess.run(['swipl', 'action.pl'],
                                           stdout=open(protocol_file, "w"),
                                           stderr=open(error_file, "w"),
                                           check=True, cwd=seed_path)

                            console.log(f"🛬  Finished executing seed [green]{seed_dir}[/]!")
                        else:
                            console.log(f"✖️  [bright_black]Skipping {configuration_dir} seed {seed_dir}.[/]")

                    futures.append(executor.submit(process_seed))

                for future in concurrent.futures.as_completed(futures):
                    future.result()

            os.chdir('..')

    finally:
        # make sure to come back to the original starting directory.
        os.chdir(current_dir)
