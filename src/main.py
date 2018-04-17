'''
Created on 9 Apr 2018
'''
from nltk import CFG, ChartParser
from nltk.grammar import FeatureGrammar
from nltk import FeatureChartParser

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
text_extended = """\
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
    Bart thinks Lisa drinks milk on the table
    
    Bart likes drinking milk
    Lisa may have drunk milk
    Lisa may have seen Bart drinking milk
    Lisa may not have seen Bart drinking milk
    what does Homer drink
    what salad does Bart serve
    whom does Homer serve salad
    whom do Homer and Lisa serve
    """

def context_free_grammar():
    cfg = CFG.fromstring("""\
    ################# Rules #################
    S -> NP VP
    S -> PP NP VP
    S -> Wh Aux NP VP 
    NP -> ProperNoun | CC ProperNoun | N | ProperNoun NP | AP N | DET NP | N PP    
    VP -> V | V NP | Adv VP | V NP VP
    AP -> Adj | Adj AP
    PP -> P NP | P NP VP
    
    ################# Lexicons ################# 
    N -> 'milk'| 'shoes' | 'salad' | 'kitchen' | 'midnight' | 'table'
    V -> 'laughs' | 'laughed' | 'drink' | 'wears' | 'serves' | 'drinks' | 'thinks' | 'wear'
    ProperNoun -> 'Bart' | 'Homer' | 'Lisa'
    Aux -> 'do' | 'does'
    CC -> 'and'
    Adj -> 'blue' | 'healthy' | 'green' 
    DET -> 'a' | 'the' 
    Adv -> 'always' | 'never' 
    P -> 'in' | 'before' | 'on' | 'when'
    Wh -> 'when'
    """)
    cfparser = ChartParser(cfg)
    sents = text.splitlines()
    for sent in sents:
        parses = cfparser.parse(sent.split())
        print(sent)
        for tree in parses:
            print(tree)
            
def unification_grammar():
    ugrammar = FeatureGrammar.fromstring("""\
    ################### RULES #################
    S -> NP[NUM=?n] VP[NUM=?n]
    S -> PREP_P S
    S -> Wh_P AUX[NUM=?n] NP VP
    
    NP[NUM=?n] -> ProperNoun[NUM=?n] | CC ProperNoun[NUM=?n] | ProperNoun[NUM=?n] NP[NUM=?n]
    NP[NUM=?n] -> N[NUM=?n] | ADJ_P NP[NUM=?n] | DET[NUM=?n] NP[NUM=?n] | N[NUM=?n] PREP_P
     
    VP[SUBCAT=?rest] -> V[NUM=?n, SUBCAT=?rest] | VP[TENSE=?t, SUBCAT=[HEAD=?arg, TAIL=?rest]] ARG[CAT=?arg]
    VP[SUBCAT=?rest] -> ADV_P V[NUM=?n, SUBCAT=?rest] | V[NUM=?n, SUBCAT=?rest] ADV_P 
    
    ADJ_P -> ADJ | ADJ AP
    ADV_P -> ADV | ADV ADV_P

    PREP_P -> PREP NP | PREP S
    MOD_P -> MOD AUX[NUM=pl] |  MOD ADV AUX[NUM=pl]
    Wh_P -> Wh | Wh ARG[CAT=?arg] 
    
    ################# Lexicons #################
    ################## NOUN ###################
    ###########################################
    ProperNoun[NUM=sg] -> 'Homer' | 'Bart' | 'Lisa'
    N[NUM=sg] -> 'milk' | 'salad' | 'midnight' | 'kitchen' | 'table' 
    N[NUM=pl] -> 'shoes' | 'tables'
    
    ################# VERB ####################
    ###########################################
    
    ############### PRESENT ###################
    #########----- Intransitive -----##########
    V[TENSE=pres, NUM=sg, SUBCAT=nil]-> 'laughs' | 'smiles' | 'walks' | 'serves' | 'drinks'
    V[TENSE=pres, NUM=pl, SUBCAT=nil] -> 'laugh' | 'smile' | 'walk' | 'serve' |'drink'
    
    #########----- Transitive ------###########
    V[TENSE=pres, NUM=sg, SUBCAT=[HEAD=s,TAIL=nil]] -> 'thinks' | 'believes'
    V[TENSE=pres, NUM=pl, SUBCAT=[HEAD=s,TAIL=nil]] -> 'think' | 'believe'
    
    V[TENSE=pres, NUM=sg, SUBCAT=[HEAD=np,TAIL=nil]] ->'serves' | 'drinks' | 'wears' | 'likes' 
    V[TENSE=pres, NUM=pl, SUBCAT=[HEAD=np,TAIL=nil]] ->'serve' | 'drink' | 'wear' | 'like'
    
    V[TENSE=pres, NUM=sg, SUBCAT=[HEAD=pp,TAIL=nil]] ->'walks' | 'teaches' 
    V[TENSE=pres, NUM=pl, SUBCAT=[HEAD=pp,TAIL=nil]] ->'walk' | 'teach' 
    
    ######### primary & secondary ########
    V[TENSE=pres, NUM=sg, SUBCAT=[HEAD=np, TAIL=[HEAD=np,TAIL=nil]]] -> 'serves'
    V[TENSE=pres, NUM=pl, SUBCAT=[HEAD=np, TAIL=[HEAD=np,TAIL=nil]]] -> 'serve'
    V[TENSE=pres, NUM=pl, SUBCAT=[HEAD=s, TAIL=[HEAD=np,TAIL=nil]]] -> 'think' | 'believe'
    
    ################# Past ####################
    #########----- Intransitive -----##########
    V[TENSE=past, SUBCAT=nil] -> 'laughed' | 'smiled' | 'walked'
    
    #########----- Transitive ------###########
    V[TENSE=past, SUBCAT=[HEAD=np,TAIL=nil]] -> 'drank' | 'wore' | 'served'
    V[TENSE=pastpart, SUBCAT=[HEAD=np,TAIL=nil]] ->'drunk' | 'worn' | 'served' | 'seen'
    
    ################ Determiner ###############
    DET[NUM=sg] -> 'a' | 'the' | 'that'
    DET[NUM=pl] -> 'the' | 'these' | 'those'
    
    ################ Conjunction ##############
    CC -> 'and'
    
    ############ Adverb & Adjective ############
    ADJ -> 'blue' | 'healthy' | 'green' | 'same'
    ADV -> 'always' | 'never' | 'intensely' | 'not'
    
    ############## Preposition ##################
    PREP -> 'in' | 'before' | 'when' | 'on' | 'beyond'
    
    AUX[NUM=sg] -> 'does' | 'has'
    AUX[NUM=pl] -> 'do' | 'have'
    VTB[NUM=sg] -> 'is'
    VTB[NUM=pl] -> 'are'
    
    Wh -> 'when' | 'what' | 'where' | 'whom'
    
    ARG[CAT=np] -> NP
    ARG[CAT=pp] -> PP
    ARG[CAT=s] -> S
    """)
    uparser = FeatureChartParser(ugrammar)
    sents = text_extended.splitlines()
    for sent in sents:
        parses = uparser.parse(sent.split())
        print(sent)
        for tree in parses:
            print(tree)

if __name__ == '__main__':
#     context_free_grammar()
    unification_grammar()