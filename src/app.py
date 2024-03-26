from flask import Flask, render_template, request, redirect, url_for, jsonify

from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

import datetime
import requests
from dotenv import load_dotenv
import os
import pandas as pd
import json
from bson import json_util




# Conectando ao MongoDB
load_dotenv()
MongoURL = os.getenv("MongoURL")

client = MongoClient(MongoURL, server_api=ServerApi('1'))
db = client.task_manager
collection = collection = db.tasks



app = Flask(__name__)

@app.route('/')
def index():
    tasks = collection.find({})
    return render_template('index.html', tasks=tasks)

@app.route('/teste')
def teste():
    return 'APP ok'

@app.route('/tasks')
def get_tasks():
    tasks = []
    for post in collection.find():
        post['_id'] = str(post['_id'])
        tasks.append(post)

    tasks = json.dumps(tasks)

    return tasks

@app.route('/tasks_formatado')
def listar_documentos():
    # Obtendo todos os documentos da coleção
    documentos = list(collection.find({}))

    # Convertendo os documentos em JSON
    json_data = json_util.dumps(documentos)

    # Retornando a resposta JSON
    return jsonify(json_data)


@app.route('/add_task', methods=['POST'])
def add_task():
    name = request.form['name']
    description = request.form['description']
    task = {'name': name, 'description': description}
    collection.insert_one(task)
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True, port=3000)
