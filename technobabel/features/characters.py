from itertools import izip

def char_unigram(post):
    for c in post['text']:
        yield '1c_'+c, 1

def char_bigram(post):
    it1, it2 = iter(post['text']), iter(post['text'])
    next(it2)
    for c1, c2 in izip(it1, it2):
        yield '2c_'+c1+'_'+c2, 1

def char_trigram(post):
    it1, it2, it3 = iter(post['text']), iter(post['text']), iter(post['text'])
    next(it2)
    next(it3)
    next(it3)
    for c1, c2, c3 in izip(it1, it2, it3):
        yield '3c_'+c1+'_'+c2+'_'+c3, 1
