file_name = '../../data/new_bhic_data/BR-reg_dbdeec05-1863-9fe8-ee53-30c8cb008d3e.xml'
file_name = '../../data/new_bhic_data/BR-birth.xml'
import xml.etree.ElementTree as etree
import pprint

# nsmap = {}
#for event, elem in etree.iterparse(file_name, events=('start-ns','end-ns')):
#
#  if event == 'start-ns':
#      ns, url = elem
#      nsmap[ns] = url
#print nsmap

nsmap = {'': 'https://maior.memorix.nl/XSI/3.0/', u'xsi': 'http://www.w3.org/2001/XMLSchema-instance', u'dc': 'http://purl.org/dc\
/elements/1.1/'}


def etree_to_dict(t):

    d = {t.tag : map(etree_to_dict, t.getchildren())}
    d.update(('@' + k, v) for k, v in t.attrib.iteritems())
    d['text'] = t.text
    return d



count = 1
depth = 0
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
            dict = etree_to_dict(elem)
            parse_document(dict)


            # print process_element(elem)
            elem.clear()

    #print depth, event, elem
    #print depth, elemtag
    count += 1
    if count > 100000:
        break

