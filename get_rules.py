import csv
import pickle
import os
from Utils import dictionaries, dictionariest



def print_rules_to_csv(subj):
   
    
    rf_name = subj + "/" + subj + "_rules.dump"
    if not os.path.exists(rf_name):
        return
    rules_file = open(rf_name, 'r')
    all_rules = pickle.load(rules_file)
    if len(all_rules) < 6: return
    good, r60_70, r50_60, weird , ons, lows= all_rules
    rules_file.close()
    csv_names = ['good.csv', 'r60_70.csv', 'rtop_dbot.csv', 'weird.csv', 'rules_wierd_dbo.csv',  'ons.csv', 'lows.csv']

    for rd, csvn in zip(all_rules, csv_names):
        csvf_name = subj + "/" + csvn
        with open(csvf_name, 'w') as csvfile1:
            fieldnames = ['Property', 'Type', 'Ratio', 'support']
            writer = csv.DictWriter(csvfile1, fieldnames=fieldnames)

            writer.writeheader()
            if csvn == 'ons.csv':
                for r, rt in rd.items():
                    prop = r.encode('utf-8')
                    pos = float(rt)
                    data = {'Property': prop, 'Type': "", 'Ratio': pos, 'support': ""}
                    writer.writerow(data)
                continue
            for k, r in rd.items():
                prop = (r['p']).encode('utf-8')
                typet = (r['t']).encode('utf-8')
                pos = float(r['pos'])
                tot = float(r['tot'])
                ratio = pos/tot
                data = {'Property': prop, 'Type': typet, 'Ratio': ratio, 'support': tot}
                writer.writerow(data)

        csvfile1.close()



def print_f_rules_to_csv(subj):


    rf_name = subj + "/" + subj + "_f_rules.dump"
    if not os.path.exists(rf_name):
        return
    rules_file = open(rf_name, 'r')
    all_rules = pickle.load(rules_file)
    rules_file.close()
    csvf_name = subj + "/" + subj + "_f_rules.csv"

    with open(csvf_name, 'w') as csvfile1:
        fieldnames = ['p1', 'p2', 'Ratio']
        writer = csv.DictWriter(csvfile1, fieldnames=fieldnames)

        writer.writeheader()
        for (p1,p2), r in all_rules.items():
            p1_uni = (p1).encode('utf-8')
            p2_uni = (p2).encode('utf-8')

            pos = float(r)

            data = {'p1': p1_uni, 'p2': p2_uni, 'Ratio': pos}
            writer.writerow(data)

    csvfile1.close()


if __name__ == '__main__':




    for d in dictionaries:
        for s, suri in d.items():
            print_rules_to_csv(s)
            print_f_rules_to_csv(s)
        

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



