import hashlib
import random
import uuid
from typing import Union

import chardet

from ctools.id_worker_tools import IdWorker

idWorker = IdWorker(1, 2, 0)

def get_random_str(size: int = 10):
  """
  根据长度获取随机字符串
  :param size:
  :return:
  """
  return "".join(random.sample('abcdefghijklmnopqrstuvwxyz0123456789', size))


def get_uuid():
  return str(uuid.uuid1()).replace("-", "")


def get_snowflake_id():
  return idWorker.get_id()


def decode_bytes(bytes_str: Union[bytes, bytearray]):
  res_str = ""
  if bytes_str:
    detect = chardet.detect(bytes_str)
    if detect:
      confidence = 0
      chardet_error = False
      try:
        confidence = float(detect.get('confidence'))
        res_str = bytes_str.decode(encoding=detect.get('encoding'))
      except Exception:
        chardet_error = True

      try:
        if confidence <= 0.95 or chardet_error:
          encoding = "utf-8" if detect.get('encoding') == "utf-8" else "gbk"
          res_str = bytes_str.decode(encoding=encoding)
      except Exception:
        res_str = str(bytes_str)
  return res_str


def check_sum(content: str):
  try:
    algorithm = hashlib.sha256()
    algorithm.update(content.encode())
    return algorithm.hexdigest()
  except Exception:
    return None


def is_list(v: str):
  try:
    list(v)
    if v[0] == "[" and v[-1] == "]":
      return True
    else:
      return False
  except Exception:
    return False

def is_digit(v: str):
  try:
    float(v)
    return True
  except Exception:
    return False

def is_bool(v: str):
  if v in ["False", "True"]:
    return True
  else:
    return False

def is_obj(k: str):
  if k in ['operate', 'pm_browser_sm_options', 'pw_context_sm_service']:
    return True
  else:
    return False

def dict_to_params(obj: dict):
  params = ""
  for k, v in obj.items():
    if k == 'varname':
      continue
    v = str(v)
    if not is_list(v) and not is_digit(v) and not is_bool(v) and not is_obj(k):
      if k == "path" and v[:4] != "http":
        v = "r'%s'" % v
      else:
        v = "'%s'" % v
    params += "%s=%s, " % (k, v)
  params = params[:params.rfind(',')]
  return params
