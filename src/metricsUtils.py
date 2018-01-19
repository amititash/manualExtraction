from algoClasses import get_all_algorithms, get_algorithm_by_name
from cleanDataUtils import stem
import os

def get_metrics(set_of_entities, goldenset_entities):
    true_positives=0
    false_positives=0
    false_negatives=0
    list_tp = []
    list_fp = []
    list_fn = []
    for entity in set_of_entities:
        if entity in goldenset_entities:
            true_positives+=1
            list_tp.append(entity)
        else:
            false_positives+=1
            list_fp.append(entity)

    for entity in goldenset_entities:
        if not entity in set_of_entities:
            false_negatives += 1
            list_fn.append(entity)

    precision = true_positives/(true_positives + false_positives)
    recall = true_positives/(true_positives + false_negatives)
    fscore = 2*precision*recall/ (precision + recall)
    return (precision, recall, fscore, list_tp, list_fp, list_fn)

# Writes debug info (true positives, false positives, true negatives) to a file for debugging purposes
def write_metric_info(entitynames, goldenset_names, tp, fp, fn, file):
    try:
        with open(file, 'w') as file_debug:
            for name in entitynames:
                output_str = name
                stemmed_name = stem(name)
                if stemmed_name in tp:
                    file_debug.write(name + ";tp\n")
                elif stemmed_name in fp:
                    file_debug.write(name + ";fp\n")
                else:
                    file_debug.write(name + ";tn\n")

            for name in goldenset_names:
                if stem(name) in fn:
                    file_debug.write(name + ";fn\n")
    except IOError:
        print("Could not read file:" + file)

# Calculates metrics and writes it to a debug file
def calculate_and_write_metrics(goldenset_file, counts_dict, output_directory):
    try:
        with open(goldenset_file) as goldenset_file:
            goldenset_nonstemmed_entities = set([line.rstrip('\n').lower() for line in goldenset_file])
            goldenset_entities = set([stem(ent) for ent in goldenset_nonstemmed_entities])
    except IOError:
        print("Could not read file:" + goldenset_file)

    all_algos = get_all_algorithms()
    for algo_name in all_algos:
        (precision, recall, fscore, list_tp, list_fp, list_fn) = get_metrics(set(stem(e) for e in counts_dict[algo_name].keys()), goldenset_entities)
        print(algo_name + " stats (precision, recall, fscore): " + ','.join(str(e) for e in [precision, recall, fscore]))
        write_metric_info(counts_dict[algo_name].keys(), goldenset_nonstemmed_entities, list_tp, list_fp, list_fn, os.path.join(output_directory, "debug_" + algo_name +".tsv"))

