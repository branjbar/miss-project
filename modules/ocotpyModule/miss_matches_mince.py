__author__ = 'Bijan'
"""
    Uses map-reduce to generate a list of all paired documents that are encompassed by one or more blocks.
     finally just the paired documents which are encompassed in more than one document are exported in a csv file
     to be imported to mysql database called: miss_maches
     mysql> load data infile 'matches.csv' into table miss_matches fields terminated by ';' lines terminated by '\n'

    source: the main dictionary that map_reduce is applied on


"""
import mincemeat

import pickle


pickled_file = open('../data/block_dump_1000.txt', 'r')
source = pickle.load(pickled_file)


def final(key, value):
    """
        converts a reduced (key,value) pair to a semicolon delimited string to be stored in the output csv
        assuming the key and values are

        >>> final ("2846142_2846282", [[85,343,female_Adr_Lou_na_rs_A365_L620],[87,345,female_Mar_Sen_ia_rs_M600_S536],[86,344,male_Jan_Lou_an_rs_J500_L620]])
        2846142;2846282;3;[85,343,female_Adr_Lou_na_rs_A365_L620],[87,345,female_Mar_Sen_ia_rs_M600_S536],[86,344,male_Jan_Lou_an_rs_J500_L620]
    """

    if len(value) > 2: #just print the documents which are encompassed by at least two blocks
        s = ''
        for m in value: # here make a string from the list of details
            s += '['
            for j in m[:-1]:
                s += str(j) + ','
            s += str(m[-1]) + '],'

        s = s[:-1]
        csv_text = key.replace('_',';') + ';' + str(len(value)) + ';' + s + '\n'

        with open("../data/matches.csv", "a") as myfile:
            myfile.write(csv_text)
            # print key, value

# client
def mapfn(key, value):
    """
        for each block_key construct new keys with every document pair and yield all those new keys with details.
    """
    # print value
    if int(key) != 1888:
        for doc1 in value['docs']:
            for doc2 in value['docs']:
                doc1_id = int(doc1[0])
                doc2_id = int(doc2[0])
                if doc1_id < doc2_id:
                    new_key = str(doc1_id) + '_' + str(doc2_id)
                    yield new_key, [doc1[1], doc2[1], value['block_key'], key]



def reducefn(key, value):
    """
        simply aggregate all the values with the same key and sends that the final() function
    """
    return value


s = mincemeat.Server()
s.datasource = source
s.mapfn = mapfn
s.reducefn = reducefn
# s.collectfn = final


results = s.run_server(password="changeme")
for key in results.keys():
    final(key, results[key])
print results