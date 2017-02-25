import csv
import pickle
import os
from Utils import dictionaries, dictionariest


def get_incs_f(subj_name):
    rf_name = subj_name + "/" + subj_name + "_incs.dump"
    if not os.path.exists(rf_name):
        return
    incs_file = open(rf_name, 'r')
    incos = pickle.load(incs_file)
    if len(incos) < 2: return
    (inco_dict, inco_ones) = incos
    incs_file.close()
    csvf_name = subj_name + "/" + subj_name + "_incs.csv"
    with open(csvf_name, 'w') as csvfile:
        fieldnames = ['Person', 'Property', 'Type', 'rn']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writeheader()
        for pers, pt in inco_dict.items():
            uni_pers = pers.encode('utf-8')
            for p, t, rn in pt:
                uni_p = p.encode('utf-8')
                uni_t = t.encode('utf-8')
                writer.writerow({'Person': uni_pers, 'Property': uni_p, 'Type': uni_t, 'rn': rn})
                #print {'Person': pers, 'Property': p, 'Type': t}
    csvfile.close()

    csvf_name = subj_name + "/" + subj_name + "_ons_incs.csv"
    with open(csvf_name, 'w') as csvfile:
        fieldnames = ['Person', 'Property', 'Type', 'rn']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writeheader()
        for pers, pt in inco_ones.items():
            uni_pers = pers.encode('utf-8')
            for p, t, rn in pt:
                uni_p = p.encode('utf-8')
                uni_t = t.encode('utf-8')
                writer.writerow({'Person': uni_pers, 'Property': uni_p, 'Type': uni_t, 'rn': rn})
                # print {'Person': pers, 'Property': p, 'Type': t}
    csvfile.close()


if __name__ == '__main__':
    subjects0 = {'politician': "http://dbpedia.org/ontology/Politician"}
    for d in dictionaries:
        for s, suri in d.items():
            get_incs_f(s)

