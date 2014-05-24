__author__ = 'Bijan'

from modules import basic
import time
import threading

table_all_documents = {}
table_all_persons = {}
block_dict = {}


def update_persons_table(db, limit):
    global table_all_persons, block_dict
    __now__ = time.time()

    type = limit[1]
    lim = limit[0]

    print time.ctime(), " - Loading table all_persons."

    the_query = "select id, first_name, prefix, last_name, block_key, block_id, date_1 as date, place_1 as place," \
                " gender, role, register_id, register_type from all_persons_new"
    if type:
        the_query += " where register_type = '%s'" % type

    if lim:
        the_query += " limit %d" % lim


    cur = basic.run_query(db, the_query)
    desc = cur.description

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

    print time.ctime(), " - table all_persons imported in ", time.time() - __now__

    __now__ = time.time()
    print time.ctime(), " - building block_dict."

    block_dict = build_block_dict()

    print time.ctime(), " - building block_dict is imported in", time.time() - __now__

def update_documents_table(db, limit):
    global table_all_documents
    __now__ = time.time()

    type = limit[1]
    lim = limit[0]

    print time.ctime(), " - Loading table all_documents."

    the_query = "select id, type_text, date, `index`, municipality, concat(latitude,',', longitude) geocode," \
                " reference_ids from all_documents"
    if type:
        the_query += " where type_text = '%s'" % type

    if lim:
        the_query += " limit %d" % int(lim / 6)


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

    print time.ctime() , " - table all_documents imported in ", time.time() - __now__


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
            blocks[block_id]['members'].append(person['id'])
        else:
            blocks[block_id] = {'members' : [person['id']]}

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


def main(limit=None):
    db = basic.do_connect()
    if limit:
        load_data(db,limit)
    else:
        load_data(db)


if __name__ == "__main__":

    db = basic.do_connect()
    from modules import dataManipulation
    dataManipulation.refresh_person_id(db)
    # dataManipulation.referesh_register_id(db)