from modules.data_import.parse_document import parse_document
from modules.data_import.write_sql import add_to_sql

import xml.etree.ElementTree as etree
import pprint

# nsmap = {}
# for event, elem in etree.iterparse(file_name, events=('start-ns','end-ns')):
#
#  if event == 'start-ns':
#      ns, url = elem
#      nsmap[ns] = url
#print nsmap

nsmap = {'': 'https://maior.memorix.nl/XSI/3.0/', u'xsi': 'http://www.w3.org/2001/XMLSchema-instance', u'dc': 'http://purl.org/dc\
/elements/1.1/'}


def etree_to_dict(t):
    d = {t.tag: map(etree_to_dict, t.getchildren())}
    d.update(('@' + k, v) for k, v in t.attrib.iteritems())
    d['text'] = t.text
    return d


pp = pprint.PrettyPrinter(indent=4)


def xml_to_sql(doc_type, person_id, test=False):
    """
    imports the most recent xml dumps of BHIC center
    """
    file_name = '/Users/bijan/sandbox/bhic_data/BS-%s.xml' % doc_type

    document_id = person_id  # initialization
    count = 1  # a counter to stop the running in case of testing
    depth = 0  # a counter to figure out when each xml element is finished.
    for event, elem in etree.iterparse(file_name, events=('end', 'start', 'start-ns')):
        try:
            elemtag = elem.tag.split('}')[1]
        except:
            elemtag = ''

        if event == 'start' and elemtag == 'record':
            depth += 1
        if event == 'end' and elemtag == 'record':
            depth -= 1
            if depth == 0:
                dict = etree_to_dict(elem)  # converts the xml to a nested dict
                simple_dict = parse_document(dict, doc_type)  # simplifies the nested dict and returns a simple dict
                # pp.pprint(simple_dict)

                add_to_sql(person_id, document_id, simple_dict, doc_type)


                if doc_type == 'birth':
                    person_id += 3
                if doc_type == 'marriage':
                    person_id += 6
                if doc_type == 'death':
                    person_id += 4
                document_id += 1


                elem.clear()
        if test:
            count += 1
            if count > 10000:
                break


if __name__ == '__main__':
    offset = {'birth': 1, 'marriage': 30000001, 'death': 60000001}  # this offset separates documents based on their type

    doc_type = 'birth'
    xml_to_sql(doc_type, offset[doc_type], True)