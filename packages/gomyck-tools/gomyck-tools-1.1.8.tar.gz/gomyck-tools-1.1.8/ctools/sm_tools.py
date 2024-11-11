import base64

from gmssl import sm2, func
from gmssl.sm4 import CryptSM4, SM4_ENCRYPT, SM4_DECRYPT

sm2_crypt: sm2.CryptSM2


def sign_with_sm2(sign_data: str) -> str:
  return sm2_crypt.sign(sign_data.encode('UTF-8'), func.random_hex(sm2_crypt.para_len))


def verify_with_sm2(sign_val: str, sign_data: str) -> bool:
  return sm2_crypt.verify(sign_val, sign_data.encode('UTF-8'))


def encrypt_with_sm2(encrypt_data: str) -> str:
  return base64.b64encode(sm2_crypt.encrypt(encrypt_data.encode('UTF-8'))).decode('UTF-8')


def decrypt_with_sm2(encrypt_data: str) -> str:
  return sm2_crypt.decrypt(base64.b64decode(encrypt_data.encode('UTF-8'))).decode('UTF-8')


def encrypt_with_sm4(key: bytes, encrypt_text: str):
  crypt_sm4 = CryptSM4()
  crypt_sm4.set_key(key, SM4_ENCRYPT)
  encrypt_value = base64.b64encode(crypt_sm4.crypt_ecb(encrypt_text.encode()))
  return encrypt_value.decode()


def decrypt_with_sm4(key: bytes, decrypt_text: str):
  crypt_sm4 = CryptSM4()
  crypt_sm4.set_key(key, SM4_DECRYPT)
  decrypt_value = crypt_sm4.crypt_ecb(base64.b64decode(decrypt_text))
  return decrypt_value.decode()
