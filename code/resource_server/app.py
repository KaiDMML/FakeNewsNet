import json

from flask import Flask
from flask import jsonify
from flask import request
from flask_cors import CORS

from resource_server.ResourceAllocator import ResourceAllocator

app = Flask(__name__)

cors = CORS(app)

keys_state = dict()


def init_state(num_keys):
    print("No. of twitter keys : {}".format(num_keys))
    keys_state["get_retweet"] = ResourceAllocator(num_keys, time_window=905, window_limit=75)
    keys_state["get_tweet"] = ResourceAllocator(num_keys, time_window=905, window_limit=900)
    keys_state["get_follower_friends_ids"] = ResourceAllocator(num_keys, time_window=920, window_limit=15)
    keys_state["get_followers_ids"] = ResourceAllocator(num_keys, time_window=900, window_limit=15)
    keys_state["get_friends_ids"] = ResourceAllocator(num_keys, time_window=900, window_limit=15)
    keys_state["get_user"] = ResourceAllocator(num_keys, time_window=905, window_limit=900)
    keys_state["get_user_tweets"] = ResourceAllocator(num_keys, time_window=925, window_limit=900)


@app.route('/get-keys', methods=['GET'])
def get_key_index():
    args = request.args

    try:
        type = args["resource_type"]

        allocator = keys_state[type]
        resource_index = allocator.get_resource_index()

        response = {}
        if resource_index < 0:
            response["status"] = 404
            response["wait_time"] = abs(resource_index)
        else:
            response["status"] = 200
            response["id"] = resource_index

        return jsonify(response)

    except Exception as ex:
        print(ex)

    return jsonify({'result': 500})


def get_num_process():
    json_object = json.load(open("config.json"))
    return int(json_object["num_twitter_keys"])


if __name__ == '__main__':
    init_state(get_num_process())
    app.run(host='0.0.0.0', debug=False)
