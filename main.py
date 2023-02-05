import pymongo
from flask import Flask, jsonify, request
import json
from dotenv import load_dotenv
import os

app = Flask(__name__)

load_dotenv()
USERNAME = os.getenv("USERNAME")
PASSWORD = os.getenv("PASSWORD")
DATABASE = os.getenv("DATABASE")
COLLECTION = os.getenv("COLLECTION")
HOST = os.getenv("HOST")

uri = "mongodb+srv://{}:{}@{}".format("kalp", PASSWORD, HOST)
client = pymongo.MongoClient(uri)
db = client[DATABASE]
collection = db[COLLECTION]


@app.route("/")
def index():
    documents = collection.find()
    data = [doc for doc in documents]
    res = json.dumps(data, default=str)
    return json.loads(res), 200


@app.route("/list", methods=["GET"])
def get_data():
    documents = collection.find()
    data = [doc for doc in documents]
    raw_data = json.dumps(data, default=str)
    parsed_data = json.loads(raw_data)
    resources = []

    category = request.args.get("category")

    if category:
        for doc in parsed_data[0]['data']:
            if doc['categories'][0] == category:
                resources.append(doc)

        res = dict({
            "count": len(resources),
            "data": resources
        })
        return res
    else:
        return []


if __name__ == "__main__":
    app.run(debug=False, host='0.0.0.0')
