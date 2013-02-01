import re

digit_re = re.compile('[0-9]')
letter_re = re.compile('\w', re.UNICODE)
upper_re = re.compile('^[A-Z]+$')

def gen_lexical_features(post):
    '''gen_lexical_features(post) -> iteratable over feature-value pairs'''
    for word in post['text'].split():
        yield 'length='+str(len(word)), 1 # word lengths

        if digit_re.search(word) and letter_re.search(word):
            yield 'alpha_numeric_mix', 1 # any words with alpha/numeric mix?

        if upper_re.match(word):
            yield 'all_uppercase', 1 # all uppercase word

        if digit_re.search(word):
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
