# In this file we want to begin removing text comments from the file CommentsById.csv, we will not process the elements
import nltk

import os
import string
import pandas as pd

 
import re 
import time 
import nltk.corpus  
import unidecode 
from nltk.tokenize import word_tokenize 
from nltk.stem import WordNetLemmatizer 
from autocorrect import Speller 
from bs4 import BeautifulSoup 
from nltk.corpus import stopwords 
from nltk import word_tokenize 
import string 

import spacy


def remove_newLT(text):
    '''
    This input takes in a line of text data from the data frame or list and removes all new line or tab characters.
    
    This input will also correct spaces found in . com links
    
    '''
    
    reform = ( text.replace('\\n', ' ')
              .replace('\n', ' ')
              .replace('\t',' ')
              .replace('\\', ' ')
              .replace('. com', '.com') )
    
    return reform

def remove_Html(text):
    '''
    This method takes in text data and removes all links and .com 
    '''
    
    basket = BeautifulSoup(text, "html.parser")
    strippedT = basket.get_text(separator=" ")
    
    #here we are removing all http presence using regex re.sub to capture our link fragments
    remove_https = re.sub(r'http\S+', '', strippedT)
    remove_com = re.sub(r"\ [A-Za-z]*\.com", " ", remove_https)
    
    return remove_com

def remove_white(text):
    '''
    Remove_white takes in text data, in the form of a string and removes all additional white space found in the text.
    
    Returns: Cleaned text without extra whitespaces
    
    '''
    pattern = re.compile(r'\s+') 
    
    Without_whitespace = re.sub(pattern, ' ', text)
    
    text = Without_whitespace.replace('?', ' ? ').replace(')', ') ')
    
    return text



def remove_doubles(text):
    '''
    Remove_doubles: Will correct any duplicate characters that may have accidentally been added via the user when entering the data.
    
    Returns: Text without duplicate characters
    
    
    '''
    #first we begin by converting all elements of the text to lower case
    text = text.lower()
    
    # Pattern matching for all case alphabets
    Pattern_alpha = re.compile(r"([A-Za-z])\1{1,}", re.DOTALL)
    
    # Limiting all the  repeatation to two characters.
    Formatted_text = Pattern_alpha.sub(r"\1\1", text) 
    
    # Pattern matching for all the punctuations that can occur
    Pattern_Punct = re.compile(r'([.,/#!$%^&*?;:{}=_`~()+-])\1{1,}')
    
    # Limiting punctuations in previously formatted string to only one.
    Combined_Formatted = Pattern_Punct.sub(r'\1', Formatted_text)
    
    # The below statement is replacing repeatation of spaces that occur more than two times with that of one occurrence.
    Final_Formatted = re.sub(' {2,}',' ', Combined_Formatted)
    
    return Final_Formatted



def expand_contrt(text):
    '''
    
    expand_contrt: Will intake a string element and begins to search word for word, for contractions to expand wihtin the text data. This function also removes all special characters that do not belong or contribute to the significance of the words we are looking for. Also accented or unique characters that are not unicode are effectively removed or revereted to their unicode equivielent
    
    Returns: Text data with expanded contractions 
    
    '''
    
    #The english language holds a massive number of contractions, the full list of contractions can be found on wikipedia list of contractions (https://en.wikipedia.org/wiki/Wikipedia:List_of_English_contractions)
    contractions = {"ain't": "is not",
    "aren't": "are not",
    "can't": "cannot",
    "can't've": "cannot have",
    "'cause": "because",
    "could've": "could have",
    "couldn't": "could not",
    "couldn't've": "could not have",
    "didn't": "did not",
    "doesn't": "does not",
    "don't": "do not",
    "hadn't": "had not",
    "hadn't've": "had not have",
    "hasn't": "has not",
    "haven't": "have not",
    "he'd": "he would",
    "he'd've": "he would have",
    "he'll": "he will",
    "he'll've": "he he will have",
    "he's": "he is",
    "how'd": "how did",
    "how'd'y": "how do you",
    "how'll": "how will",
    "how's": "how is",
    "i'd": "i would",
    "i'd've": "i would have",
    "i'll": "i will",
    "i'll've": "i will have",
    "i'm": "i am",
    "i've": "i have",
    "isn't": "is not",
    "it'd": "it would",
    "it'd've": "it would have",
    "it'll": "it will",
    "it'll've": "it will have",
    "it's": "it is",
    "let's": "let us",
    "ma'am": "madam",
    "mayn't": "may not",
    "might've": "might have",
    "mightn't": "might not",
    "mightn't've": "might not have",
    "must've": "must have",
    "mustn't": "must not",
    "mustn't've": "must not have",
    "needn't": "need not",
    "needn't've": "need not have",
    "o'clock": "of the clock",
    "oughtn't": "ought not",
    "oughtn't've": "ought not have",
    "shan't": "shall not",
    "sha'n't": "shall not",
    "shan't've": "shall not have",
    "she'd": "she would",
    "she'd've": "she would have",
    "she'll": "she will",
    "she'll've": "she will have",
    "she's": "she is",
    "should've": "should have",
    "shouldn't": "should not",
    "shouldn't've": "should not have",
    "so've": "so have",
    "so's": "so as",
    "that'd": "that would",
    "that'd've": "that would have",
    "that's": "that is",
    "there'd": "there would",
    "there'd've": "there would have",
    "there's": "there is",
    "they'd": "they would",
    "they'd've": "they would have",
    "they'll": "they will",
    "they'll've": "they will have",
    "they're": "they are",
    "they've": "they have",
    "to've": "to have",
    "wasn't": "was not",
    "we'd": "we would",
    "we'd've": "we would have",
    "we'll": "we will",
    "we'll've": "we will have",
    "we're": "we are",
    "we've": "we have",
    "weren't": "were not",
    "what'll": "what will",
    "what'll've": "what will have",
    "what're": "what are",
    "what's": "what is",
    "what've": "what have",
    "when's": "when is",
    "when've": "when have",
    "where'd": "where did",
    "where's": "where is",
    "where've": "where have",
    "who'll": "who will",
    "who'll've": "who will have",
    "who's": "who is",
    "who've": "who have",
    "why's": "why is",
    "why've": "why have",
    "will've": "will have",
    "won't": "will not",
    "won't've": "will not have",
    "would've": "would have",
    "wouldn't": "would not",
    "wouldn't've": "would not have",
    "y'all": "you all",
    "y'all'd": "you all would",
    "y'all'd've": "you all would have",
    "y'all're": "you all are",
    "y'all've": "you all have",
    "you'd": "you would",
    "you'd've": "you would have",
    "you'll": "you will",
    "you'll've": "you will have",
    "you're": "you are",
    "you've": "you have",
    }
    import unidecode 
    
    #we begin by tokeninzing the text
    word_tokens = text.split(' ')

    
    for w in word_tokens:
        if w in contractions:
            #replace contracted word
            word_tokens = [item.replace(w, contractions[w]) for item in word_tokens]
            
    
    reform = ' '.join(str(w) for w in word_tokens)
    
    #removing all special characters as well
    reform = re.sub(r"[^a-zA-Z0-9:$-,%.?!]+", ' ', reform) 
    
    #This segment confirms that all characters represented in the text segment are unicode
    reform2 = unidecode.unidecode(reform)
    return reform2


def remove_nonE(text):
    '''
    If a word is found to be slang, or not found within the normal corpus of words used in the english language then the word will be stripped from the text data
    
    *Not sure how effective this is once the words have neen spell checked
    
    Returns: text that has been stripped of non-english words
    '''
    word_tokens = text.split(' ')
    wordz = set(nltk.corpus.words.words())
    
    reform = ""
    for w in word_tokens:
        if w in wordz:
            reform += w+" "
        else:
            reform += ""
            
    return reform
    
    
    
def spellck(text):
    '''
    spellck: Takes in a string of text data and checks each word using the python spellchecker
    
    
    Returns: correctly spelt words
    '''
    
    spell = Speller(lang='en')
    cor = spell(text)
    
    return cor


def clean( text1 ):
    text = remove_newLT(text1)
#     text = remove_Html(text)
    text = remove_white(text)
    text = remove_doubles(text)
    text = expand_contrt(text)
    # text = spellck(text)
    
    return text




def load_comm():
    '''
    This method will load the comments dataframe, and extract the text column from it.
    
    Returns:
    Dataframe containing all comment information
    
    '''
    
    df = pd.read_csv("Data2/Comments.csv")
    df['CreationDate'] = df['CreationDate'].apply(pd.to_datetime)
    return df



def link_pres( text ):
    '''
    This function returns a boolean to the presence of a link in the comment, if the a link exisits in the comment the comment then becomes of the link type
    '''
    matches = re.findall('https?://(?:[-\w.]|(?:%[\da-fA-F]{2}))+', text)
    
    return bool(matches)



def Comment_Type( text ):
    '''
    We make a generalized assumption that the percentage of special characters relative to the the total number of characters is higher in comments that focus on code, thus we do no relative pre-proccesing to the text as special characters would be removed. 
    
    This function will take in the text line and calculate the total number of characters, then using regex we will extract all special characters and count those, a simple calculation will reveal the realtive percentage of special characters to total characters
    
    '''
    
    #First we must begin to scan the text for all hyperlinks as a link will automatically push the comment to that of link type.
    matches = re.findall('https?://(?:[-\w.]|(?:%[\da-fA-F]{2}))+', text)
   
    
    alpha = 0 
    digit = 0
    special = 0
    
    for i in range(len(text)):
        if(text[i].isalpha()):
            alpha = alpha + 1
        elif(text[i].isdigit()):
            digit = digit + 1
        else:
            special = special + 1

            
    perce_special = ((digit+special)/100)
    
    if not matches:
        if perce_special >= 0.25:
            return 'Code Response'
        else:
            return 'Written Response'
    else: 
        return 'Link Response'
    
    
    
def load_comments_data( data ):
    from nltk.sentiment import SentimentIntensityAnalyzer
    sia = SentimentIntensityAnalyzer() 
    
    
    indrange = data.index

    df2 = pd.DataFrame(columns = ['Body', 'TypeC', 'neg', 'neu', 'pos'])
    
    for e in range(len(data.index)):
        #Clean will return our text body cleaned 
        ee = Comment_Type(str(data['Text'][e]))
        
        bod = str(data['Text'][e])
        bod2 = clean(bod)
        #We can now analyze sentiment
        score = sia.polarity_scores(bod)
    
        df2 = df2.append({'Body': bod2, 'TypeC': ee, 'neg':score['neg'], 'neu':score['neu'], 'pos':score['pos']}, ignore_index=True)
        
    merged = pd.merge(data, df2, left_index=True, right_index=True)
    merged = merged.drop("Text", 1)
    merged['CreationDate'] = merged['CreationDate'].apply(pd.to_datetime)
        
        

    return merged

