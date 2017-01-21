
import http_server
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
import json
import networkx as nx
from networkx.readwrite import json_graph

import logging, sys
from Utils import GraphObjectEncoder

class SubjectGraph():
    def __init__(self, new_uri):
        self.uri = new_uri
        self.graph = nx.MultiDiGraph()
        self.graph.add_node(self.uri)
        #self.grph_objs = {}

        #self.prop_objects = {}
        #self.type_objects = {}

    def add_prop(self, new_prop):
        #if prop exist update counter.

        if new_prop not in self.graph:
            prop_node = PropertyNode(new_prop)
            #prop_node.support += 1
            self.graph.add_node(new_prop, obj=prop_node)
            # self.graph[new_prop]['object'] = prop_node
            self.graph.add_edge(self.uri, new_prop)
            #self.prop_objects[new_prop] = prop_node
            logging.info('new prop was added: ' + new_prop)

        self.graph.node[new_prop]['obj'].support += 1
        logging.info('prop was updated: ' + new_prop)

    def normalize_graph(self, totals):
        # divide every atribute of the support with the number at totals
        for tnode in self.graph.nodes(data=True):
            sup = self.graph[tnode]['obj'].support
            self.graph[tnode]['obj'].ratio = float(sup) / totals



    def update_prop(self, prop_key, args):
        pass

    def add_type_to_prop(self, prop_uri, new_type):
        # add new type if type found adds 1 to support
        if prop_uri not in self.graph:
            logging.info('prop not in graph: ' + prop_uri)
            return


        if new_type not in self.graph:
            type_node = TypeNode(new_type, prop_uri)
            new_type_p = new_type + '@' + prop_uri
            self.graph.add_node(new_type_p, obj=type_node)
            # self.graph[new_prop]['object'] = prop_node
            self.graph.add_edge(prop_uri, new_type_p)

        self.graph.node[new_type_p]['obj'].support += 1
        # if self.grph_objs[new_type].checked:
        #     self.grph_objs[new_type].is_unique = False
        #
        # self.grph_objs[new_type].checked = True

    def reset_uniques(self):
        pass

    def update_uniques(self):
        pass

    def add_relation(self, from_type, to_type, at_prop, relatio_uri):
        '''
        gets 2 types and the rilation between them and add it as an edge to the graph.
        :param from_type:
        :param to_type:
        :param relatio_uri: the uri for the relation to be added
        :return:
        '''

        if at_prop in self.graph:
            types = self.graph.neighbors(at_prop)
            fn = from_type + '@' + at_prop
            tn = to_type + '@' + at_prop
            if fn in types and tn in types:
                if self.graph.has_edge(fn,tn, relatio_uri):
                    self.graph[fn][tn]['support'] +=1
                else:
                    self.graph.add_edge(fn, tn, key=relatio_uri, attr_dict={ 'support': 1 })


                logging.info('relation added at: ' + fn + ';' + tn + ';' + relatio_uri)



    def update_relation(self):
        pass


class GraphObject():
    def __init__(self, new_uri):
        self.uri = new_uri
        self.title = self.uri.rsplit('/', 1)[-1]
        self.support = 0
        self.ratio = -1

    def __str__(self):
        return self.title


class PropertyNode(GraphObject):

    def __init__(self, new_uri):
        GraphObject.__init__(self, new_uri)

    def __hash__(self):
        return hash(self.uri)




class TypeNode(GraphObject):


    def __init__(self, new_uri, parent_prop):
        GraphObject.__init__(self, new_uri)
        self.is_unique = True
        self.checked = False
        self.uniques = 0
        self.prop_uri = parent_prop

    def __hash__(self):
        return hash(self.uri + '@' +self.prop_uri)



    def uniqueness(self):
        return  1 if self.is_unique else 0



class Relation(GraphObject):
    def __init__(self, new_uri):
        GraphObject.__init__(self, new_uri)

    def __hash__(self):
        return hash(self.uri)








if __name__ == '__main__':
    '''
    TODO:
    1. make proper graph object.
    2. proper inheritence
    3. dict functions - test before going crazy with it.
    4. make sure type is hashed with the right  property
    5. maintain the weight and suport functions
    6. run the shit to find main properties of politician and soccer player
    7. put it on the web
    8. update inconsistencies
    9. print incs.

    '''



    logging.basicConfig(stream=sys.stderr, level=logging.DEBUG)

    ng = SubjectGraph("Politician")
    ng.add_prop("dateOfBirth")
    ng.add_prop("placeOfDeath")
    ng.add_prop("placeOfDeath")
    ng.add_type_to_prop("placeOfDeath", "City")
    ng.add_type_to_prop("placeOfDeath", "Country")
    #ng.add_type_to_prop("http://dbpedia.org/property/dateOfBirth", "april,13 1989")
    ng.add_relation("City", "Country","placeOfDeath" ,"located_in")
    G = ng.graph
    p1 = G.nodes()
    # this d3 example uses the name attribute for the mouse-hover value,
    # so add a name to each node

    i=7
    for n in G:
        i*=2
        G.node[n]['name'] = str(n)
        G.node[n]['value'] = i
        G.node[n]['group'] = i/2

    # write json formatted data
    d = json_graph.node_link_data(G)  # node-link format to serialize
    # write json
    json.dump(d, open('force/force.json', 'w'), cls=GraphObjectEncoder)
    print('Wrote node-link JSON data to force/force.json')
    # open URL in running web browser
    http_server.load_url('force/force.html')
    print('Or copy all files in force/ to webserver and load force/force.html')