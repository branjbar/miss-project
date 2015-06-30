__author__ = 'bijan'

from modules.basic_modules.basic import run_query, log, write_list_to_csv
from modules.NERD.dict_based_nerd import Nerd


reference_dict = {}
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
    for c in cur.fetchall():
        text = c[1] + ' ' + c[2] + ' ' + c[3]

        nerd = Nerd(text)

        refs = nerd.get_references()
        for ref in refs:
            reference_dict[ref[1]] = reference_dict.get(ref[1],0) + 1
            if 'Sint' in ref[1]:
                print ref[1]
            if reference_dict[ref[1]] == 340:
                print ref[1]

        # relations = nerd.get_relations()
        # ref_list = []
        # for index, rel in enumerate(relations):
        #
        #     ref_list.append(Reference(str(doc_id)+ str(2 * index), rel['ref1'][1]))
        #     ref_list.append(Reference(str(doc_id)+ str(2 * index + 1), rel['ref2'][1]))
        #
        # if ref_list:
        #     doc = Document(doc_id, ref_list, place, date, doc_type)
        #     self.notaries[doc_id] = doc
        #
        #     for index in xrange(len(ref_list)/2):
        #         self.fill_in_blocks([ref_list[2 * index], ref_list[2 * index+1]], doc)

    log("load_notaries finished.")
    write_list_to_csv(reference_dict.values(),'number_of_occurences_of_fullnames.csv')


if __name__ == '__main__':
    load_notaries()