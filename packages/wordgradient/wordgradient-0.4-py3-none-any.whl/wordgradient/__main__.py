from rich.console import Console
from rich_gradient import Gradient
import argparse
from wordgradient._csv_reader import CSVReader
import sys
from wordgradient.__init__ import __VERSION__
import re

# Module entrypoint

def main():
    
    console = Console()
    argparser = argparse.ArgumentParser(
        prog='WordGradient',
        description='''
        Minimal CLI tool to create language frequency heatmap. 
        ''',
        epilog='https://github.com/ctosullivan/WordGradient'
        )
    
    argparser.add_argument('-i','--inverse',help='inverts the language frequency gradient - most uncommon words are output first',action='store_true')
    argparser.add_argument('-r','--rainbow',help='outputs word ordered by language frequency in a random rainbow spectrum of colours',action='store_true')
    argparser.add_argument('-hd','--head',help='outputs a gradient of the top ten words ordered by language frequency',action='store_true')
    argparser.add_argument('-t','--tail',help='outputs a gradient of the bottom ten words ordered by language frequency',action='store_true')
    argparser.add_argument('-v','--version',help='outputs version info and exits',action='store_true')
    argparser.add_argument('words',nargs='*',help="Example usage: wordgradient lots of words to be sorted")
    argparser.add_argument('stdin', nargs='?', type=argparse.FileType('r'), default=sys.stdin,help="Example usage: echo lots of words to be sorted | wordgradient")
    cli_args= argparser.parse_args()
    
    unsorted_words = []

    def validate_word_args(word_arg_list=list) -> list:
        '''
        Function that takes a list of word arguments, splits lines by whitespace and removes non-alpha characters, converting to uppercase
        Args:
            word_arg_list: a list of word arguments that may include non-alpha characters and whitespace
        Returns:
            A list of uppercase strings without whitespace & non-alpha characters

        '''
        validated_word_list = []
        for line in word_arg_list:
            line = line.split()
            for item in line:
                item = item.split()
                for word in item:
                    non_alpha_regex = re.compile(r'[^a-zA-Z]')
                    word = re.sub(non_alpha_regex,"",word)
                    validated_word_list.append(word.upper())
        return validated_word_list


    if cli_args.words:
        unsorted_words = validate_word_args(cli_args.words)
        
    #Credit - https://stackoverflow.com/a/53541456
    elif not sys.stdin.isatty():
        word_file = cli_args.stdin.readlines()
        unsorted_words = validate_word_args(word_file)

    if cli_args.version:
        print(f"Version is wordgradient {__VERSION__}")
        print("Copyright (C) Cormac O' Sullivan 2024")
        print("License - MIT - https://github.com/ctosullivan/WordGradient/blob/master/LICENSE")
        print("This is free software: you are free to change and redistribute it")
        print("There is NO WARRANTY, to the extent permitted by law")
        sys.exit(0)

    if not unsorted_words:
        print("No word arguments provided: try wordgradient -h for help")
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

    # Output & colour options

    if cli_args.rainbow:
        output_colours = None
    elif cli_args.head:
        output_colours = ["greenyellow", "lime"]
        sorted_word_list = sorted_word_list[0:10]
    elif cli_args.tail:
        output_colours = ["tomato", "red"]
        sorted_word_list = sorted_word_list[-10:]
    elif cli_args.inverse:
        output_colours = ["red", "lime"]
    else:
        output_colours = ["lime", "red"]

    console.print(Gradient('\n'.join(sorted_word_list), rainbow=cli_args.rainbow,colors=output_colours))

if __name__ == "__main__":
    main()