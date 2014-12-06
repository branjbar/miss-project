"""
a class to extract names.

"""
import copy

__author__ = 'Bijan'

from modules.basic_modules import basic
from modules.basic_modules.basic import log

meertens_names = {}

PUNCTUATION_LIST = [',', ';', '.', ':', '[', ']', '(', ')', '"', "'"]
PREFIXES = ['van', 'de', 'van der', 'van den', 'van de']
# FREQ_NAMES = ['te', 'een', 'eende', 'voor', 'als', 'zijn', 'die', 'gulden', 'heeft',
# 'gelegen', 'door', 'huis', 'kinderen', 'schepenen', 'wijlen', 'goederen',
# 'haar',  'hij', 'andere', 'groot', 'genaamd', 'dochter', 'verkopen', 'sijn',
# 'land', 'heer']

# TODO: other patterns for relationship: kinderen van [blah] en [blue]
# TODO: other patterns for relationship: zoon van [blah] en [blue]
# TODO: other patterns for relationship: dochter van [blah] en [blue]
FREQ_NAMES = ['te', 'kinderen', 'dochter']

RELATION_INDICATORS_BEFORE_MIDDLE = [["kinderen van", "en"], ["zoon van", "en"], ["dochter van", "en"]]

RELATION_INDICATORS_MIDDLE = {"gehuwd met": "married with",
                              "weduwe van": "widow of",
                              "weduwe": "widow of",
                              "en zijn vrouw": "husband of",
                              ", weduwe van": "widow of",
                              "weduwnaar van": "widower of",
                              "vrouw van": "wife of",
                              ", gehuwd met": "married with",
                              "man van": "husband of",
                              "weduwe wijlen": "widow of",
                              ", weduwnaar van": ", wedower of",
                              ", de weduwe van": "widow of",
                              "getrouwt met": "married with",
                              "huijsvrouw van": "wife of",
                              "weduwnaar": "widower of",
                              "weduwe van wijlen": "widow of",
                              ", de weduwe": "widow of",
                              ", weduwe": "widow of",
                              ", vrouw van": "wife of",
                              ", huisvrouw van": "wife of",
                              "en haar man": "wife of",
                              "huisvrouw van": "wife of",
                              "en zijn huisvrouw": "husband of",
                              "getrouwd met": "married with",
                              "zoon van": "son of",
                              ", dochter van": "daughter of",
                              ", zoon van": "son of",
                              "dochter van": "daughter of",
                              "dochter": "daughter of"
}


class Nerd():
    """
    a full class for named entity recognition
    """

    def __init__(self, text, extract_flag=True):
        """

        :param text: gets text as input.
        :param extract_flag:
        :return:
        """
        self.text = text
        self.pp_text = ''  # pre-processed text
        self.word_list = []
        self.word_list_labeled = {}
        self.references = []
        self.relations = []

        if extract_flag:
            self.pre_processing()
            if len(self.text) > 5:
                self.extract_names()


    def get_relations(self):
        if not self.relations:
            self.extract_relations()
        rel_list = self.relations
        return rel_list

    def get_references(self):
        if not self.references:
            self.extract_references()
        return self.references

    def pre_processing(self):
        """
            preprocesses the text (mostly for notarial acts).
            E.g., adds space before and after ","
             replaces multiple spaces by single ones.
             detects the names connected to previous word
        """
        self.text = self.text.replace('"', '')
        for c in PUNCTUATION_LIST:
            self.text = self.text.replace(c, ' ' + c + ' ')
        text = self.text.replace('  ', ' ')

        new_text = ''

        # spliting the connected words using the upper case in between, e.g., "(=Beatrix)"
        for word in text.split():
            new_word = word
            if len(word) > 3:
                new_word = ''
                for index, letter in enumerate(word):
                    if letter.isupper() and 1 < index < len(word):
                        new_word += ' '

                    new_word += letter

            new_text += new_word + ' '

        self.pp_text = new_text

    def extract_names(self):
        """ (list) --> (dist)
            for each word the specifications are reported:
            1 : started with capital letter
            2 : last name prefix
            3 : First word of the whole paragraph which continues with a capital letter word
            4: Very frequent words
            -1: has capital letter but doesn't exist in the list
        """
        # search for capital letters
        # global meertens_names
        #
        # if not meertens_names:
        # import_dutch_data_set()

        # get a list of words from pre-processed words.
        self.word_list = self.pp_text.split()

        word_spec = {}  # for word specific
        for index, word in enumerate(self.word_list):
            word_spec[index] = None

            if word[0].isupper() and index > 0 and len(word) > 1:
                word_spec[index] = 1

        # TODO Consider a start like this: "Hendrik de Jong, lid der sted.....", here because of "de", it's hard to detect the first name.


        # search for last name prefixes
        for index, word in enumerate(self.word_list):
            # one component prefixes
            if word in PREFIXES \
                    and word_spec.get(index - 1) \
                    and word_spec.get(index + 1):
                word_spec[index] = 2

            # two component prefixes
            if index < len(self.word_list) - 1 \
                    and word + " " + self.word_list[index + 1] in PREFIXES \
                    and word_spec.get(index - 1) \
                    and word_spec.get(index + 2):
                word_spec[index] = 2
                word_spec[index + 1] = 2

        # Consider first word as a name if second word is already chosen to be a name
        if not self.word_list[0] == 'Testament' and word_spec.get(1) == 1:
            word_spec[0] = 3

        # Consider first word as a name if second word is already chosen to be a prefix and third name is a name
        if not self.word_list[0] == 'Testament' and self.word_list[1] in PREFIXES and word_spec.get(2) == 1:
            word_spec[0] = 3
            word_spec[1] = 2

        # Consider first word as a name if second and third words are already chosen to be a prefix and forth name is a name
        if not self.word_list[0] == 'Testament' and self.word_list[1] + " " + self.word_list[
            2] in PREFIXES and word_spec.get(3) == 1:
            word_spec[0] = 3
            word_spec[1] = 2
            word_spec[2] = 2

        for index, word in enumerate(self.word_list):
            if word in FREQ_NAMES:
                word_spec[index] = 4




        # for index, word in enumerate(self.word_list):
        # if word_spec[index] and not meertens_names.get(word.lower()):
        # word_spec[index] = -1

        self.word_list_labeled = word_spec

    def extract_references(self):
        """ (list) --> (list)
            connects the extracted names by using the specification of

        """

        refs_list = []
        reference = ''
        # need_last_name_flag = False
        for index, word in enumerate(self.word_list):
            if self.word_list_labeled[index] in [1, 2, 3]:
                reference += word + ' '
            else:
                reference = reference.strip()
                ref_len = len(reference.split(' '))

                # if more than one name is extracted:
                if ref_len > 1:
                    refs_list.append([index - ref_len, reference])
                    # if need_last_name_flag:
                    # refs_list[-2][1] = refs_list[-2][1] + ' ' + reference.split()[-1]
                    # need_last_name_flag = False

                # TODO: Improve dochter name extraction!
                # if none name word after name(s) is 'dochter' we still consider the name as a reference.
                # if index < len(self.word_list) and self.word_list[index] == 'dochter':
                # need_last_name_flag = True  # let the next reference borrow its last name to this reference
                # refs_list.append([index - ref_len, reference])
                reference = ''

        self.references = refs_list

    def extract_relations(self):
        """
            uses the pre-defined patterns to find relations between individuals
        """
        self.relations = []
        for index1, ref1 in enumerate(self.get_references()):
            for index2, ref2 in enumerate(self.get_references()):
                if index2 == index1 + 1:
                    term = ' '.join(self.word_list[ref1[0] + len(ref1[1].split()): ref2[0]])
                    if term in RELATION_INDICATORS_MIDDLE.keys():
                        self.relations.append(
                            {"ref1": ref1, "ref2": ref2, "relation": RELATION_INDICATORS_MIDDLE[term]})

                    # Following is to detect relations in patterns like "Gerrit Hendrix en Hendersken Thijssen echtelieden"
                    try:
                        term1 = ' '.join(self.word_list[ref1[0] + len(ref1[1].split()):ref2[0]])
                        term2 = self.word_list[len(ref2[1].split()) + ref2[0]]
                        if term1 == "en" and term2 == "echtelieden":
                            self.relations.append({"ref1": ref1, "ref2": ref2, "relation": "husband of"})
                    except:
                        pass

                    # Following is to detect relations in patterns like "Jorden Thomassen en Catharina Hendriks zijn vrouw"
                    try:
                        term1 = ' '.join(self.word_list[ref1[0] + len(ref1[1].split()):ref2[0]])
                        term2 = ' '.join(
                            self.word_list[len(ref2[1].split()) + ref2[0]: len(ref2[1].split()) + ref2[0] + 2])
                        if term1 == "en" and term2 == "zijn vrouw":
                            self.relations.append({"ref1": ref1, "ref2": ref2, "relation": "husband of"})
                    except:
                        pass

                    # Following is to detect relations in patterns like "kinderen van Johannes Janse Smits en Antonetta Jan Roeloff Donckers"
                    try:
                        term1 = ' '.join(
                            self.word_list[ref1[0]-2:ref1[0]])
                        term2 = ' '.join(self.word_list[ref1[0] + len(ref1[1].split()):ref2[0]])
                        if [term1, term2] in RELATION_INDICATORS_BEFORE_MIDDLE:
                            self.relations.append({"ref1": ref1, "ref2": ref2, "relation": "married with"})
                    except:
                        pass


    def get_statistics(self):
        """
        returns useful statistics like number of entities and references extracted.
        """
        if not self.references:
            self.get_references()
        if not self.relations:
            self.get_relations()

        return {'ref_len': len(self.references), 'rel_len': len(self.relations)}


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
    from modules.basic_modules import myOrm

    ref = []
    rel = []
    for t_id in xrange(4815, 20000000):
        if not t_id % 100:
            print t_id
        act = myOrm.get_notarial_act(t_id, century18=True)
        fd = open('stat_nerd.csv', 'a')
        if act:
            text = act['text1'] + ' ' + act['text2'] + act['text3']
            nerd = Nerd(text)
            fd.write('%d, %d, %d \n' % (t_id, nerd.get_statistics().values()[0], nerd.get_statistics().values()[1]))
            # fd.close()

            # ref.append(nerd.get_statistics()['ref_len'])
            # rel.append(nerd.get_statistics()['rel_len'])
    print ref
    print rel


if __name__ == "__main__":
    main()