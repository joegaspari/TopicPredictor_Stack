# File Structure

J.work
    -Data (first try set)
    -Data2 (Final set)
        -.ipynb_checkpoints
        -FinalData
            -.ipynb_checkpoints
            -adata.csv
            -adataCombined.csv
            -cdata.csv
            -cdataCombined.csv
            -qdata.csv
        -AllPosts.csv
        -Answers.csv
        -Comments.csv
        -Figdescriptions.docx
        -Questions.csv
        -Top50tags.csv
    -Supplement
    -comDefs.py
    -posts.py
    -preProcess.ipynb
    -README.md
    -StackDash.twb
# preProcess.ipynb

This notebook was utilized to work with and visualize the methods created in both posts.py and comDefs.py

  * Data folder found within J.work contains the original csv files used in our analysis. Our goal was to link the users to each post type to illustrate the changes in response over time. It was found that the data was highly skewed and did not accurately encompass the set, thus a random sample was produced for each response type and saved within files found in J.work/Data2.

The methods used in generating clean text responses specific to the data provided by Stack Overflow are found in post.py and comDefs.py

# posts.py

### load_Q & load_A 
Two methods used to load saved CSV data and clean unwanted columns, converting string dates into proper date time format.

### Cleaning Methods
    clean( text ): 
        -method calls following preprocessing methods
            -remove_newLT(text)
            -remove_Html(text)
            -remove_white(text)
            -remove_doubles(text)
            -expand_contrt(text)
            -remove_nonE(text)
            -spellck(text)

### Question Topic / Tag Processing
    Top tags are generated using get_topWords( dataframe, topN )
    Individual tags are assigned using methods clean_tokenize( tag ) & generate_tag( df_tag )


### Combining Data
posts.py was utilized for the analysis found in each CSV file in Data2/FinalData 
    load_clean_Q( dataF ) & load_clean_A( dataF ) combines all the calculated fields for each entry of questions and answers into one data frame that is eventually exported as a CSV for use in tableau. 




# comDefs.py 
This file is primarily utilized by comment data as this data is processed in a slightly different manner, as to include special characters related to high level coding language. 

### load_comm()
    loads comment data csv found in Data2, and cleans away unrelated columns. 
### Cleaning Methods
    clean( text ):
        -remove_newLT(text)
        -remove_white(text)
        -remove_doubles(text)
        -expand_contrt(text)


### Response Typing 

To generate response type for each answer and comment, we used Comment_Type() to create an individual label for each entry in our set. 

### Combining Data
load_comments_data( data ) method was used to combine all calculated feilds into one dataframe for each entry. This data frame is subsequently written to CSV format and saved in Data2/FinalData