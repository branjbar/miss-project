"""
Here we do the hashing and update, search the """
from modules.NERD.dict_based_nerd import Nerd

from modules.basic_modules.basic import run_query
import solr
import copy
from modules.basic_modules.myOrm import Reference

NOTARY_OFFSET_old = 4000000
NOTARY_OFFSET = 30000000


class Hashing():
    def __init__(self):
        """
        initializes the Solr connection
        :return:
        """
        self.s = solr.SolrConnection('http://localhost:8983/solr')
        self.commit_counter = 0
        self.commit_number = 0
        self.current_document_id = 2846095

    def add_key(self, ref_list, document_id):
        """

        :param ref_list: list of references that should be indexed
        :param document_id: document id
        :return:
        """
        if document_id and ref_list:
                feature_list = []
                for i1, key1 in enumerate(ref_list):
                    for i2, key2 in enumerate(ref_list):
                        if i1 < i2:
                            feature = sorted([key1, key2])
                            feature_list.append(feature[0] + '_' + feature[1])

                if feature_list:
                    self.s.add(features=feature_list, id=document_id)

                self.commit_counter += 1
                if self.commit_counter > 5000:
                    self.s.commit()
                    self.commit_counter = 0

                    print self.commit_number
                    self.commit_number += 1

    def update_all_persons(self):

        query = "select first_name, last_name, register_id from all_persons_new limit 100"

        cur = run_query(query)
        self.commit_number = 0

        ref_list = []
        for c in cur:
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

                if d_id == self.current_document_id:

                    ref_list.append(first_name + '_' + last_name)
                else:
                    self.add_key(ref_list, self.current_document_id)
                    self.current_document_id = copy.copy(d_id)
                    ref_list = [first_name + '_' + last_name]

    def update_notaries(self):
        query = """
        SELECT row_id, text1, text2, text3, place, date from notary_acts
        """
        cur = run_query(query)
        for c in cur.fetchall():
            notary_id = c[0] + NOTARY_OFFSET
            doc_id = 'n' + str(c[0])
            text = c[1] + ' ' + c[2] + ' ' + c[3]

            nerd = Nerd(text)
            relations = nerd.get_relations()
            ref_list = []
            for index, rel in enumerate(relations):

                ref_list.append(Reference(str(doc_id) + str(2 * index), rel['ref1'][1]))
                ref_list.append(Reference(str(doc_id) + str(2 * index + 1), rel['ref2'][1]))

            if ref_list:
                feature_list = []
                for index in xrange(len(ref_list)/2):
                    feature_list.append('_'.join(sorted([ref_list[2 * index].get_compact_name(), ref_list[2 * index+1].get_compact_name()])).decode('utf-8', 'ignore'))

                self.s.add(features=feature_list, id=notary_id)

            self.commit_counter += 1
            if self.commit_counter > 5000:
                self.s.commit()
                self.commit_counter = 0

                print self.commit_number
                self.commit_number += 1

    def search(self, features_list=[]):
        query_results = ''
        if features_list:
            query = 'features:'
            for feature in features_list:

                query += feature + '~.01 OR '

            query = query[:-4]
            print query
            query_results = self.s.query(query, rows=200, highlight=True, fields="features, id")

        return query_results

if __name__ == '__main__':
    my_hash = Hashing()
    # my_hash.update_all_persons()
    my_hash.update_notaries()
    my_hash.s.commit()
