import pickle
from SPARQLWrapper import SPARQLWrapper, JSON
import sys
import os


DBPEDIA_URL = "http://dbpedia.org/sparql"

try_rules = [{'p': "http://dbpedia.org/ontology/residence" ,'t':	"http://dbpedia.org/resource/City"},
             {'p': "http://dbpedia.org/ontology/birthPlace", 't':"http://dbpedia.org/resource/City"}]


def fix_dbpedia(db, rules, s_uri, subj, load=True):


    rf_name = subj + "/" + subj + "_rules.dump"
    if not os.path.exists(rf_name):
        return

    sparql = SPARQLWrapper(db)
    if load:
        rules_file = open(rf_name, 'r')
        all_rules = pickle.load(rules_file)
        (rules, r_67, r_56,r4) = all_rules
        rules_file.close()
    print "find inconsistencies, number of rules: {} ".format(str(len(rules)))
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

    if not os.path.exists(subj):
        os.makedirs(subj)

    dump_name = subj + "_incs.dump"
    inc_file = open(subj + "/" + dump_name, 'w')

    pickle.dump(inco_dict, inc_file)
    inc_file.close()
    return inco_dict




if __name__ == '__main__':
    subjects_f = {'person': "http://dbpedia.org/ontology/Person",
                  'Event': "http://dbpedia.org/ontology/Event",
                  'Location': "http://dbpedia.org/ontology/Location",
                  'Organisation': "http://dbpedia.org/ontology/Organisation",
                  'Manga': "http://dbpedia.org/ontology/Manga",
                  'Animal': "http://dbpedia.org/ontology/Animal",
                  'Mammal': "http://dbpedia.org/ontology/Mammal",
                  'Eukaryote': "http://dbpedia.org/ontology/Eukaryote",
                  'Software': "http://dbpedia.org/ontology/Software",
                  'Play': "http://dbpedia.org/ontology/Play"}

    subjects1 = {'person': "http://dbpedia.org/ontology/Person",
             'Manga': "http://dbpedia.org/ontology/Manga",
             'Animal': "http://dbpedia.org/ontology/Animal",
             'Mammal': "http://dbpedia.org/ontology/Mammal",
             'Software': "http://dbpedia.org/ontology/Software"}
    subjects0 = {'person': "http://dbpedia.org/ontology/Animal"}

    rules = {}
    for s, suri in subjects_f.items():
        fix_dbpedia(DBPEDIA_URL, rules, suri, s, load=True)

