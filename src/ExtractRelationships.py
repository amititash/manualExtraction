import argparse
from relationUtils import extract_relationships

if __name__ == '__main__':
    print("-----------------------------------")
    print("Extracting relationships from input file")
    print("-----------------------------------")
    argparser = argparse.ArgumentParser()
    argparser.add_argument("input", help="Input Json file having the manual contents")
    argparser.add_argument("jar", help="Path of open ie jar")
    argparser.add_argument("categories_to_filter_out", help="string containing all the categories to filter out")
    argparser.add_argument("output_descriptions_file", help="Output file path for cleaned up text of all the entries in the manual.")
    argparser.add_argument("output_relations_file", help="Output file path for relationships extracted")
    args = argparser.parse_args()

    extract_relationships(args.input, args.jar, args.output_descriptions_file, args.output_relations_file, args.categories_to_filter_out)

