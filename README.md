<!-- ABOUT THE PROJECT -->
# Introduction
Stack Overflow has become one of the main sources students use to reference coding information and other related topics. The site provides publicly available data that we have chosen to subject to analysis. The data set was chosen as it provides a wealth of information surrounding the trending topics students or individuals in software development may ask. This set can also elucidate how users interact with each other and which users are most active. Our study of the data works to highlight the sentiment users show towards topics they ask questions about, or how they themselves contribute to other's discussions through comments or answers. 

# Objective
By examining data from Stack Overflow regarding questions, answers, and comments we can gather insight into the topics that have been causing individuals to flock to sites such as this, for help. The goal of this study is to accurately identify trending topics within user posts (Questions/Answers/Comments). We are also examining how users choose to respond and what attitudes they carry in their response. 

## About The Project
For our project we scraped data from Stack Overflow and performed multiple analyses on it. Language processing was used to explore trends in the popularity of computer languages and topics, as well as to identify the sentiment of users, on Stack Overflow over time. <br>
The second part of our project involved using Linear Discriminant and Cosine Similarity analysis to identify and predict the topics of user entered text and recommend similar questions.   


## Dataset
We downloaded pre-scraped data, available here:


* https://www.brentozar.com/archive/2015/10/how-to-download-the-stack-overflow-database-via-bittorrent/


We first attempted to scrape the data directly using the Stack Overflow API. However due to query limits, it was decided that starting with the above dataset would be much faster. After downloading the dataset, it was loaded into a local Microsoft SQL database so that it could be queried directly from the Python working environment.<br>


## Built With
The data processing was done in Python using Jupyter Notebook. The topic/similar question predictor part of the project was built as a simple Flask application and then integrated into Tableau. The actual visualization of the data is presented in Tableau.<br>
The following Python libraries were used in performing the language processing and analysis:
* [NLTK](https://www.nltk.org/)
* [Gensim](https://radimrehurek.com/gensim/)
* [Pickle](https://docs.python.org/3/library/pickle.html#module-pickle)
* [Beautiful Soup](https://www.crummy.com/software/BeautifulSoup/)


## Project part I - Language Analysis 

Post data was found to be significantly saturated with formatting characters, these and other character abnormalities were subject to preprocessing completed in the python script J.work/posts.py. We then apply a sentiment intensity analysis using the NLTK sentiment tool kit. This process examines the cleaned text and provides a score of positive/negative/neutral as a distribution between [0,1]. This analysis was completed on all data sets found in Data2/FinalData

  ### Response Typing 

  We classify user responses as we believe different types of responses provide more significance within discussions. We begin to simply define the types as Code, Written or Link type responses. We perform a separate pre-processing script on our answer and comment data when identifying the response type. The code can be found in J.work/comDefs.py. This is due to the way we have chosen to classify the data, when the code found in method Comment_Type() encounters a http tag it automatically assigns the response type Link. We left special characters/operators that are most often used in code in the text data, we do this as to identify a cut-off percentage with which to distinguish code versus written responses. Since there are a few special characters that overlap between common written language and high level computer language it was found that a cut-off of 25% provided the best split between code and written response. Upon review of the set with assigned cut-off, it was found that this percentage was most accurate at labeling the data.  

## Project part II - Question and Topic Predictor

### Question Topics

Stack overflow provides a helpful tool on their site, when a user posts a question they are required to assign tags that relate to the topic of the question they seek help with. Within posts.py we have created a function called get_topWords() which will generate a list of tops tags from the data frame containing questions.  

  #### get_topWords( dataFrame, N )
    This method cleans all tags and strips the set of stopwords and special characters found in the tags feild of dataFrame. Using collections and the number specified in argument 2 we return a list of length specified. This list is of the top N most frequent words in the entire corpus of tags generated from the data set. 


We then iterate through each question entry extract all the tags, clean them and perform set intersection to determine which to include as the final label. If the label was not found in the set, or more than one was assigned then the most frequent tag is included or a NaN flag is raised. It was determined that 3.533% of the set was labeled with NaN after this process was completed. The analysis resulted in the formation of 50 different topic categories. 

### Usage
In order to access the question analyzer, ensure all dependencies are installed and then type:
```sh
python app.py
```
And navigate to<br> http://127.0.0.1:5000/

### Topic Predictor

```sh
buildLDAModel.ipynb 
```
Contains the code needed to build an LDA model based on the scraped question text data.<br>
The following calls the methods needed to process the text and prepare a set of tokens for the dictionary:
  ```sh
for key in dict:
    tokens = tokenizeText(dict[key]['Text'])
    tokens = removeFirstLastThree(tokens)
    tokens = toLowerCase(tokens)
    tokens = removeStopWords(tokens)
    tokens = applyPStemmer(tokens)
    tokens = get_lemma(tokens)
  ```

Then we create a dictionary for the text tokens and save it so that it can be reused:
  ```sh
dict = corpora.Dictionary(text_tokens)
dict.save('dictionary.gensim')
  ```
This dictionary is then used to create a bag of words model which is also saved:
  ```sh
bagOfWords = [dict.doc2bow(t) for t in text_tokens]
pickle.dump(bagOfWords, open('corpus.pkl', 'wb'))
  ```
Then the actual LDA model can be generated and saved. The number of topics, passes and words was varied and the following provided good results: 

```shl 
NUM_TOPICS = 25
NUM_WORDS = 2

lda model = gensim.models.ldamodel.LdaModel(corpus, num_topics = NUM_TOPICS, id2word=dictionary, passes=15)
ldamodel.save('models/lda_model.model')
  ```
Once the LDA model is built and saved, it can be loaded and run as follows:
```shl 
ldamodel =  models.LdaModel.load('models/lda_model.model')
topics = ldamodel.print_topics(num_words=NUM_WORDS)
  ```
Where NUM_WORDS gives the number of words in each of the NUM_TOPICS that the model identifies 

Printing this gives:
```shl 
(12, '0.192*"self" + 0.026*"let"')
(8, '0.118*"file" + 0.038*"line"')
(17, '0.115*"image" + 0.046*"category"')
(16, '0.107*"div" + 0.103*"class"')
(10, '0.084*"string" + 0.075*"public"')
(22, '0.058*"int" + 0.034*"array"')
(23, '0.237*"app" + 0.076*"tag"')
(15, '0.037*"version" + 0.030*"build"')
(14, '0.139*"property" + 0.047*"binding"')
(7, '0.067*"function" + 0.057*"var"')
(24, '0.022*"strong" + 0.019*"like"')
(19, '0.102*"http" + 0.073*"com"')
(18, '0.072*"stack" + 0.070*"http"')
(4, '0.032*"server" + 0.028*"test"')
(11, '0.192*"android" + 0.049*"view"')
(21, '0.115*"model" + 0.079*"date"')
(9, '0.033*"task" + 0.032*"system"')
(6, '0.048*"row" + 0.046*"list"')
(13, '0.066*"product" + 0.059*"query"')
(1, '0.065*"width" + 0.063*"color"')
  ```

```sh
applyLDAModel.ipynb 
```
Contains the code needed to build load and run the built LDA model. <br>

Next potential topics manually considered and assigned to each of the pairs of two topic words.
```shl 
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
```
So for example 'width' and 'color' from above were decided to be related to 'CSS styling.' 

This script is run by calling the getTopics function and passing in the text for which you want the top three topics identified for based on the LDA model. The text is cleaned using the same steps as in the buildLDAModel document. Dataframes can also be handled instead of strings by calling the preapareTextDf method.<br>

In the case of a dataframe, the LDA model is applied to each row:
```sh
df['Body_processed_topics_sorted'] = df.apply(lambda x: sorterTopThree(x['Body_processed_topics']), axis=1)
```
And then the top three topics are saved to the dataframe:
```sh
df['Body_processed_topics_sorted'] = df.apply(lambda x: sorterTopThree(x['Body_processed_topics']), axis=1)
```
Which was then saved as a new .csv file so that the results could analyzed. 
```sh
qdataCombined.to_csv("FinalData\\qdataCombined.csv", encoding="utf-8")
```

### Similar Question Predictor
```sh
cosinesimilarity.py 
```
Iterates over the dataframe of questions and finds the top 5 that are closest to the passed in text based on the cosine similarities.<br>

The question is added to the first row of the dataframe of questions:
```sh
df.loc[-1] = [-1, text]  
df.index = df.index + 1  
df.sort_index(inplace=True)
```
Then the document cosine similarity matrix is created and used to find the
5 closest matches to the question (which is always the first row) 
```sh
cv = CountVectorizer(stop_words = 'english', min_df=5, max_features=500)
count_matrix = cv.fit_transform(df['Text'])

cosine_sim = cosine_similarity(count_matrix)

closest_Q = list(enumerate(cosine_sim[0]))

sorted_similar = sorted(closest_Q, key=lambda x:x[1], reverse=True)
sorted_similar = sorted_similar[1:6]
```
### Testing
Test #1 <br>
![unit_t1](https://user-images.githubusercontent.com/28748883/145751900-34f060e8-97f6-465a-bd80-99d6d57f6cbc.png)

## Discussion 
It is essential to note that the data was collected as posts type 1 (questions) post type 2 (answers) and comments. These three categories are related in that users posts questions, other users submit answers and both parties can comment as frequently under their own and others questions and answers. We look at question data to explain the topics with which users struggle the most, within this data we are able to extract yearly trends that forecast the popularity or need for help within certain subject areas of computer software. Answer and comment data are utilized to portrait a more in depth view of the sentiment and emotions towards a particular subject. 
### Questions
Using significant tags found within the corpus of most popular tags we are able to label each post as it pertains to a particular topic. This allows us the ability to visualize the change in topic popularity over time, with respect to overall sentiment. It was found that on average topics such as git, eclipse and node.js are of the top most disliked within the set. The most like topics are excel and wordpress. We can alter our view within the dashboard to examine each year and the subject matter most talked about, this also alters the tree map showing the relative density of each topic by year. 

### Answers
Since our answer data did not explicitly define tags of related content to classify each post, we began by creating our own analysis of the text. 

******* LUKE ADD HOW YOU EXTRACTED THE GENERAL TOPICS *******
The general topics found within answer responses are most often of the type HTML or TCP/IP domains. Through examination of the data we see that the top three types of content within answer responses was found to be HTML, TCP/IP Domains, and methods and variables. We wanted to identify who was answering questions the most and which of these individual accounts were the most positive of the entire set, these user accounts can be found in the dash board figure title: Top 10 User Accounts by Answers. An interesting detail was found upon creation of visualizations in that Answer data does not contain link type responses. The code used to generate labels for both answers and comments is identical and should classify under three categories, yet no response are found as link type within the answer data set. 







Test #2
![unit_t2](https://user-images.githubusercontent.com/28748883/145751928-b24c9207-a9de-4a5a-909c-a627e7b9cfae.png)

Test #3
![unit_t3](https://user-images.githubusercontent.com/28748883/145751940-a6a192d1-5245-4e9d-b4d2-3f6ff4ee497b.png)

Test #4
![unit_t4](https://user-images.githubusercontent.com/28748883/145751959-a4f17962-e0a4-4173-b7e6-e8c904589664.png)

Test #5
![unit_T5](https://user-images.githubusercontent.com/28748883/145751969-7ca43c93-c075-4d24-89bc-524ecc9dd80a.png)



## References
The following sites were used as a reference during the creation of our project:

* [LDA Topic Modelling With Gensim](https://predictivehacks.com/lda-topic-modelling-with-gensim/) 

