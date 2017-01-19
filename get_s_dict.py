import pickle
import os
import csv

def get_subj_from_dump(subj_name):
    rf_name = subj_name + "/" + subj_name + "_top.dump"
    rp_name = subj_name + "/" + subj_name + "_prop.dump"
    if not os.path.exists(rf_name):
        return
    sujects_f = open(rf_name, 'r')
    all_subj = pickle.load(sujects_f)

    sujects_f.close()

    print "the number of {} is:{}".format(subj_name, len(all_subj))
    csvf_name = subj_name + "/" + subj_name + "_subject.csv"
    with open(csvf_name, 'w') as csvfile1:
        fieldnames = ['uri']
        writer = csv.DictWriter(csvfile1, fieldnames=fieldnames)

        writer.writeheader()
        for r in all_subj:
            subj_uri = (r).encode('utf-8')

            data = {'uri' : subj_uri}
            writer.writerow(data)

    csvfile1.close()

    if not os.path.exists(rp_name):
        return
    sujects_p = open(rp_name, 'r')
    all_prop = pickle.load(sujects_p)

    sujects_p.close()

    print "the number of {} is:{}".format(subj_name, len(all_prop))
    csvp_name = subj_name + "/" + subj_name + "_props.csv"
    with open(csvp_name, 'w') as csvfile2:
        fieldnames = ['uri', 'cnter']
        writer = csv.DictWriter(csvfile2, fieldnames=fieldnames)

        writer.writeheader()
        for r, c in all_prop.items():
            subj_uri = (r).encode('utf-8')
            
            data = {'uri' : subj_uri, 'cnter' : c}
            writer.writerow(data)

    csvfile1.close()








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


    ssubjects = {#'personn': "http://dbpedia.org/ontology/Person",
                'politician': "http://dbpedia.org/ontology/Politician",
                'soccer_player': "http://dbpedia.org/ontology/SoccerPlayer",
                'baseball_players': "http://dbpedia.org/ontology/BaseballPlayer",
                'comedian': "http://dbpedia.org/ontology/Comedian",
                'architectural_structure' : "http://dbpedia.org/ontology/ArchitecturalStructure"}



    for s, suri in ssubjects.items():
        get_subj_from_dump(s)
        
