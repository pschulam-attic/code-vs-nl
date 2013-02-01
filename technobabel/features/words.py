def unigram(post):
    for word in post['text'].split():
        yield word, 1
