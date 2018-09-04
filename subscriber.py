from google.cloud import pubsub_v1
import json
import mypipeline
from multiprocessing import Queue
import multiprocessing as mp
import time

def receive_messages(project, subscription_name, receiverQueue: Queue):
    """Receives messages from a pull subscription."""
    subscriber = pubsub_v1.SubscriberClient()
    subscription_path = subscriber.subscription_path(
        project, subscription_name)

    def callback(message):
        #print('Received message: {}'.format(message))
        rawdata = json.loads(message.data.decode('utf-8'))
        receiverQueue.put(rawdata)
        message.ack()

    subscriber.subscribe(subscription_path, callback=callback)

    # The subscriber is non-blocking, so we must keep the main thread from
    # exiting to allow it to process messages in the background.
    print('Listening for messages on {}'.format(subscription_path))

def wait_completion(workerlst):
    for eachworker in workerlst:
        eachworker.terminate()
        eachworker.join()


if __name__ == '__main__':
    messageQueue = mp.Queue()
    L1 = mp.Queue()
    L2_succ = mp.Queue()
    L2_fail = mp.Queue()
    L3 = mp.Queue()
    num_worker = 1
    num_uploader = 1
    workerlst=[]
    print('Starting workers')
    for idx in range(num_worker):
        p=mp.Process(target=mypipeline.mypipeline, args=(messageQueue, L1, L2_succ, L2_fail, L3),daemon=True )
        workerlst.append(p)
        p.start()
        print(idx)
    print('Pipeline Worker Started')
    for idx in range(num_uploader):
        p=mp.Process(target=mypipeline.L1_uploader, args=(L1,),daemon=True)
        workerlst.append(p)
        p.start()

    print('L1 Worker Started')
    for idx in range(num_uploader):
        p=mp.Process(target=mypipeline.L2queue_SUCC, args=(L2_succ,),daemon=True)
        workerlst.append(p)
        p.start()
    for idx in range(num_uploader):
        p=mp.Process(target=mypipeline.L2queue_FAIL, args=(L2_fail,),daemon=True)
        workerlst.append(p)
        p.start()
    print('L2 Worker Started')
    for idx in range(num_uploader):
        p=mp.Process(target=mypipeline.L3queue, args=(L3,),daemon=True)
        workerlst.append(p)
        p.start()
    print('L3 Worker Started')
    receive_messages('yl3573-214601', 'pubsub_test', messageQueue)
    while True:
        try:
            print('All started')
            time.sleep(10)
        except:
            print('existing....')
            wait_completion(workerlst)
            print('existing....Done')
            raise



