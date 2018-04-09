'''
Created on Apr 6, 2018
'''
from nltk.tokenize import word_tokenize
from nltk.tag import pos_tag
import nltk

'''
- NOUN = nouns 
- VERB = verbs 
- ADJ = adjectives 
- ADV = adverbs 
- PRON = pronouns 
- DET = determiners and articles 
- ADP = prepositions and postpositions 
- NUM = numerals 
- CONJ = conjunctions 
- PRT = particles 
- . = punctuation marks 
- X = a catch-all for other categories such as abbreviations or foreign words 
'''

text = '''\
Bart laughs
Homer laughed
Bart and Lisa drink milk
Bart wears blue shoes
Lisa serves Bart a healthy green salad
Homer serves Lisa
Bart always drinks milk
Lisa thinks Homer thinks Bart drinks milk
Homer never drinks milk in the kitchen before midnight
when Homer drinks milk Bart laughs
when does Lisa drink the milk on the table
when do Lisa and Bart wear shoes
'''
sents = text.splitlines()
tagger_lexicon = {}
for sent in sents:
    words = word_tokenize(sent)
    tagged_sent = pos_tag(words)
    for tagged_word in tagged_sent:
        word = tagged_word[0]
        tag =  tagged_word[1]
        if tag not in tagger_lexicon.keys():
            tagger_lexicon[tag] = [word]
        elif word not in tagger_lexicon[tag]:
            tagger_lexicon[tag].append(word)
        else:
            pass
lexicon_dict = {'N': ['milk', 'shoes', 'salad', 'thinks', 'kitchen', 'midnight', 'table'],
                'V': ['laughs', 'laughed', 'drink', 'wears', 'serves', 'drinks', 'thinks', 'does', 'do', 'wear'],
                'ProperNoun': ['Bart', 'Homer', 'Lisa'],
                'CC': ['and'],
                'Adj': ['blue', 'healthy', 'green'], 
                'DET': ['a', 'the'], 
                'Adv': ['always', 'never', 'when'], 
                'P': ['in', 'before', 'on']
                }
print(tagger_lexicon)