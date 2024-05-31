from flask import Flask, request, jsonify, render_template
import pickle
import pandas as pd
from utils import get_req_data_for_model_rec ,recommend_models ,extract_first_5_words
from utils import get_req_data_for_dataset_rec ,recommend_datasets
import requests

app = Flask(__name__)

######################################
# for deploying the application on web
######################################
# url = "https://huggingface.co/datasets/adarshh9/vector-db-ModelMatch/resolve/main/vector_db.pickle?download=true"
# destination = "data/vector_db.pickle"

# response = requests.get(url, stream=True)
# if response.status_code == 200:
#     with open(destination, 'wb') as f:
#         for chunk in response.iter_content(1024):
#             if chunk:
#                 f.write(chunk)
#         print(f"File downloaded successfully and saved to {destination}")
# else:
#     print(f"Failed to download file. Status code: {response.status_code}")
######################################

vectors_model ,df_model ,cv_model ,task_types ,tasks ,model_types ,frameworks = get_req_data_for_model_rec()

vectors_dataset ,df_dataset ,cv_dataset = get_req_data_for_dataset_rec()

@app.route('/' ,methods=['GET'])
def homePage():
    return render_template('home.html')

@app.route('/model_rec_page')
def modelPage():
    return render_template('model_page.html', types=task_types, tasks=tasks, model_types=model_types, frameworks=frameworks)

@app.route('/modelRecommend', methods=['POST'])
def modelRecommend():
    data = request.json
    user_input = data['user_input']
    recommendations = recommend_models(cv_model ,df_model ,vectors_model ,user_input.lower())
    recommendations_list = []
    for index, row in recommendations.iterrows():
        model_tags = row['text']
        tags = extract_first_5_words(model_tags)
        recommendations_list.append({
            'modelId': row['modelId'],
            'downloads': row['downloads'],
            'likes': row['likes'],
            'createdAt': row['createdAt'],
            'author': row['author'],
            'tags': tags
        })
    return jsonify(recommendations_list)

@app.route('/dataset_rec_page')
def datasetPage():
    return render_template('dataset_page.html')

@app.route('/datasetRecommend', methods=['POST'])
def datasetRecommend():
    data = request.json
    user_input = data['user_input']
    recommendations = recommend_datasets(cv_dataset ,df_dataset ,vectors_dataset ,user_input.lower())
    recommendations_list = []
    for index, row in recommendations.iterrows():
        recommendations_list.append({
            'datasetId': row['id'],
            'downloads': row['downloads'],
            'likes': row['likes'],
            'createdAt': row['createdAt'],
            'author': row['author'],
            'tags': row['tags']
        })
    print(len(recommendations_list))
    return jsonify(recommendations_list)

if __name__ == '__main__':
    app.run(debug=True)