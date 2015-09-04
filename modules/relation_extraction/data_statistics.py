from modules.solr_search.solr_query import SolrQuery

__author__ = 'bijan'

from modules.basic_modules.basic import run_query, log, write_list_to_csv
from modules.NERD.dict_based_nerd import Nerd




def load_notaries(limit=None):
    log("load_notaries started.")
    if limit:
        query = """
                SELECT row_id, text1, text2, text3, place, date from notary_acts where date like %s limit %d
                """ % ("'%-18%'", limit)
    else:
        query = """
                SELECT row_id, text1, text2, text3, place, date from notary_acts where date like %s
                """ % ("'%-18%'")
    cur = run_query(query)
    name_pair_freq = {}
    my_solr = SolrQuery()
    fuzzy_freq = []
    used_keys = []

    for c in cur.fetchall():
        text = c[1] + ' ' + c[2] + ' ' + c[3]

        nerd = Nerd(text)

        relations = nerd.get_relations()
        for index, rel in enumerate(relations):
            name1 = rel['ref1'][1]
            ref_name1 = name1.split()[0] + ' ' + name1.split()[-1]
            name2 = rel['ref2'][1]
            ref_name2 = name2.split()[0] + ' ' + name2.split()[-1]
            ref_name_list = [ref_name1, ref_name2]
            ref_name_list.sort()
            ref_list = ' '.join(ref_name_list)
            name_pair_freq[ref_list] = name_pair_freq.get(ref_list, 0) + 1

    for index, the_key in enumerate(name_pair_freq.keys()):
        print index, 'out of', len(name_pair_freq.keys())
        if not the_key in used_keys:
            used_keys.append(the_key)
            search_results = my_solr.search(the_key.replace(' ','_'),'cat:notarial act')
            fuzzy_freq.append(search_results.results.numFound)
            for result in search_results.highlighting.iteritems():
                new_key = result[1]['features'][0].replace('<em>', '').replace('</em>', '').replace('_',' ')
                if new_key not in used_keys:
                    used_keys.append(new_key)

    log("load_notaries finished.")
    write_list_to_csv(name_pair_freq.values(), 'number_of_occurences_of_fullname_pairs.csv')
    write_list_to_csv(fuzzy_freq, 'number_of_occurences_of_fuzzy_fullname_pairs.csv')


if __name__ == '__main__':
    load_notaries()