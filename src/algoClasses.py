# Algo classes
from spacyParser import spacyParser
from analyze import analyze_entities, get_native_encoding_type
from Payload import Payload

# Constants denoting various algorithms implemented.
SPACY_ENTITIES_ALGO = "Spacy Entities"
SPACY_NOUN_CHUNKS_ALGO = "Spacy Noun Chunks"
GOOGLE_API_ALGO = "Google Cloud API"

class Algo:
    def get_name():
        raise NotImplementedError("Derived classes will implement this")

    def get_entities(text):
        raise NotImplementedError("Derived classes will implement this")

class SpacyEntitiesAlgo(Algo):
    def get_name():
        return SPACY_ENTITIES_ALGO

    def get_entities(text):
        spacy_parser = spacyParser().spacy_parser
        doc = spacy_parser(text)
        return set([ent.text for ent in doc.ents])

class SpacyNounchunksAlgo(Algo):
    def get_name():
        return SPACY_NOUN_CHUNKS_ALGO

    def get_entities(text):
        spacy_parser = spacyParser().spacy_parser
        doc = spacy_parser(text)
        return set([ent.text for ent in doc.noun_chunks])

class GoogleEntitiesAlgo(Algo):
    def get_name():
        return GOOGLE_API_ALGO

    def get_entities(text):
        result = analyze_entities(text, get_native_encoding_type())
        entitiesList = [Payload(ent) for ent in result['entities']]
        filteredEntitiesList = list(filter(lambda x: x.type=='OTHER', entitiesList))
        return set([x.name for x in filteredEntitiesList])

def get_all_algorithms():
    return [SPACY_ENTITIES_ALGO, SPACY_NOUN_CHUNKS_ALGO, GOOGLE_API_ALGO]

def get_algorithm_by_name(algo_name):
    if algo_name == SPACY_ENTITIES_ALGO:
        return SpacyEntitiesAlgo
    elif algo_name == SPACY_NOUN_CHUNKS_ALGO:
        return SpacyNounchunksAlgo
    elif algo_name == GOOGLE_API_ALGO:
        return GoogleEntitiesAlgo
    else:
        raise "Algo name not implemented: " + algo_name
