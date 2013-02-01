def unigram(post):
    for word in post['tokenized_text']:
        if not word: continue
        yield '1g_'+word, 1
