import os
from flask import Flask, request, render_template, jsonify
from redditClient import RedditClient
from flask.ext.cache import Cache



cache = Cache(config={'CACHE_TYPE': 'simple'})

reddit = RedditClient()
app = Flask(__name__)
cache.init_app(app)



def strtobool(v):
    return v.lower() in ["yes", "true", "t", "1"]


@app.route('/')
def index():
    return render_template('index.html')

def cache_key():
    return request.full_path

@app.route('/reddit/headlines')
@cache.cached(timeout=3600, key_prefix=cache_key)
def headlines():
        query = request.args.get('query')
        # data = reddit.get_data( topic = query)
        data = reddit.get(topic = query)
        return jsonify({'data': data})



port = int(os.environ.get('PORT', 5000))
app.run(host="0.0.0.0", port=port, debug=True)
