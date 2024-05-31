import pickle
import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity

def get_req_data_for_model_rec():
    with open('data/model/vector_db.pickle', 'rb') as file:
        vectors = pickle.load(file)

    with open('data/model/req_df.pickle', 'rb') as file:
        df = pickle.load(file)

    with open('data/model/count_vectorizer.pickle', 'rb') as file:
        cv = pickle.load(file)

    with open('data/model/types.pickle', 'rb') as file:
        task_types = pickle.load(file)

    with open('data/model/tasks.pickle', 'rb') as file:
        tasks = pickle.load(file)

    with open('data/model/model_types.pickle', 'rb') as file:
        model_types = pickle.load(file)

    with open('data/model/frameworks.pickle', 'rb') as file:
        frameworks = pickle.load(file)

    return vectors ,df ,cv ,task_types ,tasks ,model_types ,frameworks


def get_req_data_for_dataset_rec():
    with open('data/dataset/vectors_db.pickle', 'rb') as file:
        vectors = pickle.load(file)

    with open('data/dataset/req_df.pickle', 'rb') as file:
        df = pickle.load(file)

    with open('data/dataset/count_vectorizer.pickle', 'rb') as file:
        cv = pickle.load(file)

    return vectors ,df ,cv
    

def recommend_models(cv ,df ,vectors ,user_input):
    user_vector = cv.transform([user_input]).toarray()
    similarity_with_user = cosine_similarity(vectors, user_vector)
    recommended_indices = sorted(range(len(similarity_with_user)), key=lambda i: similarity_with_user[i], reverse=True)[:10]
    recommended_models = df.iloc[recommended_indices].sort_values(by='downloads', ascending=False)
    return recommended_models

def recommend_datasets(cv ,df ,vectors ,user_input):
    user_vector = cv.transform([user_input]).toarray()
    similarity_with_user = cosine_similarity(vectors ,user_vector)
    recommended_indices = sorted(range(len(similarity_with_user)) ,key=lambda i: similarity_with_user[i] ,reverse=True)[:10]
    recommended_datasets = df.iloc[recommended_indices].sort_values(by='downloads', ascending=False)
    return recommended_datasets

def extract_first_5_words(tags):
    # Split the tags string into words
    words = tags.split()
    # Take the first 5 words
    first_5_words = ' '.join(words[:5])
    return first_5_words