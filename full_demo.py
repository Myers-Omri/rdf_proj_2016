from miner import *
from find_inconsistecies import fix_dbpedia

DBPEDIA_URL = "http://tdk3.csf.technion.ac.il:8890/sparql"


if __name__ == '__main__':
    quick = True

    db = DBPEDIA_URL


    min_pos_th = 10 #a small number just to separate the bizzar rule as we will see in the example.
    positive_total_ratio_th = 0.82  #selected after trying few values found to be the most suitable for the ration between
    #positive to total appearence where the positive is when tuple (p,t ) is unique
    subjects_f= {'person': "http://dbpedia.org/ontology/Person",
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
    subjects0 = {'Animal': "http://dbpedia.org/ontology/Animal"}
    
    for s, suri in subjects0.items():

        all_rules = mine_rules(db, quick, s, min_pos_th, positive_total_ratio_th)
        #rf_name = "rules/" + s + "_rules.dump"
        #rules_file = open(rf_name, 'w')
        #pickle.dump(all_rules, rules_file)
        #rules_file.close()

        # incs_name = "incs/" + s + "_incs.dump"
        # rules, r60_70, r50_60, dumy = all_rules
        # fix_dbpedia(db, rules, suri,incs_name, False)

