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
from wilhelm_python_sdk.database_clients import get_database_client
from wilhelm_python_sdk.database_clients import get_node_label_attribute_key
from wilhelm_python_sdk.vocabulary_parser import GERMAN
from wilhelm_python_sdk.vocabulary_parser import get_attributes
from wilhelm_python_sdk.vocabulary_parser import get_definitions
from wilhelm_python_sdk.vocabulary_parser import get_inferred_links
from wilhelm_python_sdk.vocabulary_parser import get_vocabulary


def load_into_database(yaml_path: str):
    """
    Upload https://github.com/QubitPi/wilhelm-vocabulary/blob/master/german.yaml to Neo4j Database.

    :param yaml_path:  The absolute or relative path (to the invoking script) to the YAML file above
    """
    vocabulary = get_vocabulary(yaml_path)
    label_key = get_node_label_attribute_key()

    with get_database_client() as database_client:
        for word in vocabulary:
            attributes = get_attributes(word, GERMAN, label_key)
            database_client.save_a_node_with_attributes("Term", attributes)
            definitions = get_definitions(word)
            for definition_with_predicate in definitions:
                definition = definition_with_predicate[1]
                database_client.save_a_node_with_attributes("Definition", {label_key: definition})

        # save links between term and definitions
        for word in vocabulary:
            definitions = get_definitions(word)
            for definition_with_predicate in definitions:
                predicate = definition_with_predicate[0]
                definition = definition_with_predicate[1]
                term = word["term"]
                if predicate:
                    database_client.save_a_link_with_attributes(
                        language=GERMAN,
                        source_label=term,
                        target_label=definition,
                        attributes={label_key: predicate}
                    )
                else:
                    database_client.save_a_link_with_attributes(
                        language=GERMAN,
                        source_label=term,
                        target_label=definition,
                        attributes={label_key: "definition"}
                    )

        # save link_hints as database links
        for link in get_inferred_links(vocabulary, label_key):
            database_client.save_a_link_with_attributes(
                language=GERMAN,
                source_label=link["source_label"],
                target_label=link["target_label"],
                attributes=link["attributes"]
            )
