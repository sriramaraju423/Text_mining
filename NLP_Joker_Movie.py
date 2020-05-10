#!/usr/bin/env python
# coding: utf-8

# In[28]:


import requests
from bs4 import BeautifulSoup as bs
import re
from afinn import Afinn
import pandas as pd
import numpy as np
import seaborn as sb


# In[7]:


Joker_Movie_Reviews = []
page_reviews=[] #list to iterate within page
url = "https://www.imdb.com/title/tt7286456/reviews?ref_=tt_ov_rt"
response = requests.get(url)
soup=bs(response.content,"html.parser")
reviews = soup.findAll("div",attrs={"class","text show-more__control"})
for j in range(len(reviews)):
    page_reviews.append(reviews[j].text)
Joker_Movie_Reviews = Joker_Movie_Reviews+page_reviews


# In[10]:


Joker_Movie_Reviews


# In[9]:


len(Joker_Movie_Reviews)


# In[ ]:


#This code just pulls the top 25 as reviews on imdb won't be available as pages. THere will be a load more option and then we can load all the reviews. FOr this i may need to write trigger. Which i will be doing at later point of time


# In[11]:


#Cleaning the reviews list


# In[14]:


Joker_Movie_Reviews_2 = []
for sent in Joker_Movie_Reviews:
    sent = re.sub("[^A-Za-z" "]+"," ",sent).lower()
    sent = re.sub("[0-9" "]"," ",sent).strip()
    Joker_Movie_Reviews_2.append(sent)
Joker_Movie_Reviews_2 = list(filter(None,Joker_Movie_Reviews_2))
Joker_Movie_Reviews_2


# In[15]:


#Let's use affin lexicon and do the sentiment analysis


# In[18]:


af = Afinn()


# In[19]:


sentiment_scores = [af.score(review) for review in Joker_Movie_Reviews_2]
sentiment_scores


# In[20]:


sentiment_category = ['positive' if score > 0 
                          else 'negative' if score < 0 
                              else 'neutral' 
                                  for score in sentiment_scores]


# In[25]:


Joker_Movie_Reviews_df = pd.DataFrame(np.column_stack([sentiment_scores,sentiment_category]),columns=['sentiment_scores','sentiment_category'])
Joker_Movie_Reviews_df


# In[26]:


Joker_Movie_Reviews_df.describe()


# In[27]:


Overall_sentiment = (Joker_Movie_Reviews_df['sentiment_scores'].astype(float)).mean()
Overall_sentiment


# In[30]:


fc = sb.factorplot(x="sentiment_category", hue="sentiment_category", 
                    data=Joker_Movie_Reviews_df, kind="count", 
                    palette={"negative": "#FE2020", 
                             "positive": "#BADD07", 
                             "neutral": "#68BFF5"})


# In[31]:


#Most negative and most positive review


# In[32]:


Joker_Movie_Reviews_2[sentiment_scores.index(min(sentiment_scores))]


# In[33]:


Joker_Movie_Reviews_2[sentiment_scores.index(max(sentiment_scores))]

