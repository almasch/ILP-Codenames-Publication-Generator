import random
from typing import List


def read_words(words_filename: str) -> List[str]:
    """
    Reads a file containing words and returns a list of those words.

    :param words_filename: The name of the file to read words from.
    :return: A list of words read from the file.
    """
    with open(words_filename, "r") as words:
        word_list = []
        for word in words:
            word_list.append(word.strip())
    return word_list


def agents_for_game(seed: str):
    """
    Get a random sample set of 25 words from the codename words.
    """
    random.seed(seed)
    return random.sample(range(1,25), 8)


def generate_game_board(seed: str, words_filename: str):
    """
    Generate a game board using a given seed. With the same seed and words_filename, the game board will always be
    the same.

    Parameters:
    - seed (str): A seed to initialize the random number generator.
    - words_filename (str): The name of the file containing the codenames words.

    Returns:
    - dict: A dictionary containing the game board information. The dictionary has the following keys:
      - "words" (list): A list of 25 randomly selected words from the "codenames" list.
      - "friends" (list): A list of positions (indices) representing the friend cards on the game board.
      - "enemies" (list): A list of positions (indices) representing the enemy cards on the game board.
      - "killer" (int): The position (index) representing the killer card on the game board.
      - "innocents" (list): A list of positions (indices) representing the innocent cards on the game board.

    Note:
    - The function uses the "random" module and requires seeding with the given seed.
    """

    random.seed(seed)
    codenames = read_words(words_filename)
    words = random.sample(codenames, 25)
    index_pool = list(range(25))

    friends = [index_pool.pop(random.randrange(len(index_pool))) for _ in range(9)]
    enemies = [index_pool.pop(random.randrange(len(index_pool))) for _ in range(8)]
    killer = index_pool.pop((random.randrange(len(index_pool))))
    innocents = index_pool

    return {"words": words,
            "friends": friends,
            "enemies": enemies,
            "innocents": innocents,
            "killer": killer}