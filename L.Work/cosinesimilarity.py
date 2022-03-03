import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from nltk.stem import PorterStemmer
from nltk.tokenize import word_tokenize

def removeFirstLastThree(text):
    text = text[3:]
    text = text[:len(text)-3]
    return text

def applyPStemmer_df(text):
    ps = PorterStemmer()
    stemmed_words=[]

    for w in text:
        stemmed_words.append(ps.stem(w))

    return stemmed_words


def prepare_LDA_df(text):
    return word_tokenize(text)

def getCSim(text):
    text_file = 'FinalData\qdata.csv'

    df = pd.read_csv(text_file, encoding='utf-8', low_memory=False)
    
    # Change this to how many questions you want the program to go over
    df = df.head(20000)

    df = df[['Id', 'Text']]
    df = df[df['Text'].notna()]

    df['Text'] = df.apply(lambda x: removeFirstLastThree(x['Text']), axis=1)

    toAdd = {'Body_q' : text}

    df_input = pd.DataFrame()

    for z in range(0,len(df.index)):
        df_input = df_input.append(toAdd, ignore_index=True)

    df.loc[-1] = [-1, text]  
    df.index = df.index + 1  
    df.sort_index(inplace=True) 

    cv = CountVectorizer(stop_words = 'english', min_df=5, max_features=500)
    count_matrix = cv.fit_transform(df['Text'])

    cosine_sim = cosine_similarity(count_matrix)

    closest_Q = list(enumerate(cosine_sim[0]))
    
    sorted_similar = sorted(closest_Q, key=lambda x:x[1], reverse=True)
    sorted_similar = sorted_similar[1:6]

    to_return = []
    i = 0
    for q in sorted_similar:
        to_return.append("<strong>Question {}</strong><br>:  {}".format(i, str(df['Text'][q[0]])))
        i += 1
        
    return to_return

# getCSim('would like to know how i can initialize an array(or list), yet to be populated with values, to have a defined size')