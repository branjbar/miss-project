import copy
from modules.data_import import simple_dict_template

nsmap = '{https://maior.memorix.nl/XSI/3.0/}'


def parse_document(doc_dict, doc_type):
    """
    transfers a nested dictionary of a document to a simple dictionary
    """

    simple_dict = copy.deepcopy(simple_dict_template)
    simple_dict['uuid'] = doc_dict['@uuid']
    simple_dict['type'] = doc_type

    # parsing the marriage xml
    if doc_type == 'marriage':
        for item in doc_dict[nsmap + 'record']:
            try:

                if item.get('@label') == 'Aktenummer':
                    simple_dict['access no.'] = item.get(nsmap + 'field')[0].get('text')
            except:
                pass
            try:
                if item.get('@label') == 'Datum':
                    simple_dict['date'] = item.get(nsmap + 'field')[0].get('text')

            except:
                pass

            # extracting the location data
            if item.get('@label') == 'Register':
                for sub_item in item.get(nsmap + 'field')[0].get(nsmap + 'entity')[0].get(nsmap + 'record'):
                    try:
                        if sub_item['@label'] == 'Gemeente':
                            simple_dict['municipality'] = sub_item.get(nsmap + 'field')[0].get('text')
                    except:
                        pass


            # extracting the Groom data
            if item.get('@label') == 'Bruidegom':
                simple_dict['groom']['uuid'] = item.get(nsmap + 'field')[0].get(nsmap + 'entity')[0]['@uuid']
                for sub_item in item.get(nsmap + 'field')[0].get(nsmap + 'entity')[0].get(nsmap + 'record'):

                    if sub_item['@label'] == 'Voornaam' and sub_item.get(nsmap + 'field'):
                        simple_dict['groom']['first_name'] = sub_item.get(nsmap + 'field')[0].get('text')
                    if sub_item['@label'] == 'Achternaam' and sub_item.get(nsmap + 'field'):
                        simple_dict['groom']['last_name'] = sub_item.get(nsmap + 'field')[0].get('text')
                    if sub_item['@label'] == 'Tussenvoegsel' and sub_item.get(nsmap + 'field'):
                        simple_dict['groom']['prefix'] = sub_item.get(nsmap + 'field')[0].get('text')
                    if sub_item['@label'] == 'Geboorteplaats' and sub_item.get(nsmap + 'field'):
                        simple_dict['groom']['place'] = sub_item.get(nsmap + 'field')[0].get('text')
                    if sub_item['@label'] == 'Geboortedatum' and sub_item.get(nsmap + 'field'):
                        simple_dict['groom']['date'] = sub_item.get(nsmap + 'field')[0].get('text')

            if item.get('@label') == 'Moeder bruidegom':
                simple_dict['groom']['mother']['uuid'] = item.get(nsmap + 'field')[0].get(nsmap + 'entity')[0]['@uuid']
                for sub_item in item.get(nsmap + 'field')[0].get(nsmap + 'entity')[0].get(nsmap + 'record'):

                    if sub_item['@label'] == 'Achternaam' and sub_item.get(nsmap + 'field'):
                        simple_dict['groom']['mother']['last_name'] = sub_item.get(nsmap + 'field')[0].get('text')
                    if sub_item['@label'] == 'Voornaam' and sub_item.get(nsmap + 'field'):
                        simple_dict['groom']['mother']['first_name'] = sub_item.get(nsmap + 'field')[0].get('text')
                    if sub_item['@label'] == 'Tussenvoegsel' and sub_item.get(nsmap + 'field'):
                        simple_dict['groom']['mother']['prefix'] = sub_item.get(nsmap + 'field')[0].get('text')

            if item.get('@label') == 'Vader bruidegom':
                simple_dict['groom']['father']['uuid'] =  item.get(nsmap + 'field')[0].get(nsmap + 'entity')[0]['@uuid']
                for sub_item in item.get(nsmap + 'field')[0].get(nsmap + 'entity')[0].get(nsmap + 'record'):
                    if sub_item['@label'] == 'Achternaam' and sub_item.get(nsmap + 'field'):
                        simple_dict['groom']['father']['last_name'] = sub_item.get(nsmap + 'field')[0].get('text')
                    if sub_item['@label'] == 'Voornaam' and sub_item.get(nsmap + 'field'):
                        simple_dict['groom']['father']['first_name'] = sub_item.get(nsmap + 'field')[0].get('text')
                    if sub_item['@label'] == 'Tussenvoegsel' and sub_item.get(nsmap + 'field'):
                        simple_dict['groom']['father']['prefix'] = sub_item.get(nsmap + 'field')[0].get('text')

            if item.get('@label') == 'Bruid':

                simple_dict['bride']['uuid'] = item.get(nsmap + 'field')[0].get(nsmap + 'entity')[0]['@uuid']
                for sub_item in item.get(nsmap + 'field')[0].get(nsmap + 'entity')[0].get(nsmap + 'record'):
                    if sub_item['@label'] == 'Achternaam' and sub_item.get(nsmap + 'field'):
                            simple_dict['bride']['last_name'] = sub_item.get(nsmap + 'field')[0].get('text')
                    if sub_item['@label'] == 'Voornaam' and sub_item.get(nsmap + 'field'):
                        simple_dict['bride']['first_name'] = sub_item.get(nsmap + 'field')[0].get('text')
                    if sub_item['@label'] == 'Tussenvoegsel' and sub_item.get(nsmap + 'field'):
                        simple_dict['bride']['prefix'] = sub_item.get(nsmap + 'field')[0].get('text')
                    if sub_item['@label'] == 'Geboorteplaats' and sub_item.get(nsmap + 'field'):
                        simple_dict['bride']['place'] = sub_item.get(nsmap + 'field')[0].get('text')
                    if sub_item['@label'] == 'Geboortedatum' and sub_item.get(nsmap + 'field'):
                        simple_dict['bride']['date'] = sub_item.get(nsmap + 'field')[0].get('text')

            if item.get('@label') == 'Moeder bruid':
                simple_dict['bride']['mother']['uuid'] = item.get(nsmap + 'field')[0].get(nsmap + 'entity')[0]['@uuid']
                for sub_item in item.get(nsmap + 'field')[0].get(nsmap + 'entity')[0].get(nsmap + 'record'):

                    if sub_item['@label'] == 'Achternaam' and sub_item.get(nsmap + 'field'):
                        simple_dict['bride']['mother']['last_name'] = sub_item.get(nsmap + 'field')[0].get('text')
                    if sub_item['@label'] == 'Voornaam' and sub_item.get(nsmap + 'field'):
                        simple_dict['bride']['mother']['first_name'] = sub_item.get(nsmap + 'field')[0].get('text')
                    if sub_item['@label'] == 'Tussenvoegsel' and sub_item.get(nsmap + 'field'):
                        simple_dict['bride']['mother']['prefix'] = sub_item.get(nsmap + 'field')[0].get('text')

            if item.get('@label') == 'Vader bruid':
                simple_dict['bride']['father']['uuid'] = item.get(nsmap + 'field')[0].get(nsmap + 'entity')[0]['@uuid']
                for sub_item in item.get(nsmap + 'field')[0].get(nsmap + 'entity')[0].get(nsmap + 'record'):

                    if sub_item['@label'] == 'Achternaam' and sub_item.get(nsmap + 'field'):
                        simple_dict['bride']['father']['last_name'] = sub_item.get(nsmap + 'field')[0].get('text')
                    if sub_item['@label'] == 'Voornaam' and sub_item.get(nsmap + 'field'):
                        simple_dict['bride']['father']['first_name'] = sub_item.get(nsmap + 'field')[0].get('text')
                    if sub_item['@label'] == 'Tussenvoegsel' and sub_item.get(nsmap + 'field'):
                        simple_dict['bride']['father']['prefix'] = sub_item.get(nsmap + 'field')[0].get('text')

    # parsing the birth xml
    if doc_type == 'birth':

        for item in doc_dict[nsmap + 'record']:
            try:
                if item.get('@label') == 'Aktenummer':
                    simple_dict['access no.'] = item.get(nsmap + 'field')[0].get('text')
            except:
                pass

            # extracting the location data
            try:
                if item.get('@label') == 'Register':
                    for sub_item in item.get(nsmap + 'field')[0].get(nsmap + 'entity')[0].get(nsmap + 'record'):
                        try:
                            if sub_item['@label'] == 'Gemeente':
                                simple_dict['municipality'] = sub_item.get(nsmap + 'field')[0].get('text')
                        except:
                            pass
            except:
                pass


            # extracting the kid data
            if item.get('@label') == 'Kind':
                simple_dict['child']['uuid'] = item.get(nsmap + 'field')[0].get(nsmap + 'entity')[0]['@uuid']
                for sub_item in item.get(nsmap + 'field')[0].get(nsmap + 'entity')[0].get(nsmap + 'record'):

                    if sub_item['@label'] == 'Datum geboorte' and sub_item.get(nsmap + 'field'):
                        simple_dict['date'] = sub_item.get(nsmap + 'field')[0].get('text')
                    if sub_item['@label'] == 'Geslacht' and sub_item.get(nsmap + 'field'):
                        simple_dict['child']['gender'] = sub_item.get(nsmap + 'field')[0].get('text')
                    if sub_item['@label'] == 'Voornaam' and sub_item.get(nsmap + 'field'):
                        simple_dict['child']['first_name'] = sub_item.get(nsmap + 'field')[0].get('text')
                    if sub_item['@label'] == 'Achternaam' and sub_item.get(nsmap + 'field'):
                        simple_dict['child']['last_name'] = sub_item.get(nsmap + 'field')[0].get('text')
                    if sub_item['@label'] == 'Tussenvoegsel' and sub_item.get(nsmap + 'field'):
                        simple_dict['child']['prefix'] = sub_item.get(nsmap + 'field')[0].get('text')

            if item.get('@label') == 'Moeder':
                simple_dict['mother']['uuid'] = item.get(nsmap + 'field')[0].get(nsmap + 'entity')[0]['@uuid']
                for sub_item in item.get(nsmap + 'field')[0].get(nsmap + 'entity')[0].get(nsmap + 'record'):
                    if sub_item['@label'] == 'Voornaam' and sub_item.get(nsmap + 'field'):
                        simple_dict['mother']['first_name'] = sub_item.get(nsmap + 'field')[0].get('text')
                    if sub_item['@label'] == 'Achternaam' and sub_item.get(nsmap + 'field'):
                        simple_dict['mother']['last_name'] = sub_item.get(nsmap + 'field')[0].get('text')
                    if sub_item['@label'] == 'Tussenvoegsel' and sub_item.get(nsmap + 'field'):
                        simple_dict['mother']['prefix'] = sub_item.get(nsmap + 'field')[0].get('text')


            if item.get('@label') == 'Vader':
                if item.get(nsmap + 'field'):
                    simple_dict['father']['uuid'] = item.get(nsmap + 'field')[0].get(nsmap + 'entity')[0]['@uuid']
                    for sub_item in item.get(nsmap + 'field')[0].get(nsmap + 'entity')[0].get(nsmap + 'record'):
                        if sub_item['@label'] == 'Voornaam' and sub_item.get(nsmap + 'field'):
                            simple_dict['father']['first_name'] = sub_item.get(nsmap + 'field')[0].get('text')
                        if sub_item['@label'] == 'Achternaam' and sub_item.get(nsmap + 'field'):
                            simple_dict['father']['last_name'] = sub_item.get(nsmap + 'field')[0].get('text')
                        if sub_item['@label'] == 'Tussenvoegsel' and sub_item.get(nsmap + 'field'):
                            simple_dict['father']['prefix'] = sub_item.get(nsmap + 'field')[0].get('text')


    # parsing the death xml
    if doc_type == 'death':

        for item in doc_dict[nsmap + 'record']:
            try:
                if item.get('@label') == 'Aktenummer':
                    simple_dict['access no.'] = item.get(nsmap + 'field')[0].get('text')
            except:
                pass

            # extracting the location data
            try:
                if item.get('@label') == 'Register':
                    for sub_item in item.get(nsmap + 'field')[0].get(nsmap + 'entity')[0].get(nsmap + 'record'):
                        try:
                            if sub_item['@label'] == 'Gemeente':
                                simple_dict['municipality'] = sub_item.get(nsmap + 'field')[0].get('text')
                        except:
                            pass
            except:
                pass


            # extracting the kid data
            if item.get('@label') == 'Overledene':
                simple_dict['child']['uuid'] = item.get(nsmap + 'field')[0].get(nsmap + 'entity')[0]['@uuid']
                for sub_item in item.get(nsmap + 'field')[0].get(nsmap + 'entity')[0].get(nsmap + 'record'):

                    if sub_item['@label'] == 'Datum overlijden' and sub_item.get(nsmap + 'field'):
                        simple_dict['date'] = sub_item.get(nsmap + 'field')[0].get('text')
                    if sub_item['@label'] == 'Geslacht' and sub_item.get(nsmap + 'field'):
                        simple_dict['child']['gender'] = sub_item.get(nsmap + 'field')[0].get('text')
                    if sub_item['@label'] == 'Voornaam' and sub_item.get(nsmap + 'field'):
                        simple_dict['child']['first_name'] = sub_item.get(nsmap + 'field')[0].get('text')
                    if sub_item['@label'] == 'Achternaam' and sub_item.get(nsmap + 'field'):
                        simple_dict['child']['last_name'] = sub_item.get(nsmap + 'field')[0].get('text')
                    if sub_item['@label'] == 'Tussenvoegsel' and sub_item.get(nsmap + 'field'):
                        simple_dict['child']['prefix'] = sub_item.get(nsmap + 'field')[0].get('text')

            if item.get('@label') == 'Moeder':
                simple_dict['mother']['uuid'] = item.get(nsmap + 'field')[0].get(nsmap + 'entity')[0]['@uuid']
                for sub_item in item.get(nsmap + 'field')[0].get(nsmap + 'entity')[0].get(nsmap + 'record'):
                    if sub_item['@label'] == 'Voornaam' and sub_item.get(nsmap + 'field'):
                        simple_dict['mother']['first_name'] = sub_item.get(nsmap + 'field')[0].get('text')
                    if sub_item['@label'] == 'Achternaam' and sub_item.get(nsmap + 'field'):
                        simple_dict['mother']['last_name'] = sub_item.get(nsmap + 'field')[0].get('text')
                    if sub_item['@label'] == 'Tussenvoegsel' and sub_item.get(nsmap + 'field'):
                        simple_dict['mother']['prefix'] = sub_item.get(nsmap + 'field')[0].get('text')


            if item.get('@label') == 'Vader':
                if item.get(nsmap + 'field'):
                    simple_dict['father']['uuid'] = item.get(nsmap + 'field')[0].get(nsmap + 'entity')[0]['@uuid']
                    for sub_item in item.get(nsmap + 'field')[0].get(nsmap + 'entity')[0].get(nsmap + 'record'):
                        if sub_item['@label'] == 'Voornaam' and sub_item.get(nsmap + 'field'):
                            simple_dict['father']['first_name'] = sub_item.get(nsmap + 'field')[0].get('text')
                        if sub_item['@label'] == 'Achternaam' and sub_item.get(nsmap + 'field'):
                            simple_dict['father']['last_name'] = sub_item.get(nsmap + 'field')[0].get('text')
                        if sub_item['@label'] == 'Tussenvoegsel' and sub_item.get(nsmap + 'field'):
                            simple_dict['father']['prefix'] = sub_item.get(nsmap + 'field')[0].get('text')

            if item.get('@label') == 'Relatie':

                if item.get(nsmap + 'field'):
                    simple_dict['relative']['uuid'] = item.get(nsmap + 'field')[0].get(nsmap + 'entity')[0]['@uuid']
                    for sub_item in item.get(nsmap + 'field')[0].get(nsmap + 'entity')[0].get(nsmap + 'record'):
                        if sub_item['@label'] == 'Voornaam' and sub_item.get(nsmap + 'field'):
                            simple_dict['relative']['first_name'] = sub_item.get(nsmap + 'field')[0].get('text')
                        if sub_item['@label'] == 'Achternaam' and sub_item.get(nsmap + 'field'):
                            simple_dict['relative']['last_name'] = sub_item.get(nsmap + 'field')[0].get('text')
                        if sub_item['@label'] == 'Tussenvoegsel' and sub_item.get(nsmap + 'field'):
                            simple_dict['relative']['prefix'] = sub_item.get(nsmap + 'field')[0].get('text')
    return simple_dict