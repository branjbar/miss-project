__author__ = 'Bijan'
"""
    here the idea is to get a person id, and generating the complete pedegree, assuming there is just one root with
    two parents and those have each two parents, and so on so forth
"""

from modules import loadData
import random

def pedigree(document):
    """ (int) --> json dict
    """

    tree = {}
    if document:
        person_id_list = document['reference_ids'].split(',')
        index = 0
        for person_id in person_id_list:
            person = loadData.table_all_persons.get(int(person_id))
            if person:
                tree_temp = {
                    "fname": person['first_name'],
                    "lname": (person['prefix'] + ' ' + person['last_name']).strip().replace('  ' , ' '),
                    "date": person['date'][-4:],
                    "location": person['place'][:20],
                    "register_id": person['register_id'],
                    "register_type": person['register_type'],
                    "id": person['id'],
                    "parents": []
                }

                index += 1
                tree[index] = []
                tree[index].append(tree_temp)


        # return tree
    # tree = {"1": [{"born": "06-05-1837", "location": "Zeelst", "name": "Adriana Kuijk", "parents":[]}], "2": [{"born": "06-05-1837", "location": "Zeelst", "name": "Christiaan Kuijk", "parents":[]}], "3": [{"born": "06-05-1837", "location": "Zeelst", "name": "Helena Asten", "parents":[]}]}
  #   tree = {
  # "name": "Clifford Shanks",
  # "born": 1862,
  # "married": 1880,
  # "died": 1906,
  # "location": "Petersburg, VA",
  # "parents": []}
    return get_tree(tree)

def get_tree(sudo_tree):

    tree = {}
    if sudo_tree and sudo_tree.get(1) and sudo_tree.get(2) and sudo_tree.get(3) and not sudo_tree.get(4):
        tree = sudo_tree[1][0]
        tree['parents'].append(sudo_tree[2][0])
        tree['parents'].append(sudo_tree[3][0])

    if sudo_tree and sudo_tree.get(1) and sudo_tree.get(2) and sudo_tree.get(3) and sudo_tree.get(4) and not sudo_tree.get(5):
        tree = {"fname": "","lname": "",
                    "date": '',
                    "location": '',
                    "register_id": '',
                    "register_type": '',
                    "id": '',
                    'parents': []
        }
        tree['parents'].append(sudo_tree[1][0])
        tree['parents'].append(sudo_tree[4][0])
        tree['parents'][0]['parents'] = []
        tree['parents'][0]['parents'].append(sudo_tree[2][0])
        tree['parents'][0]['parents'].append(sudo_tree[3][0])

    if sudo_tree and sudo_tree.get(1) and sudo_tree.get(2) and sudo_tree.get(3) and sudo_tree.get(4) and sudo_tree.get(5):
        tree = {"fname": "","lname": "",
                    "date": '',
                    "location": '',
                    "register_id": '',
                    "register_type": '',
                    "id": '',
                    'parents': []
        }
        tree['parents'].append(sudo_tree[1][0])
        tree['parents'].append(sudo_tree[2][0])
        tree['parents'][0]['parents'] = []
        tree['parents'][0]['parents'].append(sudo_tree[3][0])
        tree['parents'][0]['parents'].append(sudo_tree[4][0])
        tree['parents'][1]['parents'] = []
        tree['parents'][1]['parents'].append(sudo_tree[5][0])
        tree['parents'][1]['parents'].append(sudo_tree[6][0])


    return tree

if __name__ == "__main__":
    print pedigree()