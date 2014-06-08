import pickle
from modules.basic_modules import basic
from modules.basic_modules.basic import log

"""
In this code we develop a complete matching technique for KDD conference which works as following:
For each two name references r1 and r2 in the same block, we compute their similarity as Sim_nc(r1,r2) + Sim_dc(r1,r2)
"""


# get block references and confidences for all with size less than 100 and store the results in dictionary
def import_block_and_reference_dicts(from_file=True):
    """
    generates block, reference and documents details required for matching
    """
    global block_dict, reference_dict, document_dict

    if not from_file:

        log("import blocks started")

        block_query = " SELECT id, first_name, last_name, block_key, block_id, register_id, register_type" \
                      " FROM links_based.all_persons_new "

        db = basic.do_connect()
        cur = basic.run_query(db, block_query)
        count = 0
        block_dict = {}
        reference_dict = {}
        document_dict = {}
        for row in cur.fetchall()[:10000]:
            ref_id = row[0]
            first_name = row[1]
            last_name = row[2]
            block_key = row[3]
            block_id = row[4]
            register_id = row[5]
            register_type = row[6]

            # add name and block to reference dictionary
            reference_dict[ref_id] = [first_name, last_name, block_id, register_id, register_type]

            # add the reference to block dictionary
            if not block_dict.get(block_id):
                block_dict[block_id] = [block_key, [ref_id], 1]
            else:
                block_dict[block_id][1].append(ref_id)
                block_dict[block_id][2] += 1

            # add block to reference to document dict
            if not document_dict.get(register_id):
                document_dict[register_id] = {'references': [ref_id],
                                              'blocks': [block_id],
                                              'type': register_type,
                                              }
            else:
                document_dict[register_id]['references'].append(ref_id)
                document_dict[register_id]['blocks'].append(block_id)

            count += 1
            if not count % 1000:
                print count / 1000

        log("import blocks ended.")

        with open('../../data/matching_kdd/import_data_10000.txt', 'w') as f:
            pickle.dump([block_dict, reference_dict, document_dict], f)

        log("dumping blocks ended.")
    else:
        print "--importing data."
        with open('../../data/matching_kdd/import_data_10000.txt', 'r') as f:
            block_dict, reference_dict, document_dict = pickle.load(f)


def get_similarity(reference_1, reference_2):
    """
    compute similarity between two references first based on name similarity and then based on document context.
    """

    refe
    sim_nc = 1


# parse through all blocks, and for each reference pairs in each block check the similarity



def main():

    import_block_and_reference_dicts(True)

if __name__ == "__main__":
    main()

