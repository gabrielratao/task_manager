from flask import Flask, render_template, request, redirect, url_for, jsonify
from flask_cors import CORS


from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

import datetime
import requests
from dotenv import load_dotenv
import os
import pandas as pd
import json
from bson import json_util
from bson import ObjectId



# Conectando ao MongoDB
load_dotenv()
MongoURL = os.getenv("MongoURL")

client = MongoClient(MongoURL, server_api=ServerApi('1'))
db = client.task_manager
collection = db.tasks



app = Flask(__name__)
CORS(app) #acesso ao navegador

@app.route('/')
def index():
    tasks = collection.find({})
    return render_template('index.html', tasks=tasks)

@app.route('/teste')
def teste():
    return jsonify('APP ok')

#read tasks
@app.route('/tasks')
def get_tasks():
    tasks = []
    for post in collection.find():
        post['_id'] = str(post['_id'])
        tasks.append(post)

    
    return jsonify(tasks)
    
#create tasks
@app.route('/tasks', methods=['POST'])
def add_task():
    body = request.json
    print(body)
    # name = request.form['name']
    # description = request.form['description']
    # task = {'name': body['name'], 'description': body['description']} criar apenas com propriedades especificas
    task = body
    collection.insert_one(task)
    # return redirect(url_for('index'))
    body['_id'] = str(body['_id'])
    return jsonify({body['name']: "criado com sucesso",
                    "properties": body})

#delete task
@app.route('/tasks/<string:id>', methods=['DELETE'])
def remove_task(id):
    print(id)
    result = collection.delete_one({'_id': ObjectId(id)})
    if result.deleted_count == 1:
        return jsonify({'id': id,
                        'deleted': True})
    else:
        return jsonify({'id': id,
                        'deleted': False})

#update task
@app.route('/tasks/<string:id>', methods=['PUT', 'PATCH'])
def update_taks(id):
    # collection.update_one()
    body = request.json
    result = collection.update_one({'_id': ObjectId(id)}, {'$set': body})
    
    if result.modified_count == 1:
        return jsonify({'id': id,
                        'updated': True,
                        'properties': body})
    else:
        return jsonify({'id': id,
                        'updated': False})




if __name__ == '__main__':
    app.run(debug=False, port=3000)
