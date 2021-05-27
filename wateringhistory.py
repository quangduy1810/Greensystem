from re import T
from mysql.connector.catch23 import STRING_TYPES
from pkg_resources import Environment
from getconnect import Connection
from devicestate import *
import time
from envirstate import *


def getPumpHistory():
    data = aio.data('pump')
    get = []
    for i in data:
        get = get + [{'created_at':i.created_at,'value':i.value}]
    return get


def getLightHistory():
    data = aio.data('light')
    get = []
    for i in data:
        get = get + [{'created_at':i.created_at,'value':i.value}]
    return get
