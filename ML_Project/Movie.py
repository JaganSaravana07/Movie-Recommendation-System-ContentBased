import numpy as numpy
import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel
from sklearn.metrics.pairwise import sigmoid_kernel
from sklearn.metrics.pairwise import cosine_similarity
import pickle

df = pd.read_csv("Movies.csv", lineterminator = "\n")
df['Overview'] = df['Overview'].fillna('')


def clean_data(x):
    if isinstance(x, list):
        return [str.lower(i.replace(" ", "")) for i in x]
    else:
        #Check if director exists. If not, return empty string
        if isinstance(x, str):
            return str.lower(x.replace(" ", ""))
        else:
            return ''

def sigmoid(matrix):
  return sigmoid_kernel(matrix,matrix)

def cosin(matrix):
  return cosine_similarity(matrix,matrix)

def overview():
  tfidf = TfidfVectorizer(max_features = None, strip_accents = 'unicode', analyzer = 'word', ngram_range = (1,3), token_pattern = r'\w{1,}', stop_words='english')
  tfidf_matrix = tfidf.fit_transform(df['Overview'])
  return cosin(tfidf_matrix)

def genre():
  count = CountVectorizer(stop_words='english')
  df['Genre'] = df['Genre'].apply(clean_data)
  count_matrix = count.fit_transform(df['Genre'])
  return sigmoid(count_matrix)


cos = overview()
sig = genre()

models = [cos,sig]
pickle.dump(models,open("model.pkl",'wb'))
