__author__ = 'Bijan'

STANDARD_QUERY = "SELECT id, first_name, last_name, date_1, place_1, gender, role, register_id, register_type \
          FROM all_persons WHERE "


from modules import basic


def row_to_reference(db, row, table="all_persons"):
    ''' (list, table) -> (dict)
    adds labels to different elements of the list, according to the table type,
    and makes a reference
    '''

    if table == 'all_persons':
        # first get the geocode:
        place = row[4]
        if place:
            query = 'select latitude, longitude from geocode where municipality = "' + place + '"'
            cur = basic.run_query(db, query) # fetch the person with the the random id
            geocode = cur.fetchone()
        else:
            geocode = None

        ref = {}
        ref['id'] = row[0]
        ref['first_name'] = row[1].decode('ascii','ignore')
        ref['last_name'] = row[2].decode('ascii','ignore')
        ref['year'] = row[3][6:12]
        ref['place'] = geocode
        ref['gender'] = row[5]
        # if not row[5] or not (row[5] == "male" or row[5] == "female"):
        #     ref['gender'] = basic.estimate_gender(db, row[1])

        ref['role'] = row[6]
        ref['register_id'] = row[7]
        ref['register_type'] = row[8]

        return ref

    if table == 'all_documents':
        ref = {}
        key_dict = {0:'id', 1: 'type_number', 2: 'archive', 3: 'type_text', 4: 'date', 5: 'index',
         6: 'municipality', 7: 'latitude', 8: 'longitude', 9: 'access no.', 10: 'inventory no.', 11: "reference_ids"}
        for key in key_dict.keys():
            ref[key_dict[key]] = row[key]

        return ref

    if table == 'blocks':
        ref = {}
        key_dict = {0: 'id', 1: 'block_key', 2: 'block_size', 3: 'components'}

        for key in key_dict.keys():
            ref[key_dict[key]] = row[key]
        return ref

    if table == 'links':
        ref = {}
        key_dict = {0: 'type', 1: 'id1', 2: 'id2', 3: 'role1', 4: 'role2', 5: 'id'}

        for key in key_dict.keys():
            ref[key_dict[key]] = row[key]
        return ref



def get_person(db, person_id = None):
    ''' (db, integer) -> (dict)
    return a person with the id
    '''

    # if no id then find a random person
    if person_id:
        cur = basic.run_query(db, STANDARD_QUERY + ' id = ' + str(person_id)) # fetch the person with the the random id
        row = cur.fetchone()
        reference = {}
        if row:
            reference = row_to_reference(db, row)
        return reference

    if not person_id:
        flag = False  # this flag is used to be sure we get a valid person (i.e., has at least name)
        while not flag:

            # generate a random number
            from random import randrange
            person_id = randrange(1,5244863)

            cur = basic.run_query(db, STANDARD_QUERY + ' id = ' + str(person_id)) # fetch the person with the the random id
            reference = row_to_reference(db, cur.fetchone())
            if reference['first_name'] or reference['last_name']:
                flag = True # if the person has name, then flag is toggled
        return reference


def get_document(db, document_id = None):
    ''' (db, integer) -> (dict)
    return a document with the id
    '''
    # if no id then find a random person
    if document_id:
        document_query = "SELECT all_documents.id, type_number, archive, type_text, date, `index`, province, " \
                     "municipality, latitude, `access no.`, `inventory no.`, group_concat(all_persons.id SEPARATOR ', ') " \
                     "FROM all_documents join all_persons where all_documents.id = " \
                      + str(document_id) + " and all_documents.id = all_persons.register_id "

        cur = basic.run_query(db, document_query)
        row = cur.fetchone()
        if row:
            reference = row_to_reference(db, row, "all_documents")
        else:
            reference = {}

        return reference

    if not document_id:
        flag = False  # this flag is used to be sure we get a valid person (i.e., has at least name)
        while not flag:

            # generate a random number
            from random import randrange
            document_id = randrange(2846095,23729952)

            document_query = "SELECT all_documents.id, type_number, archive, type_text, date, `index`, province, " \
                         "municipality, latitude, `access no.`, `inventory no.`, group_concat(all_persons.id SEPARATOR ', ') " \
                         "FROM all_documents join all_persons where all_documents.id = " \
                          + str(document_id) + " and all_documents.id = all_persons.register_id "


            cur = basic.run_query(db, document_query)
            row = cur.fetchone()

            if row[0]:
                flag = True # if the person has name, then flag is toggled
        reference = row_to_reference(db, row, "all_documents")
        return reference


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

def get_relatives(db, person_id):
    """
     uses the 'relations' table in order to extract the id of all relatives of person_id
    """
    relatives_id = []
    if person_id:
        relative_query = 'select ref2, relation_type from relations where ref1 = ' + str(person_id)
        cur = basic.run_query(db, relative_query)
        rows = cur.fetchall()
        if rows:
            for row in rows:
                relatives_id.append([row[0],row[1]])

    return relatives_id

if __name__ == "__main__":
    db = basic.do_connect()
    print get_block(db, 100)

