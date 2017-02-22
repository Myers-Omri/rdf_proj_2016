from miner import *
from Utils import *
from find_inconsistecies import fix_dbpedia

DBPEDIA_URL = "http://tdk3.csf.technion.ac.il:8890/sparql"


if __name__ == '__main__':
    quick = True

    db = DBPEDIA_URL


    #min_pos_th = 0 #a small number just to separate the bizzar rule as we will see in the example.
   # positive_total_ratio_th = 0.82  #selected after trying few values found to be the most suitable for the ration between
    #positive to total appearence where the positive is when tuple (p,t ) is unique

    for d in dictionaries:
        for s, suri in d.items():
            t = Thread(target=mine_all_rules, args=(DBPEDIA_URL, s, suri, quick,))
            t.start()
            #mine_all_rules(DBPEDIA_URL, s, suri, quick)
                


    # for s, suri in subjects0.items():
    #
    #     all_rules = mine_rules(db, quick, s, min_pos_th, positive_total_ratio_th)
    #     #rf_name = "rules/" + s + "_rules.dump"
    #     #rules_file = open(rf_name, 'w')
    #     #pickle.dump(all_rules, rules_file)
    #     #rules_file.close()
    #
    #     # incs_name = "incs/" + s + "_incs.dump"
    #     # rules, r60_70, r50_60, dumy = all_rules
    #     # fix_dbpedia(db, rules, suri,incs_name, False)
    #
