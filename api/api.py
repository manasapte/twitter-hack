from flask import Flask, jsonify
from flask_redis import Redis

app = Flask(__name__)
redis = Redis(app)

@app.route('/trends/<name>/<slug>')
def trends(name, slug):
  key = name + '/' + slug
  ranked_trends = redis.zrange(key, 0, 4, desc=True, withscores=True)
  trends = [{'term': trend[0], 'rank': trend[1]} for trend in ranked_trends]

  return jsonify({'trends': trends}) 

@app.route('/tweets/<name>/<slug>/<term>')
def tweets(name, slug, term):
  key = name + '/' + slug + '/' + term
  tweets = redis.lrange(key, 0, -1)
  
  if tweets is None:
    tweets = []

  return jsonify({'term': term, 'tweets': tweets})

if __name__ == '__main__':
  #v = redis.lrange("nba/espn/espn", 0, -1)
  app.run(host='0.0.0.0')

