import json
from urllib import urlopen

__author__ = 'bian'


def parse_notarial_acts():
    """
    parses through a list of notarial acts and for each notarial act, uses the api to retrieve the relationships
    :return:
    """
    notary_text_list = ["Bijan Ranjbar en zijn vrouw Hoda Sharei."]
    json_data_list = []
    for txt in notary_text_list:

        url = 'http://swarmlab-srv01.unimaas.nl:20002/miss/ner/api/v1.0/miss_api_text?q=' + txt
        url = url.encode('utf-8').replace('\\','')
        jsonurl = urlopen(url)
        json_data = json.loads(jsonurl.read())
        json_data_list.append(json_data)

    return json_data_list

def generate_records(json_data_list):
    """
    gets a list of json data and for each record generates one evidence of relationship
    :param json_data_list:
    :return:
    """
    for json_data in json_data_list:
        for rel in json_data["relationships"]:
            print rel['ref1']['name'],
            print rel['type'],
            print rel['ref2']['name'],




if __name__ == "__main__":

    json_data_list = parse_notarial_acts()
    generate_records(json_data_list)