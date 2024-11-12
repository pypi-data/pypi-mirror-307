import sys
import csv

try:
    from importlib import resources as impresources
except ImportError:
    # Try backported to PY<3.7 `importlib_resources`.
    import importlib_resources as impresources
from . import wordlist


class CSVReader:
    '''
    A context manager to handle csv opening, reading and closure.
    Returns: 
        A dict of word|frequency pairs
    Raises:
        FileNotFoundError - if the csv file cannot be found
        IOError - if an I/O related error occurs during file opening
        Exception - if an unexpected error occurs

    # Credits - https://realpython.com/python-magic-methods/handling-setup-and-teardown-with-context-managers
    - https://stackoverflow.com/a/20885799
    '''

    def __init__(self, encoding="utf-8",file_path=(impresources.files(wordlist) / 'unigram_freq.csv')) -> None:
        self.file_path = file_path
        self.encoding = encoding
        self.word_dict = {}

    def __enter__(self) -> dict:
        try:
            self.file_obj = open(self.file_path, mode="r", encoding=self.encoding)
            csv_file = csv.reader(self.file_obj, delimiter=',', quotechar='|')
            for row in csv_file:
                self.word_dict[row[0].upper()] = row[1]
            return self.word_dict
        except AttributeError:
            # Python < PY3.9, fall back to method deprecated in PY3.11.
            template = impresources.read_text(wordlist, 'unigram_freq.csv')
            # or for a file-like stream:
            template = impresources.open_text(wordlist, 'unigram_freq.csv')

        
        except FileNotFoundError:
            print(f"Error: The file '{self.file_path}' was not found.")
            sys.exit(1)
        
        except IOError:
            print(f"Error: An I/O error occurred while reading the file '{self.file_path}'.")
            sys.exit(1)
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
            sys.exit(1)

    def __exit__(self, exception_type, exception_value, traceback):
        self.file_obj.close()