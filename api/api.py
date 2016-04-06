from flask import Flask, jsonify
from flask_redis import Redis

app = Flask(__name__)
redis = Redis(app)

@app.route('/trends/<name>/<slug>')
def trends(name, slug):
  key = name + '/' + slug
  print key
  ranked_trends = redis.zrange(key, 0, 4, desc=True, withscores=True)
  print ranked_trends
  trends = [{'term': trend[0], 'rank': trend[1]} for trend in ranked_trends]

  return jsonify({'trends': trends}) 

if __name__ == '__main__':
  app.run(host='0.0.0.0')

