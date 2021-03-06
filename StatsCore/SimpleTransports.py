import json
import socket
import datetime


def get_time_stamp():
    return str(datetime.datetime.now())


class Transport:
    def postMessageOnTransport(self, message):
        message['ts'] = get_time_stamp()
        self.post(json.dumps(message).encode('utf-8'))


class UDPStatsTransport(Transport):
    def __init__(self, host='localhost', port=8080):
        self._host = host
        self._port = port

    def status(self):
        return 'UDP Transport %s:%i' % (self._host, self._port)

    def initTransport(self):
        self._sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    def post(self, message):
        self._sock.sendto(message, (self._host, self._port))


class TCPStatsTransport(Transport):
    def __init__(self, host='localhost', port=8080):
        self._host = host
        self._port = port


    def status(self):
        return 'TCP Transport %s:%i' % (self._host, self._port)

    def initTransport(self):
        self._sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._sock.connect((self._host, self._port))

    def post(self, message):
        try:
            self._sock.send(message)
        except:
            self._sock.connect((self._host, self._port))
            self._sock.send(message)
