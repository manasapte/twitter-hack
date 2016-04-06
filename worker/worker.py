import redis
import boto3
import json
import threading

class worker(threading.Thread):
    def __init__(self, threadId, topic):
        threading.Thread.__init__(self)
        self.queue = boto3.resource('sqs').Queue("https://sqs.us-west-1.amazonaws.com/799329042485/first_queue")
        self.threadId = threadId
        self.topic = topic

    def run(self):
        messages = queue.receive_messages(MaxNumberOfMessages=10, VisibilityTimeout=1)
        bodies = [json_loads(message[0].body) for message in messages]
        print bodies
	deleteIds = [{'Id': count++, 'ReceiptHandle': message.receipt_handle} for message in messages]
	queue.delete_messages(Entries=deleteIds)

topics=["buzzfeed", "nba", ""]
[worker()]
