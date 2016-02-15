import json
from urllib import urlopen
from modules.basic_modules.myOrm import get_notarial_act

__author__ = 'bijan'



def parse_notarial_acts_for_names(N=200922):
    """
    parses through a list of notarial acts and for each notarial act, uses the api to retrieve the names
    N: last record
    :return:
    """
    csv_text = ';'.join(["id", "Given Name", "Prefix", "Family Name", "Evidence", "Location", "Date", "Notary_id", "Nummer", "FOLIO",
                         "FOLIOTOT", "TOEGANG", "text", "\n"])

    with open("name_extraction.csv", "a") as my_file:
        my_file.write(csv_text)

    name_id = 0
    for row_id in xrange(1, N):
        text_record = get_notarial_act(row_id)
        txt = text_record['text1'] + ' ' + text_record['text2'] + ' ' + text_record['text3']
        details = [text_record['place'], text_record['date'], str(text_record['id']), text_record['Nummer'],
                   text_record['FOLIO'], text_record['FOLIOTOT'], text_record['TOEGANG'], txt]

        url = 'http://swarmlab-srv01.unimaas.nl:20002/miss/ner/api/v1.0/miss_api_text?q=' + txt
        url = url.encode('utf-8').replace('\\', '')
        jsonurl = urlopen(url)
        json_data = json.loads(jsonurl.read())
        for extracted_ref in json_data.get("named_individuals",[]):
            ref = split_full_name(extracted_ref['name'])


            # all prefix words should start with small letter, otherwise something is going wrong!
            if ref[0].split() and not all([w[0].isupper() for w in ref[0].split()]):
                print "ERROR: Bad Extraction in first name ", '; '.join(ref)
                break
            if ref[1].split() and not all([w[0].islower() for w in ref[1].split()]):
                print "ERROR: Bad Extraction in prefix ", '; '.join(ref)
                break

            name_id += 1
            csv_text = str(name_id) + ';'
            csv_text += ';'.join(ref) + ';'
            start = max(extracted_ref['position'] - 2,0)
            end = extracted_ref['position'] + len(extracted_ref['name'].split())+2
            evidence_text = ' '.join(json_data['text'].split()[start : end ])
            csv_text += evidence_text + ';'
            csv_text += ';'.join(details)
            csv_text += '\n'

            with open("name_extraction.csv", "a") as my_file:
                my_file.write(csv_text)



def parse_notarial_acts_for_relationships(N=200922):
    """
    parses through a list of notarial acts and for each notarial act, uses the api to retrieve the relationships
    N: last record
    :return:
    """
    csv_text = ';'.join(["id", "person_1_given_name", "person_1_prefix", "person_1_family_name", \
                         "person_2_given_name", "person_2_prefix", "person_2_family_name", \
                         "Relationship Type", "Evidence", "Location", "Date", "notary_id", "Nummer", "FOLIO",
                         "FOLIOTOT", "TOEGANG", "\n"])

    with open("relationship_evidence.csv", "a") as my_file:
        my_file.write(csv_text)

    relation_id = 0
    for row_id in xrange(1, N):
        text_record = get_notarial_act(row_id)
        details = [text_record['place'], text_record['date'], str(text_record['id']), text_record['Nummer'],
                   text_record['FOLIO'], text_record['FOLIOTOT'], text_record['TOEGANG']]
        txt = text_record['text1'] + ' ' + text_record['text2'] + ' ' + text_record['text3']

        url = 'http://swarmlab-srv01.unimaas.nl:20002/miss/ner/api/v1.0/miss_api_text?q=' + txt
        url = url.encode('utf-8').replace('\\', '')
        jsonurl = urlopen(url)
        json_data = json.loads(jsonurl.read())

        for rel in json_data.get("relationships",[]):
            ref1 = split_full_name(rel['ref1']['name'])
            ref2 = split_full_name(rel['ref2']['name'])


            # all prefix words should start with small letter, otherwise something is going wrong!
            if ref1[0].split() and not all([w[0].isupper() for w in ref1[0].split()]):
                print "ERROR: Bad Extraction in ", '; '.join(ref1)
                break
            if ref2[0].split() and not all([w[0].isupper() for w in ref2[0].split()]):
                print "ERROR: Bad Extraction in ", '; '.join(ref2)
                break

            relation_id += 1
            csv_text = str(relation_id) + ';'
            csv_text += ';'.join(ref1) + ';'
            csv_text += ';'.join(ref2) + ';'
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
    
    
    please note that except from 0.17% of family names, for the rest each family name is a single word!  
    :param full_name:
    :return:
    """

    family_name = full_name.split()[-1]
    prefix_start = -1
    flag = False
    for iter, word in enumerate(reversed(full_name.split()[:-1])):
        if not flag and not word[0].isupper():
            flag = True

        if flag and word[0].isupper():
            prefix_start = len(full_name.split()) - iter - 1
            break

    given_name = ' '.join(full_name.split()[:prefix_start])
    prefix = ' '.join(full_name.split()[prefix_start:-1])
    return [given_name.strip(), prefix.strip(), family_name.strip()]


if __name__ == "__main__":
    parse_notarial_acts_for_names(10000)
