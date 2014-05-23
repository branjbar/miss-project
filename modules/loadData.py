__author__ = 'Bijan'

from modules import basic
import time

table_all_documents = {}
table_all_persons = {}
table_all_persons_features = {}


def load_data(db, limit = None):
    """ (database) --> (list of lists)
    this file imports all important tables to memory in order to increase the process speed.

    """

    global table_all_documents, table_all_persons, table_all_persons_features

    __now__ = time.time()
    print time.ctime(), " - Loading table all_persons."
    table_all_persons = load_table(db, 'all_persons', limit)

    # print time.ctime(), " - Loading table all_persons_features."
    # table_all_persons_features = load_table(db, 'all_persons_features', limit)
    #
    print time.ctime(), " - Loading table all_documents."
    table_all_documents = load_table(db, 'all_documents', limit)

    print time.ctime(), " - Elapsed time:", time.time() - __now__
    print time.ctime(), " - Loading data completed."


def load_table(db, table_name, limit = None):
    """ (db, string, integer) --> (list of lists)
    returns the a sql table as a python list of lists
    """

    rows_dict = {}
    if table_name == 'all_persons':
        query = "select * from %s " % table_name

    if table_name == 'all_documents':
        query = "select * from %s" % table_name

    if limit:
        query += " limit %d" % limit

    cur = basic.run_query(db, query)
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
    # main()
    b_dict = {}
    blocking_index = 1

    q = "select id, block_id, block_key from all_persons_features"
    cur = basic.run_query(db, q)
    table = {}
    for c in cur.fetchall():
        table[c[0]] = {'block_id':c[1], 'block_key':c[2].decode('ascii','ignore')}

    print 'table imported'
    for key_p in table.keys():
        blocking_key = table[key_p]['block_key']
        if not b_dict.get(blocking_key):
            b_dict[blocking_key] = blocking_index
            blocking_index += 1

    query = ''
    index = 1
    for key_p in table.keys():
        blocking_key = table[key_p]['block_key']
        query += "update all_persons set block_key = '%s', block_id = %d where id = %d ;\n" % (blocking_key, b_dict[blocking_key],key_p)
        t = time.time()
        index += 1
        if index % 1000:
            with open("query.sql", "a") as myfile:
                myfile.write(query)
            query = ''
            index = 0
            # print time.time() - t
            # t = time.time()