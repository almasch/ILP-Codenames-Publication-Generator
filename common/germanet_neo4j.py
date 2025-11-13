from neo4j import GraphDatabase
from typing import List
import logging

from rich.console import Console

logger = logging.getLogger("generator")
console = Console()

def prolog_fact_for_type(word_type, a, b):
    return f"{word_type}('{a}','{b}')"


def retrieve_facts_for_combined_knowledge(predicate_name: str, term: str,
                                          filter: [str],
                                          neo4j_location: str,
                                          normal_knowledge_tree):
    """
    :param predicate_name: This string is used as predicate name.
    :param term: The term to retrieve facts for.
    :param neo4j_location: The url of the Neo4j database.
    :param normal_knowledge_tree: If True, the normal knowledge tree is used. If False, all edges are merged to a single relation.
    :param filter:
    :return: A tuple containing two sets - words and hypernyms
    """

    console.print(f"    Retrieve facts for: [yellow]{term}[/]")

    combined_filter = '|'.join(filter)

    driver = GraphDatabase.driver(f'bolt://{neo4j_location}')
    session = driver.session()
    cypher = f'''
        MATCH (seed:Synset)<--(term:LexUnit) WHERE term.orth_form="{term}" 
            WITH seed, [(x)<-[:{combined_filter}*]-(seed) | x] as hypernyms 
            WITH hypernyms + seed  as all_nodes 
            UNWIND all_nodes as concept1 
            MATCH (concept1)-[relation:{combined_filter}]->(concept2) 
            WITH concept1,concept2, [(concept1)<--(term:LexUnit) | term ] as terms1, [(concept2)<--(term:LexUnit) | term ] as terms2, relation 
            RETURN DISTINCT concept1,terms1, concept2, terms2, relation
        '''

    logger.debug(cypher)

    neo = session.run(cypher)

    words = set()
    hypernyms = set()

    for x in neo:
        terms1 = x['terms1']
        terms2 = x['terms2']
        relation = x["relation"].type.lower()
        logger.debug(relation)
        for t1 in terms1:
            word1_orth = t1["orth_form"]
            word1_lexunit = str(t1["lexunit_id"])
            word1 = prolog_fact_for_type(predicate_name, word1_orth, word1_lexunit)
            words.add(f"{word1}.")
            for t2 in terms2:
                word2_orth = t2["orth_form"]
                word2_lexunit = str(t2["lexunit_id"])
                if not word2_orth.startswith('GNROOT'):
                    word2 = prolog_fact_for_type(predicate_name, word2_orth, word2_lexunit)
                    words.add(f"{word2}.")


                    if normal_knowledge_tree:
                        # this code uses the given relations
                        hypernyms.add(f"{relation}({word1},{word2}).")
                    else:
                        # this if for the combined sub trees and ignores the given relations
                        hypernyms.add(f"has_hypernym({word1},{word2}).")

    return words, hypernyms


def combined_hypernym_knowledge(word_type: str, words: List[str], relations: List[str], neo4j_location: str, normal_knowledge_tree=True):
    """
    Retrieves combined hypernym knowledge for a given word type and list of words.

    Parameters:
    - word_type (str): The type of word for which the hypernym knowledge is to be retrieved.
    - words (List[str]): List of words for which the hypernym knowledge is to be retrieved.
    - relations (List[str]): List of specific relations to consider while retrieving the hypernym knowledge.

    Returns:
    - dict: A dictionary containing the retrieved hypernym knowledge. The dictionary has two keys:
        - "words": A set of words that are related to the input words.
        - "hypernyms": A set of hypernyms associated with the input words.

    Example Usage:
    word_type = "noun"
    words = ["cat", "dog"]
    relations = ["HAS_HYPERNYM", "HAS_MEMBER_HOLONYM"]
    result = combined_hypernym_knowledge(word_type, words, relations)
    print(result["words"])
    print(result["hypernyms"])
    """
    res_words = set()
    res_hypernyms = set()
    for word in words:
        verbs, hypernyms = retrieve_facts_for_combined_knowledge(word_type, word, relations, neo4j_location, normal_knowledge_tree)
        res_words.update(verbs)
        res_hypernyms.update(hypernyms)

    if logger.isEnabledFor(logging.DEBUG):
        for verb in res_words:
            logger.debug(verb)
        for hypernym in res_hypernyms:
            logger.debug(hypernym)

    return {"words": res_words, "hypernyms": res_hypernyms}


# demo
if __name__ == '__main__':
    # this method can be used to test the output of combined_hypernym_knowledge
    words_list = [
        "Krankenhaus", "Skelett", "Oktopus", "Hubschrauber", "Känguru", "Mikroskop", "Superheld", "Teleskop",
        "Fallschirm", "Schnabeltier", "Olymp", "Satellit", "Engel", "Roboter", "Einhorn", "Hexe", "Bergsteiger",
        "Taucher", "Gift", "Brücke", "Feuer", "Tisch", "Wal", "Mond", "Fisch", "Doktor", "Kirche", "Gürtel",
        "Zitrone", "Wind", "Löwe", "Auge", "Luft", "Hase", "Bank", "Gras", "Auflauf", "Zwerg", "Wald", "Auto",
        "Burg", "Apfel", "Öl", "Koch", "Bär", "Katze", "Leben", "Glück", "Riese", "Gesicht", "Papier", "Anwalt",
        "Forscher", "Nacht", "Siegel", "Strasse", "Becken", "Optik", "Inka", "Berliner", "Feder", "Mexico",
        "Peking", "Loch", "Ness", "Adler", "Europa", "Hamburger", "Verein", "Winnetou", "Frankreich", "Alpen",
        "Osten", "Afrika", "Essen", "Linse", "Chemie", "Arm", "Torte", "Tau", "Kippe", "Fuchs", "Boot", "Korn",
        "Melone", "Quartett", "Bar", "Bahn", "Knie", "Fall", "Drucker", "Blinker", "Sekretär", "Niete", "Moos",
        "Blüte", "Abgabe", "Bart", "Jura", "Tafel"]

    combined_hypernym_knowledge("noun", words_list, ["HAS_HYPERNYM", "HAS_MEMBER_HOLONYM"])
