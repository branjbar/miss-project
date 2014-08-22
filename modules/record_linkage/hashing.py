"""
updating solr
"""

from modules.basic_modules.basic import run_query
import solr
s = solr.SolrConnection('http://localhost:8983/solr')


__author__ = 'bijan'


query = "select first_name, last_name, register_id from all_persons_new"

cur = run_query(query)


c_counter = 0
import copy

def add_key(ref_list, document_id):
    global c_counter
    if document_id and ref_list:
        feature_list = []
        for i1, key1 in enumerate(ref_list):
            for i2, key2 in enumerate(ref_list):
                if i1 < i2:
                    feature = sorted([key1, key2])
                    feature_list.append(feature[0] + '_' + feature[1])
        
        if feature_list:
            s.add(features=feature_list, id=document_id)
            # print feature_list
            pass

        c_counter += 1
        if c_counter > 5000:
            s.commit()
            c_counter = 0
            print c_counter

ref_list = []
document_id = 2846095

for c in cur:


    # print c
    d_id = c[2]

    if len(c[0].split()) > 0:
        first_name = c[0].split()[0].decode('utf-8', 'ignore')
    else:
        first_name = None

    if len(c[1].split()) > 0:
        last_name = c[1].split()[-1].decode('utf-8', 'ignore')
    else:
        last_name = None

    
    if first_name and last_name:
        
        if d_id == document_id:
            
            ref_list.append(first_name + '_' + last_name)
        else:
            add_key(ref_list, document_id)
            document_id = copy.copy(d_id)
            ref_list = [first_name + '_' + last_name]


