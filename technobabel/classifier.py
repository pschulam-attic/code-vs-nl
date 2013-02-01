#!/usr/bin/env python
import json
import argparse
import heapq
import logging
import lxml.html
from collections import Counter
import creg
import pprint
import random

from tokenizer import tokenize

def extract_block(block):
    text = block.text_content()
    label = ('pre' if block.tag == 'pre' else
            ('mixed' if block.find('.//code') is not None else 'nl'))
    return text, label

def read_qas(fn):
    with open(fn) as f:
        for line in f:
            item = json.loads(line)
            body = item['Body']
            body_element = lxml.html.fragment_fromstring(body, create_parent='post')
            for text, label in map(extract_block, body_element):
                yield {'text': text, 'tokenized_text': tokenize(text)}, label

from features.words import unigram
from features.lexical import gen_lexical_features

FEATURES = [unigram, gen_lexical_features]

def main():
    logging.basicConfig(level=logging.INFO)
    parser = argparse.ArgumentParser(description='Train classifier')
    parser.add_argument('train', help='Training dataset')
    parser.add_argument('dev', help='Development dataset')
    parser.add_argument('test', help='Evaluation dataset')
    parser.add_argument('--ptrain', help='Percentage of training posts', type=float, default=None)
    parser.add_argument('--pdev', help='Percentage of development posts', type=float, default=None)
    parser.add_argument('--ptest', help='Percentage of evaluation posts', type=float, default=None)
    parser.add_argument('--ntrain', help='Number of training posts', type=int, default=1000)
    parser.add_argument('--ndev', help='Number of development posts', type=int, default=1000)
    parser.add_argument('--ntest', help='Number of evaluation posts', type=int, default=1000)
    args = parser.parse_args()

    def dataset(fn, n_instances, p_keep=None, class_order=None, rand=random.random):
        if class_order:
            for cl in class_order:
                yield {}, cl
        for i, (post, label) in enumerate(read_qas(fn)):
            if not p_keep and i > n_instances: break
            elif rand() >= p_keep: continue
            features = Counter()
            for f in FEATURES:
                for fname, fval in f(post):
                    features[fname] += fval
            yield features, label

    logging.info('Extracting features for training set')
    train_data = creg.CategoricalDataset(dataset(args.train, args.ntrain, p_keep=args.ptrain, class_order=('mixed', 'pre', 'nl')))
    model = creg.LogisticRegression(l1=1)
    logging.info('Training classifier')
    model.fit(train_data)

    logging.info('Extracting features for test set')
    test_data = creg.CategoricalDataset(dataset(args.test, args.ntest, p_keep=args.ptest))
    logging.info('Predicting on test data')
    predictions = model.predict(test_data)

    label_dist = Counter(v for _, v in test_data)
    print label_dist
    truth = (y for x, y in test_data)

    errors = sum(1 if pred != real else 0 for (pred, real) in zip(predictions, truth))
    print 'Accuracy: %.3f' % (1-errors/float(len(test_data)))

    pprint.pprint(heapq.nlargest(20, model.weights['pre'].iteritems(), key=lambda t: abs(t[1])))
    pprint.pprint(heapq.nlargest(20, model.weights['mixed'].iteritems(), key=lambda t: abs(t[1])))

if __name__ == '__main__':
    main()
