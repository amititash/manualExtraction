import sys
from spacyParser import spacyParser
from algoClasses import get_all_algorithms, get_algorithm_by_name
from cleanDataUtils import get_text_to_process, clean_and_filter_entities
from Payload import Payload
spacy_parser = spacyParser().spacy_parser

key_delimiter = ';'

# Makes a key for cooccuring entity dict
def make_key(entity1, entity2):
    return entity1 + key_delimiter + entity2

# Indicates whether one string is a subset of other
def subset(str1, str2):
    if (str1 in str2) or (str2 in str1):
        return True
    return False

# Updates count of cooccuring entities
def update_cooccuring_dict(dict, entities, sents):
    entity_count = len(entities)
    ents = list(entities)
    for i in range(0, entity_count):
        for j in range(i+1, entity_count):
            if not subset(ents[i], ents[j]):
                for sent in sents:
                    if ents[i] in sent.text and ents[j] in sent.text: # If they belong to same sentence
                        key = make_key(ents[i], ents[j])
                        if key in dict:
                            dict[key] += 1
                        else:
                            dict[key] = 1

# Calculates count of each object
def update_dict(dict_cnt, set_of_objects):
    for obj in set_of_objects:
        if not obj in dict_cnt:
            dict_cnt[obj] = 1
        else:
            dict_cnt[obj] += 1

# Displays progress bar
def display_progress(i,n):
    hash = ((60*i)//n)
    print("[{}{}] {}%".format('#' * hash, ' ' * (60-hash), "{0:.0f}".format((i/n)*100)), end="\r")

# Creates Json objects from json list and updates it with detected entities using different algorithms
def process_data(jList, categories_to_filter_out, model_file, filter_flag=True):
    return_list=[]
    num_entries = len(jList)
    print("-------------------------------")
    print("Total entries: %d" % num_entries)
    print("-------------------------------")
    cnt=0
    all_algos = get_all_algorithms()
    cooccuring_counts_dict = {}
    counts_dict = {}
    for algo_name in all_algos:
        cooccuring_counts_dict[algo_name] = {}
        counts_dict[algo_name] = {}
    for j in jList:
        cnt+=1
        if cnt%10==0:
            display_progress(cnt, num_entries)

        try:
            payloadJ = Payload(j)
            cleaned_entities_text = get_text_to_process(payloadJ, categories_to_filter_out)
            if not cleaned_entities_text:
                continue

            doc = spacy_parser(cleaned_entities_text)
            j['id'] = cnt
            j['cleanedText'] = cleaned_entities_text
            for algo_name in all_algos:
                algo = get_algorithm_by_name(algo_name)
                entities = algo.get_entities(cleaned_entities_text)
                (j[algo_name + 'stemmed_entities'], j[algo_name + 'non_stemmed_entities']) = clean_and_filter_entities(entities, model_file, filter_flag)

                update_cooccuring_dict(cooccuring_counts_dict[algo_name], j[algo_name + 'non_stemmed_entities'], list(doc.sents))
                update_dict(counts_dict[algo_name], j[algo_name + 'non_stemmed_entities'])
            return_list.append(Payload(j))
        except:
            print("Encountered error: " + str(sys.exc_info()[0]))
            print("While processing the following data: ")
            print(cleaned_entities_text)
            continue

    display_progress(num_entries, num_entries)
    return return_list, cooccuring_counts_dict, counts_dict


