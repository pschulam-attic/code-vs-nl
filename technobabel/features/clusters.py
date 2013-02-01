clusDict = {}
for line in open('joint_c100.txt','r'):
    word, cluster = line.split()
    clusDict[word] = cluster
    
def clus_list(post):
        
    for word in post['tokenized_text']:
        yield clusDict[word], 1
