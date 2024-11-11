import inspect
import threading
from functools import wraps

import bottle
from bottle import response, Bottle, request
from ctools.dict_wrapper import DictWrapper
from ctools.api_result import R
from ctools.sys_log import flog as log

bottle.BaseRequest.MEMFILE_MAX = 1024 * 1024 * 50
func_has_params = {}

class GlobalState:
  lock = threading.Lock()
  withOutLoginURI = [
    '/login',
    '/get_sys_version'
  ]
  allowRemoteCallURI = [

  ]
  token = {}

def init_app(context_path=None):
  app = Bottle()
  app.context_path = context_path

  @app.hook('before_request')
  def before_request():
    # abort(401, '系统时间被篡改, 请重新校时!')
    pass

  @app.error(401)
  def unauthorized(error):
    after_request()
    response.status = 200
    log.error("系统未授权: {} {} {}".format(error.body, request.method, request.fullpath))
    return R.error(resp=R.Code.cus_code(9999, "系统未授权! {}".format(error.body)))

  @app.error(403)
  def unauthorized(error):
    after_request()
    response.status = 200
    log.error("访问受限: {} {} {}".format(error.body, request.method, request.fullpath))
    return R.error(resp=R.Code.cus_code(8888, "访问受限: {}".format(error.body)))

  @app.error(405)
  def cors_error(error):
    if request.method == 'OPTIONS':
      after_request()
      response.status = 200
      return
    log.error("请求方法错误: {} {} {}".format(error.status_line, request.method, request.fullpath))
    return R.error(msg='请求方法错误: {}'.format(error.status_line))

  @app.error(500)
  def cors_error(error):
    after_request()
    response.status = 200
    log.error("系统发生错误: {} {} {}".format(error.body, request.method, request.fullpath))
    return R.error(msg='系统发生错误: {}'.format(error.exception))

  @app.hook('after_request')
  def after_request():
    enable_cors()

  app.install(params_resolve)
  return app

def enable_cors():
  response.headers['Access-Control-Allow-Origin'] = '*'
  response.headers['Access-Control-Allow-Methods'] = 'GET, POST, PUT, DELETE, OPTIONS'
  request_headers = request.headers.get('Access-Control-Request-Headers')
  response.headers['Access-Control-Allow-Headers'] = request_headers if request_headers else ''
  response.headers['Access-Control-Expose-Headers'] = '*'

# annotation
def rule(key):
  def return_func(func):
    @wraps(func)
    def decorated(*args, **kwargs):
      # if GlobalState.licenseInfo is not None and key not in GlobalState.licenseInfo.access_module:
      #   log.error("系统未授权! {} {}".format(request.fullpath, '当前请求的模块未授权!请联系管理员!'))
      #   return R.error(resp=R.Code.cus_code(9999, "系统未授权! {}".format('当前请求的模块未授权!请联系管理员!')))
      return func(*args, **kwargs)
    return decorated
  return return_func

# annotation or plugins, has auto install, don't need to call
def params_resolve(func):
  @wraps(func)
  def decorated(*args, **kwargs):
    if func_has_params.get(request.fullpath) is not None and not func_has_params.get(request.fullpath):
      return func(*args, **kwargs)
    if func_has_params.get(request.fullpath) is None:
      sig = inspect.signature(func)
      params = sig.parameters
      if not params.get('params'):
        func_has_params[request.fullpath] = False
        return func(*args, **kwargs)
      else:
        func_has_params[request.fullpath] = True
    if request.method == 'GET':
      queryStr = request.query.decode('utf-8')
      page_info = PageInfo(
        page_size=10 if request.headers.get('page_size') is None else int(request.headers.get('page_size')),
        page_index=1 if request.headers.get('page_index') is None else int(request.headers.get('page_index'))
      )
      queryStr.page_info = page_info
      return func(params=queryStr, *args, **kwargs)
    elif request.method == 'POST':
      content_type = request.get_header('content-type')
      if content_type == 'application/json':
        params = request.json
        return func(params=DictWrapper(params), *args, **kwargs)
      elif content_type and 'multipart/form-data' in content_type:
        form_data = request.forms.decode()
        form_files = request.files.decode()
        params = FormDataParams(data=DictWrapper(form_data), files=form_files)
        return func(params=params, *args, **kwargs)
      else:
        params = request.query.decode('utf-8')
        return func(params=params, *args, **kwargs)
    else:
      return func(*args, **kwargs)
  return decorated

class PageInfo:
  def __init__(self, page_size, page_index):
    self.page_size = page_size
    self.page_index = page_index

class FormDataParams:
  def __init__(self, data, files):
    self.data = data
    self.files = files

  def __getattr__(self, key):
    try:
      return self.data[key]
    except Exception:
      return self.files[key]


