import pickle
from SPARQLWrapper import SPARQLWrapper, JSON
import sys
import os


DBPEDIA_URL = "http://dbpedia.org/sparql"

try_rules = [{'p': "http://dbpedia.org/ontology/residence" ,'t':	"http://dbpedia.org/resource/City"},
             {'p': "http://dbpedia.org/ontology/birthPlace", 't':"http://dbpedia.org/resource/City"}]


def fix_dbpedia(db, rules, s_uri, subject_name, load=False):

    sparql = SPARQLWrapper(db)
    if load:
        rules_file = open(rules, 'r')
        all_rules = pickle.load(rules_file)
        (rules, r_67, r_56,r4) = all_rules
        rules_file.close()
    print "find inconsistencies, number of rules: {} ".format(len(rules))
    i = 0
    inco_dict = {}
    for r in rules:
        i+=1
        p = r['p']
        t = r['t']
        # count entities that ruin uniqueness
		# for every property and type we mined before count and find the
		#violations.
        query_text = ("""
            SELECT ?s ?cnt
            WHERE {
            {
                SELECT ?s (COUNT(*) AS ?cnt)
                WHERE{
                    ?o <http://dbpedia.org/ontology/type> <%s>.
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

            if s not in inco_dict:
                inco_dict[s] = []
            inco_dict[s].append((p, t))

    if not os.path.exists(subject_name):
        os.makedirs(subject_name)

    dump_name = subject_name + "_incs.dump"
    inc_file = open(subject_name + "/" + dump_name, 'w')

    pickle.dump(inco_dict, inc_file)
    inc_file.close()
    return inco_dict




if __name__ == '__main__':
    uri = "http://dbpedia.org/ontology/Person"
    fix_dbpedia(DBPEDIA_URL, try_rules,uri,"try_incs.dump", False)

