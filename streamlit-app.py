import streamlit as st
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import pandas as pd
import pickle

with open('data/vector_db.pickle' ,'rb') as file:
    vectors = pickle.load(file)

with open('data/req_df.pickle' ,'rb') as file:
    df = pickle.load(file)

with open('data/count_vectorizer.pickle' ,'rb') as file:
    cv = pickle.load(file)

with open('data/types.pickle' ,'rb') as file:
    types = pickle.load(file)

with open('data/tasks.pickle' ,'rb') as file:
    tasks = pickle.load(file)

model_types = ["Transformers", "Layoutlmv3", "Layoutlmv2", "Layoutlm", "Vision Encoder Decoder", "Langchain", "Text Generation Inference", "Adapter Transformers", "Diffusers", "Timm", "Mistral", "Zoedepth", "Vit", "Beit", "Segformer", "Swinv2", "Other"]
frameworks = ["Pytorch", "Tensorflow", "Safetensors", "Tensorboard", "Onnx", "OpenAI API", "Tflite", "Jax", "Other"]

def recommend_models(user_input):
    user_vector = cv.transform([user_input]).toarray()
    similarity_with_user = cosine_similarity(vectors ,user_vector)
    recommended_indices = sorted(range(len(similarity_with_user)) ,key=lambda i: similarity_with_user[i] ,reverse=True)[:10]
    # recommended_models = []
    recommended_models = df.iloc[recommended_indices].sort_values(by='downloads', ascending=False)

    # for index in recommended_indices:
    #     print(df.iloc[index]['text'])
    return recommended_models

# Streamlit app
st.title("Model Recommendation System")

# Dropdown menus for user inputs
task_type = st.selectbox("Select Task Type:",types)
index_of_selected_type = types.index(task_type)

task = st.selectbox("Select Task:",tasks[index_of_selected_type])

model_type = (st.selectbox("Select Model Type:", model_types)).replace(' ', '-')
framework = (st.selectbox("Select Framework:", frameworks)).replace(' ', '-')

if model_type=='Other':
    model_type = ''
if framework=='Other':
    framework = ''

user_input = f"{task_type.replace(' ', '-')} {task} {model_type} {framework}"

# Button to get recommendations
if st.button("Get Recommendations"):
    recommendations = recommend_models(user_input.lower())
    print(user_input.lower())
    st.write("Recommended Models:")

    base_url = 'https://huggingface.co/'
    for _, row in recommendations.iterrows():
        model = row['modelId']
        downloads = row['downloads']
        likes = row['likes']
        createdAt = row['createdAt']
        author = row['author']
        model_link = f"{base_url}{model}"
        st.markdown(f"{model} - {downloads} Downloads - {likes} Likes - {author} Author - Created At {createdAt} - [Link]({model_link})")