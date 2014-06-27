__author__ = 'Bijan'

from modules.basic_modules import basic
from modules.basic_modules.basic import log
from modules.record_linkage.nerd import html_generate

meertens_names = {}
prefix_1 = ['van', 'te', 'de']

def extract_name(word_list):
    """ (list) --> (dist)
        for each word the specifications are reported:
        1 : started with capital letter
        2 : last name prefix
        3 : First word of the whole paragraph
        4: has capital letter but doesn't exist in the list
    """
    global prefix_1
    # search for capital letters
    global meertens_names
    if not meertens_names:
        import_dutch_data_set()

    word_spec = {}  # for word specificate
    for index, word in enumerate(word_list):
        word_spec[index] = None

        if word[0].isupper() and index > 0 and len(word) > 1:
            word_spec[index] = 1

    # Consider first word as a name if second word is already chosen to be a name
    if not word_list[0] == 'Testament' and word_spec.get(1) == 1:
        word_spec[0] = 3

    # search for last name prefixes
    for index, word in enumerate(word_list):
        if word in prefix_1 and word_spec.get(index - 1) and word_spec.get(index+1):
            word_spec[index] = 2
        if (word == "den" or word == "der") and word_list[index-1] == "van" and word_spec.get(index - 2) and word_spec.get(index+1):
            word_spec[index] = 2
            word_spec[index-1] = 2

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
            if len(reference.split(' ')) > 1:
                refs_list.append(reference)
            reference = ''

    return refs_list



def import_dutch_data_set():
    """
        imports the Dutch data set for name disambiguation
    """
    global meertens_names
    log('importing names')
    the_query = "SELECT name, type FROM meertens_names"
    cur = basic.run_query(the_query)

    meertens_names = {}
    for c in cur.fetchall():
        meertens_names[c[0].lower()] = c[1]

    log('importing names is done')



def main():
    log('importing names')
    the_query = "SELECT name, type FROM meertens_names"
    cur = basic.run_query(None, the_query)
    name_dict = {}
    name_list = []
    for c in cur.fetchall():
        name_dict[c[0].lower()] = c[1]
        name_list.append(c[0].lower())

    log('importing notarial acts')
    the_query = "SELECT inhoud1, inhoud2, inhoud3, datering, plaats from notary_acts"
    cur = basic.run_query(None, the_query)
    notarial_list = []
    for c in cur.fetchall()[:1000]:
        # each notarial_list element is [text, date, place]
        notarial_list.append([c[0] + ' ' + c[1] + ' ' + c[2], c[3], c[4]])

    log('extracting names')
    output = []
    for n in notarial_list:
        text = n[0]
        index_dict = {}
        text = basic.text_pre_processing(text)
        for index, word in enumerate(text.split()):
            # uses Meertens data
            if not word == 'van' and name_dict.get(word.lower()):
                index_dict[index] = name_dict.get(word.lower())

            # uses the first uppercase character
            # if word[0].isupper() and index > 0 and len(text.split()[index-1]) > 1:
            #     index_dict[index] = "last_name"
            # else:
            #     if word[0].isupper() and index > 0:
            #         index_dict[index] = "first_name_m"

        output.append([text, index_dict])

    html_generate.export_html(output)

if __name__ == "__main__":
    main()