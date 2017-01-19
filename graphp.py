
import pickle
import sys
import os
import time
import matplotlib.pyplot as plt
import networkx as nx
import sys

import SimpleHTTPServer, BaseHTTPServer
import socket
import thread
import webbrowser



def load_url(path):
    PORT = 8000
    httpd = StoppableHTTPServer(("127.0.0.1",PORT), handler)
    thread.start_new_thread(httpd.serve, ())
    webbrowser.open_new('http://localhost:%s/%s'%(PORT,path))
    input("Press <RETURN> to stop server\n")
    httpd.stop()
    print("To restart server run: \n%s"%server)




handler = SimpleHTTPServer.SimpleHTTPRequestHandler
input = raw_input
server = "python -m SimpleHTTPServer 8000"



class StoppableHTTPServer(BaseHTTPServer.HTTPServer):

    def server_bind(self):
        BaseHTTPServer.HTTPServer.server_bind(self)
        self.socket.settimeout(1)
        self.run = True

    def get_request(self):
        while self.run:
            try:
                sock, addr = self.socket.accept()
                sock.settimeout(None)
                return (sock, addr)
            except socket.timeout:
                pass

    def stop(self):
        self.run = False

    def serve(self):
        while self.run:
            self.handle_request()



class subject():
    def __int__(self, new_uri):
        props = {}
        uri = new_uri

    def add_prop(self, new_prop):
        pass

    def update_prop(self, prop_key, args):
        pass




class property():
    def __init__(self, new_uri):
        uri = new_uri











import json
    #import networkx as nx
from networkx.readwrite import json_graph
#import http_server



if __name__ == '__main__':
    # G = nx.Graph()
    # G.add_edges_from([(1, 2), (1, 3)])
    # #nx.draw(G)
    # #nx.draw_random(G)
    # #nx.draw_circular(G)
    # nx.draw_spectral(G)
    # plt.show()

    """Example of writing JSON format graph data and using the D3 Javascript library to produce an HTML/Javascript drawing.
    """
# Author: Aric Hagberg <aric.hagberg@gmail.com>

#    Copyright (C) 2011-2016 by
#    Aric Hagberg <hagberg@lanl.gov>
#    Dan Schult <dschult@colgate.edu>
#    Pieter Swart <swart@lanl.gov>
#    All rights reserved.
#    BSD license.
    G = nx.barbell_graph(9,7)
    # this d3 example uses the name attribute for the mouse-hover value,
    # so add a name to each node
    for n in G:
        G.node[n]['name'] = n
    # write json formatted data
    d = json_graph.node_link_data(G) # node-link format to serialize
    # write json
    json.dump(d, open('force/force.json','w'))
    print('Wrote node-link JSON data to force/force.json')
    # open URL in running web browser
    load_url('force/force.html')
    print('Or copy all files in force/ to webserver and load force/force.html')