
# coding: utf-8

# In[51]:


import nltk
from nltk import word_tokenize
from nltk.util import ngrams
from collections import Counter
import numpy as np
import pandas as pd
import re


# # Read the lexicon file

# In[52]:


lexicon = pd.read_excel("Files\\NileULex_v0.27.xlsx")
lexicon = lexicon.drop(lexicon.index[[range(0, 9)]])
lexicon.drop(lexicon.columns[2:], axis=1, inplace=True)
lexicon.columns = ['term', 'polarity']
# lexicon


# # categorize lexicon according to its length

# In[53]:


lexicon_unigram = []
lexicon_bigram = []
lexicon_trigram = []
lexicon_fougram = []
lexicon_fivegram = []
lexicon_sixgram = []
lexicon_sevengram = []

for index, row in lexicon.iterrows():
    if len(row["term"].strip().split(" ")) == 1:
        lexicon_unigram.append(
            [(row["term"].strip().split(" "))[0], row["polarity"]])

    elif len(row["term"].strip().split(" ")) == 2:
        lexicon_bigram.append(
            [tuple(row["term"].strip().split(" ")), row["polarity"]])

    elif len(row["term"].strip().split(" ")) == 3:
        lexicon_trigram.append(
            [tuple(row["term"].strip().split(" ")), row["polarity"]])

    elif len(row["term"].strip().split(" ")) == 4:
        lexicon_fougram.append(
            [tuple(row["term"].strip().split(" ")), row["polarity"]])

    elif len(row["term"].strip().split(" ")) == 5:
        lexicon_fivegram.append(
            [tuple(row["term"].strip().split(" ")), row["polarity"]])

    elif len(row["term"].strip().split(" ")) == 6:
        lexicon_sixgram.append(
            [tuple(row["term"].strip().split(" ")), row["polarity"]])

    elif len(row["term"].strip().split(" ")) == 7:
        lexicon_sevengram.append(
            [tuple(row["term"].strip().split(" ")), row["polarity"]])

# lexicon_bigram


# In[54]:


# tweet unigram
def unigram_tweet(tweet):
    unigram_list = tweet.strip().split(" ")
    return unigram_list


# # Calculating the lexicon for each tweet

# In[55]:


def calc_lexicon(tweet):
    pos = 0
    comp_pos = 0
    neg = 0 
    comp_neg = 0
    word_count = 0
    token = nltk.word_tokenize(tweet.strip())
    multigrams = [unigram_tweet(tweet), ngrams(token, 2), ngrams(token, 3), ngrams(
        token, 4), ngrams(token, 5), ngrams(token, 6), ngrams(token, 7)]
    lexicongrams = [lexicon_unigram, lexicon_bigram, lexicon_trigram,
                    lexicon_fougram, lexicon_fivegram, lexicon_sixgram, lexicon_sevengram]
    # filteration(text)

    for i in range(0, 6):
        for lex in lexicongrams[i]:
            if lex[0] in multigrams[i]:
                word_count = multigrams[i].count(lex[0])
                if lex[1] == 'negative':
                    neg += word_count
                elif lex[1] == 'compound_neg':
                    comp_neg += word_count
                elif lex[1] == 'compound_pos':
                    comp_pos += word_count
                elif lex[1] == 'positive':
                    pos += word_count
    tweet_pos_lexicon = pos + (1.5*comp_pos)
    tweet_neg_lexicon = neg + (1.5*comp_neg)
    lexical_calculations = [tweet_pos_lexicon, tweet_neg_lexicon]

    return lexical_calculations


# # Testing the method

# In[57]:


#text = 'يؤتمن ابقي قابلني يا ابن الاحبي اتكسف علي دمك '
#text = ' اختلاس احتلال'
text = 'فينو اهبل اهبل'
calc_lexicon(text)
