
import time
import os
import webbrowser
import cherrypy
import simplejson
import logging
from ws4py.messaging import TextMessage
from ws4py.server.cherrypyserver import WebSocketPlugin, WebSocketTool
from ws4py.websocket import WebSocket

from system import *
import ConfigParser

""" set up part 

    WEB_DIR : Part to all .html
    JS_DIR : Part to all .js 
    CSS_DIR : Part to all .css
"""
WEB_DIR = os.path.join(os.path.abspath("."), u"web_app")
JS_DIR = os.path.join(os.path.abspath("./web_app/public"), u"js")
CSS_DIR = os.path.join(os.path.abspath("./web_app/public"), u"css")
FONTS_DIR = os.path.join(os.path.abspath("./web_app/public"), u"fonts")
IMG_DIR = os.path.join(os.path.abspath("./web_app/public"), u"img")

"""  Global variable
"""
host = '127.0.0.1'
port = 8080
link_server = "http://127.0.0.1:8080"
""" web appication cherrypy """
 
class Webapp(object):
 
    def __init__(self):
        # *** reply to client ***
        self.name = 'lettuce'
        self.duration = 45
        self.high_temperature = 5.0
        self.low_temperature = 2.0
        self.high_moisture = 25.0
        self.low_moisture = 20.0
        self.high_ph = 7.0
        self.low_ph = 2.0
        self.ec_daily = None



# ***** < Waiting for reply to client > *****
    @cherrypy.expose
    def get_update_standard(self):
        cherrypy.response.headers['Content-Type'] = 'application/json'
        _json = {'General': [{'name':self.name }, {'start_date':'2016-9-18'}, {'duration':self.duration}],
                      'PH': [{'high': self.high_ph}, {'low':self.low_ph}],
                      'Temperature': [{'high':self.high_moisture}, {'low':self.low_moisture}],
                      'Moisture': [{'high': self.high_temperature}, {'low':self.low_temperature}],
                      'EU_Daily': [{'3.0':{'1':'5'}}, {'4.0':{'6':'20'}}, {'5.0':{'21':'45'}}]
                      }
        return simplejson.dumps(_json)

# ***** > Waiting for reply to client < *****

# ***** < Waiting for reply to Web Browser > *****
    @cherrypy.expose
    def set_update_standard(self,a,b,c,d,e,f,g,h,i):
        cherrypy.response.headers['Content-Type'] = 'application/json'
        self.name = a
        self.duration = b
        self.high_temperature = c
        self.low_temperature = d
        self.high_moisture = e
        self.low_moisture = f
        self.high_ph = g
        self.low_ph = h
        self.ec_daily = i
        _json = {'status':True}
        print ' >>>>>>>>>>>>>>>>>>>>>> set_update_standard'
        return simplejson.dumps(_json)

# ***** > Waiting for reply to Web Browser < *****


# **************** with out updete.py ************************

    """ index page (Login page)"""
    @cherrypy.expose
    def index(self):
      return open(os.path.join(WEB_DIR, u'index.html'))
    
    """ auto open browser """
    def open_page(self, ):
        webbrowser.open(link_server)
    
    """ websocket """
    @cherrypy.expose
    def ws(self):
        cherrypy.log("Handler created: %s" % repr(cherrypy.request.ws_handler))
    
        cherrypy.request.ws_handler.set_main_app(self)
        return
    
# ***************         ***          ***********************

# ************     Cless _WebSocket      ************

class _WebSocket(WebSocket):

    def set_main_app(self, mainapp):
        self._mainapp = mainapp
    
    def received_message(self, m):
        print 'Mess ==== : ====', m
        cherrypy.engine.publish('websocket-broadcast', m)
    
    def closed(self, code, reason="A client left the room without a proper explanation."):
        cherrypy.engine.publish('websocket-broadcast', TextMessage(reason))


"""Setup the Configuration (Part to css , js)"""
config = {'/js':
         {'tools.staticdir.on': True,
          'tools.staticdir.dir': JS_DIR,
          },
         '/css':
         {'tools.staticdir.on': True,
          'tools.staticdir.dir': CSS_DIR,
          },
          '/fonts':
         {'tools.staticdir.on': True,
          'tools.staticdir.dir': FONTS_DIR,
          },
          '/img':
         {'tools.staticdir.on': True,
          'tools.staticdir.dir': IMG_DIR,
          },
         '/ws':
         {'tools.websocket.on': True,
          'tools.websocket.handler_cls': _WebSocket,
          }
         }

if __name__ == '__main__':
    # cherrypy.log.error_log.propagate = False
    # cherrypy.log.access_log.propagate = False
    cherrypy.config.update({'server.socket_port': port,
                            'log.screen': True })
    WebSocketPlugin(cherrypy.engine).subscribe()
    cherrypy.tools.websocket = WebSocketTool()
    cherrypy.quickstart(Webapp(), '/', config=config)


else:
   cherrypy.engine.subscribe('start', Webapp().open_page)
   cherrypy.tools.websocket = WebSocketTool()
   cherrypy.tree.mount(Webapp, '/', config=config)
   cherrypy.engine.start()

# ***************************************************

# if __name__ == '__main__':
