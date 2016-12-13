import pickle

if __name__ == '__main__':

    prop_file = open("Play_top.dump", 'r')
    all_persons = pickle.load(prop_file)
    prop_file.close()
    
    print "the number of persons is:{}".format(len(all_persons))
    for p ,c in all_persons.items():
        print p.encode('utf-8'), c


