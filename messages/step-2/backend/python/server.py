import json
from bottle import route, run, request, response, static_file, hook
from pymemcache.client import Client
import logging

DB_HOST = 'localhost'
DB_PORT = 5652
APP_HOST = 'localhost'
APP_PORT = 5650

db = Client((DB_HOST, DB_PORT), default_noreply=False)

def get_count():
    count = db.get('aaa')
    return count

def get_messages(count):
    ids = range(1, count)
    return db.get_multi(map(lambda x: 'message:'+str(x), ids))

@route('/api/message')
def get_message():
    count = get_count()
    logging.warning(count)

    messages = get_messages(count)

    # message = db.get('message')
    if messages is not None:
        decoded = map(lambda x: x.decode('utf8'), messages)
        return {'message': decoded}
    response.status = 400



def incr_count():
    count = db.get('aaa')
    if count:
        return db.incr('aaa', 1)
    else:
        db.set('aaa', 1)
        return 1


@route('/api/message', method='POST')
def post_message():
    sender = request.get_header('uniqys-sender')
    body = request.json
    message = body['message']

    count = incr_count()

    db.set('message:'+str(count), message.encode('utf8'))

run(host=APP_HOST, port=APP_PORT, debug=True, reloader=True)