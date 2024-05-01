## AI Chatbot 
This project is a chatbot project which is created specifically for answering questions related to educational subjects. Topics like data science, AI, Databases is what covered here. 

This chatbot is based on NLP techniques like 
1. LDA topic modeling for extarcting topics from question and refining our search and making it robust and efficient.
2. Cosine Similarity based vector search in MongoDB to find answer for the question from our DB which is closest match.
3. TF-IDF vectorizer for vectorizing the questions.
4. Finally there is UI created which is implemented on Gradio 

### How to run?
    1) Configure your keys in config.py()
    2) Make sure you have access to mongoDb atlas
    3) Have all python dependencies ready (gradio and pymongo to be specific)
    4) Run gradio.py

