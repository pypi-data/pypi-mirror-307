from bottle import ServerAdapter, Bottle
from geventwebsocket.handler import WebSocketHandler

from ctools import sys_log

"""
app = init_app('/websocket_demo')

@app.route('/script_debug', apply=[websocket])
@rule('DOC:DOWNLOAD')
def script_debug(ws: WebSocket):
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
socket_app = bottle_websocket.init_bottle()
socket_app.mount(app.context_path, app)
socket_app.run()
"""

class CBottle:

  def __init__(self, bottle: Bottle, port=8888, quiet=False):
    self.port = port
    self.quiet = quiet
    self.bottle = bottle

  def run(self):
    socket_server = WebSocketServer(port=self.port)
    self.bottle.run(server=socket_server, quiet=self.quiet)

  def mount(self, context_path, app):
    self.bottle.mount(context_path, app)

def init_bottle(port=8889, quiet=False) -> CBottle:
  bottle = Bottle()
  return CBottle(bottle, port, quiet)

class CustomWebSocketHandler(WebSocketHandler):
  def log_request(self):
    if '101' not in str(self.status):
      log_msg = self.format_request()
      for nk in sys_log.neglect_keywords:
        if nk in log_msg:
          return
      self.logger.info(log_msg)

class WebSocketServer(ServerAdapter):

  def __init__(self, host='0.0.0.0', port=8011):
    super().__init__(host, port)
    self.server = None

  def run(self, handler):
    from gevent import pywsgi
    self.server = pywsgi.WSGIServer((self.host, self.port), handler, handler_class=CustomWebSocketHandler)
    self.server.serve_forever()

  def stop(self):
    self.server.stop()
