# This file will read the data from data from , create a topic column and create json of Question , Answer and lable (topic).
# This goes to question_to_vector file.

from dataPreprocessing import preprocess_text,tokenize_text,lemmatize_text,remove_stopwords,get_part_of_speech_tags
import pandas as pd
import gensim
import pickle

from topicNameExtraction import text_to_words, infer_topic_names



def topicModelling():
   return ""



def getTopics(userQuestion):
    # Load the dictionary from the file
    lda_model = gensim.models.LdaModel.load('model/lda_model')
    with open('model/dictionary.pkl', 'rb') as f:
        dict_word = pickle.load(f)

    new_data = pd.DataFrame(data=[userQuestion], columns=['Question'])

    #new_data.head()
    new_data['Question_processed'] = new_data['Question'].apply(preprocess_text)
    new_data['Question_processed'] = new_data['Question_processed'].apply(tokenize_text)
    new_data['Question_processed'] = new_data['Question_processed'].apply(remove_stopwords)
    new_data['Question_processed'] = new_data['Question_processed'].apply(lemmatize_text)
    new_data['Question_processed'] = new_data['Question_processed'].apply(lambda x: ' '.join(x))

    new_text = new_data.Question_processed.values.tolist()
    new_text_words = text_to_words(new_text)
    new_corpus_vec = [dict_word.doc2bow(text) for text in new_text_words]

    topic_names = infer_topic_names(lda_model, dict_word)

    # Infer topics for the new data
    new_topics = [max(lda_model.get_document_topics(doc), key=lambda x: x[1])[0] for doc in new_corpus_vec]

    # Interpret the inferred topics for the new data
    new_data['Topic_Num'] = new_topics
    new_data['Topic'] = new_data['Topic_Num'].map(topic_names)

    user_output = new_data[['Question', 'Question_processed', 'Topic']]
    # Extract the 'Topic' column from user_output
    topics = user_output['Topic']

    topics_list = topics.astype(str).tolist()

    # Join the elements of the list into a single string
    topics_string = ' '.join(topics_list)

    return topics_string