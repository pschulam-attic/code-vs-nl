import json
from pprint import pprint
import lxml.html
import sys

from tokenizer import tokenize

inputFile = open(sys.argv[1])

for line in inputFile:
    
    data = json.loads(line)
    body = data['Body']
    body_element = lxml.html.fragment_fromstring(body, create_parent='post')
    body_text = body_element.text_content()
    print ' '.join(tokenize(body_text)).encode('utf8')

inputFile.close()
