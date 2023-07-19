# -*- coding: utf-8 -*-
"""
Created on Tue Jul 18 15:34:59 2023

@author: jatin
"""

import pandas as pd
from wordcloud import WordCloud as wc
from wordcloud import STOPWORDS as sw
import matplotlib.pyplot as plt
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer as sia

data=pd.read_excel(r'C:\Users\jatin\Downloads\Python+Tableau Project\BlogMe\articles.xlsx')

data.head()

data.columns

data['content'][2]

#summary of the data
data.describe()

#summary of the columns
data.info()

#no. of unique sources
data['source_name'].value_counts()

data.groupby(['source_name','source_id'])['article_id'].count()

#number of reactions by publishers
data.groupby(['source_name','source_id'])['engagement_reaction_count'].sum()

#dropping the 'engagement_comment_plugin_count' column
del data['engagement_comment_plugin_count']

data[data['title'].isna()==True]

data['title'][3181]='NA'
data['title'][3751]='NA'

words_string = ' '.join(list(data['title']))
wc_1 = wc(stopwords=list(sw)).generate(words_string)
plt.imshow(wc_1)
plt.axis('off')


def keyword(kw):
    lskw = ['murder']
    di={}
    lis = []
    words = list(kw.lower().split(' '))
    for i in lskw:
        di[i]=0
        if i in words:
            di[i]+=words.count(i)
            lis.append(1)
        else:
            lis.append(0)
    print(lis)
    #return di

#to see which articles have the word 'murder' in the title to analyze the engagement reaction
murd_ls = []
for i in data['title']:
    try:
        if 'murder' in i.lower():
            murd_ls.append(1)
        else:
            murd_ls.append(0)
    except:
        murd_ls.append(0)

data['keyword_flag']=pd.Series(murd_ls)

keyword(words_string)

#initialize sia
senti_n = sia()

neg_sent = []
neu_sent = []
pos_sent = []

for i in data['title']:
    try:
        sent = senti_n.polarity_scores(i)
        neg_sent.append(sent['neg'])
        neu_sent.append(sent['neu'])
        pos_sent.append(sent['pos'])
    except:
        neg_sent.append(0)
        neu_sent.append(0)
        pos_sent.append(0)

data['neg_sentiment'] = pd.Series(neg_sent)
data['neu_sentiment'] = pd.Series(neu_sent)
data['pos_sentiment'] = pd.Series(pos_sent)


data.to_excel('blogme_clean.xlsx',sheet_name='blogmedata', index=False)
