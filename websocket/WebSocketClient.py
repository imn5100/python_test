# -*- coding=utf-8 -*-
import codecs
import json
import urlparse

from tornado import escape, gen, httpclient, httputil, ioloop, websocket
from urllib import urlencode
from Frame import Frame

APPLICATION_JSON = 'application/json'

DEFAULT_CONNECT_TIMEOUT = 60
DEFAULT_REQUEST_TIMEOUT = 60

CMD_ABORT = 'ABORT'
CMD_ACK = 'ACK'
CMD_BEGIN = 'BEGIN'
CMD_COMMIT = 'COMMIT'
CMD_CONNECT = 'CONNECT'
CMD_DISCONNECT = 'DISCONNECT'
CMD_NACK = 'NACK'
CMD_STOMP = 'STOMP'
CMD_SEND = 'SEND'
CMD_SUBSCRIBE = 'SUBSCRIBE'
CMD_UNSUBSCRIBE = 'UNSUBSCRIBE'


def add_url_params(url, params):
    url_parts = list(urlparse.urlparse(url))
    query = dict(urlparse.parse_qsl(url_parts[4]))
    query.update(params)
    url_parts[4] = urlencode(query)
    return urlparse.urlunparse(url_parts)


class WebSocketClient:
    def __init__(self, connect_timeout=DEFAULT_CONNECT_TIMEOUT,
                 request_timeout=DEFAULT_REQUEST_TIMEOUT):
        self.connect_timeout = connect_timeout
        self.request_timeout = request_timeout

    def connect(self, url):
        headers = httputil.HTTPHeaders({'Content-Type': APPLICATION_JSON})
        request = httpclient.HTTPRequest(url=url,
                                         connect_timeout=self.connect_timeout,
                                         request_timeout=self.request_timeout,
                                         headers=headers)
        ws_conn = websocket.WebSocketClientConnection(ioloop.IOLoop.current(),
                                                      request)
        ws_conn.connect_future.add_done_callback(self._connect_callback)

    def send(self, data):
        if not self._ws_connection:
            raise RuntimeError('Web socket connection is closed.')

        self._ws_connection.write_message(escape.utf8(json.dumps(data)))

    def close(self):
        if not self._ws_connection:
            raise RuntimeError('Web socket connection is already closed.')

        self._ws_connection.close()

    def _connect_callback(self, future):
        if future.exception() is None:
            self._ws_connection = future.result()
            self._on_connection_success()
            self._read_messages()
        else:
            self._on_connection_error(future.exception())

    @gen.coroutine
    def _read_messages(self):
        while True:
            msg = yield self._ws_connection.read_message()
            if msg is None:
                self._on_connection_close()
                break

            self._on_message(msg)

    def _on_message(self, msg):
        pass

    def _on_connection_success(self):
        pass

    def _on_connection_close(self):
        pass

    def _on_connection_error(self, exception):
        pass


class DoloresStompWebSocketClient(WebSocketClient):

    def __init__(self, token, driver_id, user_id):
        WebSocketClient.__init__(self)
        self.token = token
        self.driver_id = driver_id
        self.user_id = user_id
        self.sub_topic = '/dolores/driver/%s/%s' % (self.user_id, self.driver_id)

    def connect(self, url):
        url = add_url_params(url, {'token': self.token})
        WebSocketClient.connect(self, url)

    def _on_message(self, msg):
        if msg.startswith('a["') and msg.endswith("\u0000\"]"):
            msg = u'\u0000'.join(msg.rsplit('\u0000', 1)).encode('utf-8').decode('string-escape')[3:-3]
        msg = Frame.read_message_to_frame(msg)
        if msg.cmd == 'MESSAGE':
            print(msg)

    def _on_connection_success(self):
        print('Connected!')
        conn_frame = Frame(CMD_CONNECT,
                           headers={'accept=version': '1.1,1.0', 'heart-beat': '10000,10000'})
        sub_frame = Frame(CMD_SUBSCRIBE, headers={'id': 'sub-0', 'destination': self.sub_topic})
        self.send(conn_frame.convert_to_data())
        self.send(sub_frame.convert_to_data())

    def _on_connection_close(self):
        print('Connection closed!')
        exit(0)

    def _on_connection_error(self, exception):
        print('Connection error: %s', exception)
        exit(0)

    def send_frame_msg(self, destination, msg):
        msg_body = json.dumps({'name': msg})
        frame = Frame(CMD_SEND, headers={'destination': destination, 'content-length': len(msg_body)},
                      body=msg_body)
        print(frame.convert_to_data())
        self.send(frame.convert_to_data())


def main():
    token = '4a08398861816f734436c6b10f1d1493'
    client = DoloresStompWebSocketClient(token, 'fe73bd5d5e173c80e6ec7c23694a3af802a66c75008a2cb4', 1)
    client.connect('ws://wst.shawblog.me/dolores/873/qdqavh3w/websocket')
    try:
        ioloop.IOLoop.instance().start()
    except KeyboardInterrupt:
        client.close()


if __name__ == '__main__':
    main()
