from rich.console import Console
from rich_gradient import Gradient
import argparse
from wordgradient._csv_reader import CSVReader
import sys

# Module entrypoint

def main():
    
    console = Console()
    argparser = argparse.ArgumentParser(
        prog='WordGradient',
        description='Minimal CLI tool to create word frequency heatmap',
        epilog='https://github.com/ctosullivan/WordGradient'
        )

    argparser.add_argument('-i','--inverse',help='inverts the word frequency gradient - most uncommon words are coloured green',action='store_true')
    argparser.add_argument('word_args',nargs='?')
    argparser.add_argument('infile', nargs='?', type=argparse.FileType('r'), default=sys.stdin)
    cli_args= argparser.parse_args()

    unsorted_words = []

    if cli_args.word_args:
        unsorted_words = cli_args.word_args.split()

    #Credit - https://stackoverflow.com/a/53541456
    elif not sys.stdin.isatty():
        file = cli_args.infile.readlines()
        for line in file:
            line = line.split()
            for item in line:
                unsorted_words.append(item)

    if not unsorted_words:
        print("No arguments provided: try wordgradient -h for help")
        sys.exit(0)

    with CSVReader() as word_frequency_dict:
        word_frequency_dict = word_frequency_dict

    cli_word_args_dict = {}

    for word in unsorted_words:
        word = word.upper()
        if word in word_frequency_dict:
            cli_word_args_dict[word] = word_frequency_dict[word]
        else:
            cli_word_args_dict[word] = "1"

    sorted_word_list = [item[0] for item in list(sorted(cli_word_args_dict.items(), key=lambda item: int(item[1]),reverse=not cli_args.inverse))]

    console.print(Gradient('\n'.join(sorted_word_list),colors=["lime", "red"]))

if __name__ == "__main__":
    main()