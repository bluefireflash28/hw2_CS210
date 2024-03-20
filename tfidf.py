import re
from collections import defaultdict
import math
import os

#Part 1 Preprocessing

#Step 1.1 Clean
def clean(text):
    
    file_text = re.sub(r'[^\w\s]', '', file_text) #removes characters that are not words or whitespaces
    file_text = re.sub(r'\s+', ' ', file_text) #removes characters that are multiple whitepaces
    file_text = re.sub(r'http[s]?://\S+', '', file_text) #removes the website link
    return file_text.lower() #makes all the text lowercase
    """
    text = re.sub(r'\b\d+\b', '', text)
    
    # Remove URLs
    text = re.sub(r'http[s]?://\S+', '', text)
    
    # Remove non-word characters and extra whitespaces
    text = re.sub(r'[^\w\s]', '', text)
    text = re.sub(r'\s+', ' ', text)
    return text.lower()
    """

#Step 1.2 Removing the stopwords
def remove_stopwords(file_text, stopwords):
    words = file_text.split()
    new_text = [word for word in words if word not in stopwords]
    return " ".join(new_text) #put all the stopwords into one string

def get_stopwords(): #gets all of the stopwords
    with open("stopwords.txt", "r") as file:
        stopwords = set(word.strip() for word in file) 
        return stopwords
    
#Step 1.3 Stemming and Lemmatization
def stem_words(file_text):
    # Words ending with "ing"
    file_text = re.sub(r'ing\b', '', file_text)
    # Words ending with "ly"
    file_text = re.sub(r'ly\b', '', file_text)
    # Words ending with "ment"
    file_text = re.sub(r'ment\b', '', file_text)
    return file_text

#Part 2: Computing TF-IDF Scores
def compute_term_frequency(document):
    tf = defaultdict(int)
    total_terms = len(document) #gets the amount of words
    for term in document:
        tf[term] += 1 /total_terms #gets the term frequency
    return tf

def compute_inverse_document_frequency(documents):
    total_documents = len(documents)
    idf = defaultdict(int)
    for document in documents:
        for term in set(document):
            idf[term] += 1
    for term in idf:
        idf[term] = math.log(total_documents / (idf[term] + 1)) + 1
    return idf

def calculate_score(tf, idf):
    tfidf = defaultdict(int)
    for term in tf:
        tfidf[term] = tf[term] * idf[term] #multiply the tf and iddf
        tfidf[term] = round(tfidf[term], 2)
    return tfidf

def print_top_words(tfidf, document_name):
    sorted_tfidf = sorted(tfidf.items(), key=lambda x: x[1], reverse=True) #make it go from highest to lowest
    top_terms = sorted_tfidf[:5] #get the top 5
    output_file = "tfidf_" + document_name
    with open(output_file, "w") as file:
        file.write("[")
        for i, (word, score) in enumerate(top_terms):
            if i > 0:
                file.write(", ")
            file.write(f"('{word}', {score})")
        file.write("]")

#Main Preprocessing function
def preprocess():
    stopwords = get_stopwords() #loads all the stopwords
    with open("tfidf_docs.txt", "r") as files:
        for file_name in files:
            file_name = file_name.strip() #goes through every single file 
            with open(file_name, "r") as document: #calls all the functions
                file_text = document.read()
                cleaned_file_text = clean(file_text)
                text_no_stopwords = remove_stopwords(cleaned_file_text, stopwords)
                stemmed_text = stem_words(text_no_stopwords)
                output_file = "preproc_" + file_name
                with open(output_file, "w") as file_output:
                    file_output.write(stemmed_text) #puts all of the output into the file

preprocess()
preprocessed_documents = {}
for file_name in os.listdir():
    if file_name.startswith("preproc_"):
        with open(file_name, "r") as file:
            preprocessed_documents[file_name[8:]] = file.read().split()
    # Compute TF-IDF scores for each document
    idf = compute_inverse_document_frequency(preprocessed_documents.values())
    for document_name, document in preprocessed_documents.items(): 
        tf = compute_term_frequency(document)
        tfidf = calculate_score(tf, idf)
        print_top_words(tfidf, document_name)