# -*- coding=utf-8 -*-
import codecs
import json

from tornado import escape, gen, httpclient, httputil, ioloop, websocket

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


class StompWebSocketClient(WebSocketClient):

    def _on_message(self, msg):
        if msg.startswith('a["') and msg.endswith("\u0000\"]"):
            msg = u'\u0000'.join(msg.rsplit('\u0000', 1))
            msg = codecs.escape_decode(bytes(msg))[0].decode('utf-8')
            msg = msg[3:-3]
        print(Frame.read_message_to_frame(msg))

    def _on_connection_success(self):
        print('Connected!')
        sub_topic = '/dolores/driver/1/fe73bd5d5e173c80e6ec7c23694a3af802a66c75008a2cb4'
        conn_frame = Frame(CMD_CONNECT,
                           headers={'accept=version': '1.1,1.0', 'heart-beat': '10000,10000'})
        sub_frame = Frame(CMD_SUBSCRIBE, headers={'id': 'sub-0', 'destination': sub_topic})
        self.send(conn_frame.convert_to_data())
        self.send(sub_frame.convert_to_data())

    def _on_connection_close(self):
        print('Connection closed!')
        exit(0)

    def _on_connection_error(self, exception):
        print('Connection error: %s', exception)
        exit(0)


def main():
    client = StompWebSocketClient()
    token = '17e4e9af155210ebeea8ffb2ec70b9cc'
    client.connect('ws://wst.shawblog.me/dolores/873/qdqavh3w/websocket?token=' + token)
    try:
        ioloop.IOLoop.instance().start()
    except KeyboardInterrupt:
        client.close()


if __name__ == '__main__':
    main()
