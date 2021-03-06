# -*- coding: utf-8 -*-
"""mlhw1q4(completed).ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1LrUnd9MscmpjfcPTLJj9WWI3k7MfhcxO

Part (a) :

define an function to read each document and convert it into a vector of words and obtain appearance time of each word, tf of each word and a list of all kinds of word in each .txt document saving as dictionaries
"""

#upload text to colab first

def preprocess(x):
  import string
  with open (x, 'r+') as f:
    filestr=f.read()
  
  #convert words into a vector :
  words = ''.join(c for c in filestr if c not in string.punctuation)#remove punctuation
  words = words.lower()#convert all letters to lowercase
  words = words.split()#split words by blank or \n
  #print(words)
  
  #appearance time of each word :
  count = {} 
  for n in range(0,len(words)):
    count[ words[n] ] = words.count( words[n] )
  #print(count)
  
  #tf of each word :
  tf = {}
  for k,v in count.items():
    tf[k] =  v / len(words) 
  
  return [count,tf,words]

"""Part (b) :

b1. write a funtion to obtain result of funtion "preprocess" on each document from paths provided in a list and put appearance counter of words, tf of words in every doucument and a collection of all kinds of words appear in all documents  respectively into three lists : counter, tfdic, all_words
"""

def obtain(path):
  counter = []
  tfdic = []
  i = 1
  all_words = set() 
  for n in path:
    counter.append( preprocess(n)[0] )
    tfdic.append( preprocess(n)[1] )
    all_words = all_words.union( set(preprocess(n)[2]) )
  return [counter,tfdic,all_words]  

paths = ['d_query.txt','d1.txt','d2.txt','d3.txt','d4.txt','d5.txt']
counter = obtain(paths)[0]
tfdic = obtain(paths)[1]
all_words = obtain(paths)[2]
docnumber = len(paths)
print ("all words:",all_words)
print()  
for i in range(1,docnumber): 
  print("appearance time of words in d"+str(i)+":",counter[i])
#   print("time frequency of words in d"+str(i)+":",tfdic[i])
#   print("size:",len(tfdic[i]))
  print()
# print("appearance time of words in d_query:",counter[0])
# print("time frequency of words in d_query:",tfdic[0])
# print("size:",len(tfdic[0]))

"""b2.write a funtion to unify the format of counter and tfdic to make every dictionary have same attributes and dimension, put them respectively into two lists: counters, tfdics"""

def unifydics(aim):
  l = aim
  result = []
  for n in range(0,len(l)):
    for x in all_words:
      if x not in l[n]:
        l[n][x]=0
    keys = sorted(l[n].keys()) 
    ks = {}
    for k in keys:
      ks[k] = l[n][k]
    result.append(ks)
  return result      

counters = unifydics (counter)
tfdics = unifydics (tfdic)

# for i in range(1,docnumber): 
#   print()
#   print("unified A.T. of words in d"+str(i)+":",counters[i])
#   print("unified tf of words in d"+str(i)+":",tfdics[i])
#   print("size:",len(tfdics[i]))
# print()
# print("unified A.T. of words in d_query:",counters[0])
# print("unified tf of words in d_query:",tfdics[0])  
# print("size:",len(tfdics[0]))

"""b3. write a funtion to obtain idf of each words in every document and put them together into one list : idfdics , actually they are all the same but I save them as the same format and container as tf"""

def getidf(counters):
  import math
  idfdics = []
  docnumber = len(counters)
  for n in range(0,docnumber):
    idf = {}
    for k,v in counters[n].items():
      c=0
      for m in range(0,docnumber):
        if counters[m][k] != 0 :
          c = c + 1
      if c == 0:
        c = c + 1 #in case c == 0    
      idf[k] = math.log10(docnumber / c )
    idfdics.append(idf)  
  return idfdics

idfdics = getidf(counters)

# for n in range(1,docnumber):
#   print("inverse document frequency of words in d"+str(n)+":",idfdics[i])
# print("inverse document frequency of words in d_query:",idfdics[0])

"""b4. write a funtion to obtain tf-idf of each words in every document and put them together into one list : tfidfdics"""

def gettfidf(tfdics,idfdics):
  tfidfdics = []
  for n in range(0,docnumber):
    tfidf = {}
    for k,v in tfdics[n].items():
      tfidf[k] = tfdics[n][k] * idfdics[n][k]
    # print(tfidf)
    tfidfdics.append(tfidf)
  return tfidfdics

tfidfdics = gettfidf(tfdics,idfdics)

for n in range(1,docnumber):
  print("tf-idf of words in d"+str(n)+":",tfidfdics[n])
print("tf-idf of words in d_query:",tfidfdics[0])

"""Part (c) :

define a function that can calculate cosine similarity between two dictionaries of tf-idf
"""

def cosinesimilarity(x,y):
  if len(x) != len(y):
    print("dimension does not match")
    return 0
  
  import numpy as np
  product = 0
  squarex = 0
  squarey = 0
  for kx,ky in zip(x.keys(),y.keys()):
    product = product + x[kx]*y[ky]
    squarex = squarex + np.square(x[kx])
    squarey = squarey + np.square(y[ky])
   
  euclideanx = np.sqrt(squarex) 
  euclideany = np.sqrt(squarey)
  similarity = product / ( euclideanx * euclideany )
  
  # print("product: ",product," euclideanx: ",euclideanx," euclideany: ",euclideany," similarity: ",similarity)
  # print()
  return similarity

"""Part (d) :

define a recognintion funtion that can use function defined above to compare cosine similarity among documents and return sequence number of result document and maximum value of similarity
"""

def recognition(tfidfs):
  similarity = []
  for n in range(1,len(tfidfs)):
    similarity.append( cosinesimilarity(tfidfs[0],tfidfs[n]) )
  index = similarity.index(max(similarity))
  maximum = max(similarity)  
  #print("similarities: ",similarity)
  print("d "+str(index+1)+" is the documen with maximum cosine similarity value of "+str(maximum))
  print()
  return [index+1,maximum]

recognition(tfidfdics)