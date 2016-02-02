import random


from modules.NERD import dict_based_nerd
from modules.basic_modules import loadData
from modules.basic_modules.basic import run_query
from modules.basic_modules.myOrm import get_notarial_act, Document, NOTARY_OFFSET
from modules.solr_search.hashing import generate_features  # I'm getting erros here! Probably the notary offset should be somewhere else.
from modules.solr_search.solr_query import SolrQuery


__author__ = 'bijan'


def get_nerd_data(request, t_id):
    my_hash = SolrQuery()
    if request.args.get('confirm'):
        opinion = request.args.get('confirm')
        comment = request.args.get('comment').replace("'", "").replace('"', '"')
        if opinion == "True":
            query = "update notary_acts set eval=1, comment='%s' where row_id=%s" % (comment, t_id)
            loadData.table_notarial_acts[int(t_id)]['eval'] = 1
            loadData.table_notarial_acts[int(t_id)]['comment'] = comment
        else:
            query = "update notary_acts set eval=0, comment='%s' where row_id=%s" % (comment, t_id)
            loadData.table_notarial_acts[int(t_id)]['eval'] = 0
            loadData.table_notarial_acts[int(t_id)]['comment'] = comment
        run_query(query)
        t_id = int(t_id)
        t_id += 1

    else:

        personal_text = request.args.get('personalText')
        if request.args.get('lucky'):
            search_id = str(random.randint(0, 20000))
        else:
            search_id = request.args.get('search_term')

        if search_id and search_id.isdigit():
            t_id = int(search_id)

    match_details = {}

    if not personal_text:
        # here we look for the first document with at least one relations extracted.

        counter = 0
        flag = False
        t_id = int(t_id)
        if t_id > NOTARY_OFFSET:
            t_id -= NOTARY_OFFSET
            century18 = False
            act = get_notarial_act(t_id, century18)
            text = act['text1'] + ' ' + act['text2'] + act['text3']
            nerd = dict_based_nerd.Nerd(text)
            reference_list = []
            for ref in nerd.get_references():
                if ref[1] not in reference_list:
                    reference_list.append(ref[1])

            for i in xrange(1, len(reference_list)):
                ref1 = reference_list[i - 1]
                ref2 = reference_list[i]

                index_key = generate_features(ref1.split(), ref2.split())
                solr_results = my_hash.search(index_key, 'cat:birth OR cat:marriage OR cat:death')
                if solr_results.results:
                    flag = True
                    t_id = int(t_id) - 1
                    break

        else:
            century18 = True
            while not flag and counter < 1000:
                # to understand whether someone is searching for a specific notarial act or is just wandering around!

                act = get_notarial_act(t_id, century18)
                text = act['text1'] + ' ' + act['text2'] + act['text3']
                nerd = dict_based_nerd.Nerd(text)
                reference_list = []
                for ref in nerd.get_references():
                    if ref[1] not in reference_list:
                        reference_list.append(ref[1])

                for i in xrange(1, len(reference_list)):
                    ref1 = reference_list[i - 1]
                    ref2 = reference_list[i]

                    index_key = generate_features(ref1.split(), ref2.split())
                    solr_results = my_hash.search(index_key, 'cat:birth OR cat:marriage OR cat:death')
                    if solr_results.results:
                        flag = True
                        t_id = int(t_id) - 1
                        break
                t_id = int(t_id) + 1

                ######

            act = get_notarial_act(t_id, century18)

    else:
        act = {'text1': personal_text, 'text2': '', 'text3': '', 'id': -1, 'date': 0 - 0 - 0, 'place': 'bhic',
               'comment': 'personal text'}

    navbar_choices = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    if act:
        text = act['text1'] + ' ' + act['text2'] + act['text3']

        nerd = dict_based_nerd.Nerd(text)
        text = {'text': nerd.word_list,
                'name_indexes': nerd.word_list_labeled,
                'row_id': t_id,
                'id': act['id'],
                'date': act['date'],
                'place': act['place'],
        }
        match_details['comment'] = act['comment']
        navbar_choices = [i for i in xrange(int(t_id), int(t_id) + 10)]

    else:
        text = None

    nerd.extract_relations()
    nerd.extract_solr_relations()

    nerd_relationships = nerd.get_relations()
    for index, rel in enumerate(nerd_relationships):
        html_list = []
        for doc_dict in rel["html"]:
            doc = Document()
            doc.set_id(doc_dict["id"])
            html = doc.get_html(doc_dict.get("search_results", []), doc_dict.get("couple_names"))
            html_list.append(html)
        nerd_relationships[index]["html"] = html_list

    nerd_references = nerd.get_references()
    name_alternatives = nerd.get_name_alternatives()
    output = {'text': text,
              'match_details': match_details,
              'nerd_references': nerd_references,
              'navbar_choices': navbar_choices,
              'nerd_relationships': nerd_relationships,
              'name_alternatives': name_alternatives}
    return output