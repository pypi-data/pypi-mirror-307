# -*- coding: utf-8 -*-
"""
@ Created on 2024-09-04 15:44
---------
@summary: 
---------
@author: XiaoBai
"""
import base64
from typing import Union

from Crypto.Cipher import AES
from Crypto.Cipher import PKCS1_v1_5
from Crypto.PublicKey import RSA
from Crypto.Util.Padding import pad, unpad


def aes_encrypt_ecb(key: bytes, plaintext: str, is_hex: bool = False) -> Union[bytes, str]:
    """

    :param key: aes密钥
    :param plaintext: 待加密明文
    :param is_hex: 输出结果是否转为十六进制
    :return:
    """
    if isinstance(key, str):
        key = key.encode()
    cipher = AES.new(key=key, mode=AES.MODE_ECB)
    padded_plaintext = pad(plaintext.encode('utf-8'), AES.block_size)
    ciphertext = cipher.encrypt(padded_plaintext)
    if is_hex:
        return bytes.hex(ciphertext)
    else:
        return base64.b64encode(ciphertext)


def aes_decrypt_ecb(key, ciphertext, is_hex: bool = False):
    if isinstance(key, str):
        key = key.encode()

    cipher = AES.new(key=key, mode=AES.MODE_ECB)
    if is_hex is True:
        encrypted_data = bytes.fromhex(ciphertext)
    else:
        encrypted_data = base64.b64decode(ciphertext)

    decrypted_data = cipher.decrypt(encrypted_data)
    de_plaintext = unpad(decrypted_data, AES.block_size)

    return de_plaintext.decode('utf-8')


def rsa_encrypt(key: str, data: str):
    public_key = RSA.import_key(base64.b64decode(key))
    rsa = PKCS1_v1_5.new(public_key)
    encrypt_msg = rsa.encrypt(data.encode('utf-8'))
    return base64.b64encode(encrypt_msg).decode()
