import pandas as pd
import numpy as np
import pickle
from afinn import Afinn
import matplotlib.pyplot as plt
import re
import TweetDataCollection as tw
#preprocessing
data=pd.read_csv('demon.csv',header=None)
frame=pd.read_csv('Data.csv',sep='\t',header=None)
newframe=[]
for tweet in data[1]:
    tweet = re.sub(r"^https://t.co/[a-zA-Z0-9]*\s", " ", tweet)
    tweet = re.sub(r"\s+https://t.co/[a-zA-Z0-9]*\s", " ", tweet)
    tweet = re.sub(r"\s+https://t.co/[a-zA-Z0-9]*$", " ", tweet)
    tweet = tweet.lower()
    tweet = re.sub(r"that's","that is",tweet)
    tweet = re.sub(r"there's","there is",tweet)
    tweet = re.sub(r"what's","what is",tweet)
    tweet = re.sub(r"where's","where is",tweet)
    tweet = re.sub(r"it's","it is",tweet)
    tweet = re.sub(r"who's","who is",tweet)
    tweet = re.sub(r"i'm","i am",tweet)
    tweet = re.sub(r"she's","she is",tweet)
    tweet = re.sub(r"he's","he is",tweet)
    tweet = re.sub(r"they're","they are",tweet)
    tweet = re.sub(r"who're","who are",tweet)
    tweet = re.sub(r"ain't","am not",tweet)
    tweet = re.sub(r"wouldn't","would not",tweet)
    tweet = re.sub(r"shouldn't","should not",tweet)
    tweet = re.sub(r"can't","can not",tweet)
    tweet = re.sub(r"couldn't","could not",tweet)
    tweet = re.sub(r"won't","will not",tweet)
    tweet = re.sub(r"\W"," ",tweet)
    tweet = re.sub(r"\d"," ",tweet)
    tweet = re.sub(r"\s+[a-z]\s+"," ",tweet)
    tweet = re.sub(r"\s+[a-z]$"," ",tweet)
    tweet = re.sub(r"^[a-z]\s+"," ",tweet)
    tweet = re.sub(r"\s+"," ",tweet)
    newframe.append(tweet)




#Creating TFIDF Classifier
with open('tfidfmodel.pickle','rb') as f:
    vectorizer = pickle.load(f)
with open('classifier.pickle','rb') as f:
    clf = pickle.load(f)

#Using AFINN Classifier
analyst=Afinn()
lis=np.zeros(len(data))
for num in range(0,len(data)):
    lis[num]=analyst.score(newframe[num])
    if lis[num]==0:
        lis[num]=int(clf.predict(vectorizer.transform([newframe[num]])))
        if lis[num]==0:
            lis[num]=-1
lis = pd.DataFrame(data=lis,index=range(len(lis)))


countdict={}
for num in range(0,len(lis[0].unique())):
    countdict[lis[0].unique()[num]]=0
for num in range(0,len(lis)):
    countdict[lis[0][num]]+=1
x=np.array(list(countdict.keys()))
y=np.array(list(countdict.values()))


print('\n............Common data.................')
count=0
print('Total ratings of tweets:',len(y),' which are',x)
print('Total percentage of positive tweets: ',(countdict[1]+countdict[2]+countdict[3]+countdict[4]+countdict[5]+countdict[7]+countdict[8])/np.sum(y)*100)
print('Total percentage of negative tweets: ',(countdict[-1]+countdict[-2]+countdict[-3]+countdict[-4]+countdict[-5]+countdict[-6]+countdict[-7]+countdict[-8]+countdict[-9])/np.sum(y)*100)
print('Total percentage of extremely negative tweets: ',(countdict[-9]+countdict[-5]+countdict[-6]+countdict[-7]+countdict[-8])/(np.sum(y))*100)
recent=tw.recent()
rating={}
for tweet in recent:
	rate=analyst.score(str(tweet))
	if rate==0:
		rate=int(clf.predict(vectorizer.transform([str(tweet)])))
		if rate==0:
			rate=-1
	if rate in rating:
		rating[rate]+=1
	else:
		rating[rate]=1
x = np.array(list(rating.keys()))
y = np.array(list(rating.values()))
print("Latest sentiment: ",x.dot(y)/np.sum(y))
finalData = pd.Series(y,x)
plot=finalData.plot(kind='bar',title='Rating distribution of tweets',label='Tweet frequency')
plot.set_xlabel('Rating of tweets')
plot.set_ylabel('Frequency of tweets')
plt.show(plot)