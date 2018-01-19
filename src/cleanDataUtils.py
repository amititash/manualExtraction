from nltk.stem.snowball import SnowballStemmer
from sklearn.feature_extraction.stop_words import ENGLISH_STOP_WORDS as stopwords
from spacyParser import spacyParser
from trainAndPredictUtils import filter_using_pretrained_model
import re

spacy_parser = spacyParser().spacy_parser

#lambda methods
is_not_null_or_integer = lambda s: (not s) or (not s.isdigit() and not (s[0] == '-' and s[1:].isdigit()))

# Stem the words to its root entity
def stem(entity):
    return SnowballStemmer("english").stem(entity)

# Cleans text by removing unicode characters
def clean_text(entities_text):
    cleaned_text = entities_text.replace('\"','') #Remove double quotes
    cleaned_text = str(cleaned_text.encode('ascii','ignore').decode('ascii')) #remove unicode characters
    doc = spacy_parser(cleaned_text)
    tokens = []
    prev_token_tag = ""
    for token in doc:
        if token.text[0].isupper() and not token.tag_ in ["NN", "NNP", "JJ"]:
            tokens.append(".")
        tokens.append(token.text)
    cleaned_text = " ".join(tokens)
    return cleaned_text.strip('. ')

# Gets the cleaned text to process from json
def get_text_to_process(entity_payload, categories_to_filter_out):
    if entity_payload.category in categories_to_filter_out:
        return ''

    entities_text = ". ".join([entity_payload.description,
                                "The category is " + entity_payload.category.lower(), 
                                "The sub category is " + entity_payload.sub_category.lower(),
                                "The title is " + entity_payload.title.lower(), ""])

    return clean_text(entities_text)

# Cleans up detected entities by removing integers, stop words, determiners
def clean_entities(entities):
    cleaned_entities = set(filter(is_not_null_or_integer, [ent.lower().strip('. ,;').replace('\"','') for ent in entities]))
    cleaned_entities = set([re.sub("^[a|an|the|its|his|your|it\'s|your\'s|yours|hers]+\s","", ent) for ent in cleaned_entities])
    return cleaned_entities - stopwords - set(['category', 'sub category','title']) # remove stop words and added words

# Cleans up detected entities by removing integers, stop words, determiners, filters out non-automobile words and returns stemmed and non-stemmed versions.
def clean_and_filter_entities(entities, model_file, filter_flag=True):
    cleaned_entities = clean_entities(entities)
    if filter_flag:
        cleaned_entities = filter_using_pretrained_model(cleaned_entities, model_file)
    stemmed_cleaned_entities = set([stem(ent) for ent in cleaned_entities])
    return (stemmed_cleaned_entities, cleaned_entities)



