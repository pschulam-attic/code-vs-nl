def unigram(post):
    for word in post['text'].split():
        yield '1g_'+word, 1
