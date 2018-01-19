import argparse, json, os
from dataProcessUtils import process_data
from relationUtils import filter_relations, extract_relationships, extract_relationships
from metricsUtils import calculate_and_write_metrics
from outputUtils import sort_and_write_entities, write_relations
from train import train_and_output_model

#These categories are either not formated well or not extracted well for us to extract entities or relations.
categories_to_filter_out = 'No Category;Contents;Reference;Technical data;Everything from A to Z'

def printHeader(headerStr):
    print("-----------------------------------")
    print(headerStr)
    print("-----------------------------------")

if __name__ == '__main__':
    printHeader("Extract Entities and Relationships from Manual data")
    argparser = argparse.ArgumentParser()
    argparser.add_argument("input", help="Input Json file having the manual contents")
    argparser.add_argument("openiejar", help="Path of open ie jar used to extract relationships")
    argparser.add_argument("output_dir", help="Output Directory containing all the output files")
    argparser.add_argument("training_data_file", help="Training file for training model to filter extracted entities")
    argparser.add_argument("--extractedRel", help="(optional) Extracted relationships file. If not specified, we auto discover them.", required=False)
    argparser.add_argument("--goldenset", help="(optional) Goldenset file to compute precision and recall", required=False)
    args = argparser.parse_args()

    model_file = os.path.join(args.output_dir, "model.pkl")
    train_and_output_model(args.training_data_file, model_file)

    if args.extractedRel:
        relations_file = args.extractedRel
    else:
        printHeader("Extract Relationships")
        descriptions_file = os.path.join(args.output_dir, "descriptions.tsv")
        relations_file = os.path.join(args.output_dir, "relations.tsv")
        extract_relationships(args.input, args.openiejar, descriptions_file, relations_file, categories_to_filter_out)

    printHeader("Extracting Entities")

    #Process data once and get all the entities and information needed for further analysis
    try:
        with open(args.input) as data_file:
            data = json.loads(str(data_file.read()))
            processed_data, cooccuring_cnt_dicts, counts_dict = process_data(data, categories_to_filter_out, model_file)
    except IOError:
        print("Could not read file:" + args.input)

    relations_dict, spo_relations_dict = filter_relations(relations_file, counts_dict)
    print()

    if args.goldenset:
        printHeader("Calculating Metrics")
        calculate_and_write_metrics(args.goldenset, counts_dict, args.output_dir)


    printHeader("Outputing Entities")
    sort_and_write_entities(counts_dict, args.output_dir)
    sort_and_write_entities(cooccuring_cnt_dicts, args.output_dir, True)
    write_relations(relations_dict, args.output_dir, "rel_")
    write_relations(spo_relations_dict, args.output_dir, "rel_spo_")