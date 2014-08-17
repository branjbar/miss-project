"""
A class for different types of entity resolution
"""
import time
from modules.NERD.dict_based_nerd import Nerd
from modules.basic_modules.basic import string_compare, run_query, log


class FullData():
    """
        this loads the complete data which is needed for a task.
        Later this will be integrated with the load_data module.
    """
    def __init__(self):
        self.docs = {}
        self.refs = {}
        self.notaries = {}
        self.matches = {}
        self.blocks = {}


    def load_references_all_persons(self, limit=None):
        log("load_references_all_persons started.")
        if limit:
            query = """
                    SELECT id, first_name, last_name, place_1, date_1, register_id, register_type from all_persons_new limit %d
                    """ % limit
        else:
            query = """
                    SELECT id, first_name, last_name, place_1, date_1, register_id, register_type from all_persons_new
                    """

        cur = run_query(query)
        for c in cur.fetchall():
            ref_id = c[0]
            name = c[1] + ' ' + c[2]
            place = c[3]
            date = c[4]
            doc_id = c[5]
            doc_type = c[6]

            ref = Reference(ref_id, name)
            doc = Document(doc_id, [ref], place, date, doc_type)
            if self.docs.get(doc_id):
                self.docs[doc_id].ref_list.append(ref)
            else:
                self.docs[doc_id] = doc
        log("load_references_all_persons finished.")

    def load_notaries(self, limit=None):
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
            doc_id = 'n' + str(c[0])
            text = c[1] + ' ' + c[2] + ' ' + c[3]
            place = c[4]
            date = c[5]
            doc_type = 'notary'

            nerd = Nerd(text)
            relations = nerd.get_relations()
            ref_list = []
            for index, rel in enumerate(relations):

                ref_list.append(Reference(str(doc_id)+ str(2 * index), rel['ref1'][1]))
                ref_list.append(Reference(str(doc_id)+ str(2 * index + 1), rel['ref2'][1]))

            if ref_list:
                doc = Document(doc_id, ref_list, place, date, doc_type)
                self.notaries[doc_id] = doc
                self.fill_in_blocks(ref_list, doc)

        log("load_notaries finished.")

    def fill_in_blocks(self, ref_list, doc):
        """
        for each to ref in ref_list add the docuemnt to the block
        """
        for ref1 in ref_list:
            for ref2 in ref_list:
                if ref1.ref_id < ref2.ref_id:
                    key_list = [ref1.get_compact_name(),ref2.get_compact_name()]
                    key_list = sorted(key_list)
                    block_key = key_list[0] + '_' + key_list[1]
                    if self.blocks.get(block_key):
                        if not doc.doc_id in self.blocks.get(block_key):
                            self.blocks[block_key].append(doc.doc_id)
                    else:
                        self.blocks[block_key] = [doc.doc_id]


    def generate_blocks(self):
        log("generate_blocks started")

        for doc in self.docs.values():
            self.fill_in_blocks(doc.ref_list, doc)

        log("generate_blocks finished")

class Reference():
    """
    a class for using any reference
    """

    def __init__(self, ref_id=None, name=None):
        self.ref_id = ref_id
        self.name = name

    def __repr__(self):
        return str(self.ref_id) + '_' + str(self.name)

    def get_compact_name(self):
        if len(self.name) > 1:
            return self.name.split()[0] + '_' + self.name.split()[-1]
        else:
            return ''


class Document():
    """
    a class for using any document
    """

    def __init__(self, doc_id=None, ref_list=None, place=None, date=None, doc_type=None):
        self.doc_id = doc_id
        self.ref_list = ref_list
        self.place = place
        self.date = date
        self.doc_type = doc_type

    def __repr__(self):
        return str(self.doc_id) + '_' + str(self.doc_type) + '_' +str(self.ref_list) + '_' + str(self.place) + '_' + str(self.date)

    def add_ref(self, ref):
        self.ref_list.append(ref)


class Match():
    """
    a class for storing are found matches
    """
    def __init__(self, match_id=None, doc_id1=None, doc_id2=None, match_type=None):
        self.match_id = match_id
        self.doc_id1 = doc_id1
        self.doc_id2 = doc_id2
        self.match_type = match_type

    def __repr__(self):

        return str(self.match_id) + '_' + str(self.doc_id1) + '_' + str(self.doc_id2) + '_' + str(self.match_type)


class ER():

    def __init__(self):
        self.document_source = Document()
        self.document_target = Document()

    def compare_docs(self):
        name_set1 = []
        name_set2 = []

        # generating a set of compact names of source document
        for ref in self.document_source.ref_list:
            name_set1.append(ref.get_compact_name())
        name_set1 = set(name_set1)

        # generating a set of compact names of target document
        for ref in self.document_target.ref_list:
            name_set2.append(ref.get_compact_name())
        name_set2 = set(name_set2)

        # Getting intersection of documents
        similarity = list(name_set1.intersection(name_set2))

        return similarity


if __name__ == '__main__':
    er = ER()

    file_name = open('blocks.csv','a')
    data = FullData()
    data.load_references_all_persons()
    data.generate_blocks()
    data.load_notaries()
    for b in data.blocks.keys():
        if len(data.blocks[b]) > 1:
            # print data.blocks[b]
            file_name.write(str(data.blocks[b]) + '\n')
        else:
            del data.blocks[b]






    # data.load_notaries(100)
    # match_id = 0
    # # print data.notaries
    #
    # log("matching started.")
    # for doc_source in data.notaries.values():
    #     # for doc_target in data.notaries.values():
    #     for doc_target in data.docs.values():
    #         # if doc_source.doc_id < doc_target.doc_id:
    #         er.document_source = doc_source
    #         er.document_target = doc_target
    #         similarity = er.compare_docs()
    #         if len(similarity) > 2:
    #             match_id += 1
    #             match = Match(match_id, doc_source.doc_id, doc_target.doc_id, 'notary_to_certificate')
    #             data.matches[match_id] = match
    #
    # for d in data.matches.values():
    #     print d
    #
    # log("matching finished.")






