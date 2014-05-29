from modules.basic_modules import basic


__author__ = 'Bijan'

import time
import threading
import logging

table_all_documents = {}
table_all_persons = {}
block_dict = {}
match_pairs = []



def update_persons_table(db, limit):
    global table_all_persons, block_dict
    __now__ = time.time()

    if not db:
        db = basic.do_connect()

    lim = limit[0]
    type = limit[1]
    addendum = limit[2]
    logging.debug('Loading table all_persons.')

    the_query = "select id, first_name, prefix, last_name, block_key, block_id, date_1 as date, place_1 as place," \
                " gender, role, register_id, register_type from all_persons_new"
    if type:
        q_type = None
        for t in type:
            if not q_type:
                q_type = " register_type = '%s'" % t
            else:
                q_type += " or register_type = '%s'" % t
        the_query += " where %s" % q_type

    if lim:
        the_query += " limit %d" % lim

    if addendum:
        the_query += " " + addendum

    cur = basic.run_query(db, the_query)
    desc = cur.description

    if not addendum:
        t2 = threading.Thread(target=update_documents_table, args=(db, limit))
        t2.daemon = True
        t2.start()


    tmp_index = 0
    for row in cur.fetchall():
        row_dict = {}
        tmp_index += 1
        for index, value in enumerate(row):
            try:
                row_dict[desc[index][0]] = value.decode('ascii','ignore')
            except:
                row_dict[desc[index][0]] = value
        table_all_persons[row_dict['id']] = row_dict

    logging.debug("table all_persons imported in %s" % str(time.time() - __now__))

    if not addendum:
        __now__ = time.time()
        logging.debug(" - building block_dict.")

        block_dict = build_block_dict()
        logging.debug("block_dict is built in %s" % str(time.time() - __now__))


def update_documents_table(db, limit):
    global table_all_documents, block_dict

    if not db:
        db = basic.do_connect()

    __now__ = time.time()

    lim = limit[0]
    type = limit[1]
    addendum = limit[2]

    logging.debug(" Loading table all_documents.")

    the_query = "select id, type_text, date, `index`, municipality, concat(latitude,',', longitude) geocode," \
                " reference_ids from all_documents"
    if type:
        q_type = None
        for t in type:
            if not q_type:
                q_type = "type_text = '%s'" % t
            else:
                q_type += " or type_text = '%s'" % t
        the_query += " where %s" % q_type

    if lim:
        the_query += " limit %d" % lim

    if addendum:
        the_query += " " + addendum


    cur = basic.run_query(db, the_query)
    desc = cur.description

    tmp_index = 0
    for row in cur.fetchall():
        row_dict = {}
        tmp_index += 1
        for index, value in enumerate(row):
            try:
                row_dict[desc[index][0]] = value.decode('ascii','ignore')
            except:
                row_dict[desc[index][0]] = value
        table_all_documents[row_dict['id']] = row_dict

    logging.debug("table all_documents imported in %s" % str( time.time() - __now__))

    if not addendum:
        block_dict = get_matching_pairs(block_dict)


def get_matching_pairs(block_dict):
    """
        uses the blocks in order to fina every document that share more than two common blocks.

    """
    __now__ = time.time()
    logging.debug("generating blocks started")

    doc_dict = {}
    for b in block_dict.keys():
        if b != 1888:
            for doc1 in block_dict[b]['members']:
                for doc2 in block_dict[b]['members']:
                    if not doc1['doc'] is doc2['doc']:
                        if doc1['doc'] < doc2['doc']:
                            key = str(doc1['doc']) + '_' + str(doc2['doc'])

                            if doc_dict.get(key) and not b in doc_dict[key]['block_id']:
                                doc_dict[key]['block_id'].append(b)
                                # print (doc1['doc'], doc2['doc']),'<-', b
                            else:
                                doc_dict[key] = {'id': key, 'block_id': [b]}

    print time.ctime(), ' - elapsed time: ', time.time() - __now__
    return doc_dict


def load_data(db, limit = None):
    """ (database) --> (list of lists)
    this file imports all important tables to memory in order to increase the process speed.

    """

    global table_all_documents, table_all_persons, table_all_persons_features, block_dict

    __now__ = time.time()
    # table_all_persons = load_table(db, 'all_persons', limit)
    t1 = threading.Thread(target=update_persons_table, args=(db, limit))
    t1.daemon = True
    t1.start()



    # print time.ctime(), " - Loading table all_persons_features."
    # table_all_persons_features = load_table(db, 'all_persons_features', limit)
    #
    # print time.ctime(), " - Loading table all_documents."
    # table_all_documents = load_table(db, 'all_documents', limit)
    # t2 = threading.Thread(target=load_table, args = (db,'all_documents', limit))
    # t2.daemon = True
    # t2.start()

    # print time.ctime(), " - building block_dict."
    # block_dict = build_block_dict()


    # print time.ctime(), " - Elapsed time:", time.time() - __now__
    # print time.ctime(), " - Loading data completed."


def build_block_dict():

    blocks = {}
    for key_p in table_all_persons.keys():
        person = table_all_persons[key_p]
        block_id = int(person['block_id'])
        if blocks.get(block_id):
            blocks[block_id]['members'].append({'ref': person['id'],'doc': person['register_id']})
        else:
            blocks[block_id] = {'members' : [{'ref': person['id'],'doc': person['register_id']}]}

    return blocks

def load_table(db, table_name, limit = None):
    """ (db, string, integer) --> (list of lists)
    returns the a sql table as a python list of lists
    """

    rows_dict = {}
    if table_name == 'all_persons':
        # query = "select * from %s " % table_name
        the_query = "select id, first_name, prefix, last_name, block_key, block_id, date_1 as date, place_1 as place," \
                    " gender, role, register_id, register_type from all_persons_new"
        if limit:
            the_query += " limit %d" % limit
    if table_name == 'all_documents':
        # query = "select * from %s" % table_name
        the_query = "select id, type_text, date, `index`, municipality, concat(latitude,',', longitude) geocode," \
                    " reference_ids from all_documents"
        if limit:
            the_query += " limit %d" % int(limit/3)

    cur = basic.run_query(db, the_query)
    desc = cur.description
    row_index = 1
    for row in cur.fetchall():
        row_dict = {}
        for index, value in enumerate(row):
            try:
                row_dict[desc[index][0]] = value.decode('ascii','ignore')
            except:
                row_dict[desc[index][0]] = value
        rows_dict[row_dict['id']] = row_dict


    return rows_dict
#
#
# def get_blocks_of_document(docuemnt_id):
#     """
#         returns the bag of blocks for a specific docuemnt
#     """
#     doc = myOrm.get_document(docuemnt_id)
#     if doc:
#
#         document_block_list = {}
#         for ref_id in doc['reference_ids'].split(','):
#             if document_block_list.get(docuemnt_id):
#                 document_block_list[docuemnt_id].append(myOrm.get_person(ref_id)['block_id'])
#             else:
#                 document_block_list[docuemnt_id] = myOrm.get_person(ref_id)['block_id']
#         return document_block_list
#     else:
#         return []

def main(limit=None):
    db = basic.do_connect()
    if limit:
        load_data(db,limit)
    else:
        load_data(db)


if __name__ == "__main__":
    pass