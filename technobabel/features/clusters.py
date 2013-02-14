clusDict = dict(l.strip().split() for l in open('joint_c100.txt'))
    
def clus_list(post):
    for word in post['tokenized_text']:
        yield clusDict[word], 1
