from flask import Flask
from flask import request
from flask import render_template

from modules import basic
from modules import myOrm


def store_email(request):

    name = request.form.get('name')
    paper_id = request.form.get('id')
    title = request.form.get('title')
    affiliation = request.form.get('affiliation')
    email = request.form.get('email')
    if email:
        email = email.lower().strip()
    paper = request.form.get('paper')
    action = request.form.get('button')
    # print name, affiliation, email, paper, action
    person_name = name
    try:
        person_name = name.split(', ')[1] + ' ' + name.split(', ')[0]
    except:
        pass

    if action == 'remove':
        email = "NONE"

    data = {'paper_id': paper_id, 'title': title, 'author': name, 'name': person_name, 'email': email, 'affiliation': affiliation, 'paper':paper, 'conference': 'AAMAS2014'}
    if data['email']:
        outfile = open('data.json', 'a')
        json.dump(data, outfile, indent=2)
        outfile.close()


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

        db = basic.do_connect()
        block = myOrm.get_block(db,p_id)
        return render_template('index.html', p = block, name='bijan')


    @app.route('/load_data/', methods=['GET', 'POST'])
    def load_data():
        from modules import loadData
        if not len(loadData.table_all_documents):
            loadData.main(10000)
        tables = {'Persons': len(loadData.table_all_persons),
                  'Person_Blocks':len(loadData.table_all_persons_features),
                  'Documents':len(loadData.table_all_documents),}
        return render_template('index.html', message="Data is loaded!", p=tables, name='bijan')

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
                doc['REF1'] = myOrm.get_document(db, match['id1'])
                ind = 1
                for ref in doc['REF1'].get('reference_ids').split(','):
                    ref_person = myOrm.get_person(db, ref)
                    ref_dict['REF1_' + str(ind)] = ref_person
                    ind += 1
            else:
                doc['REF1'] = {'id1': match['id1'],'province': 'UNKNOWN'}

            if match['id2']:
                doc['REF2'] = myOrm.get_document(db, match['id2'])
                ind =1
                for ref in doc['REF2'].get('reference_ids').split(','):
                    ref_person = myOrm.get_person(db, ref)
                    ref_dict['REF2_' + str(ind)] = ref_person
                    ind += 1
            else:
                doc['REF2'] = {'id2': match['id2'],'province': 'UNKNOWN'}
        return render_template('index.html', p=match, p2=doc, p3=ref_dict, name='bijan')


    app.debug = True
    # app.run(host='0.0.0.0')
    app.run()


def main():
    routing()

if __name__ == "__main__":
    main()