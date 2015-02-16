from flask import request
from flask import render_template

from modules.NERD.nerd_visualization import get_nerd_data
from modules.basic_modules import basic, loadData, myOrm, generatePedigree
from interface import app



# TODO: designing a nice homepage, with nice pictures and shortcuts to
# TODO: designing a simple, but fabulous search engine.
from modules.basic_modules.myOrm import Reference, Document
from modules.basic_modules.treeStructure import TreeStructure
from modules.record_linkage.hashing import Hashing, generate_features

# new_blocks = pickle.load(open("matches_notary_civil.p", "r"))

# try:
# story_file = open('../data/good_stories.txt', 'r')
# except:
# story_file = open('data/good_stories.txt', 'r')

# lucky_stories = []
# line = story_file.readline()
# while line:
# lucky_stories.append(line.split()[1])
# line = story_file.readline()


# pickle.dump(hash_table, open("hashing_v1.p", 'w'))


my_hash = Hashing()


def recursive_search(search_results, new_search_term_list):
    solr_results_list = []
    for doc_id in search_results.keys():
        doc = Document()
        doc.set_id(doc_id)
        for couple in doc.get_couples():
            name1 = couple[0]
            name2 = couple[1]
            if len(name1) > 2 and len(name2) > 2:
                search_term = generate_features(name1.split(), name2.split())
                if search_term not in new_search_term_list:
                    new_search_term_list.append(search_term)
                    solr_results_list.append(my_hash.search(search_term, ''))

    for solr_result in solr_results_list:
        if solr_result:
            for result in solr_result.highlighting.iteritems():
                search_results[result[0]] = result[1]['features'][0].replace('<em>', '').replace('</em>', '')

    return new_search_term_list, search_results


def routing():
    @app.route('/search/', methods=['GET', 'POST'])
    def searching_intel():

        search_term_1 = "Adriaan_Made_Lijntje_Timmers"
        # search_term_1 = "Jacobus_Sneep_Stijntje_Made"
        # search_term_1 = "Maria_Verheijen_Peter_Keukens"
        # search_term_1 = "Anna_Senders_Gerardus_Greef"
        solr_results_1 = my_hash.search(search_term_1, '')

        search_results = {}

        if solr_results_1:
            for result in solr_results_1.highlighting.iteritems():
                search_results[result[0]] = result[1]['features'][0].replace('<em>', '').replace('</em>', '')

        print 'step 1', len([]), ', ', len(search_results)
        new_search_term_list, search_results = recursive_search(search_results, [])
        print 'step 2', len(new_search_term_list), ', ', len(search_results)
        new_search_term_list, search_results = recursive_search(search_results, new_search_term_list)
        print 'step 3', len(new_search_term_list), ', ', len(search_results)
        new_search_term_list, search_results = recursive_search(search_results, new_search_term_list)
        print 'step 4', len(new_search_term_list), ', ', len(search_results)
        # new_search_term_list, search_results = recursive_search(search_results, new_search_term_list)
        # print 'step 5', len(new_search_term_list), ', ', len(search_results)
        # new_search_term_list, search_results = recursive_search(search_results, new_search_term_list)
        # print 'step 6', len(new_search_term_list), ', ', len(search_results)

        tree = TreeStructure()

        if search_results:

            for doc_id in search_results.keys():
                doc = Document()
                doc.set_id(doc_id)
                new_data = doc.get_relatives(search_results[doc_id], [])
                for leaf in new_data['leaves']:
                    tree.add_leaf(leaf)
                for branch in new_data['branches']:
                    tree.add_branch(branch)

        tree.update()

        return render_template('search_page.html', dataset=tree.get_dict())


    @app.route('/hash_matches/', methods=['GET', 'POST'])
    @app.route('/hash_matches/<p_id>', methods=['GET', 'POST'])
    def hash_matches(p_id=None):
        search_term = request.args.get('search_term')  # the main searching term
        field_query = request.args.get('field_query')  # the field query from previous sessions
        facet_query = request.args.get('fq')  # the new facet query coming from this session
        m_query = request.args.get('mq')  # the main query which likes to replace the search query

        lucky = request.args.get('lucky')
        if lucky:
            search_term = '*'

        # user_query = "Antonie_Biggelaar & Geertruida Bekkers"
        doc_list = []
        search_results = {}
        html_year = []
        couple_names = []
        facets = {}

        if m_query:
            search_term = ''
            field_query = m_query

        if not search_term:
            search_term = '*'

        if not field_query:
            field_query = ''
        else:
            field_query += ' -'
            field_query.replace(' - -', ' -')

        # here we manage the features_ss facet
        if facet_query and facet_query.split(':')[0] == 'features_ss':
            if not search_term or search_term == '*':
                search_term = facet_query.split(':')[1].replace(' - ', '_').replace(' ', '_').replace('__', '_')
            else:
                field_query += 'features_ss: ' + facet_query.split(':')[1].replace(' - ', '_').replace(' ',
                                                                                                       '_').replace(
                    '__', '_')

        # here we manage the location facet
        if facet_query and facet_query.split(':')[0] == 'location_s':
            field_query += 'location_s: ' + '"' + facet_query.split(':')[1].replace('+', ' ') + '"'

        if facet_query and facet_query.split(':')[0] == 'date':
            field_query += 'date_dt: ' + '[' + facet_query.split(':')[1].split('-')[0] + '-00-00T00:00:00Z TO ' + \
                           str(int(facet_query.split(':')[1].split('-')[1]) + 1) + '-00-00T00:00:00Z ]'

        if facet_query and facet_query.split(':')[0] == 'cat':
            field_query += 'cat: ' + '"' + facet_query.split(':')[1].replace('+', ' ') + '"'

        search_term = ' '.join(search_term.split('_'))
        search_term = search_term.replace('&', '').replace('-', '').replace('  ', ' ')
        ref1 = ' '.join(search_term.split()[:2])
        ref2 = ' '.join(search_term.split()[-2:])

        search_term = generate_features(ref1.split(), ref2.split())
        solr_results = my_hash.search(search_term, field_query)

        if solr_results:
            # first let's get the facets from results
            facet_fields = solr_results.facet_counts['facet_fields']
            for key in facet_fields:
                facets[key] = sorted(facet_fields[key].iteritems(), key=lambda x: x[1], reverse=True)[:20]

            # polishing the feature_ss with removing the underline and adding &
            for index, value in enumerate(facets['features_ss']):
                facets['features_ss'][index] = [
                    value[0].replace('_', ' ', 1).replace('_', ' - ', 1).replace('_', ' '), value[1]]

            # adding the date range to the facets
            facets['date'] = []
            facet_ranges = solr_results.facet_counts['facet_ranges']['date_dt']['counts']
            for x in sorted(facet_ranges.items(), key=lambda s: s[0]):
                facets['date'].append([x[0][:4] + '-' + str(int(x[0][:4]) + 10), x[1]])

            # now we get the main results and highlights
            search_results = {}

            if len(search_term.split('_')) == 4:
                couple_names = ['_'.join(search_term.split('_')[:2]), '_'.join(search_term.split('_')[-2:])]

            # here we simultaneously get the search results and highlights
            for result in solr_results.highlighting.iteritems():
                search_results[result[0]] = result[1]['features'][0].replace('<em>', '').replace('</em>', '')

        if search_results:
            doc_list = []
            html_year = []
            for doc_id in search_results.keys():
                doc = Document()
                doc.set_id(doc_id)
                html = doc.get_html(search_results[doc_id], couple_names)  # {year:....., html:.....}

                # TODO: Later we sort the html_year based on the years. For equal years we can think of reordering the card based on their type and roles!
                html_year.append(html)

                doc_list.append(html)

        html_year.sort(key=lambda x: x['year'])
        doc_list.sort(key=lambda x: x['year'])

        return render_template('hash_vis.html',
                               doc_list=doc_list,
                               search_term=search_term,
                               field_query=field_query,
                               couple_name=' - '.join(couple_names).replace('_', ' '),
                               found_results=len(search_results),
                               html_year=html_year,
                               facets=facets)


    @app.route('/complex_matches/', methods=['GET', 'POST'])
    @app.route('/complex_matches/<p_id>', methods=['GET', 'POST'])
    def complex_matches(p_id=None):
        search_id = request.args.get('search_term')
        if search_id and search_id.isdigit():
            p_id = int(search_id)

        if not p_id:
            p_id = 0

        p_id = int(p_id)
        if p_id < 0:
            p_id = 0

        block_key = new_blocks[p_id][0]
        block_list = new_blocks[p_id][1]

        doc_list = []
        doc_list_d3 = []
        for doc_id in block_list:
            doc = Document()
            doc.set_id(doc_id)
            doc_list_d3.append(doc.__dict_new__())
            html = doc.get_html(block_key, [block_key])
            # for key in block_key.split('_'):
            # html = html.replace(key, '<span class="highlight"> %s </span>'%key)
            doc_list.append(html)

            navbar_choices = []
            for a_match_id in range(p_id, p_id + 11):
                navbar_choices.append(a_match_id)

        return render_template('match_vis.html', doc_list_d3=doc_list_d3, doc_list=doc_list,
                               block_key=block_key.split('_'),
                               navbar_choices=navbar_choices)


    @app.route('/get_ref/<p_id>')
    @app.route('/get_ref/')
    def get_ref(p_id=None):
        if p_id:
            ref = Reference()
            ref.set_id(p_id)

            return str(ref)
        else:
            return 'error'


    @app.route('/get_doc/<p_id>')
    @app.route('/get_doc/')
    def get_doc(p_id=None):
        if p_id:
            doc = Document()
            doc.set_id(p_id)
            return str(doc.__dict_new__())
        else:
            return 'error'


    @app.route('/', methods=['GET', 'POST'])
    def home():
        return render_template('index.html', header="Welcome!"
                               , message="to MiSS Web Interface. Use the upper "
                                         "menu to proceed with data exploration. You "
                                         "can start with loading data!")


    @app.route('/person/', methods=['GET', 'POST'])
    @app.route('/person/<p_id>', methods=['GET', 'POST'])
    def person_page(p_id=None):
        # if gets an id, searches for a person with that id
        search_id = request.args.get('search_term')
        if search_id and search_id.isdigit():
            p_id = int(search_id)

        person = myOrm.get_person(p_id)
        if person:
            rel = {}
            relatives_id = myOrm.get_relatives(person['id'])

            for index, relative in enumerate(relatives_id):
                relative_person = myOrm.get_person(relative)

                if relative_person:
                    rel['Relative_' + str(index)] = relative_person

            document = loadData.table_all_documents.get(int(person['register_id']))
            json_dict = generatePedigree.pedigree(document, person['id'])
            return render_template('index.html', p=person, p2=rel, name='bijan', json_dict_h=json_dict)
        else:
            return render_template('index.html', message='No results found!', name='bijan')

    @app.route('/document/', methods=['GET', 'POST'])
    @app.route('/document/<p_id>', methods=['GET', 'POST'])
    def document_page(p_id=None):
        # if gets an id, searches for a document with that id
        search_id = request.args.get('search_term')
        if search_id and search_id.isdigit():
            p_id = int(search_id)

        document = myOrm.get_document(p_id)
        ref_dict = {}
        if document:
            for ref in document.get('reference_ids').split(','):
                ref_person = myOrm.get_person(ref)
                if ref_person:
                    ref_dict['Role' + str(ref_person['role'])] = ref_person

            json_dict = generatePedigree.pedigree(document)
            return render_template('index.html', p=document, p2=ref_dict, json_dict_h=json_dict, name='bijan')
        else:
            return render_template('index.html', message='No results found!', name='bijan')

    @app.route('/block/', methods=['GET', 'POST'])
    @app.route('/block/<p_id>', methods=['GET', 'POST'])
    def block_page(p_id=None):
        # if gets an id, searches for a document with that id
        search_id = request.args.get('search_term')
        if search_id and search_id.isdigit():
            p_id = int(search_id)

        block = myOrm.get_block(p_id)
        if block:
            return render_template('index.html', p=block, name='bijan')
        else:
            return render_template('index.html', message='No results found!', name='bijan')


    @app.route('/load_data/', methods=['GET', 'POST'])
    def load_data():

        message = ""
        header = "Data Setup"
        tables = {}

        if request.method == "GET":

            if request.args.get('clear'):
                loadData.table_all_persons = {}
                loadData.table_all_documents = {}
                loadData.block_dict = {}

            else:
                if request.args.get('limit'):
                    data_type = []
                    if request.args.get('birth'):
                        data_type.append('birth')
                    if request.args.get('marriage'):
                        data_type.append('marriage')
                    if request.args.get('death'):
                        data_type.append('death')
                    loadData.main([int(request.args.get('limit')), data_type, ''])
                    tables = {'data': 'loading'}

                else:
                    if not len(loadData.table_all_persons) and request.args.get('refresh'):
                        tables = {'data': 'loading'}
                    else:

                        tables = {'Persons': len(loadData.table_all_persons),
                                  'Matches': len(loadData.match_pairs),
                                  'Documents': len(loadData.table_all_documents), }

        return render_template('index.html', header=header, message=message, data=tables, name='bijan',
                               page_name='load_data')

    @app.route('/links_matches/', methods=['GET', 'POST'])
    @app.route('/links_matches/<p_id>', methods=['GET', 'POST'])
    def link_page(p_id=None):
        # if gets an id, searches for a document with that id
        search_id = request.args.get('search_term')
        if search_id and search_id.isdigit():
            p_id = int(search_id)
        if p_id and not p_id.isdigit():
            p_id = 0
        match = myOrm.get_links(p_id)

        doc1_id = int(match['id1'])
        doc2_id = int(match['id2'])
        if doc1_id and doc2_id:
            doc1 = myOrm.get_document(doc1_id)
            doc2 = myOrm.get_document(doc2_id)

            if doc1 and doc2:
                json_dict_1 = generatePedigree.pedigree(doc1, '', '', match['role1'])
                json_dict_2 = generatePedigree.pedigree(doc2, '', '', match['role2'])
                return render_template('index.html', doc1=doc1, doc2=doc2, match_details=match, json_dict_h=json_dict_1,
                                       json_dict_h2=json_dict_2, name='bijan', page_name='miss_matches')
        else:
            return render_template('index.html', message='No results found!', name='bijan', page_name='miss_matches')


    @app.route('/miss_matches/', methods=['GET', 'POST'])
    @app.route('/miss_matches/<p_id>', methods=['GET', 'POST'])
    def miss_page(p_id=None):

        if request.args.get('confirm'):
            opinion = request.args.get('confirm')
            comment = request.args.get('comment').replace("'", "").replace('"', '')
            rowid = myOrm.get_miss_matches(p_id)['id']
            if opinion == "True":
                comment = loadData.match_pairs[int(p_id)]['comment'] + ' - ' + str(comment)
                query = "update %s set eval=1, comment='%s' where id=%s" % (loadData.MATCH_TABLE, comment, rowid)
                loadData.match_pairs[int(p_id)]['eval'] = 1
                loadData.match_pairs[int(p_id)]['comment'] = comment
            else:
                comment = loadData.match_pairs[int(p_id)]['comment'] + ' - ' + str(comment)
                query = "update %s set eval=0, comment='%s' where id=%s" % (loadData.MATCH_TABLE, comment, rowid)
                loadData.match_pairs[int(p_id)]['eval'] = 0
                loadData.match_pairs[int(p_id)]['comment'] = comment

            p_id = int(p_id)
            p_id += 1
            basic.run_query(query)

        else:
            if request.args.get('search_term'):
                p_id = request.args.get('search_term')

            if not p_id:
                p_id = '0'

            if p_id == '0' or p_id:
                p_id = int(p_id)
                p_id = max(1, p_id)

        match = myOrm.get_miss_matches(p_id)

        if match:
            ref1 = match['ref1']
            ref2 = match['ref2']

            doc1 = myOrm.get_document(myOrm.get_person(ref1)['register_id'])
            doc2 = myOrm.get_document(myOrm.get_person(ref2)['register_id'])

            json_dict_1 = generatePedigree.pedigree(doc1, ref1, '')
            json_dict_2 = generatePedigree.pedigree(doc2, ref2, '')

            expert_hints = generatePedigree.examine_match_similarity(doc1, ref1, doc2, ref2)

            navbar_choices = []
            for a_match_id in range(int(match['index']), int(match['index']) + 11):
                a_match = myOrm.get_miss_matches(a_match_id)
                if a_match:
                    navbar_choices.append({'score': a_match['score'], 'index': a_match['index']})
            return render_template('index.html', doc1=doc1, doc2=doc2, match_details=match, json_dict_h=json_dict_1,
                                   json_dict_h2=json_dict_2, name='bijan', page_name='miss_matches',
                                   navbar_choices=navbar_choices,
                                   expert_hints=expert_hints)
        else:
            return render_template('index.html', message='No results found!', name='bijan', page_name='miss_matches')


    @app.route('/report_error/', methods=['GET'])
    def error_report():
        from feedback import request_error_correction

        comment = request.args.get('comment')

        if request.args.get('document_id'):
            document = myOrm.get_document(request.args.get('document_id'))
            person_list = []
            for ref_id in document['reference_ids'].split(','):
                person_list.append(myOrm.get_person(ref_id))

            comment = request.args.get('comment')

            request_error_correction(document=document, person_list=person_list, message_type="to_bhic"
                                     , comment=comment, user="Bijan")

            return render_template('feedback.html', message='Thanks for you your feedback!', name='bijan')

        else:
            if comment:

                request_error_correction(document='', person_list='', message_type="to_bijan"
                                         , comment=comment, user="Bijan")
                return render_template('feedback.html', message='Thanks for you your feedback!', name='bijan')

            else:
                return render_template('feedback.html', message='Have you found an error in the database? '
                                                                'Then Please fill out the following'
                                                                ' form and click submit!', name='bijan')


    @app.route('/check_pedigrees/', methods=['GET'])
    @app.route('/check_pedigrees/<depth>', methods=['GET'])
    @app.route('/check_pedigrees/<depth>/<family_id>', methods=['GET'])
    def check_pedigrees(depth=4, family_id=0):

        from modules.basic_modules import generatePedigree

        json_dict = generatePedigree.check_pedigrees(int(depth), int(family_id))

        document_ids = list(set(generatePedigree.get_document_ids(json_dict['parents'])))
        document_ids = [x for x in document_ids if x]
        details = {'document_id': document_ids,
                   'document_type': ''}

        families = generatePedigree.import_families()
        navbar_choices = {}
        for tmp_depth in [5, 4, 3]:
            navbar_choices[tmp_depth] = []
            for tmp_family_id in xrange(1, 10):
                reference_id = myOrm.get_document(families[tmp_depth - 3][tmp_family_id][0])['reference_ids'].split(
                    ',')[:2]
                groom_last_name = myOrm.get_person(reference_id[0])['last_name']
                bride_last_name = myOrm.get_person(reference_id[1])['last_name']
                navbar_choices[tmp_depth].append([groom_last_name + '-' + bride_last_name, tmp_family_id])

        return render_template('visualization.html', details=details,
                               json_dict_h=json_dict, json_dict_v=json_dict, depth=depth,
                               navbar_choices=navbar_choices)

        # else:
        # return render_template('visualization.html', message='No results found!', name='bijan')


    @app.route('/nerd_vis/', methods=['GET', 'POST'])
    @app.route('/nerd_vis/<t_id>', methods=['GET', 'POST'])
    def nerd_vis(t_id=1):
        if request.method == "POST":

            post_dict = {}
            for f in request.form:
                post_dict[f] = request.form[f]
            import datetime

            post_dict['date'] = datetime.datetime.now()
            csv_text = ';'.join([str(value) for value in post_dict.values()]) + '\n'
            with open("feedback.csv", "a") as my_file:
                my_file.write(csv_text)

        output = get_nerd_data(request, t_id)
        return render_template('nerd_vis.html', text=output['text'],
                               match_details=output['match_details'],
                               refs_list=output['nerd_references'],
                               navbar_choices=output['navbar_choices'],
                               extracted_relations=output['nerd_relationships'],
                               name_alternatives=output['name_alternatives'])

    app.debug = True
    app.run(host='0.0.0.0', port=20002)
    # app.run()


def main():
    routing()


if __name__ == "__main__":
    main()
