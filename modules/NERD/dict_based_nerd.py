"""
Manual to use dict_based_nerd

    text_id = 500  # choosing row 500
    act = myOrm.get_notarial_act(text_id)  # Getting the complete row with id 500 from natry_acts table
    word_list = basic.text_pre_processing(act['text1'] + ' ' + act['text2'] + act['text3']).split()
        # pre processing the text and splitting the words in a list
    word_spec = extract_name(word_list)  # getting a dictionary of word index and its status regarding being a name or not
    refs_list = extract_references(word_list, word_spec)
        # the concrete references which consist more than one name and are good for future check are reported.


"""
import time
from modules.NERD import html_generate

__author__ = 'Bijan'

from modules.basic_modules import basic
from modules.basic_modules.basic import log
from modules.basic_modules import myOrm

meertens_names = {}

# TODO move the text pre-processing from basic modules to this place
# TODO make a class for nerd instead of using module as it is now


def extract_name(word_list):
    """ (list) --> (dist)
        for each word the specifications are reported:
        1 : started with capital letter
        2 : last name prefix
        3 : First word of the whole paragraph
        -1: has capital letter but doesn't exist in the list
    """
    # search for capital letters
    global meertens_names

    if not meertens_names:
        import_dutch_data_set()

    word_spec = {}  # for word specificate
    for index, word in enumerate(word_list):
        word_spec[index] = None

        if word[0].isupper() and index > 0 and len(word) > 1:
            word_spec[index] = 1

    # TODO Consider a start like this: "Hendrik de Jong, lid der sted.....", here because of "de", it's hard to detect the first name.
    # Consider first word as a name if second word is already chosen to be a name
    if not word_list[0] == 'Testament' and word_spec.get(1) == 1:
        word_spec[0] = 3

    PREFIXES = ['van', 'te', 'de', 'van der', 'van den', 'van de']
    # search for last name prefixes
    for index, word in enumerate(word_list):
        if word in PREFIXES and word_spec.get(index - 1) and word_spec.get(index+1):
            word_spec[index] = 2
        if index < len(word_list)-1 and word + " " + word_list[index+1] in PREFIXES and word_spec.get(index - 1) and word_spec.get(index+2):
            word_spec[index] = 2
            word_spec[index+1] = 2

    for index, word in enumerate(word_list):
        if word_spec[index] and not meertens_names.get(word.lower()):
            word_spec[index] = -1

    return word_spec


def extract_references(word_list, word_spec):
    """ (list) --> (list)
        connects the extracted names by using the specification of

    """

    refs_list = []
    reference = ''
    for index, word in enumerate(word_list):
        if word_spec[index] :
            reference += word + ' '
        else:
            reference = reference.strip()
            ref_len = len(reference.split(' '))
            if ref_len > 1:
                refs_list.append([index - ref_len, reference])
            reference = ''

    return refs_list


# TODO here extract relations, e.g., see if names fit to patterns such as ".. en ..", ".. en zijn vrouw ..", ".. weduwe van ..", or "... en haar man ..."


def import_dutch_data_set():
    """
        imports the Dutch data set for name disambiguation
    """
    global meertens_names
    log('importing Meertens names')
    the_query = "SELECT name, type FROM meertens_names"
    cur = basic.run_query(the_query)

    meertens_names = {}
    for c in cur.fetchall():
        meertens_names[c[0].lower()] = c[1]

    log('importing Meertens names is done')


def generate_html_report():
    log('importing names')
    the_query = "SELECT name, type FROM meertens_names"
    cur = basic.run_query(the_query)
    name_dict = {}
    name_list = []
    for c in cur.fetchall():
        name_dict[c[0].lower()] = c[1]
        name_list.append(c[0].lower())

    log('importing notarial acts')
    the_query = "SELECT text1, text2, text3, date, place from notary_acts"
    cur = basic.run_query(the_query)
    notarial_list = []
    for c in cur.fetchall()[:1000]:
        # each notarial_list element is [text, date, place]
        notarial_list.append([c[0] + ' ' + c[1] + ' ' + c[2], c[3], c[4]])

    log('extracting names')
    output = []
    for n in notarial_list:
        text = n[0]
        text = basic.text_pre_processing(text)
        word_list = text.split()
        word_spec = extract_name(word_list)
        output.append([text, word_spec])

    html_generate.export_html(output)


def export_names_to_sql_table():
    """
    here we replace frog, and extract names from text.
    The extracted names are added to natary_acts_refse as following:
    id, reference, index, text_id, text_row_id


    Data can be loaded to sql by using following command
    LOAD DATA INFILE 'extracted_names.csv'
    INTO TABLE notary_acts_refs FIELDS TERMINATED BY ',' LINES TERMINATED BY '\n';
    """
    ref_id = 0
    log('importing notarial acts')
    the_query = "SELECT text1, text2, text3, row_id, id from notary_acts"
    cur = basic.run_query(the_query)
    notarial_list = []
    for c in cur.fetchall():
        # each notarial_list element is [text, date, place]
        notarial_list.append([c[0] + ' ' + c[1] + ' ' + c[2], c[4], c[3]])

    log('extracting names')
    now = time.time()
    for n in notarial_list:
        text = n[0]
        text = basic.text_pre_processing(text)
        word_list = text.split()
        if word_list:
            word_spec = extract_name(word_list)
            ref_list = extract_references(word_list,word_spec)

            for ref in ref_list:
                ref_id += 1
                csv_text = str(ref_id) + ',' + str(ref[1]) + ',' + str(ref[0]) + ',' + str(n[1]) + ',' + str(n[2]) + '\n'
                with open("../../data/extracted_names.csv", "a") as my_file:
                                    my_file.write(csv_text)



    print time.time() - now

if __name__ == "__main__":
    export_names_to_sql_table()