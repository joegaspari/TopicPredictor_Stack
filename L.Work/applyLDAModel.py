# This file responds to a post request from app.py 
# Returns the 3 closest topics based on the passed in text

import re
import gensim
import pickle
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
from nltk.corpus import wordnet as wn
import pandas as pd
pd.options.mode.chained_assignment = None 

load_gensim_model = gensim.models.ldamodel.LdaModel.load('models/lda_model.model')
topics = load_gensim_model.print_topics(num_words=2)

file_to_read = open("models/dictionary.gensim", "rb")
dictionary = pickle.load(file_to_read)

def loadModels():
    word_pairs = []
    word_pairs_cleaned = []

    for topic in topics:
        word_pairs.append(list(topic))

    word_pairs_sorted = sorted(word_pairs, key = lambda x: x[0])

    regex = re.compile('[^a-zA-Z ]')

    for element in word_pairs_sorted:
        word_pairs = regex.sub('', element[1])
        word_pairs = word_pairs.replace('  ', ', ')
        word_pairs_cleaned.append([element[0], word_pairs])

    return word_pairs_cleaned


def getKeywords(word_pairs_cleaned):
    list_of_keywords = [None] * 25

    list_of_keywords[0] = ''
    list_of_keywords[2] = ''
    list_of_keywords[3] = ''
    list_of_keywords[5] = ''

    list_of_keywords[1] = [word_pairs_cleaned[0], 'CSS Styling']
    list_of_keywords[4] = [word_pairs_cleaned[1], 'Server testing']
    list_of_keywords[6] = [word_pairs_cleaned[2], 'Arrays and lists']
    list_of_keywords[7] = [word_pairs_cleaned[3], 'Functions, methods and variables']
    list_of_keywords[8] = [word_pairs_cleaned[4], 'Files']
    list_of_keywords[9] = [word_pairs_cleaned[5], 'System task management']
    list_of_keywords[10] = [word_pairs_cleaned[6], 'JAVA developement']
    list_of_keywords[11] = [word_pairs_cleaned[7], 'Android view class']
    list_of_keywords[12] = [word_pairs_cleaned[8], 'Accessing and declaring variables']
    list_of_keywords[13] = [word_pairs_cleaned[9], 'Database queries']
    list_of_keywords[14] = [word_pairs_cleaned[10], 'Static and dynamic binding']
    list_of_keywords[15] = [word_pairs_cleaned[11], 'Verson and builds']
    list_of_keywords[16] = [word_pairs_cleaned[12], 'HTML elements']
    list_of_keywords[17] = [word_pairs_cleaned[13], 'Types of images']
    list_of_keywords[18] = [word_pairs_cleaned[14], 'Protocol/network stacks']
    list_of_keywords[19] = [word_pairs_cleaned[15], 'HTTP and TCP/IP']
    list_of_keywords[21] = [word_pairs_cleaned[16], 'Software models and development life cycle']
    list_of_keywords[22] = [word_pairs_cleaned[17], 'Primitive and reference data types']
    list_of_keywords[23] = [word_pairs_cleaned[18], 'Application tags and metadata']
    list_of_keywords[24] = [word_pairs_cleaned[19], 'HTML elements']

    return list_of_keywords

def tokenizeText(text):
    return word_tokenize(text)

def removeFirstLastThree(text):
    text = text[3:]
    text = text[:len(text)-3]
    return text


def toLowerCase(text):
    text = [word.lower() for word in text]
    return text


def removeStopWords(text):
    stop_words= set(stopwords.words("english"))
    filtered_sent = []
    for w in text:
        if w not in stop_words:
            filtered_sent.append(w)
    return filtered_sent



def applyPStemmer(text):
    ps = PorterStemmer()

    stemmed_words = []
    for w in text:
        stemmed_words.append(ps.stem(w))

    return stemmed_words


def get_lemma(text):
    words = []
    for word in text:
        lemma = wn.morphy(word)
        if (len(word) <= 2 or len(word) >= 15 or word == 'code' or word.isnumeric() or word == 'gt' or word == 'lt' or word =='quot' or word == 'pre' or word == 'amp'):
            continue 
        elif lemma is None or word == lemma:
            words.append(word)
        else:
            words.append(lemma)
    return words

list_of_keywords = []

# Used with strings
def getTopics(user_input):
    tokens = tokenizeText(user_input)
    tokens = removeFirstLastThree(tokens)
    tokens = toLowerCase(tokens)
    tokens = removeStopWords(tokens)
    tokens = applyPStemmer(tokens)
    tokens = get_lemma(tokens)

    bagOfWords = dictionary.doc2bow(tokens)
    matches = load_gensim_model.get_document_topics(bagOfWords)

    word_pairs_cleaned = loadModels()
    list_of_keywords = getKeywords(word_pairs_cleaned)

    matches.sort(key = lambda x: x[1], reverse = True)

    matches = matches[:3]

    to_return = []
    
    # for match in matches:
    #     temp = list(match)
    #     if(temp[0]):
    #         if(match[1] > 0.1):
    #             to_return.append(list_of_keywords[match[0]][1])



   
    for match in matches:
        temp = list(match)
        if(list_of_keywords[temp[0]]):
                if(temp[1] > 0.1):
                    to_return.append(list_of_keywords[temp[0]][1])

    


    return to_return

# Used for handling dataframes
def prepareTextDf(df):

    df['Body_processed'] = df['Text'].astype(str)
    df['Body_processed'] = df.apply(lambda x: removeFirstLastThree(x['Body_processed']), axis=1)
    df['Body_processed'] = df.apply(lambda x: tokenizeText(x['Body_processed']), axis=1)
    df['Body_processed'] = df.apply(lambda x: applyPStemmer(x['Body_processed']), axis=1)
    df['Body_processed'] = df.apply(lambda x: removeStopWords(x['Body_processed']), axis=1)
    df['Body_processed'] = df.apply(lambda x: get_lemma(x['Body_processed']), axis=1)

    word_pairs_cleaned = loadModels()
    list_of_keywords = getKeywords(word_pairs_cleaned)

    df['Body_processed_topics'] = df.apply(lambda x: dictionary.doc2bow(x['Body_processed']), axis=1)
    df['Body_processed_topics'] = df.apply(lambda x: load_gensim_model.get_document_topics(x['Body_processed_topics']), axis=1)


    def sorterTopThree(nums):
        nums.sort(key = lambda x: x[1], reverse = True)
        return nums[:3]

    df['Body_processed_topics_sorted'] = df.apply(lambda x: sorterTopThree(x['Body_processed_topics']), axis=1)


    def getTopicsfromKwrds(keywords):
        to_return = []
        i = 0
        for match in keywords:
            temp = list(match)
            if(list_of_keywords[temp[0]]):
                    if(temp[1] > 0.1):
                        to_return.append(list_of_keywords[temp[0]][1])

            i+=1

        return to_return


    df['Body_processed_topics_words_final'] = df.apply(lambda x: getTopicsfromKwrds(x['Body_processed_topics_sorted']), axis=1)
    df = df.drop(labels=['Body_processed_topics', 'Body_processed_topics_sorted'], axis=1)
    return df

# print(getTopics('Below is an example of how you can instruct your audience on installing and setting up your app. This template doesn'))

# df = pd.read_csv('FinalData/qdata.csv',encoding='utf-8')

# Apply LDA model to each row in body and store results as a new column
# qdataCombined = pd.read_csv("FinalData\\qdata.csv")

# qdataCombined = prepareTextDf(qdataCombined.head(100))
# print(qdataCombined['Body_processed_topics_words_final'])

# qdataCombined.to_csv("FinalData\\qdataCombined.csv", encoding="utf-8")
