import re
import random
#nltk.download('stopwords')
from nltk.corpus import stopwords
stoplist = stopwords.words('english')


def preprocess(twt):
    #removing all hashtags  URl and timestamp
    twt = re.sub('RT\W(\S+):','', twt)
    twt = re.sub('@\w(\S+)','', twt)
    twt = re.sub('http\W(\S+)','', twt)
    twt = re.sub('[-!~@$%&*=+_{()}\\[\\],.<>;:#\'\'\"\"]','', twt)
    twt = re.sub('^\s+','', twt)
    twt = re.sub('\s+$','', twt)
    tweet= twt.lower()
    tweet_str = [i for i in tweet.split() if i not in stoplist]
    return ' '.join(tweet_str)

def init_cluster(centroids):
    cen_dict = {}
    for cen in centroids:
        cen_dict[cen] = [cen]
    for i in range(0, len(tweetarr)):
        min = 1
        cluster_id = 0
        flag = 0
        for j in range(0, len(centroids)):
            if tweetarr[i] not in centroids:
                flag = 1
                textline1 = tweetarr[i]
                textline2 = centroids[j]
                dist = JaccardDistance(textline1, textline2)
                if dist < min:
                    min = dist
                    cluster_id = j
        if flag == 1:
            temp = cen_dict[centroids[cluster_id]]
            temp = temp.append(tweetarr[i])


    return cen_dict
# for updating centroids
def update(cen_dict, centroids):
    newcentroids = []
    for cen in centroids:
        temp = cen_dict[cen]
        min = 1000
        for i in range(0, len(temp)):
            sum = 0
            for j in range(0, len(temp)):
                text1 = temp[i]
                text2 = temp[j]
                sum = sum + JaccardDistance(text1, text2)
            if sum < min:
                min = sum
                tempcent = temp[i]

        newcentroids.append(tempcent)
    return newcentroids

def sse(cen_dict, centroids):
    total = 0
    for c in centroids:
        t = cen_dict[c]
        s = 0
        for i in range(0, len(t)):
            if t[i] != c:
                compareText1 = c
                compareText2 = t[i]
                j = JaccardDistance(compareText1, compareText2)
                s = s + pow(j,2)
        total += s
    return total

def JaccardDistance(x, y):
    intersection = set(x).intersection(set(y))
    union = set(x).union(set(y))
    jaccarddist = len(intersection)/len(union)
    return jaccarddist

#k-means implementation
def tweetKmeans(tweetDataFile, numberOfClusters):
    obj = open(tweetDataFile,"r")
    
    for i in obj:
        text_part = i.split('|')
        tweet = preprocess(text_part[2])
        tweetarr.append(tweet)

    for i in range(int(numberOfClusters)):
        j = random.randint(1,3000) #3929
        centroids.append(tweetarr[j])
      
    #centroid dictionary with ids of cluster

    cen_dict = init_cluster(centroids)
    oldcentroids = []
    newcentroids = centroids
    i = 0
    while oldcentroids != newcentroids:
        oldcentroids = newcentroids
        cen_dict = init_cluster(oldcentroids)

        SSE = sse(cen_dict, oldcentroids)
        print("calculating SSE...",SSE)
        newcentroids = update(cen_dict, oldcentroids)

        i += 1


    cen_dict = init_cluster(newcentroids)
    SSE = sse(cen_dict, newcentroids)
    print("For Number of Clusters: ",numberOfClusters,"  SSE: ",SSE)

    for key, value in cen_dict.items():
       print(key, len([item for item in value if item]))




tweetarr = []
centroids = []

if __name__ == "__main__":

    tweetarr = []
    for k in range(5,10,1):
        tweetDataFile = 'msnhealthnews.txt'
        tweetKmeans(tweetDataFile,k)