'''
Created on 9 Apr 2018
'''
from nltk import CFG, ChartParser

def context_free_grammar():
    cfg = CFG.fromstring("""\
    S -> NP VP
    S -> PP NP VP 
    NP -> ProperNoun | CC ProperNoun | N | ProperNoun NP | AP N | DET NP | N PP    
    VP -> V | V NP | Adv VP | V NP VP
    AP -> Adj | Adj AP
    PP -> P NP | P NP VP 
    N -> 'milk'| 'shoes' | 'salad' | 'thinks' | 'kitchen' | 'midnight' | 'table'
    V -> 'laughs' | 'laughed' | 'drink' | 'wears' | 'serves' | 'drinks' | 'thinks' | 'does' | 'do' | 'wear'
    ProperNoun -> 'Bart' | 'Homer' | 'Lisa'
    CC -> 'and'
    Adj -> 'blue' | 'healthy' | 'green' 
    DET -> 'a' | 'the' 
    Adv -> 'always' | 'never' | 'when' 
    P -> 'in' | 'before' | 'on' | 'when'
    """)
    cfparser = ChartParser(cfg)
    text = """\
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
    """
    sents = text.splitlines()
    for sent in sents:
        parses = cfparser.parse(sent.split())
        print(sent)
        for tree in parses:
            print(tree)

if __name__ == '__main__':
    context_free_grammar()