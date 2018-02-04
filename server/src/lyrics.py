from konlpy.tag import Twitter
from pprint import pprint
import nltk
import csv 

pos_tagger = Twitter()
data = []
def tokenize(doc):
    # norm, stem은 optional
    return ['/'.join(t) for t in pos_tagger.pos(doc, norm=True, stem=True)]
    
def get_frequency(data):
    docs = [tokenize(row) for row in data]
    tokens = [t for d in docs for t in d]
    text = nltk.Text(tokens, name='NMSC')
    #pprint(docs)
    print(text)
    print(type(text))
    #token_str = list(map(lambda x: x[0], text.vocab().most_common(1000)))
    temp = list(filter(lambda x : 'Verb' in x[0] or
                    'Adjective' in x[0] or
                    ('Noun' in x[0] and len(x[0])>6),
        text.vocab().most_common(1000)))
    pprint(temp)
    result = []
    
    for x in temp:
        result.append({
                    'word': x[0],
                    'value': x[1]
        })
    #print(len(set(text.tokens)))
    #pprint(text.vocab().most_common(100)[50:])
    #pprint(text.vocab().most_common(100))
    #verbs = list(filter(lambda x : 'Verb' in x , token_str))
    #adjective = list(filter(lambda x : 'Adjective' in x , token_str))
    #noun = list(filter(lambda x : 'Noun' in x and len(x)>6 , token_str))
    #pprint(verbs)
    #pprint(adjective)
    pprint(result)
    
    return result

#with open('../../static/csv/detail.csv', 'r') as f:
#    reader = csv.DictReader(f)
#    for row in reader:
        #print(row.get('lyric'))
#        data.append(row.get('lyric'))
    #print(len(data))    
    
#get_frequency(data)