import re

tokenizer = re.compile('([^\s\w]|\w+)', re.UNICODE)

def tokenize(text):
    return tokenizer.findall(text.lower())
