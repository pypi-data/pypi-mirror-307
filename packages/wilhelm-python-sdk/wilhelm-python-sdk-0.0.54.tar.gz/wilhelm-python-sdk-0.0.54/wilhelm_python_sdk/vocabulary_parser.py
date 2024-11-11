# Copyright Jiaqi Liu
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
import logging
import re

import editdistance
import yaml

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

GERMAN = "German"
LATIN = "Latin"
ANCIENT_GREEK = "Ancient Greek"

EXCLUDED_DECLENSION_ENTRIES = [
    "",
    "singular",
    "plural",
    "masculine",
    "feminine",
    "neuter",
    "nominative",
    "genitive",
    "dative",
    "accusative",
    "N/A"
]

ENGLISH_PROPOSITIONS = {
    "about", "above", "across", "after", "against", "along", "among", "around", "at", "before", "behind", "below",
    "beneath", "beside", "between", "beyond", "by", "down", "during", "except", "for", "from", "in", "inside", "into",
    "like", "near", "of", "off", "on", "onto", "out", "outside", "over", "past", "since", "through", "throughout", "to",
    "toward", "under", "underneath", "until", "up", "upon", "with", "within", "without"
}
EXCLUDED_DEFINITION_TOKENS = {"the"} | ENGLISH_PROPOSITIONS


def get_vocabulary(yaml_path: str) -> list:
    with open(yaml_path, "r") as f:
        return yaml.safe_load(f)["vocabulary"]


def get_definitions(word) -> list[(str, str)]:
    """
    Extract definitions from a word as a list of bi-tuples, with the first element being the predicate and the second
    being the definition.

    For example::

    definition:
      - term: nämlich
        definition:
          - (adj.) same
          - (adv.) namely
          - because

    The method will return `[("adj.", "same"), ("adv.", "namely"), (None, "because")]`

    The method works for the single-definition case, i.e.::

    definition:
      - term: na klar
        definition:

    returns a list of one tupple `[(None, "of course")]`

    Note that any definition are converted to string. If the word does not contain a field named exactly "definition", a
    ValueError is raised.

    :param word:  A dictionary that contains a "definition" key whose value is either a single-value or a list of
                  single-values
    :return: a list of two-element tuples, where the first element being the predicate (can be `None`) and the second
             being the definition
    """
    logging.info("Extracting definitions from {}".format(word))

    if "definition" not in word:
        raise ValueError("{} does not contain 'definition' field. Maybe there is a typo".format(word))

    predicate_with_definition = []

    definitions = [word["definition"]] if not isinstance(word["definition"], list) else word["definition"]

    for definition in definitions:
        definition = str(definition)

        definition = definition.strip()

        match = re.match(r"\((.*?)\)", definition)
        if match:
            predicate_with_definition.append((match.group(1), re.sub(r'\(.*?\)', '', definition).strip()))
        else:
            predicate_with_definition.append((None, definition))

    return predicate_with_definition


def get_declension_attributes(word: object) -> dict[str, str]:
    """
    Returns the declension of a word.

    If the word does not have a "declension" field, the function returns an empty dictionary.

    If the noun's declension is, for some reasons, "Unknown", this function will return an empty dict. Otherwise, the
    declension table is flattened like with row-col index in the map key::

    "declension-0-0": "",
    "declension-0-1": "singular",
    "declension-0-2": "singular",
    "declension-0-3": "singular",
    "declension-0-4": "plural",
    "declension-0-5": "plural",

    :param word:  A vocabulary represented in YAML dictionary which has a "declension" key

    :return: a flat map containing all the YAML encoded information about the noun excluding term and definition
    """

    if "declension" not in word:
        return {}

    declension = word["declension"]

    if declension == "Unknown":
        return {}

    attributes = {}
    for i, row in enumerate(declension):
        for j, col in enumerate(row):
            attributes[f"declension-{i}-{j}"] = declension[i][j]

    return attributes


def get_attributes(word: object, language: str, node_label_property_key: str) -> dict[str, str]:
    """
    Returns a flat map as the Term node properties stored in Neo4J.

    :param word:  A German vocabulary representing

    :return: a flat map containing all the YAML encoded information about the vocabulary
    """
    return {node_label_property_key: word["term"], "language": language} | get_declension_attributes(word)


def get_inferred_links(vocabulary: list[dict], label_key: str) -> list[dict]:
    """
    Return a list of inferred links between related vocabularies.

    This function is the point of extending link inference capabilities. At this point, the link inference includes

    - :py:meth:`token sharing <wilhelm_python_sdk.vocabulary_parser.get_inferred_tokenization_links>`
    - :py:meth:`token sharing <wilhelm_python_sdk.vocabulary_parser.get_levenshtein_links>`

    :param vocabulary:  A wilhelm-vocabulary repo YAML file deserialized
    :param label_key:  The name of the node attribute that will be used as the label in displaying the node

    :return: a list of link object, each of which has a "source_label", a "target_label", and an "attributes" key
    """
    return (get_inferred_tokenization_links(vocabulary, label_key) +
            get_structurally_similar_links(vocabulary, label_key))


def get_definition_tokens(word: dict) -> set[str]:
    definitions = [pair[1] for pair in get_definitions(word)]
    tokens = set()

    for token in set(sum([definition.split(" ") for definition in set().union(set(definitions))], [])):
        cleansed = token.lower().strip()
        if cleansed not in EXCLUDED_DEFINITION_TOKENS:
            tokens.add(cleansed)

    return tokens


def get_term_tokens(word: dict) -> set[str]:
    term = word["term"]
    tokens = set()

    for token in term.split(" "):
        cleansed = token.lower().strip()
        if cleansed not in {"der", "die", "das"}:
            tokens.add(cleansed)

    return tokens


def get_declension_tokens(word: dict) -> set[str]:
    tokens = set()

    for key, value in get_declension_attributes(word).items():
        if value not in EXCLUDED_DECLENSION_ENTRIES:
            for declension in value.split(","):
                cleansed = declension.lower().strip()
                tokens.add(cleansed)

    return tokens


def get_tokens_of(word: dict) -> set[str]:
    return get_declension_tokens(word) | get_term_tokens(word) | get_definition_tokens(word)


def get_inferred_tokenization_links(vocabulary: list[dict], label_key: str) -> list[dict]:
    """
    Return a list of inferred links between related vocabulary terms which are related to one another.

    This mapping will be used to create more links in graph database.

    This was inspired by the spotting the relationships among::

        vocabulary:
          - term: das Jahr
            definition: the year
            declension:
              - ["",         singular,        plural        ]
              - [nominative, Jahr,            "Jahre, Jahr" ]
              - [genitive,   "Jahres, Jahrs", "Jahre, Jahr" ]
              - [dative,     Jahr,            "Jahren, Jahr"]
              - [accusative, Jahr,            "Jahre, Jahr" ]
          - term: seit zwei Jahren
            definition: for two years
          - term: in den letzten Jahren
            definition: in recent years

    1. Both 2nd and 3rd are related to the 1st and the two links can be inferred by observing that "Jahren" in 2nd and
       3rd match the declension table of the 1st
    2. In addition, the 2nd and 3rd are related because they both have "Jahren".

    Given the 2 observations above, this function tokenizes the "term" and the declension table of each word. If two
    words share at least 1 token, they are defined to be "related"

    :param vocabulary:  A wilhelm-vocabulary repo YAML file deserialized
    :param label_key:  The name of the node attribute that will be used as the label in displaying the node

    :return: a list of link object, each of which has a "source_label", a "target_label", and an "attributes" key
    """
    all_vocabulary_tokenizations_by_term = dict([word["term"], get_tokens_of(word)] for word in vocabulary)
    inferred_links = []
    for this_word in vocabulary:
        this_term = this_word["term"]

        for that_term, that_term_tokens in all_vocabulary_tokenizations_by_term.items():
            jump_to_next_term = False

            if this_term == that_term:
                continue

            for this_token in get_term_tokens(this_word):
                for that_token in that_term_tokens:
                    if this_token.lower().strip() == that_token:
                        inferred_links.append({
                            "source_label": this_term,
                            "target_label": that_term,
                            "attributes": {label_key: "term related"},
                        })
                        jump_to_next_term = True
                        break

                if jump_to_next_term:
                    break

    return inferred_links


def get_structurally_similar_links(vocabulary: list[dict], label_key: str) -> list[dict]:
    """
    Return a list of inferred links between structurally-related vocabulary terms.

    This was inspired by the spotting the relationships among::

        vocabulary:
          - term: anschließen
            definition: to connect
          - term: anschließend
            definition:
              - (adj.) following
              - (adv.) afterwards
          - term: nachher
            definition: (adv.) afterwards

    Two words are structurally similar iff:

    1. The edit distance are at most 3
    2. Sharing the same word stem

    :param vocabulary:  A wilhelm-vocabulary repo YAML file deserialized
    :param label_key:  The name of the node attribute that will be used as the label in displaying the node

    :return: a list of link object, each of which has a "source_label", a "target_label", and an "attributes" key
    """
    inferred_links = []

    for this in vocabulary:
        for that in vocabulary:
            if this is that:
                continue
            this_term = this["term"]
            that_term = that["term"]
            distance = editdistance.eval(this_term, that_term)
            if distance <= 3 and get_stem(this_term) == get_stem(that_term):
                inferred_links.append({
                    "source_label": this_term,
                    "target_label": that_term,
                    "attributes": {label_key: "structurally similar"},
                })

    return inferred_links


def get_stem(word: str) -> str:
    from nltk.stem.snowball import GermanStemmer
    stemmer = GermanStemmer()
    return stemmer.stem(word)
