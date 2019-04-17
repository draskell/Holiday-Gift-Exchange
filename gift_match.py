import os
import yaml

from numpy.random import shuffle

def get_gifter_matches(number_of_gifters):
    '''Makes a matchup of gifters to giftees.
    '''
    give = range(number_of_gifters)
    get = range(number_of_gifters)
    shuffle(give)
    shuffle(get)
    return zip(give,get)

def has_recipricals(pairs):
    '''Tests if any pair of pairs consist of two gifters giving
    back and forth.

    TODO: this should be using sets probably.
    '''
    ascending_pairs = []
    for i, pair in enumerate(pairs):
        # TODO: does this make sense?
        if pair[0] > pair[1]:
            ascending_pairs.append((pair[1],pair[0]))
        else:
            ascending_pairs.append(pair)
    if len(pairs) != len(set(ascending_pairs)):
        return True
    return False

def has_disallowed_pairs(pairs, config):
    '''Tests if any of the pairs are in the disallowed pairs
    set in the configuration.

    TODO: should be testing sets of tuples for intersection
    '''
    names = config['name_map']
    num_sets = []    
    for pair in config['no_match_pairs']:
        num_sets.append(set([names.index(pair[0]),names.index(pair[1])]))
    for pair in pairs:
        if set(pair) in num_sets:
            return True
    return False

def has_bad_pairs(pairs, config):
    '''Wrapper on all pair failure tests.
    '''
    # Check for giver/givee pairs that are the same name
    if len([pair for pair in pairs if pair[0] == pair[1]]) > 0:
        return True
    if has_recipricals(pairs):
        return True
    if has_disallowed_pairs(pairs, config):
        return True
    return False
