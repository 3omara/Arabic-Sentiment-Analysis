import numpy as np
import pandas as pd
import nltk

class Sequencer():

    def __init__(self, tweets, embedding_dict, padding):

        self.tweets = tweets
        self.embed = embedding_dict
        #self.min_count = min_count
        self.padding = padding
        
        # self.corpus = (" ".join(self.tweets.to_numpy().flatten())).split()

        # freq = {}

        # for i, word in enumerate(self.corpus):
        #     try:
        #         freq[word] += 1
        #     except:
        #         freq[word] = 1

        # self.sorted_freq = {key: val for key, val in sorted(freq.items(), key = lambda ele: ele[1], reverse=1)}
        # embedding_vocab = [word for word, val in self.sorted_freq.items() if val >= self.min_count]

        # self.word2embedding = {}
        # for i, word in enumerate(embedding_vocab):
        #     self.word2embedding[word] = embedding_matrix[i]


    def text_to_vec(self, tweet):
        vec = []
        tweet = tweet.split()

        for word in tweet:
            try:                
                vec.append(self.embed[word])
            except:
                pass
        
        return np.array(vec).flatten()

    def padder(self, vec):

        if self.padding - len(vec) > 0:
            pad = np.zeros(self.padding - len(vec))
            vec = np.append(vec, pad)

        return vec[:self.padding].flatten()
        

    