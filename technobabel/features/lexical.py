import string
import re

def gen_lexical_features(clean_post):
    '''gen_lexical_features(clean_post) -> iteratable over feature-value pairs'''
    for word in clean_post.split():
        yield (str(len(word)), 1) # word lengths

        if '_' in word:
            yield 'underscore', 1 # underscore feature

        if any(c in string.digit for c in word) and any(c in string.letters for c in word):
            yield 'alpha_numeric_mix', 1 # any words with alpha/numeric mix?

        if all(c in string.ascii_uppercase for c in word):
            yield 'all_uppercase', 1 # all uppercase word

        if re.search('[0-9]', word):
            yield 'hasdigit', 1
            yield 'collapseddigits=' + re.sub('[0-9]', '#', word), 1
            if not re.match('^[0-9]+$', word):
                yield 'collapsednoninitialdigits=' + re.sub('[0-9]+', '#', word), 1

        if not all(ord(c) < 128 for c in word):
            yield 'contains-nonascii', 1

        shape = word
        if re.sub(r'\w','',word)!=re.sub(r'\w','',word,flags=re.U): # contains Unicode alphabetics
            yield 'unialph', 1
            # re module doesn't provide a way to distinguish upper- vs. lowercase Unicode chars
            shape = ''.join(('X' if c.lower()!=c else ('x' if c.isalpha() else c)) for c in shape)


        # Ciaramita & Altun shape feature
        shape = re.sub(r'[A-Z]{2,}', 'X*', shape)
        shape = re.sub(r'[A-Z]', 'X', shape)
        shape = re.sub(r'[a-z]{2,}', 'x*', shape)
        shape = re.sub(r'[a-z]', 'x', shape)
        shape = re.sub(r'\d{2,}', 'd*', shape)
        shape = re.sub(r'\d', 'd', shape)
        yield 'shape=' + shape, 1



