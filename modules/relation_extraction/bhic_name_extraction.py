import json
from urllib import urlopen
from modules.basic_modules.myOrm import get_notarial_act

__author__ = 'bijan'


def parse_notarial_acts(N=200922):
    """
    parses through a list of notarial acts and for each notarial act, uses the api to retrieve the relationships
    N: last record
    :return:
    """
    csv_text = ';'.join(["id","person_1_given_name", "person_1_prefix", "person_1_family_name", \
        "person_2_given_name", "person_2_prefix", "person_2_family_name", \
        "Relationship Type", "Evidence", "Location", "Date", "notary_id", "Nummer", "FOLIO", "FOLIOTOT", "TOEGANG", "\n"])

    relation_id = 0
    with open("relationship_evidence.csv", "a") as my_file:
        my_file.write(csv_text)

    for row_id in xrange(1, N):
        text_record = get_notarial_act(row_id)
        details = [text_record['place'], text_record['date'], str(text_record['id']), text_record['Nummer'],text_record['FOLIO'],text_record['FOLIOTOT'],text_record['TOEGANG']]
        txt = text_record['text1'] + ' ' + text_record['text2'] + ' ' + text_record['text3']

        url = 'http://swarmlab-srv01.unimaas.nl:20002/miss/ner/api/v1.0/miss_api_text?q=' + txt
        url = url.encode('utf-8').replace('\\', '')
        jsonurl = urlopen(url)
        json_data = json.loads(jsonurl.read())


        for rel in json_data["relationships"]:
            ref1 = split_full_name(rel['ref1']['name'])
            ref2 = split_full_name(rel['ref2']['name'])

            relation_id += 1
            csv_text = str(relation_id) + ';'
            csv_text += '; '.join(ref1) + ';'
            csv_text += '; '.join(ref2) + ';'
            csv_text += rel['type'] + ';'
            evidence_text = ' '.join(json_data['text'].split()[
                                     rel['ref1']['position'] + len(rel['ref1']['name'].split()):rel['ref2'][
                                         'position']])
            csv_text += evidence_text + ';'
            csv_text += ';'.join(details)
            csv_text += '\n'

            with open("relationship_evidence.csv", "a") as my_file:
                my_file.write(csv_text)



def split_full_name(full_name):
    """
    uses a simple hueristic to split a full name into given name, prefix, family name
    :param full_name:
    :return:
    """

    family_name = full_name.split()[-1]
    prefix_start = -1
    for iter, word in enumerate(full_name.split()[:-1]):
        if not word[0].isupper():
            prefix_start = iter
            break

    given_name = ' '.join(full_name.split()[:prefix_start])
    prefix = ' '.join(full_name.split()[prefix_start:-1])

    return [given_name.strip(), prefix.strip(), family_name.strip()]




if __name__ == "__main__":
    parse_notarial_acts(10000)
