import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)
import matplotlib.pyplot as plt
from pandas import DataFrame
train_df = pd.read_csv('C:/Users/Dell/Downloads/train.csv')
train_text = list(train_df.text)


# !pip install tensorflow

import re

train_curated_text = []
for text in train_text:
    train_curated_text.append( re.sub(r"http\S+", "", str(text)))

from tensorflow.keras.preprocessing.text import Tokenizer
clean_text = []
tokenizer = Tokenizer(50000)
tokenizer.fit_on_texts(train_curated_text)

word_index = tokenizer.word_index

max_length = max([len(text) for text in train_curated_text])
from tensorflow.keras.preprocessing.sequence import pad_sequences


import tweepy as tw
import pandas as pd
import re




def clean_text(list_of_tweets):
  count = 0
  clean_texts = []
  # for tweet in list_of_tweets:
    # link_removed.append( re.sub(r"http\S+", "", str(tweet)))
  for tweet in list_of_tweets:
    count+=1
    clean_texts.append(re.sub(r"(\n)|(#\S+)|(@\S+)|(http\S+)","",str(tweet)))
  return count,clean_texts

def Analyse(text,date):
  consumer_key= 'kMW0xqTbbK0OaASX8hWj4vSmM'
  consumer_secret= 'nnBerO8NkPBVaPXM3xkntuAV0ZXIeksyv0V0bnOA6JKtL1vMgE'
  access_token= '1275779687323590656-YGIfDnzXVTsR1SfFIbIJUdgENMkcb2'
  access_token_secret= 'MkCPPmOURytI4clu0RmrPagcdcjsRznqQx3y12gUwJhKB'
  auth = tw.OAuthHandler(consumer_key, consumer_secret)
  auth.set_access_token(access_token, access_token_secret)
  api = tw.API(auth, wait_on_rate_limit=True)
  print(date,text)
  search_words = text
  date_since = date
  tweets = tw.Cursor(api.search,q=search_words,lang="en",since=date_since).items()
  listoftweet = [tweet.text for tweet in tweets]
  print(listoftweet)

  c,ct = clean_text(listoftweet)

  rt_removed = []
  for tweet in ct:
      if not (re.match('^(RT)',tweet)):
          rt_removed.append(tweet)
      else:
          retweet = re.sub('^(RT)','',tweet)
          if retweet not in rt_removed:
              rt_removed.append(retweet)
  import tensorflow as tf
  model = tf.keras.models.load_model('G:\Sentiment Analysis\Model7 (1).h5')

  text_sequences = tokenizer.texts_to_sequences(rt_removed)
  text_padded = pad_sequences(text_sequences,maxlen=max_length,truncating='post')
  preds = model.predict(text_padded)


  indices = []
  for pred in preds:
      indices.append(np.argmax(pred))
  neutral = indices.count(1)
  positive = indices.count(2)
  negative = indices.count(0)
  print(negative,neutral,positive)
  bar(negative,neutral,positive)


# print('neutral-',neutral,' negative-',negative,' positive-',positive)
# dict = {'negative':negative,'neutral':neutral,'positive':positive}
import tkinter as tk
from tkinter.ttk import *
root = tk.Tk()
root.geometry('300x300')
HashtagField = tk.Text(root,height=1,width=20)
dateField = tk.Text(root,height=1,width=20)
# Progress bar widget
progress1 = Progressbar(root, orient = 'horizontal',
              length = 100, mode = 'determinate')
progress2 = Progressbar(root, orient = 'horizontal',
              length = 100, mode = 'determinate')
progress3 = Progressbar(root, orient = 'horizontal',
              length = 100, mode = 'determinate')
l1 = tk.Label(text='Hashtag :')
l2 = tk.Label(text='Date :')
l3 = tk.Label(text='Negative')
l4 = tk.Label(text='Neutral')
l5 = tk.Label(text='Positive')
# Function responsible for the updation
# of the progress bar value
def bar(val1,val2,val3):
    sum = val1+val2+val3
    neg = int((val1/sum)*100)
    neu = int((val2/sum)*100)
    pos = int((val3/sum)*100)
    import time
    for i in range(0,neg):
        progress1['value'] = i
        root.update_idletasks()
        time.sleep(0.01)
    for j in range(0,neu):
        progress2['value'] = j
        root.update_idletasks()
        time.sleep(0.01)
    for k in range(0,pos):
        progress3['value'] = k
        root.update_idletasks()
        time.sleep(0.01)
button1 =  Button(root, text = 'Start', command = lambda:Analyse(HashtagField.get("1.0","end-1c"),dateField.get("1.0","end-1c")))
# HashtagField.pack()
# dateField.pack()
# progress1.pack()
# progress2.pack()
# progress3.pack()
# button1.pack()
l1.grid(row = 0, column = 0, pady = 10, padx =10)
l2.grid(row = 1, column = 0, pady = 10, padx =10 )
l3.grid(row = 2, column = 0, pady = 10 )
l4.grid(row = 3, column = 0, pady = 10 )
l5.grid(row = 4, column = 0, pady = 10 )

HashtagField.grid(row = 0, column = 1, pady = 10, padx =10)
dateField.grid(row = 1, column = 1, pady = 10, padx =10)
progress1.grid(row = 2, column = 1, pady = 10, padx =10)
progress2.grid(row = 3, column = 1, pady = 10, padx =10)
progress3.grid(row = 4, column = 1, pady = 10, padx =10)
button1.grid(row=5,column = 2)
root.mainloop()
