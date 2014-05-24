__author__ = 'Bijan'

from modules import basic
from modules import loadData

def refresh_person_id(db):
    """
        this module copies all the references in a new table with modified ids sorted based on documents ids.
    """

    q = "select id, register_id from all_persons"
    cur = basic.run_query(db, q)
    register_dict = {}
    for c in cur.fetchall():
        if not register_dict.get(int(c[1])):
            register_dict[int(c[1])] = [int(c[0])]
        else:
            register_dict[int(c[1])].append(int(c[0]))

    print 'table imported'
    index = 0
    query = ''
    register_dict = sorted(register_dict.items(), key=lambda s: s[0])
    print register_dict[:10]
    for key in register_dict:
        s = ''
        for ref in key[1]:
            index += 1
            if index > 2387327:
                query += "insert into all_persons_new select %d id, id id_old, first_name, prefix, last_name, block_key," \
                         " block_id, date_1, place_1, date_2, place_2, gender, role, register_id, register_type " \
                         "from all_persons where id = %d;\n" % (index, ref)
            s += str(index) + ','
        if index > 2387320:
            query += "update all_documents set reference_ids = '%s' where id = %d;\n" % (s[:-1], key[0])

        if not index % 10000:
            with open("query.sql", "a") as myfile:
                myfile.write(query)
            query = ''
            print index
    with open("query.sql", "a") as myfile:
        myfile.write(query)
    query = ''
    print index

def referesh_register_id(db):
    q = "select id, register_id from all_persons_new"
    cur = basic.run_query(db, q)
    register_dict = {}
    for c in cur.fetchall():
        if not register_dict.get(c[1]):
            register_dict[c[1]] = str(c[0])
        else:
            register_dict[c[1]] += ',' + str(c[0])

    print 'table imported'
    index = 0
    query = ''
    # register_dict = sorted(register_dict.items(), key=lambda s: s[0])
    for key in register_dict:
        index += 1
        query += "update all_documents set reference_ids = '%s' where id = %s;\n" % (register_dict[key], key)
        if not index % 1000:
            with open("query2.sql", "a") as myfile:
                myfile.write(query)
            query = ''
    with open("query2.sql", "a") as myfile:
        myfile.write(query)
    query = ''
    print index
