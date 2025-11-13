import shutil
import logging

logger = logging.getLogger("generator")

def prolog_example_code(id: int, word: str):
    """
    Constructs Prolog statements for an single example of a word in examples.pl.

    :param id: Int with the id of the example.
    :param word: str with the word of the example.
    :return: List of str with the Prolog statements.
    """

    result = []

    example_id = "e" + str(id)
    result.append(f"example({example_id}).")
    result.append(f"hypernym({example_id}, '{word}').")
    result.append(f"component_holonym({example_id}, '{word}').")
    result.append(f"member_holonym({example_id}, '{word}').")
    result.append(f"portion_holonym({example_id}, '{word}').")
    result.append(f"related_to({example_id}, '{word}').")

    return result


example_header = """
:- discontiguous example/1.
:- discontiguous hypernym/2.
:- discontiguous component_holonym/2.
:- discontiguous member_holonym/2.
:- discontiguous portion_holonym/2.
:- discontiguous related_to/2.

"""


def create_examples(words: [str], enemies: [int], killer: int, output_folder: str):
    """
    Generates the examples.pl file for the Aleph experiment workspace.

    :param words: List of str with the words of the coadenames game board.
    :param enemies: List of int with the indices of the enemy words in word list.
    :param killer: int with the index of the killer word in word list.
    :param output_folder: str with path to the output folder.
    :return: None
    """
    example_id = 0
    with open(f"{output_folder}/examples.pl", 'w') as examples:

        examples.write(example_header)

        for word in words:
            examples.write(f"word('{word}').\n")

        examples.write("\n")
        for enemy in enemies:
            examples.write(f"enemy('{words[enemy]}').\n")
        examples.write(f"enemy('{words[killer]}').\n")

        examples.write("\n")
        examples.write(f"killer('{words[killer]}').\n")

        examples.write("\n")
        for word in words:
            example = prolog_example_code(example_id, word)
            for item in example:
                examples.write("%s\n" % item)
            examples.write("\n")
            example_id = example_id + 1


def create_positive_cases(indices: [int], output_folder: str):
    with open(f"{output_folder}/experiment.f", 'w') as positive:
        for index in indices:
            example_id = "e" + str(index)
            positive.write("solution(%s).\n" % example_id)


def create_negative_cases(indices: [int], output_folder: str):
    with open(f"{output_folder}/experiment.n", 'w') as negative:
        for index in indices:
            example_id = "e" + str(index)
            negative.write("solution(%s).\n" % example_id)


def copy_template_files(output_folder: str, case: str):

    if case == "normal" or case == "combined":
        shutil.copy("aleph/aleph_normal_template.pl", output_folder + "/experiment.b")

    if case == "allow_noise":
        shutil.copy("aleph/aleph_allow_noise_template.pl", output_folder + "/experiment.b")

    shutil.copy("aleph/rules_template.pl", output_folder + "/rules.pl")
    shutil.copy("aleph/action_template.pl", output_folder + "/action.pl")


def create_background_knowledge(data, output_folder: str):

    with open(f"{output_folder}/background.pl", 'w') as background:

        background.write(":- dynamic hypernym/2.\n")
        background.write(":- dynamic hypernym / 2.\n")
        background.write(":- dynamic has_component_holonym / 2.\n")
        background.write(":- dynamic has_member_holonym / 2.\n")
        background.write(":- dynamic has_portion_holonym / 2.\n")
        background.write(":- dynamic is_related_to / 2.\n")

        for item in sorted(data["words"]):
            logger.debug("item " + item)
            background.write("%s\n" % item)

        for item in sorted(data["hypernyms"]):
            background.write("%s\n" % item)


def read_seeds_from_file(seed_file: str):
    """
    Read seed values from a file.

    Parameters:
    seed_file (str): The path to the seed file.

    Returns:
    List[str]: A list of seed values read from the file.
    """
    seeds = []

    with open(seed_file, 'r') as file:
        lines = file.readlines()
        for line in lines:
            seeds.append(line.strip())

    return seeds


def write_used_words(filename: str, game_board: dict):
    words = game_board["words"]

    with open(filename, 'w') as text:
        text.write("Friends\n")
        for index in game_board["friends"]:
            text.write(words[index] + " ")

        text.write("\n\nEnemies\n")
        for index in game_board["enemies"]:
            text.write(words[index] + " ")

        text.write("\n\nInnocents\n")
        for index in game_board["innocents"]:
            text.write(words[index] + " ")

        text.write("\n\nKiller\n")
        text.write(words[game_board["killer"]])

