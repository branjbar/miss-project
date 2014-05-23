__author__ = 'Bijan'

STANDARD_QUERY = "SELECT id, first_name, last_name, date_1, place_1, gender, role, register_id, register_type \
          FROM all_persons WHERE "


from modules import basic
from modules import loadData
import random


def get_person(person_id = None):
    ''' (db, integer) -> (dict)
    return a person with the id
    '''

    if loadData.table_all_persons:
        if not person_id and loadData.table_all_persons:
            person_id = random.choice(loadData.table_all_persons.keys())

        person = loadData.table_all_persons.get(person_id)
        return person
    else:
        return None


def get_document(document_id = None):
    ''' (db, integer) -> (dict)
    return a document with the id
    '''
    # if no id then find a random person

    if loadData.table_all_documents:
        if not document_id and loadData.table_all_documents:
            document_id = random.choice(loadData.table_all_documents.keys())

        document = loadData.table_all_documents.get(document_id)
        return document
    else:
        return None


def get_block(db, block_id = None):
    """ (db, integer) -> (dict)
    return the block information with the id
    """

    # if no id provided then get a random block
    if not block_id:
        from random import randrange
        cur = basic.run_query(db, 'select min(block_id), max(block_id) from all_persons_features ')
        block_id_range = cur.fetchone()
        block_id = randrange(block_id_range[0],block_id_range[1])

    block_query = 'select ' + str(block_id) + ", block_key, count(*), group_concat( concat(' ',id,') '" \
                                              ",first_name, ' ', last_name) SEPARATOR '') from all_persons_features where " \
                                              "block_id = " + str(block_id)

    cur = basic.run_query(db, block_query)
    row = cur.fetchone()

    if row:
        reference = row_to_reference(db, row, "blocks")
    else:
        reference = {}

    return reference

def get_links(db, link_id = None):
    ''' (db, integer) -> (dict)
    returns the links_match information based on the id
    '''

    # if no id provided then get a random block
    if not link_id:
        from random import randrange
        link_id = randrange(1,3857070)

    link_query = 'select *, ' + str(link_id) + ' from links limit ' + str(link_id) + ',1'
    cur = basic.run_query(db, link_query)
    row = cur.fetchone()

    if row:
        reference = row_to_reference(db, row, "links")
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
    db = basic.do_connect()
    print get_block(db, 100)

