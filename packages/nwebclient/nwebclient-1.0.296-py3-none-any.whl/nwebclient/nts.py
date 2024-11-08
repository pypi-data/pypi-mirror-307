"""

  Demo: nwebclient.runner:BaseJobExecutor.page_var

"""
import urllib.parse as p

from nwebclient import util
from nwebclient import nweb
from nwebclient import web as w


def nx_get_ws_url():
    return nweb.nweb_cfg.get('NTS_URL', 'ws://localhost:3000/')


def nx_channel_emit(guid, message):
    try:
        key = nweb.nweb_cfg.get('V4_INNER_SECRET', '')
        url = nx_get_ws_url()
        util.wget(url + 'ws-nx-emit?key=' + key + '&guid=' + guid + '&message='+p.quote(message), verify=True)
    except Exception as e:
        print("[nwebclient.nts] Error: nx_channel_emit, " + str(e))


def nx_channel_html_part(guid, on_message='', console=True):
    res = w.script('/static/js/socket.io.js')
    if console:
        on_message += 'const $console = document.querySelector("#console");'
        on_message += '$console.append(msg,document.createElement("br"));'
    res += w.js_ready("""
            const socket = io(""""+nx_get_ws_url()+"""", {
                transports:["websocket"], 
                query: "nx_guid=""" + guid + """"});
            socket.on("msg", function(msg) { 
                console.log(msg); 
                """ + on_message + """
            }); 
        """)
    if console:
        res += w.div('', id='console')
    return res
