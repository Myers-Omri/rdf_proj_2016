import pickle
from SPARQLWrapper import SPARQLWrapper, JSON
import sys
import os
from miner import miner
from graphp import evaluate_selection
from Utils import *
DBPEDIA_URL = "http://dbpedia.org/sparql"

try_rules = [{'p': "http://dbpedia.org/ontology/residence" ,'t':	"http://dbpedia.org/resource/City"},
             {'p': "http://dbpedia.org/ontology/birthPlace", 't':"http://dbpedia.org/resource/City"}]



def check_rel(t, s_uri, p, G):
    or_dict={}
    sparql = SPARQLWrapper(DBPEDIA_URL)
    query_text = ("""
        SELECT distinct  ?r12 ?r21
        WHERE {
                <%s> <%s> ?o1.
                <%s> <%s> ?o2.


               FILTER (?o1 < ?o2).
                        ?o1 a <%s>.
                        ?o2 a <%s>.

                        OPTIONAL {
                        ?o1 ?r12 ?o2.
                        ?o2 ?r21 ?o1.
                        }

                        FILTER regex(?r12, "^http://dbpedia.org/ontology", "i").
                        FILTER regex(?r21, "^http://dbpedia.org/ontology", "i").


        }""" % ( s_uri, p, s_uri, p,t,t))
    sparql.setQuery(query_text)
    sparql.setReturnFormat(JSON)
    results_inner = sparql.query().convert()
    for inner_res in results_inner["results"]["bindings"]:
        o = inner_res["o"]["value"]
        r12 = inner_res["r12"]["value"]
        r21 = inner_res["r21"]["value"]
        if G.has_edge(t,t,r12) or G.has_edge(t,t,r21):
            return True

    return False





def fix_dbpedia(db, rules, s_uri, subj, load=True):
    rf_name = subj + "/" + subj + "_rules.dump"
    rg_name = subj + "/" + subj + "_pg.dump"
    if not os.path.exists(rf_name) or not os.path.exists(rg_name):
        return

    ons = {}
    sparql = SPARQLWrapper(db)
    if load:
        rules_file = open(rf_name, 'r')
        all_rules = pickle.load(rules_file)
        (rules, r_67, r_56, wrd, ons, lows) = all_rules
        rules_file.close()

        g_file = open(rg_name, 'r')
        G = pickle.load(g_file)
        g_file.close()

    print "find inconsistencies, number of rules: {} ".format(str(len(rules)))
    i = 0
    inco_dict = {}
    inco_ons ={}
    for d, rn in [(rules, '85' ), (r_67, '67')]:
        for key, r in d.items():
            i+=1
            p = r['p']
            t = r['t']
            # count entities that ruin uniqueness
            # for every property and type we mined before count and find the
            # violations.
            query_text = ("""
                SELECT ?s ?cnt
                WHERE {
                {
                    SELECT ?s (COUNT(*) AS ?cnt)
                    WHERE{
                        ?o a <%s>.
                        ?s a <%s>;
                         <%s> ?o .

                    }GROUP BY ?s
                    ORDER BY DESC(?cnt)
                }
                FILTER ((?cnt > 1) && (?cnt < 3))
                }""" % (t, s_uri, p))
            sparql.setQuery(query_text)
            sparql.setReturnFormat(JSON)
            results_inner = sparql.query().convert()
            for inner_res in results_inner["results"]["bindings"]:
                s = inner_res["s"]["value"]

                recheck = check_rel(t, s_uri, p, G)

                if not recheck:
                    if s not in inco_dict:
                        inco_dict[s] = []
                    inco_dict[s].append((p, t, rn))

    for p in ons:
        query_text = ("""
            SELECT ?s ?cnt
            WHERE {
            {
                SELECT ?s (COUNT(*) AS ?cnt)
                WHERE{

                    ?s a <%s>;
                     <%s> ?o .

                }GROUP BY ?s
                ORDER BY DESC(?cnt)
            }
            FILTER (?cnt > 1)
            }""" % (s_uri, p))
        sparql.setQuery(query_text)
        sparql.setReturnFormat(JSON)
        results_inner = sparql.query().convert()
        for inner_res in results_inner["results"]["bindings"]:
            so = inner_res["s"]["value"]

            if so not in inco_ons:
                inco_ons[so] = []
            inco_ons[so].append((p, "***ons***","***ons***"))

    if not os.path.exists(subj):
        os.makedirs(subj)

    dump_name = subj + "_incs.dump"
    inc_file = open(subj + "/" + dump_name, 'w')
    incos = (inco_dict, inco_ons)
    pickle.dump(incos, inc_file)
    inc_file.close()
    return incos

def get_subjects(uri, i):
    sparql = SPARQLWrapper(DBPEDIA_URL)
    top_s_dict = {}
    limit = 9999
    offset = i * limit
    slimit = str(limit)
    soffset = str(offset)
    query_text = ("""
                    SELECT DISTINCT ?s
                       WHERE
                       {
                           ?s a <%s>.
                       } LIMIT %s
                       OFFSET %s

                   """ % (uri, slimit, soffset))

    sparql.setQuery(query_text)
    sparql.setReturnFormat(JSON)
    results_inner = sparql.query().convert()
    all_dict = results_inner["results"]["bindings"]
    for inner_res in all_dict:
        s = inner_res["s"]["value"]
        top_s_dict[s] = {}
    if len(all_dict) > 10:
        return top_s_dict ,True
    return top_s_dict, False



def fix_graphic(db, r_graph, s_uri, subj, fast=True, load = False):

    if load:
        r_graph = rules_dict_from_dump(subj + '/' + subj + '_pg.dump')

    mm = miner(db,subj, s_uri)
    #TODO: get the props from selected miner
    p_dump_name = subj + "/" + subj + "_prop.dump"
    # get the 100 most popular properties for type person in dbp
    ps = mm.get_p_dict_from_dump(fast, p_dump_name)

    i = 0
    cont = True
    ranks = {}
    while cont:
        subs, cont = get_subjects(s_uri, i)
        i+=1
        for s in subs:
            sg = mm.get_sub_graph( s, ps, fast)
            diff_evaluation = evaluate_selection(r_graph, sg)
            ranks[s] = diff_evaluation
        if fast:
            cont = i < 5
    if not os.path.exists(subj):
        os.makedirs(subj)
    dump_name = subj + "_Gincs.dump"
    inc_file = open(subj + "/" + dump_name, 'w')
    pickle.dump(ranks, inc_file)
    inc_file.close()



def rules_dict_from_dump(dump_name):
        r_graph_file = open(dump_name, 'r')
        p_dict = pickle.load(r_graph_file)
        r_graph_file.close()
        return p_dict


if __name__ == '__main__':

    rules = {}
    for d in [{'comedian': "http://dbpedia.org/ontology/Comedian"}]:
    #for d in dictionariesq:
        for s, suri in d.items():
            fix_dbpedia(DBPEDIA_URL, rules, suri, s, load=True)
            # fix_graphic(DBPEDIA_URL, rules, suri, s,fast=True, load=True)
