__author__ = 'Bijan'

from modules.basic_modules import basic, loadData

STANDARD_QUERY = "SELECT id, first_name, last_name, date_1, place_1, gender, role, register_id, register_type \
          FROM all_persons WHERE "

import random


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

#
# class Match():
#     """
#     a class for storing are found matches
#     """
#     def __init__(self, match_id=None, doc_id1=None, doc_id2=None, match_type=None):
#         self.match_id = match_id
#         self.doc_id1 = doc_id1
#         self.doc_id2 = doc_id2
#         self.match_type = match_type
#
#     def __repr__(self):
#
#         return str(self.match_id) + '_' + str(self.doc_id1) + '_' + str(self.doc_id2) + '_' + str(self.match_type)
#




def row_to_reference(row, table="all_persons"):
    ''' (list, table) -> (dict)
    adds labels to different elements of the list, according to the table type,
    and makes a reference
    '''

    if table == 'links':
        ref = {}
        key_dict = {0: 'type', 1: 'id1', 2: 'id2', 3: 'role1', 4: 'role2', 5: 'id'}

        for key in key_dict.keys():
            ref[key_dict[key]] = row[key]
        return ref


def get_person(person_id=None):
    ''' (integer) -> (dict)
    return a person with the id
    '''
    person = None
    if loadData.table_all_persons:
        if not person_id and loadData.table_all_persons:
            person_id = random.choice(loadData.table_all_persons.keys())

        person = loadData.table_all_persons.get(int(person_id))
    if not person and person_id:
        loadData.update_persons_table('', ['', '', 'where id = %s' % str(person_id)])
        person = loadData.table_all_persons.get(int(person_id))

    if person:
        return person
    else:
        return None


def get_document(document_id=None):
    ''' (integer) -> (dict)
    return a document with the id
    '''
    # if no id then find a random person
    document = None
    if loadData.table_all_documents:
        if not document_id:
            document_id = random.choice(loadData.table_all_documents.keys())

        document = loadData.table_all_documents.get(int(document_id))

    if not document and document_id:
        loadData.update_documents_table(['', '', 'where id = %s' % str(document_id)])
        document = loadData.table_all_documents.get(int(document_id))

    if document:
        return document
    else:
        return None


def get_block(block_id=None):
    """ (integer) -> (dict)
    return the block information with the id
    """

    if loadData.block_dict:

        if not block_id:
            retry_counter = 0
            while retry_counter < 100:
                block_id = random.choice(loadData.block_dict.keys())
                block = loadData.block_dict.get(block_id)
                if block.get('block_id') and len(block['block_id']) > 1:
                    retry_counter = 100
                else:
                    retry_counter += 1
        else:
            block = loadData.block_dict.get(block_id)

        return block

    else:
        return {}


def get_links(link_id=None):
    ''' (integer) -> (dict)
    returns the links_match information based on the id
    '''

    # if no id provided then get a random block
    if not link_id:
        from random import randrange

        link_id = randrange(1, 2980158)
    reference = {}
    index = 1
    while index < 3:
        link_query = 'select *, ' + str(link_id) + ' from links where id1 > 0 and id2 > 0 limit ' + str(link_id) + ',1'
        cur = basic.run_query(link_query)
        row = cur.fetchone()
        if row:
            reference = row_to_reference(row, "links")
        else:
            reference = {}

        if reference.get('id1') and reference.get('id2'):
            index = 5
        else:
            index += 1

    if reference.get('id1') and reference.get('id2'):
        reference['id'] = link_id
        return reference
    else:
        return {'id1': 0, 'id2': 0}


def get_notarial_act(text_id=None):
    ''' (integer) -> (dict)
    return a person with the id
    '''

    text = None
    if loadData.table_notarial_acts:
        if not text_id and loadData.table_all_persons:
            text_id = random.choice(loadData.table_all_persons.keys())

        text = loadData.table_all_persons.get(int(text_id))
    if not text and text_id:
        index = loadData.update_notarial_acts(['', '', 'where row_id = %s' % str(text_id)])
        # index = loadData.update_notarial_acts(['', '', 'where date like %s limit %s, 1' % ("'%-18%'", str(text_id))])
        text = loadData.table_notarial_acts.get(index)

    if text:
        return text
    else:
        return None


def get_miss_matches(match_index=None, match_id=None):
    """ (integer) -> (dict)
    returns the miss_match information based on the id
    """

    # if no id provided then get a random block
    if not loadData.match_pairs:
        loadData.get_matching_pairs()


    if not match_index:
        from random import randrange

        match_index = randrange(1, 1000)

    match_index = int(match_index)
    if loadData.match_pairs.get(match_index):
        reference = loadData.match_pairs[match_index]
        reference['index'] = match_index
    else:
        reference = {}
    return reference


def get_relatives(person_id):
    """
     uses the 'relations' table in order to extract the id of all relatives of person_id
    """
    modified_relative_ids = []
    if person_id:

        key_d = int(loadData.table_all_persons.get(person_id)['register_id'])

        if loadData.table_all_documents.get(key_d):

            relatives = loadData.table_all_documents[key_d]['reference_ids']
            relative_ids = relatives.split(',')
            for i in relative_ids:
                if int(i) != person_id:
                    modified_relative_ids.append(int(i))

    return modified_relative_ids


if __name__ == "__main__":
    pass
