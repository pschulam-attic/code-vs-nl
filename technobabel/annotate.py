import sys
from classifier import read_qas

def main():
    fn = sys.argv[1]
    translate = {'mixed' : 'NC', 'pre' : 'C', 'nl' : 'N'}
    sep = ('-'*30) + 'BLOCK' + ('-'*30)
    for text_dict, label in read_qas(fn):
        print '{}{}'.format(translate[label], sep)
        print
        print text_dict['text']
        print

if __name__ == '__main__': main()
