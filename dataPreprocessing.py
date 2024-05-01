import pandas as pd
import re
from nltk.tokenize import RegexpTokenizer
from nltk.corpus import stopwords
from nltk.corpus import wordnet
from nltk.stem import WordNetLemmatizer
import nltk



def preprocess_text(text):
    # Remove HTML tags
    text = re.sub(r'<[^>]+>', ' ', text)
    # Remove special characters and line breaks
    text = re.sub(r'([^\s\w_])+', ' ', text)
    text = re.sub(r'[\n\r]', ' ', text)
    # Remove numbers
    text = re.sub(r'\d+', ' ', text)
    return text

# Function to tokenize text
def tokenize_text(text):
    tokenizer = RegexpTokenizer('\w+|\$[\d\.]+|\S+')
    if isinstance(text, str):  # If text is a single string
        text = text.lower()
        words = tokenizer.tokenize(text)
        return words
    elif isinstance(text, list):  # If text is a list of strings
        lowercased_words = [word.lower() for word in text]
        tokenize_words =   [tokenizer.tokenize(word) for word in lowercased_words]
        return lowercased_words

# Function to remove stopwords
def remove_stopwords(words):
    stop = set(stopwords.words('english'))
    filtered_words = [w for w in words if w not in stop]
    return filtered_words

# Function to perform lemmatization
def lemmatize_text(words):
    lemmatizer = WordNetLemmatizer()
    lem_words = [lemmatizer.lemmatize(word, get_part_of_speech_tags(word)) for word in words]
    return lem_words

# Function to get Part of Speech tags
def get_part_of_speech_tags(word):
    tag_dict = {"J": wordnet.ADJ,
                "N": wordnet.NOUN,
                "V": wordnet.VERB,
                "R": wordnet.ADV}
    tag = nltk.pos_tag([word])[0][1][0].upper()
    return tag_dict.get(tag, wordnet.NOUN)