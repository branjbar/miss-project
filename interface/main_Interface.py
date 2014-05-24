from flask import Flask
from flask import request
from flask import render_template

from modules import basic
from modules import myOrm
from modules import loadData


def routing():
    app = Flask(__name__)

    # @app.route("/")
    # def index():
    #     return 'Index Page'
    #
    # def hello():
    #     return "Hello World!"



    @app.route('/', methods=['GET', 'POST'])
    def home():
        return render_template('index.html', header="Welcome!"
                               ,  message="to MiSS Web Interface. Use the upper "
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
            if person:
                relatives_id = myOrm.get_relatives(person['id'])

                for index, relative in enumerate(relatives_id):
                    relative_person = myOrm.get_person(relative)

                    if relative_person:
                        rel['Relative_' + str(index)] = relative_person

            return render_template('index.html', p=person, p2=rel, name='bijan')
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
                    ref_dict['Role' + str(ref_person['role']) + '_' + ref_person['gender']] = ref_person

            return render_template('index.html', p=document, p2=ref_dict, name='bijan')
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
                if not len(loadData.table_all_persons) and request.args.get('limit'):
                    data_type = ''
                    if request.args.get('birth'):
                        data_type = ' birth'
                    if request.args.get('marriage'):
                        data_type += ' marriage'
                    if request.args.get('death'):
                        data_type += ' death'
                    data_type = data_type.strip().replace(' ', "' or '")
                    loadData.main([int(request.args.get('limit')), data_type])
                    tables = {'data': 'loading'}

                else:
                    if not len(loadData.table_all_persons) and request.args.get('refresh'):
                        tables = {'data': 'loading'}
                    else:

                        tables = {'Persons': len(loadData.table_all_persons),
                                  'Blocks':len(loadData.block_dict),
                                  'Documents':len(loadData.table_all_documents),}

        return render_template('index.html', header=header, message=message, data=tables, name='bijan', page_name='load_data')

    @app.route('/link/', methods=['GET', 'POST'])
    @app.route('/link/<p_id>', methods=['GET', 'POST'])
    def link_page(p_id=None):
        # if gets an id, searches for a document with that id
        search_id = request.args.get('search_term')
        if search_id and search_id.isdigit():
            p_id = int(search_id)

        db = basic.do_connect()
        match = myOrm.get_links(db, p_id)
        doc = {}
        ref_dict = {}
        if match :
            if match['id1']:
                if myOrm.get_document(match['id1']):
                    doc['REF1'] = myOrm.get_document(match['id1'])
                    ind = 1
                    if doc.get('REF1'):
                        for ref in doc['REF1'].get('reference_ids').split(','):
                            ref_person = myOrm.get_person(ref)
                            if ref_person:
                                ref_dict['REF1_' + str(ind)] = ref_person
                                ind += 1
                else:
                    doc['REF1'] = {'id1': match['id1'],'details': 'NOT FOUNT'}

            else:
                doc['REF1'] = {'id1': match['id1'],'province': 'UNKNOWN'}

            if match['id2']:
                if myOrm.get_document(match['id2']):
                    doc['REF2'] = myOrm.get_document(match['id2'])
                    ind =1
                    if doc.get('REF2'):
                        for ref in doc['REF2'].get('reference_ids').split(','):
                            ref_person = myOrm.get_person(ref)
                            if ref_person:
                                ref_dict['REF2_' + str(ind)] = ref_person
                                ind += 1
                else:
                    doc['REF2'] = {'id2': match['id2'],'details': 'NOT FOUNT'}
            else:
                doc['REF2'] = {'id2': match['id2'],'province': 'UNKNOWN'}
        return render_template('index.html', p=match, p2=doc, p3=ref_dict, name='bijan')


    @app.route('/visualization/', methods=['GET', 'POST'])
    def visualization():
        from modules import generatePedigree

        search_id = request.args.get('search_term')
        p_id = 0
        if search_id and search_id.isdigit():
            p_id = int(search_id)

        document = myOrm.get_document(p_id)
        if document:
            json_dict = generatePedigree.pedigree(document)

            details = {'document_id': document['id'],
                       'document_type': document['type_text']}

            return render_template('visualization.html', p=details, json_dict=json_dict)

        else:
            return render_template('visualization.html', message='No results found!', name='bijan')


    app.debug = True
    # app.run(host='0.0.0.0')
    app.run()


def main():
    routing()

if __name__ == "__main__":
    main()