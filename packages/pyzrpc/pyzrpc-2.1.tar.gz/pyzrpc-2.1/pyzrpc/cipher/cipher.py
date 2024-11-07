# -*- encoding: utf-8 -*-
import base64
from Cryptodome.PublicKey import RSA
from Cryptodome.Cipher import PKCS1_v1_5

from pyzrpc.meta import CIPHER_CIPHERTEXT_KEY, CIPHER_PRIVATE_KEY_KEY


class _Cipher:

    def __init__(self, config):
        self.ciphertext = base64.b64decode(config[CIPHER_CIPHERTEXT_KEY].encode('utf-8'))
        self.private_key = base64.b64decode(config[CIPHER_PRIVATE_KEY_KEY].encode('utf-8'))

    def cipher_rsa_dec(self):
        """
        私钥解密
        :return:
        """
        key = RSA.import_key(self.private_key)
        cipher = PKCS1_v1_5.new(key)
        return cipher.decrypt(self.ciphertext, None)
