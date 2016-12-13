import csv
import pickle


def get_incs_f(inc_dump):
    incs_file = open(inc_dump, 'r')
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

