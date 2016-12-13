import csv
import pickle


def get_incs_f(subj_name):
    rf_name = subj_name + "/" + subj_name + "_incs.dump"
    if not os.path.exists(rf_name):
        return
    incs_file = open(rf_name, 'r')
    inco_dict = pickle.load(incs_file)

    incs_file.close()

    with open('inconsistencies.csv', 'w') as csvfile:
        fieldnames = ['Person', 'Property', 'Type']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writeheader()
        for pers, pt in inco_dict.items():
            uni_pers = pers.encode('utf-8')
            for p, t in pt:
                uni_p = p.encode('utf-8')
                uni_t = t.encode('utf-8')
                writer.writerow({'Person': uni_pers, 'Property': uni_p, 'Type': uni_t})
                #print {'Person': pers, 'Property': p, 'Type': t}
    csvfile.close()


if __name__ == '__main__':
    get_incs_f("try_incs.dump")

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

    for s, suri in subjects_f.items():
        get_incs_f(s)

