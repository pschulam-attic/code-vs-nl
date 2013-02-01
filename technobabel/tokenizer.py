import re

tokenizer = re.compile('\W+', re.UNICODE)

def tokenize(text):
    return tokenizer.split(text.lower())
