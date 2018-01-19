import csv, re, os, json, subprocess
from Payload import Payload
from cleanDataUtils import get_text_to_process
from algoClasses import get_all_algorithms, get_algorithm_by_name

# Reads all relations from a file
def read_relations(relations_file):
    relations = []
    try:
        with open(relations_file, 'r') as tsvin:
            tsvin = csv.reader(tsvin, delimiter='\t')
            for row in tsvin:
                relations.append(row)
    except IOError:
        print("Could not read file:" + desc_file)
    return relations

def extract_relationships(input_file, jar_path, descriptions_file, relations_file, categories_to_filter_out):
    all_text = []
    (jar_directory, filename) = os.path.split(jar_path);

    try:
        with open(input_file) as data_file:
            entitiesJsonList = json.loads(str(data_file.read()))
            for jsonEntity in entitiesJsonList:
                cleaned_text = get_text_to_process(Payload(jsonEntity), categories_to_filter_out)
                if cleaned_text:
                    all_text.append(cleaned_text)
    except IOError:
        print("Could not read file:" + input_file)

    try:
        with open(descriptions_file, 'w') as desc_file:
            for text in all_text:
                desc_file.write(text + "\n")
    except IOError:
        print("Could not read file:" + descriptions_file)

    print("Extracting relations using open IE")
    print("-----------------------------------")
    subprocess.call(["java", "-Xmx10g", "-XX:+UseConcMarkSweepGC", "-jar", jar_path, "--ignore-errors", "-s", "--format", "column", descriptions_file, relations_file], cwd=jar_directory)
    print("-----------------------------------")

# Processes relations so that the main argument is separated
def process_relation_arg(rel_arg):
    return re.sub(".*Relation\(|.*Argument\(|\,List.*$","",rel_arg)

def get_relation_string(relation):
    return ";".join([process_relation_arg(relation[2]), process_relation_arg(relation[3]), process_relation_arg(relation[4])])

def clean_relation_arg(rel_arg):
    return re.sub("[(|,]"," ", rel_arg).strip().lower()

# Returns if both entities of the relation contain one of the entities in the list of entities
def contains_both_entities(relation, entities):
    subject_contains_entity = False
    object_contains_entity = False
    for entity in entities:
        if entity in clean_relation_arg(relation[2]):
            subject_contains_entity = True
        if entity in clean_relation_arg(relation[4]):
            object_contains_entity = True
    return subject_contains_entity and object_contains_entity

def get_spo_relation(relation):
    return "\t".join([relation[0], process_relation_arg(relation[2]), process_relation_arg(relation[3]), process_relation_arg(relation[4])])

# Filters relations based on entities found
def filter_relations(relations_file, counts_dict):
    relations = read_relations(relations_file)
    all_algos = get_all_algorithms()
    relations_dict = {}
    spo_relations_dict = {}
    for algo_name in all_algos:
        filtered_relations = []
        spo_filtered_relations = []
        rel_strings = set()
        for relation in relations:
            rel_string = get_relation_string(relation)
            if(contains_both_entities(relation, counts_dict[algo_name].keys())) and not rel_string in rel_strings:
                filtered_relations.append(relation)
                spo_filtered_relations.append(get_spo_relation(relation))
            rel_strings.add(rel_string)
        relations_dict[algo_name] = filtered_relations
        spo_relations_dict[algo_name] = spo_filtered_relations

    return relations_dict, spo_relations_dict


