#!/usr/bin/env python
import json
import lxml.html
import argparse
from itertools import chain

def extract_block(block):
    text = block.text_content()
    label = ('pre' if block.tag == 'pre' else 
            ('mixed' if block.find('.//code') else 'nl'))
    return text, label

def read_qas(fn):
    with open(fn) as f:
        for line in f:
            item = json.loads(line)
            body = item['Body']
            body_element = lxml.html.fragment_fromstring(body, create_parent='post')
            for text, label in map(extract_block, body_element):
                yield {'text': text}, label

from features.words import unigram

FEATURES = [unigram]

def main():
    parser = argparse.ArgumentParser(description='Train classifier')
    parser.add_argument('data', help='Data path')
    args = parser.parse_args()

    for post, label in read_qas(args.data+'/questions_with_user.json'):
        features = dict(chain.from_iterable(f(post) for f in FEATURES))
        print features, label

if __name__ == '__main__':
    main()
