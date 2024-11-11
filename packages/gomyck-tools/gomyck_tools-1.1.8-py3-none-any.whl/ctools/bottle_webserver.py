from socketserver import ThreadingMixIn
from wsgiref.simple_server import WSGIServer, WSGIRequestHandler, make_server

from bottle import ServerAdapter, Bottle, template, static_file

"""
app = bottle_web_base.init_app('子模块写 context_path, 主模块就不用写任何东西')

@app.get('/queryList')
@bottle_web_base.rule('DOC:DOWNLOAD')
def query_list(params):
"""

"""
module_names = list(globals().keys())
def get_modules():
  mods = []
  for modname in module_names:
    if modname == 'base' or modname == 'online' or modname.startswith('__') or modname == 'importlib': continue
    module = globals()[modname]
    mods.append(module)
  return mods

def get_ws_modules():
  from . import websocket
  return [websocket]
"""

"""
http_app = bottle_webserver.init_bottle()
http_app.mount(app.context_path, app)
http_app.set_index(r'轨迹点位压缩.html')
http_app.run()
"""

class CBottle:

  def __init__(self, bottle: Bottle, port=8888, quiet=False):
    self.port = port
    self.quiet = quiet
    self.bottle = bottle

  def run(self):
    http_server = WSGIRefServer(port=self.port)
    self.bottle.run(server=http_server, quiet=self.quiet)

  def set_index(self, path, **kwargs):
    @self.bottle.route(['/', '/index'])
    def index():
      return template(path, kwargs)

  def set_static(self, root):
    @self.bottle.route('/static/<filepath:path>')
    def static(filepath):
      return static_file(filepath, root=root)

  def set_download(self, root, download_prefix=True):
    @self.bottle.route('/download/<filename>')
    def download(filename):
      return static_file(filename, root=root, download=download_prefix)

  def mount(self, context_path, app, **kwargs):
    self.bottle.mount(context_path, app, **kwargs)

def init_bottle(app:Bottle=None, port=8888, quiet=False) -> CBottle:
  bottle = app or Bottle()
  return CBottle(bottle, port, quiet)

class ThreadedWSGIServer(ThreadingMixIn, WSGIServer):
  daemon_threads = True

class CustomWSGIHandler(WSGIRequestHandler):
  def log_request(*args, **kw): pass

class WSGIRefServer(ServerAdapter):

  def __init__(self, host='0.0.0.0', port=8010):
    super().__init__(host, port)
    self.server = None

  def run(self, handler):
    req_handler = WSGIRequestHandler
    if self.quiet: req_handler = CustomWSGIHandler
    self.server = make_server(self.host, self.port, handler, server_class=ThreadedWSGIServer, handler_class=req_handler)
    self.server.serve_forever()

  def stop(self):
    self.server.shutdown()
