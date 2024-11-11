import base64

from Crypto.Cipher import PKCS1_OAEP
from Crypto.PublicKey import RSA

from ctools import work_path, cjson

ENCRYPT_CHUNK_SIZE = 245
decrypt_CHUNK_SIZE = 512


# 加密函数
def encrypt(msg, public_key):
  parts = b''
  private_key = RSA.import_key(public_key)
  cipher = PKCS1_OAEP.new(private_key)
  for i in range(0, len(msg), ENCRYPT_CHUNK_SIZE):
    parts += cipher.encrypt(msg[i:i + ENCRYPT_CHUNK_SIZE].encode())
  encrypted_base64 = base64.b64encode(parts)
  return encrypted_base64.decode()


# 解密函数
def decrypt(msg, private_key):
  parts = b''
  public_key = RSA.import_key(private_key)
  cipher = PKCS1_OAEP.new(public_key)
  encrypted_bytes = base64.b64decode(msg)
  for i in range(0, len(encrypted_bytes), decrypt_CHUNK_SIZE):
    parts += cipher.decrypt(encrypted_bytes[i:i + decrypt_CHUNK_SIZE])
  return parts.decode()


def loadLicenseInfo(auth_code):
  with open(work_path.get_app_path() + '/keys/license.key', 'r') as pri:
    decrypt_message = decrypt(auth_code.strip(), pri.read())
    return cjson.loads(decrypt_message)
