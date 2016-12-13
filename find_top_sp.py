from SPARQLWrapper import SPARQLWrapper, JSON
import os
import pickle
import sys
DBPEDIA_URL = "http://tdk3.csf.technion.ac.il:8890/sparql"


def get_top_1_percent(i, top_s_dict,uri):
    sparql = SPARQLWrapper(DBPEDIA_URL)

    limit = 10000
    offset = i * limit

    slimit = str(limit)
    soffset = str(offset)
    query_text = ("""
    SELECT ?s(COUNT(*)AS ?scnt)
    WHERE
    {
        {
            SELECT DISTINCT ?s ?p
            WHERE
            {
                {
                    SELECT DISTINCT ?s
                    WHERE
                    {
                        ?s a <%s>.
                    } LIMIT %s
                    OFFSET %s
                }
                ?s ?p ?o.
                FILTER regex(?p, "^http://dbpedia.org/", "i")
            }
        }
    } GROUP BY ?s
    ORDER BY DESC(?scnt)
    LIMIT 100""" % (uri,slimit, soffset))

    sparql.setQuery(query_text)
    sparql.setReturnFormat(JSON)
    results_inner = sparql.query().convert()
    all_dict = results_inner["results"]["bindings"]
    for inner_res in all_dict:
        s = inner_res["s"]["value"]
        cnt = inner_res["scnt"]["value"]
        if cnt>20:
            top_s_dict[s] = cnt
    if len(all_dict) > 10:
        return True
    return False

def get_all_top_of(uri , f_name, dir_name):

    i=0
    top_subjects = {}
    flag = get_top_1_percent(i, top_subjects, uri)
    while flag:
        i += 1
        flag = get_top_1_percent(i, top_subjects, uri)

        txt = "\b i progress:{} ".format(i)
        sys.stdout.write(txt)
        sys.stdout.write("\r")
        sys.stdout.flush()
        if i>150:
            flag = False

    if not os.path.exists(dir_name):
        os.makedirs(dir_name)
    s_dict_file = open(dir_name + "/" + f_name, 'w')
    pickle.dump(top_subjects, s_dict_file)
    s_dict_file.close()
    print "get top s  done for {}, i is:{}".format(f_name, i)



def get_all_p_dict(uri, dump_name,dir_name):
    sparql = SPARQLWrapper(DBPEDIA_URL)
    p_dict = {}


    query_text = ("""
            SELECT ?p (COUNT (?p) AS ?cnt)
            WHERE {
                {
                SELECT DISTINCT ?s
                WHERE {
                    ?s a <%s>.
                }LIMIT 500000
                }
                ?s ?p ?o
                FILTER regex(?p, "^http://dbpedia.org/", "i")
            }GROUP BY ?p
             ORDER BY DESC(?cnt)
             LIMIT 50
            """ % uri)
    sparql.setQuery(query_text)
    sparql.setReturnFormat(JSON)
    results_inner = sparql.query().convert()

    for inner_res in results_inner["results"]["bindings"]:
        p = inner_res["p"]["value"]
        cnt = inner_res["cnt"]["value"]
        p_dict[p] = cnt

    if not os.path.exists(dir_name):
        os.makedirs(dir_name)
    p_dict_file = open(s + "/" + dump_name, 'w')
    pickle.dump(p_dict, p_dict_file)
    p_dict_file.close()
    print "pdict done for: {}".format(dir_name)



if __name__ == '__main__':

    subjects = {'person': "http://dbpedia.org/ontology/Person",
                'Event': "http://dbpedia.org/ontology/Event",
                'Location': "http://dbpedia.org/ontology/Location",
                'Organisation': "http://dbpedia.org/ontology/Organisation",
                'Manga': "http://dbpedia.org/ontology/Manga",
                'Animal': "http://dbpedia.org/ontology/Animal",
                'Mammal': "http://dbpedia.org/ontology/Mammal",
                'Eukaryote': "http://dbpedia.org/ontology/Eukaryote",
                'Software': "http://dbpedia.org/ontology/Software",
                'Play': "http://dbpedia.org/ontology/Play"}

    for s,uri in subjects.items():
        f = s + "_top.dump"
        pn = s + "_prop.dump"
        #get_all_top_of(uri ,f, s)
        get_all_p_dict(uri, pn, s)









