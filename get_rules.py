import csv
import pickle

def print_rules_to_csv(subj):
   
    
    rf_name = "rules/" + subj + "_rules.dump"
    rules_file = open(rf_name, 'r')
    all_rules = pickle.load(rules_file)
    good, r60_70, r50_60, weird = all_rules
    rules_file.close()
    csv_names = ['good.csv', 'r60_70.csv', 'r50_60.csv', 'weird.csv']

    for rd, csvn in zip(all_rules, csv_names):
        with open(csvn, 'w') as csvfile1:
            fieldnames = ['Property', 'Type', 'Ratio', 'support']
            writer = csv.DictWriter(csvfile1, fieldnames=fieldnames)

            writer.writeheader()
            for r in rd:
                prop = (r['p']).encode('utf-8')
                typet = (r['t']).encode('utf-8')
                pos = float(r['pos'])
                tot = float(r['tot'])
                ratio = pos/tot
                data = {'Property': prop, 'Type': typet, 'Ratio': ratio, 'support': tot}
                writer.writerow(data)

        csvfile1.close()





if __name__ == '__main__':


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
       
       
        print_rules_to_csv(s)
        

    # rules_file = open("rules.dump", 'r')
    # all_rules = pickle.load(rules_file)
    # good, r60_70, r50_60, weird = all_rules
    # rules_file.close()

    # with open('rules.csv', 'w') as csvfile1:
    #     fieldnames = ['Property', 'Type', 'Ratio', 'support']
    #     writer = csv.DictWriter(csvfile1, fieldnames=fieldnames)

    #     writer.writeheader()
    #     for r in good:
    #         prop = (r['p']).encode('utf-8')
    #         typet = (r['t']).encode('utf-8')
    #         pos = float(r['pos'])
    #         tot = float(r['tot'])
    #         ratio = pos/tot
    #         data = {'Property': prop, 'Type': typet, 'Ratio': ratio, 'support': tot}
    #         writer.writerow(data)

    # csvfile1.close()

    # with open('r60_70.csv', 'w') as csvfile1:
    #     fieldnames = ['Property', 'Type', 'Ratio', 'support']
    #     writer = csv.DictWriter(csvfile1, fieldnames=fieldnames)

    #     writer.writeheader()
    #     for r in r60_70:
    #         prop = (r['p']).encode('utf-8')
    #         typet = (r['t']).encode('utf-8')
    #         pos = float(r['pos'])
    #         tot = float(r['tot'])
    #         ratio = pos / tot
    #         data = {'Property': prop, 'Type': typet, 'Ratio': ratio, 'support': tot}
    #         writer.writerow(data)

    # csvfile1.close()

    # with open('r50_60.csv', 'w') as csvfile1:
    #     fieldnames = ['Property', 'Type', 'Ratio', 'support']
    #     writer = csv.DictWriter(csvfile1, fieldnames=fieldnames)

    #     writer.writeheader()
    #     for r in r50_60:
    #         prop = (r['p']).encode('utf-8')
    #         typet = (r['t']).encode('utf-8')
    #         pos = float(r['pos'])
    #         tot = float(r['tot'])
    #         ratio = pos / tot
    #         data = {'Property': prop, 'Type': typet, 'Ratio': ratio, 'support': tot}
    #         writer.writerow(data)

    # csvfile1.close()

    # with open('rules_weird.csv', 'w') as csvfile2:
    #     fieldnames = ['Property', 'Type', 'Ratio', 'support']
    #     writer = csv.DictWriter(csvfile2, fieldnames=fieldnames)

    #     writer.writeheader()
    #     for r in weird:
    #         prop = r['p'].encode('utf-8')
    #         typet = r['t'].encode('utf-8')
    #         pos = float(r['pos'])
    #         tot = float(r['tot'])
    #         ratio = pos / tot
    #         data = {'Property': prop, 'Type': typet, 'Ratio': ratio, 'support': tot}
    #         writer.writerow(data)

    # csvfile2.close()


