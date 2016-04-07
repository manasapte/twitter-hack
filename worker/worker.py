import redis
import boto3
import json
import threading
import signal

class worker(threading.Thread):
    def __init__(self, threadId):
        threading.Thread.__init__(self)
        self.queue = boto3.resource('sqs').Queue("https://sqs.us-west-1.amazonaws.com/799329042485/first_queue")
        self.threadId = threadId
	self.r = redis.StrictRedis(host='localhost', port=6379, db=0)

    def run(self):
	while True:
            count = 0
            messages = self.queue.receive_messages(MaxNumberOfMessages=10, VisibilityTimeout=10)
            bodies = [json.loads(message.body) for message in messages]
            #print bodies
            #tags1 = [ {"list": body.get("list", ""), "rankterm": mention, "tid": body.get("tweet_id_str", "") } for body in bodies for mention in body.get("user_mentions", [])] 
            tags = [ {"list": body.get("list", ""), "rankterm": hashtag, "tid": body.get("tweet_id_str", "") } for body in bodies  for hashtag in body.get("hashtags", [])]
            [self.r.zincrby(tag["list"], tag["rankterm"]) for tag in tags] #tags1 + tags2]	
            [self.r.lpush(tag["list"] + "/" + tag["rankterm"], tag["tid"]) for tag in tags] #tags1 + tags2]
            deleteIds = [{'Id': message.message_id, 'ReceiptHandle': message.receipt_handle} for message in messages]
	    if len(deleteIds) > 0:
                self.queue.delete_messages(Entries=deleteIds)	

def signal_handler(signal, frame):
        print('You pressed Ctrl+C!')
        sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)
threads = [worker(id) for id in range(20)]
[thread.start() for thread in threads]
[thread.join() for thread in threads]
