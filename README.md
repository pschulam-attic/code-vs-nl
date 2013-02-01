# code-vs-nl

Stackoverflow experiments

## Requirements

- Python 2.7
- lxml
- [creg](http://github.com/redpony/creg)

## Usage
```bash
export DATA=/mal2/corpora/stackexchange/12aug
python -m technobabel.classifier $DATA/train/questions.json $DATA/dev/questions.json $DATA/test/questions.json
```
