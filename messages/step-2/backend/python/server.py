import json
from bottle import route, run, request, response, static_file, hook
from pymemcache.client import Client
import logging
import json
import ast

DB_HOST = 'localhost'
DB_PORT = 5652
APP_HOST = 'localhost'
APP_PORT = 5650

db = Client((DB_HOST, DB_PORT), default_noreply=False)

def get_count():
    count = db.get('count').decode('utf8')
    # if type(count) is 'str':
    return int(count)
    # else:
        # return 0

def get_messages(count):
    ids = range(1, count + 1)
    neko = db.get_multi([f'messages:{id}' for id in ids])
    inu = [{'id': id, **(ast.literal_eval(neko[f'messages:{id}'].decode('utf-8')))} for id in ids]
    return inu

@route('/api/message')
def get_message():
    count = get_count()
    messages = get_messages(count)
    return {'messages': messages}

def incr_count():
    count = db.get('count')
    if count:
        return db.incr('count', 1)
    else:
        db.set('count', 1)
        return 1


@route('/api/message', method='POST')
def post_message():
    sender = request.get_header('uniqys-sender')
    timestamp = request.get_header('uniqys-timestamp')
    blockhash = request.get_header('uniqys-blockhash')

    body = request.json
    message = body['message']

    count = incr_count()

    db.set('messages:'+str(count), {
        "sender": sender,
        "timestamp": timestamp,
        "blockhash": blockhash,
        "contents": message.encode('utf-8')
    })

run(host=APP_HOST, port=APP_PORT, debug=True, reloader=True)