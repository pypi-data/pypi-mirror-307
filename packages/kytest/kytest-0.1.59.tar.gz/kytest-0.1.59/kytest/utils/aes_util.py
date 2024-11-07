"""
pip install pycryptodome==3.14.1
@Author: kang.yang
@Date: 2024/3/18 14:46
"""
import base64
from Crypto.Cipher import AES


def encode(key, src_str):
    """
    AES加密，一种对称加密算法
    @param key: 事先定好的秘钥
    @param src_str: 需要加密的字符串
    @return:
    """
    aes = AES.new(str.encode(key), AES.MODE_ECB)
    encode_pwd = str.encode(src_str.rjust(16, '@'))
    encrypt_str = str(base64.encodebytes(aes.encrypt(encode_pwd)), encoding='utf-8')
    return encrypt_str


def decode(key, ciphertext):
    """
    AES解密，一种对称加密算法
    @param key: 事先定好的秘钥
    @param ciphertext: 需要解密的密文
    @return:
    """
    aes = AES.new(str.encode(key), AES.MODE_ECB)
    decrypt_str = (aes.decrypt(base64.decodebytes(ciphertext.encode(encoding='utf-8'))).
                   decode().replace('@', ''))
    return decrypt_str


