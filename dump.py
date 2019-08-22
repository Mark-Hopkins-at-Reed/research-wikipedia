import json
from nltk import sent_tokenize
from os import walk
from os.path import join

def all_filenames(path):
    f = []
    for (dirpath, dirnames, filenames) in walk(path):
        for filename in filenames:
            if filename.startswith('wiki'):
                f.append(join(dirpath, filename))
    return f

def dump_iter(filename):
    with open(filename) as inhandle:
        for line in inhandle:
            document = json.loads(line)            
            yield document['text']
            
def bertify(dump_path, output_file):
    with open(output_file, 'w') as outhandle:
        for dump_file in all_filenames(dump_path):
            for article in dump_iter(dump_file): 
                sents = [sent.strip() for sent in sent_tokenize(article)]
                for sent in sents:                
                    sent = sent.strip()
                    if '\n\n' in sent: # get rid of article's title
                        sent = sent.split('\n\n')[1]
                    if len(sent) > 0:
                        outhandle.write(sent)
                        outhandle.write('\n')
                outhandle.write('\n')
