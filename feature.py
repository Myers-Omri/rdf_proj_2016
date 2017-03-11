from SPARQLWrapper import SPARQLWrapper, JSON

import pickle
import sys
import os
import time
import graphp
from threading import Thread
from Utils import *

DBPEDIA_URL = "http://tdk3.csf.technion.ac.il:8890/sparql"
SMAL_URL = "http://cultura.linkeddata.es/sparql"
DEBUG = False
PROFILER = True




class DbpKiller():

    def __init__(self, kb, subj, s_uri):
        self.knowledge_base = kb
        self.subject = subj
        self.subject_uri = s_uri
        self.sparql = SPARQLWrapper(kb)
        self.RG = graphp.SubjectGraph(s_uri)
        self.timers = {'get_os': 0, 'update_so_dict': 0}

    def __get_top_15_props(self, ps, n=5):
        p_dict_ret = {}
        for i, p in enumerate(ps):
            cur = ps[p]
            p_dict_ret[p] = int(cur)
            if i > n:
                m = min(p_dict_ret, key=p_dict_ret.get)
                p_dict_ret.pop(m, None)
        return p_dict_ret


    def get_s_dict_from_dump(self, quick, dump_name):

        s_dict_file = open(dump_name, 'r')
        s_dict = pickle.load(s_dict_file)

        s_dict_file.close()
        if quick:
            return self.__get_top_15_props(s_dict, n=50)
        else:
            return self.__get_top_15_props(s_dict, n=3000)


    def get_po_dict(self, s):

        if PROFILER:
            t0 = time.time()
        po_dict = {}
        query_text = ("""
                    SELECT DISTINCT ?p ?o
                    WHERE{
                            <%s> ?p ?o .
                            ?o a ?t.
                            FILTER (regex(?p, "^http://dbpedia.org/property/", "i") || regex(?p, "^http://dbpedia.org/ontology/", "i"))
                        } """ % (s))

        self.sparql.setQuery(query_text)
        self.sparql.setReturnFormat(JSON)
        results_inner = self.sparql.query().convert()
        for inner_res in results_inner["results"]["bindings"]:
            # s = inner_res["s"]["value"]
            o = inner_res["o"]["value"]
            p = inner_res["p"]["value"]
            if p not in po_dict:
                po_dict[p]=[]
            po_dict[p].append(o)

        if PROFILER:
            t1 = time.time()
            total_time = t1 - t0
            self.timers['update_so_dict'] += total_time
        return po_dict


    def get_sim(self, p1,p2):
        if len(p1) > len(p2):
            self.get_sim(p2,p1)

        tot_sim = 0
        for o in p1:
            if o in p2:
                tot_sim+=1

        return float(tot_sim)/len(p1)


    def kill_dbp(self, quick, sim_th=0.7):
        print "mining rules for {}".format(self.subject)
        s_dump_name = self.subject + "/" + self.subject + "_top.dump"
        #p_dump_name = self.subject + "/" + self.subject + "_prop_p.dump"
        #o_dump_name = self.subject + "/" + self.subject + "_prop.dump"
        # get the 100 most popular properties for type person in dbp
        #p_dict = self.get_p_dict_from_dump(quick, p_dump_name)
        s_dict = self.get_s_dict_from_dump(quick, s_dump_name)
        #o_dict = self.get_p_dict_from_dump(quick, o_dump_name)

        #p_dump_name = self.subject + "/" + self.subject + "_prop.dump"
        # get the 100 most popular properties for type person in dbp

        sim_tup_dict = {}
        for s in s_dict:
            p_o_dict = self.get_po_dict(s)
            l1 = p_o_dict.items()
            l2 = p_o_dict.items()
            for i in range(0, len(l1) -1):
                for j in range(i+1, len(l2) -1):
                    p1 = l1[i]
                    p2 = l2[j]
                    sim = self.get_sim(p1[1],p2[1])
                    if sim > sim_th:
                        if p1[0] < p2[0]:
                            if (p1[0] , p2[0] ) not in sim_tup_dict:
                                sim_tup_dict[(p1[0], p2[0])]=0
                            sim_tup_dict[(p1[0] , p2[0] )] += sim
                        else:
                            if (p2[0], p1[0]) not in sim_tup_dict:
                                sim_tup_dict[(p2[0], p1[0])] = 0
                            sim_tup_dict[(p2[0], p1[0])] += sim

        for ps, tot_sim in sim_tup_dict.items():
            if float(tot_sim)/len(s_dict) < 0.2:
                sim_tup_dict.pop(ps, None)

        dir_name = self.subject
        if not os.path.exists(dir_name):
            os.makedirs(dir_name)
        dump_name = dir_name + "/" + self.subject + "_f_rules.dump"
        r_dict_file = open(dump_name, 'w')
        pickle.dump(sim_tup_dict, r_dict_file)
        r_dict_file.close()

        return sim_tup_dict



def find_p_incs(dict_list):
    for d in dict_list:
        for s, suri in d.items():
            dk = DbpKiller(DBPEDIA_URL, s, suri)
            dk.kill_dbp(quick=True)


if __name__ == '__main__':

    find_p_incs([{'comedian': "http://dbpedia.org/ontology/Comedian"}])


