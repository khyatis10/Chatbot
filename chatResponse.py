import pymongo
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
from openai import OpenAI
import config
import json
from question_to_vector import convertUserQuestionToVector

from topicModelling import getTopics


def query_pipeline(embed_question, topic,collection):
    """
    This function is used to create the pipeline query based on the embedded question and topics found

    Args:
        embed_question (_vector_): result of convertUserQuestionToVector from question_to_vector.py
        topic (_string_): result of getTopics from topicModelling.py

    Returns:
        pipeline (_list_): return the pipeline which will be used in similaritySearch to retrieve answer
    """
    pipeline = [
        {
            '$vectorSearch': {
                'index': 'vector-search-question', 
                'path': 'embed_question', 
                'queryVector': embed_question,
                'filter': {
                    'topic_words':topic
                        },
                'numCandidates': 100, 
                'limit': 1
            }
        }, {
            '$project': {
                '_id': 0, 
                'answer': 1,
                'category': 1,
                'score': {
                    '$meta': 'vectorSearchScore'
                }
            }
        }
    ]

    return pipeline


def similaritySearch(collection, topic, im):

    try:
        embed_question = convertUserQuestionToVector(im)
        pipeline = query_pipeline(embed_question, topic,collection)


        result = collection.aggregate(pipeline)
        for i in result:
         if i['score'] < 0.6:
            answer = "Sorry! Our database is still learning"
            return answer
         else:
            return i['answer']

    except pymongo.errors.OperationFailure as e:
        answer = "Sorry! Our database is still learning"
        return answer
    except Exception as ex:
        answer = "Sorry! Our database is still learning"
        return answer


def getResponse(userquestion):
    global tfidf, answers, X_tfidf

    topics = getTopics(userquestion)
    #print(topics)
    #topics = 'data, science, industry'
    collection = config.connect_mongoDB()
    answer = similaritySearch(collection,topics,userquestion)




    # Classify which model this belongs to
    # Pass the question to question_to_vector
    # Pass the question and vector to similarity search

    return answer

# FUTURE ENHANCEMENT
# We can extend the capability of our chatbot by integrating it with LLMs using below function

def openaiSearch(im):
    client = OpenAI(api_key=config.getOpenAIKey())
    response = client.chat.completions.create(
        model="gpt-3.5-turbo-0125",
        response_format={"type": "json_object"},
        messages=[
            {"role": "system", "content": "You are an AI assistant in an data Science world. You should identify educational questions. \
                 This platform receives question and provides relevant answer. \
                 Respond with a JSON object that contains only one field, 'answser'. Don't include the word, answer:, before the actual sentence "},
            {"role": "user",
             "content": f"{im}?"}
        ]
    )
    answer = response.choices[0].message.content
    return answer





