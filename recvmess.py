from pkg_resources import Environment
from getconnect import Connection
import time

def message(aio, feed_id, payload):
    print('Feed {0} received new value: {1}'.format(feed_id, payload))