from typing import List
from nltk.corpus import wordnet
import nltk
import matplotlib.pyplot as plt
import itertools

import networkx as nx
G = nx.Graph()

try:
    nltk.find('corpora/wordnet')
except LookupError:
    nltk.download('wordnet')
try:
    nltk.find('corpora/omw-1.4')
except LookupError:
    nltk.download('omw-1.4')
    
#Creating a list 

query_list = ["Travel", "trip", 'locomotion', 'motivity']
query_list = [q.lower() for q in query_list]
synonym_dict = dict()

def get_synonyms(query:str) -> List[str]:
    synonyms = []
    for syn in wordnet.synsets(query):
        for lm in syn.lemmas():
            if query != lm.name():
                synonyms.append(lm.name())
    return synonyms

def expand_network(synonym_dict:dict) -> dict:
    """
    For each existing synonym, add its synonmys
    """
    new_items = dict()
    for query in itertools.chain.from_iterable(synonym_dict.values()):
        if query not in synonym_dict.keys():
            new_items[query] = get_synonyms(query)
    synonym_dict.update(new_items)
    return synonym_dict

for query in query_list:
    synonym_dict[query] = get_synonyms(query)

synonym_dict = expand_network(synonym_dict)

# draw network using networkx
for query in synonym_dict.keys():
    for synonym in synonym_dict[query]:
        G.add_edge(query, synonym)
print (G)

nx.draw_networkx(G)
plt.show()