import networkx as nx


gdm = nx.MultiDiGraph()
gdm.add_node(1)
gdm.add_node(2)
gdm.add_edge(1,2, attr_dict={'name':'a', 'support': 0 })
gdm.add_edge(1,2,key="uri_uniqu" ,attr_dict={ 'support': 0 })
b = gdm.has_edge(1,2, key="uri_uniqus")
bk= gdm.has_edge(1,2, key="uri_uniqu")
gdm.add_edge(1,2,key="uri_uniqu" , attr_dict={ 'support': 1})
gdm.add_edge(1,2,key="uri_uniqu" )
gdm[1][2]["uri_uniqu"]['support']+=1

#gdm.add_edge(1,2, attr_dict={'name':'b', 'support': 0 })
#gdm.add_edge(1,2, attr_dict={'name':'c', 'support': 0 })
gdm.add_edge(1,2, attr_dict={'name':'d', 'support': 0 })



