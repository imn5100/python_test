# -*- coding=utf-8 -*-
import sys

import os
from Crypto.Cipher import AES
from binascii import b2a_hex, a2b_hex


# pip install pycrypto
class PyCrypto:
    def __init__(self, key):
        self.key = self.add_to_length(16, key)
        self.mode = AES.MODE_CBC
        self.aes = AES.new(self.key, self.mode, self.key)

    @staticmethod
    def add_to_length(length, text):
        return text + ('\0' * (length - (len(text) % length)))

    def encrypt(self, text):
        return b2a_hex(AES.new(self.key, self.mode, self.key).encrypt(self.add_to_length(16, text)))

    def decrypt(self, text):
        return AES.new(self.key, self.mode, self.key).decrypt(a2b_hex(text)).rstrip('\0')


def get_avg(name, params):
    if params and len(params) > 1 and name in params and (params.index(name) + 1) < len(params):
        return params[params.index(name) + 1]
    return None


if __name__ == '__main__':
    args = sys.argv
    decode = False
    if args and '-decode' in args:
        decode = True
    key = get_avg('-key', args)
    f = get_avg('-f', args)
    data = get_avg('-data', args)
    out_put = get_avg('-out', args)
    if key and len(key.strip()) > 0:
        if f and os.path.exists(f):
            data = open(f, 'r').read()
        if data is None or len(data.strip()) == 0:
            print('-data your_data or -f your_file')
        else:
            pyCrypto = PyCrypto(key)
            code_data = pyCrypto.decrypt(data) if decode else pyCrypto.encrypt(data)
            if out_put:
                open(out_put, 'w').write(code_data)
            else:
                print(code_data)
    else:
        print('-key  your_key')
