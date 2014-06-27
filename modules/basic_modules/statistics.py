from modules.basic_modules import myOrm, basic

__author__ = 'Bijan'

import time

def get_migration_list():
    """
        gets the migrations
    """

    query = "select id1, id2 from miss_matches"
    db = basic.do_connect()
    row_list = basic.run_query(query)
    index = 1
    t = time.time()
    csv_text = ''

    for row in row_list.fetchall():
        d1 = myOrm.get_document(row[0], db)
        d1_m = d1['municipality']
        d1_geo = d1['geocode']
        d1_year = d1['date'][-4:]
        d1_type = d1['type_text']

        d2 = myOrm.get_document(row[1], db)
        d2_m = d2['municipality']
        d2_geo = d2['geocode']
        d2_year = d2['date'][-4:]
        d2_type = d2['type_text']

        if d1_m != d2_m:
            if d1_year < d2_year:
                csv_text += d1_type + "," + d1_m +','+ d1_geo +','+ d1_year +','+ d2_m +','+ d2_geo +','+ d2_year + ',' + d2_type + '\n'
            else:
                csv_text += d2_type + "," + d2_m +','+ d2_geo +','+ d2_year +','+ d1_m +','+ d1_geo +','+ d1_year + ',' + d1_type + '\n'

            index += 1
            if not index % 1000:
                print index, time.time()-t
                t = time.time()
                with open("data/migrate.csv", "a") as myfile:
                    myfile.write(csv_text)
                csv_text = ''

    with open("data/migrate.csv", "a") as myfile:
        myfile.write(csv_text)


    print index

if __name__ == "__main__":
    get_migration_list()
