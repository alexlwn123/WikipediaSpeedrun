import wikipediaapi as wikipedia
import sys

corpus = {}
lines = {int(line[0]): line[1].translate(str.maketrans('', '', string.punctuation)).lower().split() for line in reader}

def word_ladder(start, target):
    wiki = wikipedia.Wikipedia('en')
    start_page, target_page = wiki.page(start), wiki.page(target)

    if start_page.exists() or not target_page.exists():
        print('Start and/or Target page does not exist.')
        print('Exiting...')
        sys.exit(1)

    print()


def main():
    pass

if __name__ == '__main__':
    main()