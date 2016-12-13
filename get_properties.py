import pickle

if __name__ == '__main__':

    prop_file = open("p_dict.dump", 'r')
    all_props = pickle.load(prop_file)

    i=0
    for p in all_props:
    	print p


