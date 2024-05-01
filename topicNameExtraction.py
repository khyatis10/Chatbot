
import gensim
from gensim.utils import simple_preprocess
# Function to convert text to words
import gensim.corpora as corpora



def text_to_words(texts):
    return [[word for word in simple_preprocess(str(text), deacc=True)]
            for text in texts]

# Function to extract topics using LDA model and return topic numbers
def extract_topics(text):
    dict_word = getDictUserQuestion(text)
    lda_model = gensim.models.LdaModel.load('model/lda_model')
    text_words = text_to_words([text])
    # Create corpus
    corpus_vec = [dict_word.doc2bow(words) for words in text_words]
    # Get topic distribution
    topics = lda_model.get_document_topics(corpus_vec[0])
    #print("Topics inside extract topics is **************", topics)
    # Extract most probable topic
    topic_num = max(topics, key=lambda x: x[1])[0]
    return topic_num


# Function to get topic names based on representative words
def infer_topic_names(lda_model, dict_word, num_words=3):
    topic_names = {}
    for i in range(lda_model.num_topics):
        #print("i is", i)
        words = lda_model.show_topic(i, topn=num_words)
        #print("words is", words)
        topic_names[i] = ', '.join([word for word, _ in words])
        #print("topic names ",topic_names)
    return topic_names

def getDictUserQuestion(userQuestion):
    #Need to have dictionary of all words
    text_words = text_to_words(userQuestion)
    dict_word = corpora.Dictionary(text_words)
    dict_word.filter_extremes(no_below=2, no_above=0.1, keep_n=2000)
    return dict_word