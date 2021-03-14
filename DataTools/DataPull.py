import socket
import requests
import pandas as pd
import os

def CloudPull():
    port = os.getenv('WEB_PORT')
    hostname = os.getenv('ROUTER_SERVICE')
    url = None
    func = "pull-events"
    if port == None:
        url = 'http://localhost:9999/'
    else:
        ip = socket.gethostbyname(hostname)
        url = 'http://'+ ip + ':' + port + '/'
    resp = requests.get(url + func)
    items = resp.json() 
    event_frame = pd.DataFrame.from_dict(items)
    return event_frame