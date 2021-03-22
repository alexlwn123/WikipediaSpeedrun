import wikipediaapi as wikipedia
import sys
import string
from collections import Counter
import math
import concurrent.futures

corpus = {}

wiki = wikipedia.Wikipedia('en')

pages = {} # Doc name: wiki page object
TFs = {} # Doc name: Counter
TFIDFs = {} # Doc name: Dict w/ TFIDF vectors 
vocab = Counter() # Entire corpus - Word: count
DFs = Counter # Word: Documents with word


def clean_doc(document):
    return [word for line in document.split('\n') for word in line.translate(str.maketrans('','', string.punctuation)).lower().split()]
    #lines = {int(line[0]): line[1].translate(str.maketrans('', '', string.punctuation)).lower().split() for line in reader}


def get_dfs(tfs):
#   words = [word for line.keys() in tfs.values() for word in 
  return Counter([word for tf in tfs.values() for word in tf.keys()])


def update_tfidfs():
    global TFIDFs
    global DFs
    global vocab
    global TFs

    DFs = get_dfs(TFs)
    idfs = {word: math.log(len(TFs) / count) for word, count in DFs.items()}

    TFIDFs = {title: {word : tfa * idfs[word] for word, tfa in doc_tf.items()} for title, doc_tf in TFs.items()}


def word_ladder(start, target):
    global TFIDFs
    global DFs
    global vocab
    global TFs
    wiki = wikipedia.Wikipedia('en')
    start_page, target_page = wiki.page(start), wiki.page(target)

    if not start_page.exists() or not target_page.exists():
        print('Start and/or Target page does not exist.')
        print('Exiting...')
        sys.exit(1)

    # start_doc, target_doc = clean_doc(start_page.summary), clean_doc(target_page.summary)
    # start_doc, target_doc = clean_doc(start_page.text), clean_doc(target_page.text)

    TFs[target] = add_link(target)[1]
    TFs[start] = add_link(start)[1]
    vocab += TFs[target]
    vocab += TFs[start]
    update_tfidfs()
    curr_page = start_page

    while target not in curr_page.links:
        add_links(curr_page)
        update_tfidfs()
        print(TFIDFs[:3])
        break
        

def add_link(link):
    if ':' in link:
        return
    new_page = wiki.page(link)
    print(link)
    if new_page.exists():
        new_doc = clean_doc(new_page.summary)
        return (link, Counter(new_doc))

def add_links(curr_page):
    global TFs
    global vocab

    with concurrent.futures.ThreadPoolExecutor() as executor:            
        futures = []
        results = {}
        for link in curr_page.links:
            futures.append(executor.submit(add_link, link))
        for future in concurrent.futures.as_completed(futures):
            res = future.result()
            if not res:
                continue
            vocab += res[1] 
            TFs[res[0]] = res[1]



def main():
    start = "Mario"
    target = "WWII"
    word_ladder(start, target)

if __name__ == '__main__':
    main()