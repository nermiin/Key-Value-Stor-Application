from flask import Flask, request
import redis


app = Flask(__name__)

app.debug = True
rds = redis.Redis("localhost", decode_responses=True)  # connect to server


@app.route('/')
def hello():
    return 'Welcome to my application :) '


@app.route("/HEAD/keys/<id>/", methods=["HEAD"])
def head(id=None):
    """
    check value is exist in database or not

    :param id: [check if exist or not], defaults to None

    """
    if rds.exists(id):
        return "Exists", 302
    return "Not Found", 404


@app.route("/PUT/keys", methods=["PUT"])
def put():
    """
    put key and value to redis database and with expire time
    """
    data = request.json
    expire = request.args.get("expire_in", default=31104000, type=int)  # one year
    for key, value in data.items():
        print(f"{key}:{value}")
        rds.set(key, value, ex=expire)
    return data, 201


@app.route("/GET/keys", methods=["GET"])
@app.route("/GET/keys/<id>/", methods=["GET"])
def get(id=None):
    """
    Get sepcific key or all keys in redis database
    """
    data = dict()
    filter_keys = request.args.get("filter", default="*", type=str)
    if id is None:
        for i in rds.scan_iter(match=filter_keys.replace("$", "*")):
            data[i] = rds.get(i)

    else:
        data[id] = rds.get(id)
        if data is None:
            return data, 404

    return data, 200


@app.route("/DELETE/keys/<id>/", methods=["DELETE"])
@app.route("/DELETE/keys", methods=["DELETE"])
def delete(id=None):
    """
    Delete all keys from redis database or specific keys dependence on value
    """
    if id is None:
        for val in rds.scan_iter(match="*"):
            rds.delete(val)
    else:
        rds.delete(id)
    return "Deleted", 200


if __name__ == "__main__":
    app.run()
