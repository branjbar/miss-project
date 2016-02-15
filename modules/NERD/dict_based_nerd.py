"""
a class to extract names.

"""
import datetime
import random
from modules.solr_search import solr_query

__author__ = 'Bijan'

from modules.basic_modules import basic
from modules.basic_modules.basic import log


my_solr = solr_query.SolrQuery()
meertens_names = {}

PUNCTUATION_LIST = [',', ';', '.', ':', '[', ']', '(', ')', '"', "'", '-']

# 64% of people don't have prefix in their name!, 35% have one of the prefixes in following list, Less than 1% have other prefixes 
PREFIXES = ['van', 'de', 'van der', 'van den', 'van de', 'den']  

# FREQ_NAMES = ['te', 'een', 'eende', 'voor', 'als', 'zijn', 'die', 'gulden', 'heeft',
# 'gelegen', 'door', 'huis', 'kinderen', 'schepenen', 'wijlen', 'goederen',
# 'haar',  'hij', 'andere', 'groot', 'genaamd', 'dochter', 'verkopen', 'sijn',
# 'land', 'heer']


MISLEADING_STARTING_WORDS = ["Testament","Codicil","Getuigenverklaring","Inventaris",
                             "Ontlastbrief","Opdracht","Verzoekschrift", "Belening",
                             "Donatie", "Kwitantie", "Bekentenis", "Verklaring",
                             "Codicil", "Bekentenis", "Obligatie", "Comptoir", "Vrouwe",
                             "Verkoopceduul", "Testamant", "Ondertrouw", "Reactie",
                             "Rekest", "Commissie",
                             "Tesatment", "Tetsament"] # the last one is a typo existing in text
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
                              "echtgenote van": "married with",
                              }
#                               "zoon van": "son of",
#                               ", dochter van": "daughter of",
#                               ", zoon van": "son of",
#                               "dochter van": "daughter of",
#                               "dochter": "daughter of"
# }


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
        self.name_alternatives = []
        self.solr_relations = []

        if extract_flag:
            self.pre_processing()
            if len(self.text) > 5:
                self.extract_names()

    def get_relations(self):
        if not self.relations:
            self.extract_relations()
        rel_list = self.relations
        return rel_list

    def get_solr_relations(self):
        return self.solr_relations

    def get_references(self):
        if not self.references:
            self.extract_references()
        return self.references

    def get_name_alternatives(self):
        return self.name_alternatives

    def pre_processing(self):
        """
            preprocesses the text (mostly for notarial acts).
            E.g., adds space before and after ","
             replaces multiple spaces by single ones.
             detects the names connected to previous word
             also replacing the starting digits
        """
        self.text = self.text.replace('"', '')
        for c in PUNCTUATION_LIST:
            self.text = self.text.replace(c, ' ' + c + ' ')
        text = self.text.replace('  ', ' ')

        # if the word starts with digits, we remove the digit. We check it two times.
        if text.split(' ')[0].isdigit():
            text = ' '.join(text.split()[1:])
        if text.split(' ')[0].isdigit():
            text = ' '.join(text.split()[1:])

        # splitting the connected words using the upper case in between, e.g., "(=Beatrix)"
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

        self.pp_text = new_text

    def extract_names(self):
        """ (list) --> (dist)
            for each word the specifications are reported:
            1 : started with capital letter
            2 : last name prefix
            3 : First word of the whole paragraph which continues a capital letter word
            4: Very frequent words
            -1: has capital letter but is not a name
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
        if self.word_list[0][0].isupper() and not self.word_list[0] in MISLEADING_STARTING_WORDS and word_spec.get(1) == 1:
            word_spec[0] = 3

        # Consider first word as a name if second word is already chosen to be a prefix and third name is a name
        try:
            if not self.word_list[0] in MISLEADING_STARTING_WORDS and self.word_list[1] in PREFIXES and word_spec.get(2) == 1:
                word_spec[0] = 3
                word_spec[1] = 2
        except:
            pass

        # Consider first word as a name if 2nd and 3rd words are already chosen to be a prefix and forth name is a name
        try:
            if not self.word_list[0] in MISLEADING_STARTING_WORDS and self.word_list[1] + " " + self.word_list[
                2] in PREFIXES and word_spec.get(3) == 1:
                word_spec[0] = 3
                word_spec[1] = 2
                word_spec[2] = 2
        except:
            pass

        for index, word in enumerate(self.word_list):
            if word in FREQ_NAMES:
                word_spec[index] = 4

        # this is to get rid of "Sint Oedenrode, Sint Janssstraat, Sint Janssstraat, etc."
        for index, word in enumerate(self.word_list):
            if word == 'Sint':
                word_spec[index] = -1

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
                reference = reference.strip().decode("ISO-8859-1").encode('utf8', 'ignore')
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

                    # to detect relations in patterns like "Gerrit Hendrix en Hendersken Thijssen echtelieden"
                    try:
                        term1 = ' '.join(self.word_list[ref1[0] + len(ref1[1].split()):ref2[0]])
                        term2 = self.word_list[len(ref2[1].split()) + ref2[0]]
                        if term1 == "en" and (term2 == "echtelieden" or term2 == "e"):
                            self.relations.append({"ref1": ref1, "ref2": ref2, "relation": "husband of"})
                    except:
                        pass

                    # detect relations in patterns like "Jorden Thomassen en Catharina Hendriks zijn vrouw"
                    try:
                        term1 = ' '.join(self.word_list[ref1[0] + len(ref1[1].split()):ref2[0]])
                        term2 = ' '.join(
                            self.word_list[len(ref2[1].split()) + ref2[0]: len(ref2[1].split()) + ref2[0] + 2])
                        if term1 == "en" and term2 == "zijn vrouw":
                            self.relations.append({"ref1": ref1, "ref2": ref2, "relation": "husband of"})
                    except:
                        pass

                    # detect relations in like "kinderen van Johannes Janse Smits en Antonetta Jan Roeloff Donckers"
                    try:
                        term1 = ' '.join(
                            self.word_list[ref1[0] - 2:ref1[0]])
                        term2 = ' '.join(self.word_list[ref1[0] + len(ref1[1].split()):ref2[0]])
                        if [term1, term2] in RELATION_INDICATORS_BEFORE_MIDDLE:
                            self.relations.append({"ref1": ref1, "ref2": ref2, "relation": "married with"})
                    except:
                        pass

                        # TODO: use "te" to extract locations. Or use the Lexicon of location names for this!

    def extract_solr_relations(self, negative_samples=False):
        """
        here for every pair of relationships we look at
        """

        # to get rid of redundant references:
        reference_list = []
        for ref in self.references:
            reference_list.append(ref)

        name_alternatives = []
        for i in xrange(1, len(reference_list)):
            ref1 = reference_list[i - 1]
            ref2 = reference_list[i]
            support_list = my_solr.get_support(ref1[1], ref2[1], cats='cat:birth OR cat:marriage OR cat:death')
            index_key = solr_query.generate_features(ref1[1].split(), ref2[1].split())
            solr_results = my_solr.search(index_key, 'cat:birth OR cat:marriage OR cat:death')
            name_alternative_tmp_1 = [' '.join(index_key.split('_')[:2])]
            name_alternative_tmp_2 = [' '.join(index_key.split('_')[2:])]
            if solr_results.results:
                html_list = []
                search_results = {}
                for result in solr_results.highlighting.iteritems():
                    search_results[result[0]] = result[1]['features'][0].replace('<em>', '').replace('</em>', '')

                    # get name alternatives
                    tmp_name = ' '.join(
                        result[1]['features'][0].replace('<em>', '').replace('</em>', '').split('_')[0:2])
                    if tmp_name not in name_alternative_tmp_1:
                        name_alternative_tmp_1.append(tmp_name)

                    tmp_name = ' '.join(
                        result[1]['features'][0].replace('<em>', '').replace('</em>', '').split('_')[2:])
                    if tmp_name not in name_alternative_tmp_2:
                        name_alternative_tmp_2.append(tmp_name)

                for doc_id in search_results.keys():
                    couple_names = ['_'.join(index_key.split('_')[:2]), '_'.join(index_key.split('_')[-2:])]
                    html = {"id": str(doc_id), "couple_names": couple_names, "search_results": search_results[doc_id]}
                    html_list.append(html)

                self.solr_relations.append(
                    {"ref1": ref1, "ref2": ref2, "numFound": solr_results.numFound, "html": html_list,
                     "support": support_list["support"]})

                if len(name_alternative_tmp_1) > 1 and name_alternative_tmp_1 not in name_alternatives:
                    name_alternatives.append(name_alternative_tmp_1)

                if len(name_alternative_tmp_2) > 1 and name_alternative_tmp_2 not in name_alternatives:
                    name_alternatives.append(name_alternative_tmp_2)

        nerd_relationships = []
        for index, rel1 in enumerate(self.relations):
            for rel2 in self.solr_relations:
                if [rel1['ref1'][1], rel1['ref2'][1]] == [rel2['ref1'][1], rel2['ref2'][1]]:
                    nerd_relationships.append(rel1)
                    nerd_relationships[-1]['color'] = 'green'
                    nerd_relationships[-1]['html'] = rel2['html']
                    nerd_relationships[-1]['numFound'] = rel2['numFound']
                    nerd_relationships[-1]['support'] = rel2['support']
                    nerd_relationships[-1]['class'] = 'positive'

        for index, rel1 in enumerate(self.relations):
            if not [rel1['ref1'][1], rel1['ref2'][1]] in [[rel2['ref1'][1], rel2['ref2'][1]] for rel2 in self.solr_relations]:
                nerd_relationships.append(rel1)
                nerd_relationships[-1]['color'] = 'black'
                nerd_relationships[-1]['html'] = []
                nerd_relationships[-1]['numFound'] = 0
                nerd_relationships[-1]['support'] = [0, 0, 0]
                nerd_relationships[-1]['class'] = 'negative'

        for rel2 in self.solr_relations:
            if [rel2['ref1'][1], rel2['ref2'][1]] not in [[rel1['ref1'][1], rel1['ref2'][1]] for rel1 in self.relations]:
                nerd_relationships.append({'ref1': rel2['ref1'],
                                           'ref2': rel2['ref2'],
                                           'relation': 'married with',
                                           'color': 'red',
                                           'html': rel2['html'],
                                           'numFound': rel2['numFound'],
                                           'support': rel2['support'],
                                           'class': 'positive'
                })
        if negative_samples:
            for index in xrange(len(self.references)-1):
                if [self.references[index][1], self.references[index+1][1]] not in [[rel['ref1'][1],rel['ref2'][1]] for rel in self.relations]:
                    # print [self.references[index][1], self.references[index+1][1]]
                    nerd_relationships.append({'ref1': self.references[index],
                                               'ref2': self.references[index+1],
                                               'relation': 'no relation',
                                               'color': 'white',
                                               'html': {},
                                               'numFound': 0,
                                               'support': [0,0,0],
                                               'class': 'negative'
                    })

            # if [rel2['ref1'], rel2['ref2']] not in [[rel1['ref1'][1], rel1['ref2'][1]] for rel1 in self.relations]:
            #     nerd_relationships.append({'ref1': [0, rel2['ref1']],
            #                                'ref2': [0, rel2['ref2']],
            #                                'relation': 'married with',
            #                                'color': 'red',
            #                                'html': rel2['html'],
            #                                'numFound': rel2['numFound'],
            #                                'support': rel2['support']
            #     })

        self.name_alternatives = name_alternatives
        self.relations = nerd_relationships

    def get_statistics(self):
        """
        returns useful statistics like number of entities and references extracted.
        colors: green: both pattern and evidence, black: just pattern, red: just evidence
        """
        if not self.references:
            self.extract_references()
        if not self.relations:
            self.extract_relations()
        if not self.solr_relations:
            self.extract_solr_relations()

        # here we get frequency of relation types
        rel_type = [rel['color'] for rel in self.relations]
        rel_type_freq = {x: rel_type.count(x) for x in rel_type}
        rel_type_count = {'green': [], 'black': [], 'red': []}
        for rel in [[rel['color'], len(rel['html'])] for rel in self.relations]:
            rel_type_count[rel[0]].append(str(rel[1]))

        return {'ref_len': len(self.references),
                'rel_len': len(self.relations),
                'rel_type_freq': rel_type_freq,
                'rel_type': rel_type_count,
        }


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
    fd = open('hossein_text_%.0f.csv' % (100.0*random.random()), 'a')
    fd.write('sep=;\n')
    fd.write('id;T1;T2;T3;doc_type;|T1|;|T2|;|T3|;sup(e1);sup(e2);sup(e1,e2);class;row_id;uuid;rel_index;type\n')
    count = 0;
    for t_id in xrange(20000000):
        # if not t_id % 100:
        print t_id, count
        act = myOrm.get_notarial_act(t_id, century18=True)

        if act:
            text = act['text1'] + ' ' + act['text2'] + act['text3']
            nerd = Nerd(text)
            nerd.extract_relations()
            nerd.extract_solr_relations(negative_samples=True)
            for index, rel in enumerate(nerd.get_relations()):
                sup = rel['support']
                before_text = ' '.join(nerd.pp_text.split()[max(0,rel['ref1'][0]-10):rel['ref1'][0]])
                middle_text = ' '.join(nerd.pp_text.split()[rel['ref1'][0] + len(rel['ref1'][1].split()):rel['ref2'][0]])
                after_text = ' '.join(nerd.pp_text.split()[rel['ref2'][0] + len(rel['ref2'][1].split()):rel['ref2'][0] + len(rel['ref2'][1].split())+10])

                before_text = ' '.join(before_text.replace(',','').replace('.','').replace(';','').replace(' ',' ').strip().split()[-5:])
                middle_text = middle_text.replace(',','').replace('.','').replace(';','').replace(' ',' ').strip()
                after_text = ' '.join(after_text.replace(',','').replace('.','').replace(';','').replace(' ',' ').strip().split()[:5])

                csv_line = "%d;%s;%s;%s;%s;%d;%d;%d;%d;%d;%d;%s;%d;%s;%d;%s\n" %\
                           (count,
                            before_text,
                            middle_text,
                            after_text,
                            act['AKTETYPE'],
                            len(before_text.split()),
                            len(middle_text.split()),
                            len(after_text.split()),
                            sup[1],
                            sup[2],
                            sup[0],
                            rel['class'],
                            t_id,
                            act['id'],
                            index,
                            rel['color'])
                count += 1
                fd.write(csv_line)


            #
            #
            # csv_dict = nerd.get_statistics()
            #
            # csv_line = '%d, %d, %d, %d, %d, %d, %s, %s, %s\n' % (t_id,
            #                                                      csv_dict['ref_len'], csv_dict['rel_len'],
            #                                                      csv_dict['rel_type_freq'].get('green', 0),
            #                                                      csv_dict['rel_type_freq'].get('black', 0),
            #                                                      csv_dict['rel_type_freq'].get('red', 0),
            #                                                      ', '.join(csv_dict['rel_type']['green']),
            #                                                      ', '.join(csv_dict['rel_type']['black']),
            #                                                      ', '.join(csv_dict['rel_type']['red']))



if __name__ == "__main__":
    main()
