import time


def get_date():
  """
  获取 %Y-%m-%d格式时间
  :return:
  """
  return time.strftime('%Y-%m-%d', time.localtime(time.time()))


def get_time():
  """
  获取 %H-%M-%S格式时间
  :return:
  """
  return time.strftime('%H-%M-%S', time.localtime(time.time()))


def get_date_time(offset=0):
  """
  获取 %Y-%m-%d %H:%M:%S格式时间
  :return:
  """
  return time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time() + offset))


def get_file_time():
  """
  获取 %Y-%m-%d %H:%M:%S 文件格式时间
  :return:
  """
  return time.strftime('%Y-%m-%d_%H-%M-%S', time.localtime(time.time()))

def get_timestamp(offset=0):
  return int(time.time() + offset)

def str_to_timestamp(val: str):
  return time.mktime(time.strptime(val, "%Y-%m-%d %H:%M:%S"))

def str_to_datetime(val: str):
  return time.strptime(val, "%Y-%m-%d %H:%M:%S")


