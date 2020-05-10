#!/usr/bin/env python
# coding: utf-8

# In[47]:


import requests
from bs4 import BeautifulSoup as bs
import re
from afinn import Afinn
import pandas as pd
import numpy as np
import seaborn as sb


# In[3]:


General_Knowledge_book_reviews = []
for i in range(1,100):
    page_reviews=[] #list to iterate within page
    url = "https://www.amazon.in/General-Knowledge-Dr-Binay-Karna/product-reviews/9384761540/ref=cm_cr_arp_d_paging_btm_next_2?ie=UTF8&reviewerType=all_reviews&pageNumber="+str(i)
    response = requests.get(url)
    soup=bs(response.content,"html.parser")
    reviews = soup.findAll("span",attrs={"class","a-size-base review-text review-text-content"})
    for j in range(len(reviews)):
        page_reviews.append(reviews[j].text)
    General_Knowledge_book_reviews = General_Knowledge_book_reviews+page_reviews


# In[4]:


len(General_Knowledge_book_reviews)


# In[5]:


type(General_Knowledge_book_reviews)


# In[ ]:


# with open("GeneralKnowledgebookReviews.txt","w",encoding="utf8") as output:
#     output.write(str(General_Knowledge_book_reviews))


# In[6]:


General_Knowledge_book_reviews


# In[ ]:


#Cleaning the reviews list


# In[7]:


General_Knowledge_book_reviews_2 = []
for sent in General_Knowledge_book_reviews:
    sent = re.sub("[^A-Za-z" "]+"," ",sent).lower()
    sent = re.sub("[0-9" "]"," ",sent).strip()
    General_Knowledge_book_reviews_2.append(sent)
General_Knowledge_book_reviews_2 = list(filter(None,General_Knowledge_book_reviews_2))
General_Knowledge_book_reviews_2


# In[ ]:


#Let's use affin lexicon and do the sentiment analysis


# In[8]:


af = Afinn()


# In[9]:


sentiment_scores = [af.score(review) for review in General_Knowledge_book_reviews_2]
sentiment_scores


# In[10]:


sentiment_category = ['positive' if score > 0 
                          else 'negative' if score < 0 
                              else 'neutral' 
                                  for score in sentiment_scores]


# In[11]:


General_Knowledge_book_reviews_df = pd.DataFrame(np.column_stack([sentiment_scores,sentiment_category]),columns=['sentiment_scores','sentiment_category'])
General_Knowledge_book_reviews_df


# In[12]:


General_Knowledge_book_reviews_df.describe()


# In[45]:


Overall_sentiment = (General_Knowledge_book_reviews_df['sentiment_scores'].astype(float)).mean()
Overall_sentiment


# In[48]:


fc = sns.factorplot(x="sentiment_category", hue="sentiment_category", 
                    data=General_Knowledge_book_reviews_df, kind="count", 
                    palette={"negative": "#FE2020", 
                             "positive": "#BADD07", 
                             "neutral": "#68BFF5"})


# In[49]:


#Most negative and most positive review


# In[52]:


General_Knowledge_book_reviews_2[sentiment_scores.index(max(sentiment_scores))]


# In[53]:


# most negative review


# In[54]:


General_Knowledge_book_reviews_2[sentiment_scores.index(min(sentiment_scores))]

