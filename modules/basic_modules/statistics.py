import numpy

from modules.basic_modules import myOrm, basic
from modules.basic_modules.basic import string_compare
from modules.solr_search.hashing import Hashing


__author__ = 'Bijan'

import time

def get_migration_list():
    """
        gets the migrations
    """

    query = "select id1, id2 from miss_matches"
    row_list = basic.run_query(query)
    index = 1
    t = time.time()
    csv_text = ''

    for row in row_list.fetchall():
        d1 = myOrm.get_document(row[0])
        d1_m = d1['municipality']
        d1_geo = d1['geocode']
        d1_year = d1['date'][-4:]
        d1_type = d1['type_text']

        d2 = myOrm.get_document(row[1])
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


def indexing_stat_individual():
    """
    here the goal is to compute size of blocks based on full names
    """

    #  we block the records based on the person name
    query = "select first_name, last_name from all_persons_new"
    row_list = basic.run_query(query)
    count = 0
    indexing_dict = {}
    for row in row_list.fetchall():
        count += 1
        if not count%100:
            print count

        if row[0] and row[1]:
            first_name = row[0].split()[0]
            last_name = row[1].split()[0]
        full_name = first_name + '_' + last_name

        key_flag = False
        for key in indexing_dict.keys():
            if string_compare(full_name,key,'LEV') < 3:
                indexing_dict[key] += 1
                key_flag = True
                break
        if not key_flag:
            indexing_dict[full_name] = 1

    # print indexing_dict.values()
    with open("index_person", "a") as myfile:
        myfile.write(str(indexing_dict.values()))


def indexing_stat_couple():
    """
    here the goal is to compute size of blocks based on couple names
    """

    # we block the records based on the couple names
    query = "select type_number, reference_ids from all_documents"
    row_list = basic.run_query(query)
    indexing_dict = {}
    count = 0
    for row in row_list.fetchall():
        count += 1
        if not count%100:
            print count
        type_number = row[0]
        reference_ids = row[1].split(',')

        if type_number == '1':
            new_query = ["select first_name, last_name from all_persons_new where id = " + reference_ids[1] + ' or id = ' + reference_ids[2]]

        if type_number == '2':
            new_query = ["select first_name, last_name from all_persons_new where id = " + reference_ids[0] + ' or id = ' + reference_ids[1]]
            new_query += ["select first_name, last_name from all_persons_new where id = " + reference_ids[2] + ' or id = ' + reference_ids[3]]
            new_query += ["select first_name, last_name from all_persons_new where id = " + reference_ids[4] + ' or id = ' + reference_ids[5]]

        if type_number == '3':
            new_query = ["select first_name, last_name from all_persons_new where id = " + reference_ids[0] + ' or id = ' + reference_ids[3]]
            new_query += ["select first_name, last_name from all_persons_new where id = " + reference_ids[1] + ' or id = ' + reference_ids[2]]

        for q in new_query:
            row_list = basic.run_query(q)
            results = row_list.fetchall()
            first_name_0 = results[0][0]
            last_name_0 = results[0][1]
            first_name_1 = results[1][0]
            last_name_1 = results[1][1]
            if first_name_0 and last_name_0 and first_name_1 and last_name_1:
                first_name_0 = first_name_0.split()[0]
                first_name_1 = first_name_1.split()[0]
                last_name_0 = last_name_0.split()[0]
                last_name_1 = last_name_1.split()[0]
                name0 = first_name_0 + '_' + last_name_0
                name1 = first_name_1 + '_' + last_name_1
                names = sorted([name0, name1])

                full_name = names[0] + '_' + names[1]

                key_flag = False
                for key in indexing_dict.keys():
                    if string_compare(full_name,key,'LEV') < 3:
                        indexing_dict[key] += 1
                        key_flag = True
                        break
                if not key_flag:
                    indexing_dict[full_name] = 1

    # print indexing_dict.values()
    with open("index_couple", "a") as myfile:
        myfile.write(str(indexing_dict.values()))



def get_couple_pairs():
    """
    here first we extract all the couple names from the Solr list. Then, we

    :return:
    """
    my_hash = Hashing()

    solr_results = my_hash.search('*', 'cat:death or cat:birth or cat:marriage', facet_limit=-1)
    facet_fields = solr_results.facet_counts['facet_fields']
    facets = sorted(facet_fields['features_ss'].iteritems(), key=lambda x: x[1], reverse=True)
    with open("facet_couple_name.csv", "a") as myfile:
        myfile.write(str(facets))
    num_found_list = []
    from random import shuffle
    shuffle(facets)
    print 'getting statistics started'
    for index, f in enumerate(facets):

        num_found_list.append(my_hash.search(f[0], 'cat:death or cat:birth or cat:marriage',facet_limit=0).numFound)
        x = numpy.histogram(num_found_list, bins=100)
        if not index % 100:
            print index, ' out of ', len(facets)
            print list(x[0])
            print list(x[1])

    #
    #     index += 1
    #     if not index % 1000:
    #         print index, time.time()-t
    #         t = time.time()
    #         with open("data/migrate.csv", "a") as myfile:
    #             myfile.write(csv_text)
    #         csv_text = ''
    #
    # with open("data/migrate.csv", "a") as myfile:
    #     myfile.write(csv_text)

if __name__ == "__main__":
    get_couple_pairs()
