from SPARQLWrapper import SPARQLWrapper, JSON
from find_inconsistecies import fix_dbpedia
import pickle
import sys
import os

DBPEDIA_URL = "http://tdk3.csf.technion.ac.il:8890/sparql"
SMAL_URL = "http://cultura.linkeddata.es/sparql"

def get_ot_unique_dict(o_list, o_dict_t):
    res_dict = {}
    # single= False
    # if len(os) == 1:
    #     single = True
    for o in o_list:
        if o in o_dict_t:
            for t in o_dict_t[o]:

                #if (t in res_dict) or single:
                if t in res_dict:
                    res_dict[t] = False #this is the second time t in res_dict so not unique!
                else:
                    res_dict[t] = True #this is the first time t in res_dict so unique so far!
    return res_dict


def update_pt(t_dict_t,p_unique_t_dict):
    """
    the function count the uniquenes of types for a specific object and add it to the total statistics
    about the property & type
    :param t_dict_t: dictionary for all types that appears together with a specific property and true/false for
    uniqueness
    :param p_unique_t_dict: for every p the total statistics so far
    :return: just update the dictionary.
    """
    for t, v in t_dict_t.items():
        if t not in p_unique_t_dict:
            p_unique_t_dict[t] = {'pos': 0, 'tot': 0}
        if v:
            p_unique_t_dict[t]['pos'] += 1
        p_unique_t_dict[t]['tot'] += 1


def get_os(o_list, db):
    """
    Given list of object and a specific knowledge base creates a dictionary of o and the list of dbo:type that
    defines it

    :param o_list: list of object for specific relation
    :param db: the KB we query
    :return: o_dict dictionar {'<object>' : [c1,c2,c3...] (type list)
    """
    sparql = SPARQLWrapper(db)
    o_dict = {}
    for o in o_list:
        o_dict[o] = []
        sparql.setQuery("""
                            SELECT  DISTINCT  ?c
                            WHERE{
                                <%s>  <http://dbpedia.org/ontology/type>   ?c .
                                FILTER regex(?c, "^http://dbpedia.org", "i")
                            }
                        """ % o)

        #need to filter the types to informative ones.
        sparql.setReturnFormat(JSON)
        results = sparql.query().convert()

        for result in results["results"]["bindings"]:
            c = result["c"]["value"]
            o_dict[o].append(c)

    return o_dict




def mine_rules(db, quick, subjec_name, min_pos_th=0.2, positive_total_ratio_th=0.8):
    print "mining rules for {}".format(subjec_name)
    s_dump_name = subjec_name + "/" + subjec_name + "_top.dump"
    p_dump_name = subjec_name + "/" + subjec_name + "_prop.dump"
    # get the 100 most popular properties for type person in dbp
    p_dict = get_p_dict_from_dump(quick, p_dump_name)
    s_dict = get_s_dict_from_dump(s_dump_name)
    rules70_ = []
    rules60_70 = []
    rules50_60= []
    rules_wierd = []
    progress = 0
    p_size = len(p_dict)

    for p in p_dict:
        #s_dict = {}
        #this dictionary holds the statistics for every p separately p_unique_t_dict[t]={'pos': #uniqueness, 'tot': #totalappearence}
        p_unique_t_dict = {}
         #s is a sepecific person and os=[o1,o2,o3] is the list of objects that are in the relation: P(s,o)
        #
        p_count = 0
        # for every person in the list (2000 in total)

        for i,s  in enumerate(s_dict):
            o_list = update_so_dict(p, s)
            if o_list:
                p_count += 1
            if len(o_list) > 0:
                #ot_dict is list of types for every o in the list for specific person and property
                ot_dict = get_os(o_list, db)
                t_dict = get_ot_unique_dict(o_list, ot_dict) #Done: for specific person and property find the unique types!
                update_pt(t_dict,p_unique_t_dict) #Done: add up the times that t was unique for the specific p

            txt = "\b S loop progress: {}".format(i)
            sys.stdout.write(txt)
            sys.stdout.write("\r")
            sys.stdout.flush()

        sys.stdout.write("\b the total p are : {}".format(p_count))
        sys.stdout.write("\r")
        sys.stdout.flush()

        #print total_totals
        for t, counts in p_unique_t_dict.items():
            pos = float(counts['pos'])
            tot = float(counts['tot'])
            data = {'p': p, 't': t, 'pos': pos, 'tot': tot}
            #if (tot/max_totals) >= min_pos_th:
            if (tot >= min_pos_th):
                if ((pos /tot) >= positive_total_ratio_th) :
                    rules70_.append(data)
                elif((pos /tot) >= 0.6):
                    rules60_70.append(data)
                elif((pos /tot) >= 0.5):
                    rules50_60.append(data)
            else:
                rules_wierd.append(data)

        progress += 1
        txt = "\b Properties progress:{} / {} ".format(progress, p_size)
        sys.stdout.write(txt)
        sys.stdout.write("\r")
        sys.stdout.flush()
    all_rules_list = (rules70_,rules60_70, rules50_60 ,rules_wierd)
    print "get p_rules done"
    dir_name = subjec_name
    if not os.path.exists(dir_name):
        os.makedirs(dir_name)
    dump_name = dir_name + "/" + subjec_name + "_rules.dump"
    r_dict_file = open(dump_name, 'w')
    pickle.dump(all_rules_list, r_dict_file)
    r_dict_file.close()
    return all_rules_list


def update_so_dict(p, s):
    sparql = SPARQLWrapper(DBPEDIA_URL)


    o_list = []
    query_text = ("""
                SELECT DISTINCT ?o
                WHERE{
                        <%s> <%s> ?o .
                        ?o a ?t .
                        FILTER regex(?t, "^http://dbpedia.org/", "i")
                    } """ % (s, p))
    # I figured out that a good filter for the type of the object has to  be of "^http://dbpedia.org/ontology"
    # in oreder to get valuable results
    sparql.setQuery(query_text)
    sparql.setReturnFormat(JSON)
    results_inner = sparql.query().convert()
    for inner_res in results_inner["results"]["bindings"]:
        # s = inner_res["s"]["value"]
        o = inner_res["o"]["value"]

        # if s not in s_dict:
        #   s_dict[s] = []
        o_list.append(o)

    return o_list

def get_p_dict_from_dump(quick, dump_name):
    p_dict = {}
    if quick:
        p_dict["http://dbpedia.org/property/placeOfDeath"] = 0
        p_dict["http://dbpedia.org/property/placeOfDeath"] = 0
        p_dict["http://dbpedia.org/property/birthPlace"] = 0
        p_dict["http://dbpedia.org/property/party"] = 0
        p_dict["http://dbpedia.org/property/deathPlace"] = 0
        p_dict["http://dbpedia.org/property/subfamilia"] = 0

        p_dict["http://dbpedia.org/property/superfamilia"] = 0
        p_dict["http://dbpedia.org/property/region"] = 0
        p_dict["http://dbpedia.org/property/nextElection"] = 0

        p_dict["http://dbpedia.org/property/magazine"] = 0

        p_dict["http://dbpedia.org/property/director"] = 0
        p_dict["http://dbpedia.org/property/city"] = 0
        return p_dict

    p_dict_file = open(dump_name, 'r')
    p_dict = pickle.load(p_dict_file)

    p_dict_file.close()
    return p_dict


def get_s_dict_from_dump(dump_name):

    s_dict_file = open(dump_name, 'r')
    s_dict = pickle.load(s_dict_file)

    s_dict_file.close()
    return s_dict


def get_p_dict(quick, uri):
    sparql = SPARQLWrapper(DBPEDIA_URL)
    p_dict = {}
    if quick:

        p_dict["http://dbpedia.org/ontology/birthPlace"] = 0
        #p_dict["http://dbpedia.org/ontology/residence"] = 0
    else:
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
             LIMIT 100
            """ % uri)
        sparql.setQuery(query_text)
        sparql.setReturnFormat(JSON)
        results_inner = sparql.query().convert()

        for inner_res in results_inner["results"]["bindings"]:
            p = inner_res["p"]["value"]
            # cnt = inner_res["cnt"]["value"]
            p_dict[p] = 0
    p_dict_file = open('p_dict.dump', 'w')
    pickle.dump(p_dict, p_dict_file)
    p_dict_file.close()
    print "get p_dict done"
    return p_dict


if __name__ == '__main__':
    quick = True
    choice = raw_input("quick or full")
    if choice == "full":
        quick = False

    db = DBPEDIA_URL
    choice = raw_input("dbpedia or small")
    if choice == "small":
        db = SMAL_URL

    min_pos_th = float(raw_input("enter the th weird rules \n"))
    positive_total_ratio_th = float(raw_input("enter the th for good rules rules \n"))

    subjectsf = {'person': "http://dbpedia.org/ontology/Person",
                'Event': "http://dbpedia.org/ontology/Event",
                'Location': "http://dbpedia.org/ontology/Location",
                'Organisation': "http://dbpedia.org/ontology/Organisation",
                'Manga': "http://dbpedia.org/ontology/Manga",
                'Animal': "http://dbpedia.org/ontology/Animal",
                'Mammal': "http://dbpedia.org/ontology/Mammal",
                'Eukaryote': "http://dbpedia.org/ontology/Eukaryote",
                'Software': "http://dbpedia.org/ontology/Software",
                'Play': "http://dbpedia.org/ontology/Play"}

    subjects = {'person': "http://dbpedia.org/ontology/Person",
                'Manga': "http://dbpedia.org/ontology/Manga",
                'Animal': "http://dbpedia.org/ontology/Animal",
                'Mammal': "http://dbpedia.org/ontology/Mammal",
                'Software': "http://dbpedia.org/ontology/Software"}

    for s, suri in subjects.items():

        all_rules = mine_rules(db, quick, s, suri, min_pos_th, positive_total_ratio_th)



        choice = raw_input("Find inconsistenct now? y/n")
        if choice == "y":
            rules, dumy = all_rules
            fix_dbpedia(db, rules)
