# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

#import itertools
import random
import numpy as np

email = True

names = ['Dasher',
         'Dancer',
         'Prancer',
         'Vixen',
         'Comet',
         'Cupid',
         'Dunder',
         'Blixem',
         'Rudolph']
            
not_allowed_pairs = [('Vixen','Dunder'),('Dancer','Prancer')]

def find_bad_pairs(names, not_allowed_pairs, pairs):
    num_sets = []    
    for pair in not_allowed_pairs:
        num_sets.append(set([names.index(pair[0]),names.index(pair[1])]))
    for pair in pairs:
        if set(pair) in num_sets:
            return True
    return False

def find_recipricals(pairs):
    ascending_pairs = []
    for i, pair in enumerate(pairs):
        if pair[0] > pair[1]:
            ascending_pairs.append((pair[1],pair[0]))
        else:
            ascending_pairs.append(pair)
    if len(pairs) != len(set(ascending_pairs)):
        return True
    return False

give = range(len(names))
np.random.shuffle(give)
get = range(len(names))
np.random.shuffle(get)
pairs = zip(give,get)
has_bad_pairs = find_bad_pairs(names, not_allowed_pairs, pairs)
has_reciprical_pairs = find_recipricals(pairs)

while (len([pair for pair in pairs if pair[0] == pair[1]]) > 0) or has_bad_pairs or has_reciprical_pairs:
    get = range(len(names))
    np.random.shuffle(get)
    pairs = zip(give,get)
    has_bad_pairs = find_bad_pairs(names, not_allowed_pairs, pairs)
    has_reciprical_pairs = find_recipricals(pairs)

for name in names:
    for pair in pairs:
        if names.index(name) == pair[0]:
            gives = pair[1]
        elif names.index(name) == pair[1]:
            gets = pair[0]
    print name + " gives to " + names[gives] + " and gets from " + names[gets]