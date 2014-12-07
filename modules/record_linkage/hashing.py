"""
Here we do the hashing and update, search the """
from modules.NERD import dict_based_nerd

from modules.basic_modules.basic import run_query
import solr
import copy
from modules.basic_modules.myOrm import Reference
from modules.basic_modules.basic import get_block_key

NOTARY_OFFSET_old = 4000000
NOTARY_OFFSET = 30000000


def generate_features(r1, r2):
    if r1[0] and r1[-1] and r2[0] and r2[-1]:
        if not r1[0] == '*' and not r2[0] == '*':
            r1 = [r1[0], r1[-1]]
            r2 = [r2[0], r2[-1]]
            feature = sorted(['_'.join(r1), '_'.join(r2)])
        else:
            feature = ['*']


        return '_'.join(feature)
    else:
        return 'ERROR'


def generate_blocks(r1, r2):
    if r1[0] and r1[1] and r2[0] and r2[1]:
        blocks = sorted([get_block_key(r1[0], r1[1]), get_block_key(r2[0], r2[1])])
        return '_'.join(blocks)
    else:
        return 'ERROR'


class Hashing():
    def __init__(self):
        """
        initializes the Solr connection
        :return:
        """
        self.s = solr.SolrConnection('http://localhost:8983/solr')
        self.commit_counter = 0
        self.commit_number = 0
        self.current_document_id = 0
        self.place = ''
        self.date = ''
        self.register_type = ''

    def add_key(self, ref_list, document_id, place, date, doc_type, text=''):
        """

        :param ref_list: list of references that should be indexed
        :param document_id: document id
        :return:
        """
        if document_id and ref_list:
            feature_list = []  # features based on exact names
            block_keys = []  # blocking keys based on hossein's key

            if doc_type == 'birth':
                feature_list.append(generate_features(ref_list[1], ref_list[2]))
                block_keys.append(generate_blocks(ref_list[1], ref_list[2]))
                text = 'child: %s, father: %s, mother: %s' % (
                    ' '.join(ref_list[0]), ' '.join(ref_list[1]), ' '.join(ref_list[2]))

            if doc_type == 'marriage':
                feature_list.append(generate_features(ref_list[0], ref_list[1]))
                block_keys.append(generate_blocks(ref_list[0], ref_list[1]))

                feature_list.append(generate_features(ref_list[2], ref_list[3]))
                block_keys.append(generate_blocks(ref_list[2], ref_list[3]))

                feature_list.append(generate_features(ref_list[4], ref_list[5]))
                block_keys.append(generate_blocks(ref_list[4], ref_list[5]))

                text = 'groom: %s, bride: %s, groom father: %s, groom mother: %s, bride father: %s, ' \
                       'bride mother: %s' % (
                           ' '.join(ref_list[0]), ' '.join(ref_list[1]), ' '.join(ref_list[2]), ' '.join(ref_list[3]),
                           ' '.join(ref_list[4]), ' '.join(ref_list[5]))

            if doc_type == 'death':
                feature_list.append(generate_features(ref_list[1], ref_list[2]))
                block_keys.append(generate_blocks(ref_list[1], ref_list[2]))
                feature_list.append(generate_features(ref_list[0], ref_list[3]))
                block_keys.append(generate_blocks(ref_list[0], ref_list[3]))

                text = 'deceased: %s, father: %s, mother: %s, relative: %s' % (
                    ' '.join(ref_list[0]), ' '.join(ref_list[1]), ' '.join(ref_list[2]), ' '.join(ref_list[3]))
                # notary acts!
                # else:
                # print "unknown document type to index"
                # for i1, key1 in enumerate(ref_list):
                # for i2, key2 in enumerate(ref_list):
                # if i1 < i2:
                # feature_list = generate_features(key1, key2)
                # block_keys = generate_blocks(ref_list[0], ref_list[3])

            if feature_list:
                date = self.adapt_date(date)
                feature_list = [x for x in feature_list if x != 'ERROR']
                block_keys = [x for x in block_keys if x != 'ERROR']
                self.s.add(features=feature_list, features_ss=feature_list, blockKeys=block_keys, id=document_id,
                           location_s=place, cat=doc_type,
                           date_dt=date, description=text)  # ,
                # )

            self.commit_counter += 1
            if self.commit_counter > 5000:
                self.s.commit()
                self.commit_counter = 0

                print self.commit_number
                self.commit_number += 1

    def adapt_date(self, date):
        """

        :param date: a date in arbitrary format
        :return: a date in standard format of solr.TrieDateField e.g., 1901-11-0000T00:00:00Z
        """
        date = date[:10]  # for 14.02.1983
        date = date.replace('[', '').replace(']', '')  # for [1979]
        date = date.replace('.', '-')
        date_split = date.split('-')

        if len(date_split) == 3:
            # if date is like 28-11-1902
            if len(date_split[0]) == 1:
                date_split[0] = '0' + date_split[0]

            if len(date_split[1]) == 1:
                date_split[1] = '0' + date_split[1]

            if len(date_split[2]) == 1:
                date_split[2] = '0' + date_split[2]

            if len(date_split[0]) == 2 and len(date_split[1]) == 2 and len(date_split[2]) == 4 and date_split[
                0].isdigit() \
                    and date_split[1].isdigit() and date_split[2].isdigit():
                return date_split[2] + '-' + date_split[1] + '-' + date_split[0] + 'T00:00:00Z'

            # if date is like 1902-11-28
            if len(date_split[0]) == 4 and len(date_split[1]) == 2 and len(date_split[2]) == 2 and date_split[
                0].isdigit() \
                    and date_split[1].isdigit() and date_split[2].isdigit():
                return date + 'T00:00:00Z'


        # if date is like 1902
        if len(date) == 4 and date.isdigit():
            return '%s-00-00T00:00:00Z' % date

        if date == '':
            return '0000-00-00T00:00:00Z'

        print date, 'is not in the right format.'
        return '0000-00-00T00:00:00Z'


    def update_all_persons(self):
        print "wait for 350"
        query = "select first_name, last_name, register_id, register_type, place_1, date_1 " \
                "from all_persons_new"
        # where register_type='death'"

        cur = run_query(query)
        self.commit_number = 0

        ref_list = []
        first_flag = True
        for c in cur:
            d_id = c[2]
            register_type = c[3]
            place = c[4]
            date = c[5]

            if first_flag:
                self.place = copy.copy(place)
                self.date = copy.copy(date)
                self.register_type = copy.copy(register_type)
                self.current_document_id = copy.copy(d_id)
                first_flag = False

            if len(c[0].split()) > 0:
                first_name = c[0].split()[0].decode('utf-8', 'ignore')
            else:
                first_name = ''
            if len(c[1].split()) > 0:
                last_name = c[1].split()[-1].decode('utf-8', 'ignore')
            else:
                last_name = ''

            # if first_name and last_name:

            if d_id == self.current_document_id:
                # if we're still selecting references from current_document_id
                ref_list.append([first_name, last_name])

            else:
                # if we have moved to references of a new document_id let's first commit the previous Solr
                # features and then we make a new reference list
                self.add_key(ref_list, self.current_document_id, self.place, self.date, self.register_type)
                self.current_document_id = copy.copy(d_id)
                self.place = copy.copy(place)
                self.date = copy.copy(date)
                self.register_type = copy.copy(register_type)
                ref_list = [[first_name, last_name]]

    def update_notaries(self):
        print "wait for 39"

        query = """
                SELECT row_id, text1, text2, text3, place, date from notary_acts
                """
        cur = run_query(query)
        for c in cur.fetchall():
            notary_id = c[0] + NOTARY_OFFSET
            place = c[4]
            date = c[5]
            doc_id = 'n' + str(c[0])
            text = c[1] + ' ' + c[2] + ' ' + c[3]

            nerd = dict_based_nerd.Nerd(text)
            relations = nerd.get_relations()
            ref_list = []
            for index, rel in enumerate(relations):
                ref_list.append(Reference(str(doc_id) + str(2 * index), rel['ref1'][1]))
                ref_list.append(Reference(str(doc_id) + str(2 * index + 1), rel['ref2'][1]))

            if ref_list:
                feature_list = []
                block_keys = []
                for index in xrange(len(ref_list) / 2):
                    person_1_name = ref_list[2 * index].get_compact_name()
                    person_2_name = ref_list[2 * index + 1].get_compact_name()
                    if person_1_name and person_2_name:
                        sorted_keys = sorted([person_1_name, person_2_name])
                        blocks = sorted([get_block_key(person_1_name.split('_')[0], person_1_name.split('_')[-1]),
                                         get_block_key(person_2_name.split('_')[0], person_2_name.split('_')[-1])])
                        feature_list.append('_'.join(sorted_keys).decode('utf-8', 'ignore'))
                        block_keys.append('_'.join(blocks).decode('utf-8', 'ignore'))

                if feature_list and block_keys:
                    # TODO: get GPS location as well
                    date = self.adapt_date(date)
                    text = text.decode('utf-8', 'ignore')
                    place = place.decode('utf-8', 'ignore')
                    self.s.add(features=feature_list, features_ss=feature_list, blockKeys=block_keys, id=notary_id,
                               date_dt=date,
                               location_s=place, cat='notarial act', description=text)

            self.commit_counter += 1
            if self.commit_counter > 5000:
                self.s.commit()
                self.commit_counter = 0

                print self.commit_number
                self.commit_number += 1

    def search(self, features_list, filter_query):

        if features_list:
            query = 'features: ' + features_list + '~'

        filter_query = filter_query.split(' -')
        query_results = self.s.query(query, fq=filter_query, rows=60, highlight=True, facet='true',
                                     facet_field=['features_ss', 'location_s', 'cat'],
                                     facet_range='date_dt',
                                     facet_range_start='1700-00-00T00:00:00Z',
                                     facet_range_end='1900-00-00T00:00:00Z',
                                     facet_range_gap='+10YEAR',
                                     fields="features, id, score")

        return query_results

    def block_to_name(self, blocking_key):
        """
        Here we have a blocking_key and we want to find the feature name for it!!
        """
        query = "blockKeys:%s" % blocking_key
        results = self.s.query(query, rows=1, fields="features").results
        names = "ERROR"
        for feature in results[0]['features']:
            # Here, I want to see which feature of this document corresponds to this blocking key!

            a = get_block_key('_'.join(feature.split('_')[:2]), '_'.join(feature.split('_')[-2:]),
                              "DOCUMENT")

            b = blocking_key

            if a == b:
                names = feature.split('_')

        return [' '.join(names[:2]), ' '.join(names[-2:])]


if __name__ == '__main__':
    my_hash = Hashing()
    my_hash.update_all_persons()
    my_hash.update_notaries()
    my_hash.s.commit()
