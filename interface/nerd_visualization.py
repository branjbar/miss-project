from modules.NERD.dict_based_nerd import Nerd
from modules.basic_modules import loadData
from modules.basic_modules.basic import run_query
from modules.basic_modules.myOrm import get_notarial_act, Document
from modules.record_linkage.hashing import generate_features, Hashing

__author__ = 'bijan'


def get_nerd_data(request, t_id):
    my_hash = Hashing()
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
        search_id = request.args.get('search_term')
        if search_id and search_id.isdigit():
            t_id = int(search_id)

    match_details = {}

    if not personal_text:
        ###### here we look for the first document with at least one relations extracted.

        counter = 0
        flag = False
        while not flag and counter < 1000:
            act = get_notarial_act(t_id, century18=True)
            text = act['text1'] + ' ' + act['text2'] + act['text3']
            nerd = Nerd(text)
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

        act = get_notarial_act(t_id, century18=True)

    else:
        act = {'text1': personal_text, 'text2': '', 'text3': '', 'id': -1, 'date': 0 - 0 - 0, 'place': 'bhic',
               'comment': 'personal text'}

    navbar_choices = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    if act:
        text = act['text1'] + ' ' + act['text2'] + act['text3']

        nerd = Nerd(text)
        # nerd.set_text(text)
        # nerd.pre_processing()
        # nerd.extract_names()
        text = {'text': nerd.word_list,
                'name_indexes': nerd.word_list_labeled,
                'row_id': t_id,
                'id': act['id'],
                'date': act['date'],
                'place': act['place'],
        }
        match_details['comment'] = act['comment']
        # navbar_choices = [i for i in xrange(int(act['row_id']), int(act['row_id']) + 10)]
        navbar_choices = [i for i in xrange(int(t_id), int(t_id) + 10)]

    else:
        text = None

    reference_pairs = []
    # to get rid of redundant references:
    reference_list = []
    for ref in nerd.get_references():
        # if ref[1] not in reference_list:
        reference_list.append(ref[1])
    name_alternatives = []
    for i in xrange(1, len(reference_list)):
        ref1 = reference_list[i - 1]
        ref2 = reference_list[i]
        index_key = generate_features(ref1.split(), ref2.split())
        solr_results = my_hash.search(index_key, 'cat:birth OR cat:marriage OR cat:death')
        name_alternative_tmp_1 = []
        name_alternative_tmp_2 = []
        if solr_results.results:
            html_list = []
            search_results = {}
            for result in solr_results.highlighting.iteritems():
                search_results[result[0]] = result[1]['features'][0].replace('<em>', '').replace('</em>', '')

                tmp_name = ' '.join(result[1]['features'][0].replace('<em>', '').replace('</em>', '').split('_')[0:2])
                if tmp_name not in name_alternative_tmp_1:
                    name_alternative_tmp_1.append(tmp_name)

                tmp_name = ' '.join(result[1]['features'][0].replace('<em>', '').replace('</em>', '').split('_')[2:])
                if tmp_name not in name_alternative_tmp_2:
                    name_alternative_tmp_2.append(tmp_name)

            for doc_id in search_results.keys():
                doc = Document()
                doc.set_id(doc_id)
                couple_names = ['_'.join(index_key.split('_')[:2]), '_'.join(index_key.split('_')[-2:])]
                html = doc.get_html(search_results[doc_id], couple_names)  # {year:....., html:.....}
                html_list.append(html)  # {year:....., html:.....}

            reference_pairs.append([ref1, ref2, solr_results.numFound, html_list])

            if len(name_alternative_tmp_1) > 1 and name_alternative_tmp_1 not in name_alternatives:
                name_alternatives.append(name_alternative_tmp_1)

            if len(name_alternative_tmp_2) > 1 and name_alternative_tmp_2 not in name_alternatives:
                name_alternatives.append(name_alternative_tmp_2)

    nerd_relationships = []
    # coloring the links:
    # green: pattern and civil, red: civil, black: pattern
    for index, rel1 in enumerate(nerd.get_relations()):
        if [rel1['ref1'][1], rel1['ref2'][1]] in [[rel2[0], rel2[1]] for rel2 in reference_pairs]:
            nerd_relationships.append(rel1)
            nerd_relationships[-1]['color'] = 'green'

    for index, rel1 in enumerate(nerd.get_relations()):
        if not [rel1['ref1'][1], rel1['ref2'][1]] in [[rel2[0], rel2[1]] for rel2 in reference_pairs]:
            nerd_relationships.append(rel1)
            nerd_relationships[-1]['color'] = 'black'

    for rel2 in reference_pairs:
        if [rel2[0], rel2[1]] not in [[rel1['ref1'][1], rel1['ref2'][1]] for rel1 in nerd.get_relations()]:
            nerd_relationships.append({'ref1': [0, rel2[0]],
                                       'color': 'red',
                                       'ref2': [0, rel2[1]],
                                       'relation': 'married with'})
    nerd_references = nerd.get_references()
    output = {'text': text,
              'match_details': match_details,
              'nerd_references': nerd_references,
              'navbar_choices': navbar_choices,
              'nerd_relationships': nerd_relationships,
              'reference_pairs': reference_pairs,
              'name_alternatives': name_alternatives}
    return output