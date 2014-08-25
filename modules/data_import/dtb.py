__author__ = 'bijan'

# from xml.dom import minidom
# xmldoc = minidom.parse('/Users/bijan/Desktop/DTB/DTB-B_bc5b1c61-bc40-4c1f-09fb-44dbe175af9c.xml')
# print xmldoc
# itemlist = xmldoc.getElementsByTagName('item')
# print len(itemlist)
# print itemlist[0].attributes['name'].value
# for s in itemlist[:100] :
#     print s.attributes['name'].value


# mport xml.etree.ElementTree as etree
# data = etree.parse('a_very_big.xml')

#
xmldoc = '/Users/bijan/Desktop/DTB/DTB-B_bc5b1c61-bc40-4c1f-09fb-44dbe175af9c.xml'
import xml.etree.ElementTree as etree
context = etree.iterparse(xmldoc, events=("start", "end"))

for event, elem in context:


    tag = elem.tag
    value = elem.text

    # if value:
    #     value = value.encode('utf-8').strip()

    # if event == 'start' :
    #     print elem.attrib.get('label'), value, 'start'
    #
    #
    # if event == 'end':
    #     print elem.attrib.get('label'), value, 'end'
    elem.clear()