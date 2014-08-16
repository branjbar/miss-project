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

meertens_names = {}

# TODO make a class for nerd instead of using module as it is now


def text_pre_processing(text):
    """
        preprocesses the text (mostly for notarial acts).
        E.g., adds space before and after ","
         replaces multiple spaces by single ones.
         detects the names connected to previous word
    """
    punctuation_list = [',', ';', '.', ':', '[', ']', '(', ')', '"', "'"]
    for c in punctuation_list:
        text = text.replace(c,' ' + c + ' ')
    text = text.replace('  ', ' ')

    new_text = ''
    for word in text.split():
        new_word = word
        if len(word) > 3:
            new_word = ''
            for index, letter in enumerate(word):
                if letter.isupper() and 1 < index < len(word):
                    new_word += ' '
                new_word += letter
        new_text += new_word + ' '

    text = new_text
    return text





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

def main():
    pass


if __name__ == "__main__":
    main()