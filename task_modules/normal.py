from invoke import task
import os

from common.aleph_workspace import read_seeds_from_file
from common.aleph_workspace import write_used_words
from common.aleph_workspace import create_examples
from common.aleph_workspace import create_positive_cases
from common.aleph_workspace import create_negative_cases
from common.aleph_workspace import copy_template_files
from common.aleph_workspace import create_background_knowledge

from common.codenames import generate_game_board

from common.germanet_neo4j import combined_hypernym_knowledge

from rich.console import Console

console = Console()


@task
def normal(ctx):
    """
    Generates Aleph experiments with a normal setting.
    """

    console.print("🔬Generating Aleph experiments with a normal setting.")

    relation = ["HAS_HYPERNYM", "HAS_COMPONENT_HOLONYM", "HAS_MEMBER_HOLONYM", "HAS_PORTION_HOLONYM", "IS_RELATED_TO"]

    #create the output folder
    sub_folder_path = f"{ctx.aleph_experiments_dir}/{ctx.exp_normal_dir}"
    os.makedirs(sub_folder_path, exist_ok=True)

    # process all given randoms seeds and generate ALPEH experiments
    for seed in read_seeds_from_file(ctx.seeds_file):

        console.print(f"  [green]For seed {seed}[/]")

        # create a folder for this seed
        seed_folder = f"{sub_folder_path}/{seed}"
        os.makedirs(seed_folder, exist_ok=False)

        board = generate_game_board(seed, ctx.words_file)
        words = board["words"]
        enemies = board["enemies"]
        killer = board["killer"]

        # Write a human-readable file describing the codenames game board.
        write_used_words(f"{seed_folder}/examples.txt", board)

        # Create Aleph files for positive and negative examples
        create_examples(words, enemies, killer, seed_folder)
        create_positive_cases(board["friends"], seed_folder)

        negative_combined = board["enemies"]
        negative_combined.extend(board["innocents"])
        negative_combined.append(board["killer"])
        create_negative_cases(negative_combined, seed_folder)

        copy_template_files(seed_folder, "normal")

        hyper = combined_hypernym_knowledge("noun", words, relation, ctx.neo4j_location)
        create_background_knowledge(hyper, seed_folder)
