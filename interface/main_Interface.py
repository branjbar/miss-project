from flask import Flask
from flask import request
from flask import render_template


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
    @app.route('/person/', methods=['GET', 'POST'])
    @app.route('/person/<p_id>', methods=['GET', 'POST'])
    def person_page(p_id=None):
        # if gets an id, searches for a person with that id
        search_id = request.args.get('search_term')
        if search_id and search_id.isdigit():
            p_id = int(search_id)

        from modules import basic
        db = basic.do_connect()
        person = basic.get_person(db,p_id)
        return render_template('index.html', p = person, name='bijan')

    @app.route('/document/', methods=['GET', 'POST'])
    @app.route('/document/<p_id>', methods=['GET', 'POST'])
    def document_page(p_id=None):
        # if gets an id, searches for a document with that id
        search_id = request.args.get('search_term')
        if search_id and search_id.isdigit():
            p_id = int(search_id)

        from modules import basic
        db = basic.do_connect()
        person = basic.get_document(db,p_id)
        return render_template('index.html', p = person, name='bijan')


    app.debug = True
    # app.run(host='0.0.0.0')
    app.run()


def main():


    routing()

if __name__ == "__main__":
    main()