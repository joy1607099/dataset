# -*- coding: utf-8 -*-
"""
Created on Tue Jul 21 20:52:04 2020

@author: Joy
"""


from sklearn.feature_extraction.text import CountVectorizer

import pandas as pd
import re
import nltk
import spacy
import string
pd.options.mode.chained_assignment = None

full_df = pd.read_csv("sample.csv", nrows=5)
df = full_df[["text"]]
df["date"] = full_df["date"]
df["truncated"] =full_df["truncated"]
df["text"] = df["text"].astype(str)
full_df.head()

df["date"] = full_df["date"]
df["truncated"] =full_df["truncated"]

PUNCT_TO_REMOVE = string.punctuation
def remove_punctuation(text):
    """custom function to remove the punctuation"""
    return text.translate(str.maketrans('', '', PUNCT_TO_REMOVE))

df["text_wo_punct"] = df["text"].apply(lambda text: remove_punctuation(text))
df.head()
df["text_lower"] = df["text_wo_punct"].str.lower()
df.head()



from nltk.corpus import stopwords
", ".join(stopwords.words('english'))

STOPWORDS = set(stopwords.words('english'))
def remove_stopwords(text):
    """custom function to remove the stopwords"""
    return " ".join([word for word in str(text).split() if word not in STOPWORDS])

df["text_wo_stop"] = df["text_lower"].apply(lambda text: remove_stopwords(text))
df.head()




from collections import Counter
cnt = Counter()
for text in df["text_wo_stop"].values:
    for word in text.split():
        cnt[word] += 1
        
cnt.most_common(10)

FREQWORDS = set([w for (w, wc) in cnt.most_common(10)])
def remove_freqwords(text):
    """custom function to remove the frequent words"""
    return " ".join([word for word in str(text).split() if word not in FREQWORDS])

df["text_wo_stopfreq"] = df["text_wo_stop"].apply(lambda text: remove_freqwords(text))
df.head()





# Drop the two columns which are no more needed 
df.drop(["text_wo_punct", "text_wo_stop"], axis=1, inplace=True)

n_rare_words = 10
RAREWORDS = set([w for (w, wc) in cnt.most_common()[:-n_rare_words-1:-1]])
def remove_rarewords(text):
    """custom function to remove the rare words"""
    return " ".join([word for word in str(text).split() if word not in RAREWORDS])

df["text_wo_stopfreqrare"] = df["text_wo_stopfreq"].apply(lambda text: remove_rarewords(text))
df.head()



from nltk.stem.snowball import SnowballStemmer
SnowballStemmer.languages

# Drop the two columns 
df.drop(["text_lower", "text_wo_stopfreq"], axis=1, inplace=True) 

stemmer = SnowballStemmer("english")
def stem_words(text):
    return " ".join([stemmer.stem(word) for word in text.split()])

df["text_stemmed"] = df["text_wo_stopfreqrare"].apply(lambda text: stem_words(text))
df.head()


def remove_emoji(string):
    emoji_pattern = re.compile("["
                           u"\U0001F600-\U0001F64F"  # emoticons
                           u"\U0001F300-\U0001F5FF"  # symbols & pictographs
                           u"\U0001F680-\U0001F6FF"  # transport & map symbols
                           u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
                           u"\U00002702-\U000027B0"
                           u"\U000024C2-\U0001F251"
                           "]+", flags=re.UNICODE)
    return emoji_pattern.sub(r'', string)
df["without_emoji"] = df["text_stemmed"].apply(lambda text: remove_emoji(text))




def remove_urls(text):
    url_pattern = re.compile(r'https?://\S+|www\.\S+')
    return url_pattern.sub(r'', text)

df["without_url"] = df["without_emoji"].apply(lambda text: remove_urls(text))



def remove_html(text):
    html_pattern = re.compile('<.*?>')
    return html_pattern.sub(r'', text)

df["Processed_Text"] = df["without_url"].apply(lambda text: remove_html(text))


df.drop(["text_wo_stopfreqrare", "text_stemmed","without_emoji","without_url"], axis=1, inplace=True)

vectorizer = CountVectorizer(max_features=1500, min_df=5, max_df=0.7, stop_words=stopwords.words('english'))
X = vectorizer.fit_transform(df["Processed_Text"]).toarray()

df.to_csv('sample_fpreprocessed.csv')
