__author__ = 'Bijan'

from modules.basic_modules import basic
from modules.basic_modules.basic import log
from modules.record_linkage.nerd import html_generate


log('importing names')
the_query = "SELECT name, type FROM meertens_names"
cur = basic.run_query(None, the_query)
name_dict = {}
name_list = []
for c in cur.fetchall():
    name_dict[c[0].lower()] = c[1]
    name_list.append(c[0].lower())

log('importing notarial acts')
the_query = "SELECT inhoud1, inhoud2, inhoud3, datering, plaats from notary_acts"
cur = basic.run_query(None, the_query)
notarial_list = []
for c in cur.fetchall()[:1000]:
    # each notarial_list element is [text, date, place]
    notarial_list.append([c[0] + ' ' + c[1] + ' ' + c[2], c[3], c[4]])

log('extracting names')
output = []
for n in notarial_list:
    text = n[0]
    index_dict = {}
    text = basic.text_pre_processing(text)
    for index, word in enumerate(text.split()):
        if name_dict.get(word.lower()):
            index_dict[index] = name_dict.get(word.lower())
    output.append([text, index_dict])

html_generate.export_html(output)