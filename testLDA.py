
import gensim

lda_model_1 = gensim.models.LdaModel.load('Topic_model_similarity/lda_model')
topics = lda_model_1.show_topic(0, topn=3)
print(topics)

'''
import gensim

# Load the model
lda_model1 = gensim.models.LdaModel.load('model/lda_model')

# Get the number of topics
num_topics = lda_model1.num_topics

# Print all topics
for i in range(num_topics):
    print(lda_model1.print_topic(i))'''