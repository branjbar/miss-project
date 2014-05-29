__author__ = 'Bijan'

import time, pickle


from modules.basic_modules import basic


parent_graph = {} # to store the graph
links_matches = {} # to store the matches


def find_deep_families(load_from_file=False, depth=4):
    """
    uses links data to find the deepest trees which are there
    each link is in form of row = [a	12829450	12830097	1	2]

    """
    if load_from_file:
        global parent_graph, links_matches

        db = basic.do_connect()
        link_query = "Select * from links"
        cur = basic.run_query(db, link_query)
        for row in cur.fetchall():
            if row[2] and int(row[3]) == 1 and (int(row[4]) == 2 or int(row[4]) == 3):

                # add the new edge to parent
                links_matches[str(row[1]) + '_' + str(row[2])] = [row[0],row[3],row[4]]
                if parent_graph.get(row[2]):
                    parent_graph[row[2]].append(row[1])
                else:
                    parent_graph[row[2]] = [row[1]]


        with open('../data/links_matches.txt', 'w') as f:
            pickle.dump([parent_graph,links_matches], f)

    print "--importing data."
    with open('../data/links_matches.txt', 'r') as f:
        parent_graph, links_matches = pickle.load(f)


    t = time.time()

    if depth == 3:
        print "--extracting matches of depth 3"

        for child1 in parent_graph.keys():

            doc_tree_list = get_doc_parents(child1)
            if doc_tree_list:
                csv_text = ''.join([ str(d) + ',' for d in doc_tree_list]) + '\n'

                if csv_text:
                    with open("../data/family_depth_3.csv", "a") as myfile:
                        myfile.write(csv_text)

    if depth == 5:
        for child1 in parent_graph.keys():

            doc_tree_list1 = get_doc_parents(child1)
            if doc_tree_list1:
                doc_tree_list21 = get_doc_parents(doc_tree_list1[1])
                if doc_tree_list21:
                    doc_tree_list22 = get_doc_parents(doc_tree_list21[1])
                    doc_tree_list23 = get_doc_parents(doc_tree_list21[2])


                doc_tree_list31 = get_doc_parents(doc_tree_list1[2])
                if doc_tree_list31:
                    doc_tree_list32 = get_doc_parents(doc_tree_list31[1])
                    doc_tree_list33 = get_doc_parents(doc_tree_list31[2])

                if doc_tree_list1 and \
                        doc_tree_list21 and doc_tree_list31 \
                        and doc_tree_list22 and doc_tree_list23 and\
                        doc_tree_list32 and doc_tree_list33:
                    csv_text = ''.join([ str(d) + ',' for d in doc_tree_list1 + doc_tree_list21 + doc_tree_list22 + doc_tree_list23 +
                                                               doc_tree_list31 + doc_tree_list32 + doc_tree_list33]) + '\n'

                    if csv_text:
                        with open("../data/family_depth_5.csv", "a") as myfile:
                            myfile.write(csv_text)

    if depth == 4:
        for child1 in parent_graph.keys():

            doc_tree_list1 = get_doc_parents(child1)
            if doc_tree_list1:
                doc_tree_list2 = get_doc_parents(doc_tree_list1[1])
                doc_tree_list3 = get_doc_parents(doc_tree_list1[2])

                if doc_tree_list1 and doc_tree_list2 and doc_tree_list3:
                    csv_text = ''.join([ str(d) + ',' for d in doc_tree_list1 + doc_tree_list2 + doc_tree_list3]) + '\n'

                    if csv_text:
                        with open("../data/family_depth_4.csv", "a") as myfile:
                            myfile.write(csv_text)


        #
        # for child2 in parent.keys():
        #     if child1 != child2:
        #         print child1, parent[child1], parent[child2]




    print time.time() - t


def get_doc_parents(child_doc, depth=3):
    """ (doc_id) --> [doc_id, parent_id1, parent_id2]

    """
    global parent_graph

    if depth == 3:
        parents = parent_graph.get(child_doc)
        if parents and len(parents) == 2:
            role_1 = links_matches[str(parents[0]) + '_' + str(child_doc)][2]
            role_2 = links_matches[str(parents[1]) + '_' + str(child_doc)][2]

            if role_1 == 2 and role_2 == 3:
                return [child_doc, parents[0], parents[1]]

            if role_1 == 3 and role_2 == 2:
                return [child_doc, parents[1], parents[0]]

    return []


def main():
    find_deep_families(False, 5)


if __name__ == "__main__":
    main()