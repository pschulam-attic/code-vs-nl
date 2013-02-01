import sys
from classifier import read_qas

def main():
    fn = sys.argv[1]
    sep = ('-'*30) + 'BLOCK' + ('-'*30)
    for text_dict, _ in read_qas(fn):
        print sep
        print
        print text_dict['text']
        print

if __name__ == '__main__': main()
