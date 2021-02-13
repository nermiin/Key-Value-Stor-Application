from flask import Flask, request
import flask
import redis
import requests
import json

app = Flask(__name__)

app.debug = True
db = redis.Redis("localhost",decode_responses=True)  # connect to server


@app.route('/')
def hello():
    return 'Welcome to my application :) '

@app.route("/keys/<value>/", methods=["HEAD"])
def head_request(value=None):
    """
    check value is exist in database or not

    :param value: [check if exist or not], defaults to None
    :type value: [type], optional
    """
    if db.exists(value):
        return flask.jsonify("Exists"), requests.status_codes.codes.found
    return flask.jsonify("Not Found"), requests.status_codes.codes.not_found


@app.route("/keys", methods=["GET"])
@app.route("/keys/<value>/", methods=["GET"])
def get_request(value=None):
    """
    Get sepcific key or all keys in redis database
    """
    data = dict()
    filter_keys = request.args.get("filter", default="*", type=str)
    if value is None:
        for i in db.scan_iter(match=filter_keys.replace("$", "*")):
            data[i] = db.get(i)

    else:
        data[value] = db.get(value)
        if data is None:
            return flask.jsonify(data), requests.status_codes.codes.not_found

    return flask.jsonify(data), requests.status_codes.codes.ALL_OKAY



@app.route("/keys", methods=["PUT"])
def put_request():
    """
    put key and value to redis database and with expire time
    """
    data = request.json
    expire = request.args.get("expire_in", default=31104000, type=int)  # one year
    for key, value in data.items():
        print(f"{key}:{value}")
        db.set(key, value, ex=expire)
    return flask.jsonify(data), requests.status_codes.codes.CREATED


@app.route("/keys/<value>/", methods=["DELETE"])
@app.route("/keys", methods=["DELETE"])
def delete_request(value=None):
    """
    Delete all keys from redis database or specific keys depand on value
    """
    if value is None:
        for val in db.scan_iter(match="*"):
            db.delete(val)
    else:
        db.delete(value)
    return flask.jsonify("Deleted"), requests.status_codes.codes.ALL_OKAY



if __name__ == "__main__":
    app.run()
