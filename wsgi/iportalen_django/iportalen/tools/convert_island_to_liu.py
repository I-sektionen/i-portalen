#!/usr/bin/python3
import sys
import argparse
import re
import codecs


def main(argv):  # TODO: Reduce complexity
    parser = argparse.ArgumentParser(description='Translate islands-id')
    parser.add_argument("-i", "--input", dest="input",
                        help="File with list of islands-id to translate", metavar="ISLAND")

    parser.add_argument("-o", "--output", dest="output",
                        help="File with list of Liu-id after translation", metavar="LIU", default="output.txt")

    parser.add_argument("-is", "--input_separator", dest="input_separator",
                        help="Separator of file with list of islands-id", metavar="SEPARATOR", default=";")

    parser.add_argument("-ic", "--input_column", dest="input_column",
                        help="Column for islands-id in input file", metavar="COLUMN", type=int, default=2)

    parser.add_argument("-ie", "--input_encoding", dest="input_encoding",
                        help="Encoding for input file", metavar="ENCODING", default="utf-8")

    parser.add_argument("-t", "--translator", dest="translator",
                        help="File with list of translation between islands-id and Liu-id after translation",
                        metavar="TRANSLATOR", default="aliases.txt")

    parser.add_argument("-q", "--quiet",
                        action="store_false", dest="verbose",
                        help="Don't print status messages to stdout")

    args = parser.parse_args()
    quiet = not args.verbose
    if not quiet:
        print("input:", args.input)
        print("output:", args.output)
        print("translator:", args.translator)
    input_file = codecs.open(args.input, 'r', args.input_encoding)
    output = open(args.output, 'w')
    translator = open(args.translator, 'r')
    trans_dict = {}
    pattern = re.compile("^([A-Za-z0-9=]+)$")

    for line in translator:
        line = line.replace("\n", "")
        if pattern.match(line):
            line = line.replace("\n", "")
            tmp = line.split('=')
            trans_dict[tmp[0]] = tmp[1]
        else:
            if not quiet:
                print("Error when reading translator line:", line)
    translator.close()
    islands_idn = []
    for line in input_file:
        try:
            if args.input_separator:
                islands_idn.append(line.split(args.input_separator)[args.input_column-1].replace('"', ''))
            else:
                islands_idn.append(line)
        except:
            if not quiet:
                print("Error when parsing line:", line)
    input_file.close()
    liu_id_list = []
    for il in islands_idn:
        try:
            liu_id_list.append(trans_dict[il])
        except:
            if not quiet:
                print("Error when translating following islands-id:", il)

    for li in liu_id_list:
        output.write(li+'\n')

    output.close()
if __name__ == "__main__":
    main(sys.argv[1:])
