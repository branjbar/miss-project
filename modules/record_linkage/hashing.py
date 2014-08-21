"""
updating solr
"""

from modules.basic_modules.basic import run_query
import solr
s = solr.SolrConnection('http://localhost:8983/solr')


__author__ = 'bijan'


query = "select first_name, last_name, register_id from all_persons_new limit 1000000"

cur = run_query(query)



def add_key(ref_list, document_id):
    if document_id:
        for i1, key1 in enumerate(ref_list):
            for i2, key2 in enumerate(ref_list):
                if i1 < i2:
                    feature = sorted([key1, key2])
                    s.add(features=feature[0] + '_' + feature[1], id=document_id)
        s.commit()


ref_list = []
document_id = 0

for c in cur:


    d_id = c[2]

    if len(c[0].split()) > 1:
        first_name = c[0].split()[0].decode('utf-8', 'ignore')
    else:
        first_name = None

    if len(c[1].split()):
        last_name = c[1].split()[-1].decode('utf-8', 'ignore')
    else:
        last_name = None

    if first_name and last_name:
        if d_id == document_id:
            ref_list.append(first_name + '_' + last_name)
        else:
            add_key(ref_list, document_id)
            document_id = d_id
            ref_list = [first_name + '_' + last_name]


