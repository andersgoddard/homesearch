import string
import math
import re
import pandas as pd
from collections import Counter

WORD = re.compile(r"\w+")
    
def clean_address(text):
  text = ''.join([word for word in text if word not in string.punctuation])
  text = text.lower()
  return text

def text_to_vector(text):
    words = WORD.findall(text)
    return Counter(words)

def get_cosine(vec1, vec2):

    intersection = set(vec1.keys()) & set(vec2.keys())
    numerator = sum([vec1[x] * vec2[x] for x in intersection])

    sum1 = sum([vec1[x] ** 2 for x in vec1.keys()])
    sum2 = sum([vec2[x] ** 2 for x in vec2.keys()])
    
    if sum1 == 0 or sum2 == 0:
        denominator = 0
    else:
        denominator = math.sqrt(sum1) * math.sqrt(sum2)

    if not denominator:
        return 0.0
    else:
        return float(numerator) / denominator

def getCosineSimilarities(internalDataframe, externalDataframe):
    
    internalDataframe['index'] = internalDataframe.index    
    combinedDf = pd.merge(internalDataframe, externalDataframe, on='postcode')
    similarities_dict = dict() 
    
    for i in range(len(internalDataframe)):
        index = internalDataframe['index'].iloc[i]
        similarities_dict[index] = 0   
        
    for i in range(len(combinedDf)):
        vector1 = text_to_vector(clean_address(combinedDf['Address'].iloc[i]))
        vector2 = text_to_vector(clean_address(combinedDf['full address'].iloc[i]))
        cosine = get_cosine(vector1, vector2)
        index = combinedDf['index'].iloc[i]
        if cosine > similarities_dict[index]:
            similarities_dict[index] = cosine       
    
    similarities = []
    
    for key, value in similarities_dict.items():
        similarities.append(value)
    
    return similarities