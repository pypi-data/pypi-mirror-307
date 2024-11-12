# WordGradient

A minimal CLI tool to create a language frequency heat map - useful for solving word games like Wordle and Spelling Bee and filtering uncommon words

Word list credit: https://www.kaggle.com/datasets/rtatman/english-word-frequency

With thanks to the creators of [Rich](https://github.com/Textualize/rich) and [Rich-Gradient](https://pypi.org/project/rich-gradient/).

Options:

-h, --help show this help message and exit

-i, --inverse inverts the language frequency gradient - most uncommon words are output first

-r, --rainbow outputs word ordered by language frequency in a random rainbow spectrum of colours

-hd, --head outputs a gradient of the top ten words ordered by language frequency

-t, --tail outputs a gradient of the bottom ten words ordered by language frequency

-v, --version outputs version info and exits

Installation:

pip install wordgradient

Example usage:

wordgradient lots of words to be sorted

echo "lots of words to be sorted" | wordgradient
