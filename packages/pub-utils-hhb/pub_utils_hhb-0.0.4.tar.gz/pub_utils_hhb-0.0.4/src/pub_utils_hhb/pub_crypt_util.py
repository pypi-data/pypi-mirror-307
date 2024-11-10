import uuid
import base64

from Crypto.Cipher import AES

__all__ = [
    'CryptUtil',
]


class CryptUtil:
    BLOCK_SIZE = 16

    def __init__(self, key: str = ''):
        self._key_str = key if key else self._gen_random_key_str()
        self._key_enc = self._key_str.encode('utf-8')
        self._aes = AES.new(self._key_enc, AES.MODE_ECB)

    def get_key(self) -> str:
        return self._key_str

    def set_key(self, key: str) -> None:
        if not key:
            raise Exception('arguments "key" must be a non-empty str')

        self._key_str = key
        self._key_enc = key.encode('utf-8')

    def encrypt(self, data) -> str:
        res = self._aes.encrypt(self._pad(data).encode('utf-8'))
        return str(base64.b64encode(res), encoding='utf8')

    def decrypt(self, data) -> str:
        res = base64.decodebytes(data.encode('utf-8'))
        decrypt_data = self._aes.decrypt(res).decode('utf-8')
        return self._unpad(decrypt_data)

    def _pad(self, text) -> str:
        text_size = len(text.encode('utf-8'))
        add = CryptUtil.BLOCK_SIZE - (text_size % CryptUtil.BLOCK_SIZE)
        return text + (chr(add) * add)

    def _unpad(self, text) -> str:
        return text[0:-ord(text[-1])]

    def _gen_random_key_str(self) -> str:
        return str(uuid.uuid4().hex)[:16]

# --------------------------------------------------
#                   Usage Example
# --------------------------------------------------
# crypt_key = ''
# crypt_instance = CryptUtil(crypt_key)
#
# origin_text = 'origin text'
# encrypt_data = crypt_instance.encrypt(origin_text)
# decrypt_data = crypt_instance.decrypt(encrypt_data)
#
# assert origin_text == decrypt_data
# --------------------------------------------------
