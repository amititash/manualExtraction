import re, spacy, string, pickle, csv, os, sys
from pprint import pprint
from algoClasses import get_all_algorithms, get_algorithm_by_name
from spacyParser import spacyParser

# Write entities to output directory
# Sort dictionary by items
def sort_dict_by_items(d):
    return [(k, d[k]) for k in sorted(d, key=d.get, reverse=True)]

# Filters out any entity with count less than cnt
def filter_dict_by_count(dict, cnt):
    return {k:v for k,v in dict.items() if v > cnt}

# Write dictionary to a file for debugging purposes
def write_list(list, file):
    try:
        with open(file, 'w', newline='') as csv_file:
            writer = csv.writer(csv_file)
            for value in list:
                writer.writerow([value])
    except IOError:
        print("Could not read file:" + file)

# Write dictionary to a file for debugging purposes
def write_dict(d, file):
    try:
        with open(file, 'w', newline='') as csv_file:
            writer = csv.writer(csv_file)
            for key, value in d:
                writer.writerow([key, value])
    except IOError:
        print("Could not read file:" + file)

# Sorts and Writes entities of each algo to output directory
def sort_and_write_entities(counts_dict, output_directory, coocur_flag=False):
    all_algos = get_all_algorithms()
    for algo_name in all_algos:
        entities_cnt = counts_dict[algo_name]
        prefix = "count_"
        if coocur_flag:
            entities_cnt = filter_dict_by_count(entities_cnt, 1)
            prefix = "cooccur_"
        sorted_dict = sort_dict_by_items(entities_cnt)
        write_dict(sorted_dict, os.path.join(output_directory, prefix + algo_name +".tsv"))

def write_relations(relations_dict, output_directory, prefix="rel_"):
    all_algos = get_all_algorithms()
    for algo_name in all_algos:
        rel_list = relations_dict[algo_name]
        write_list(rel_list, os.path.join(output_directory, prefix + algo_name +".tsv"))
