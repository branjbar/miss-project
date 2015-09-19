__author__ = 'bian'

dict_keys = ['den_T1', 'gehuwd_T1', 'weduwe_T1', 'kinderen_T1', 'vrouw_T1', 'wijlen_T1', 'bouwman_T1', 'verkocht_T1',
             'verzoek_T1', 'ouders_T1', 'verkopen_T1', 'landbouwer_T1', 'schuldig_T1', 'wonende_T1', 'voogd_T1',
             'echtelieden_T1', 'goederen_T1', 'repertorium_T1', 'erfgenamen_T1', 'verkoopt_T1', 'bouwlieden_T1',
             'man_T1', 'genaamd_T1', 'allen_T1', 'minderjarige_T1', 'weduwnaar_T1', 'nalatenschap_T1', 'grenzend_T1',
             'gelaste_T1', 'bekent_T1', 'borgen_T1', 'echtgenote_T1', 'beroep_T1', 'ten_T1', 'zoon_T1', 'oost_T1',
             'personen_T1', 'aangekomen_T1', 'west_T1', 'name_T1', 'broer_T1', 'zuid_T1', 'dochter_T1', 'notaris_T1',
             'arbeider_T1', 'perceel_T1', 'naast_T1', 'huwelijk_T1', 'zus_T1', 'overleden_T1', 'weduwe_T2', 'gehuwd_T2',
             'bouwman_T2', 'vrouw_T2', 'landbouwer_T2', 'wonende_T2', 'den_T2', 'genaamd_T2', 'kinderen_T2',
             'bouwland_T2', 'verkopen_T2', 'huis_T2', 'perceel_T2', 'verkocht_T2', 'wijlen_T2', 'voogd_T2',
             'weiland_T2', 'schuldig_T2', 'land_T2', 'verkoopt_T2', 'groot_T2', 'onder_T2', 'allen_T2', 'goederen_T2',
             'echtgenote_T2', 'bouwlieden_T2', 'beroep_T2', 'morgen_T2', 'bouw_T2', 'grenzend_T2', 'gulden_T2',
             'echtelieden_T2', 'gelegen_T2', 'man_T2', 'overleden_T2', 'ten_T2', 'erfgenamen_T2', 'oost_T2', 'erf_T2',
             'west_T2', 'zuid_T2', 'aangekomen_T2', 'noord_T2', 'minderjarige_T2', 'gemeente_T2', 'erfgenaam_T2',
             'ouders_T2', 'bekent_T2', 'vader_T2', 'twee_T2', 'gehuwd_T3', 'bouwman_T3', 'den_T3', 'wonende_T3',
             'weduwe_T3', 'verkopen_T3', 'landbouwer_T3', 'allen_T3', 'bouwlieden_T3', 'echtelieden_T3', 'huis_T3',
             'vrouw_T3', 'perceel_T3', 'bouwland_T3', 'beiden_T3', 'overleden_T3', 'voogd_T3', 'kinderen_T3',
             'verkocht_T3', 'beroep_T3', 'weiland_T3', 'land_T3', 'verkoopt_T3', 'landbouwers_T3', 'schepenen_T3',
             'landbouwster_T3', 'goederen_T3', 'schuldig_T3', 'genaamd_T3', 'koopman_T3', 'wonend_T3', 'wijlen_T3',
             'man_T3', 'arbeider_T3', 'bouwvrouw_T3', 'toeziende_T3', 'gulden_T3', 'zuid_T3', 'name_T3', 'delen_T3',
             'noord_T3', 'bouw_T3', 'onder_T3', 'erfgenamen_T3', 'som_T3', 'groot_T3', 'bekennen_T3', 'bijwezen_T3',
             'roerende_T3', 'betreft_T3']  # ,'T1_size','T2_size','T3_size','sup_e1','sup_e2','sup_e1_e2','classLabel']

from sklearn.externals import joblib
clf = joblib.load('pickled_decision_tree_on_weka_dataset.pkl')

import random
from modules.NERD.dict_based_nerd import Nerd

from modules.basic_modules import myOrm

# fd = open('hossein_text_%.0f.csv' % (100.0 * random.random()), 'a')
fd = open('evaluation_1800_true.csv' , 'a')
fd.write('TRUE|negative|positve|date|phrase|text|row_id|uuid\n')
count = 0

for tmp in xrange(100000):
    if count > 500:
        break
    t_id = random.randrange(0, 200000)
    print t_id
    # if not t_id % 100:
    # print t_id, count
    act = myOrm.get_notarial_act(t_id, century18=False)
    extra_condition = ('17' in act['date'][-4:-2])
    if act and extra_condition:
        text = act['text1'] + ' ' + act['text2'] + act['text3']

        nerd = Nerd(text)
        # nerd.extract_relations()
        # nerd.extract_solr_relations(negative_samples=True)
        nerd.extract_references()
        nerd.get_potential_relations()
        # for index, rel in enumerate(nerd.get_relations()):
        if nerd.get_relations():
            rel = nerd.get_relations()[0]
            before_text = ' '.join(nerd.pp_text.split()[max(0, rel['ref1'][0] - 10):rel['ref1'][0]])
            middle_text = ' '.join(nerd.pp_text.split()[rel['ref1'][0] + len(rel['ref1'][1].split()):rel['ref2'][0]])
            after_text = ' '.join(nerd.pp_text.split()[
                                  rel['ref2'][0] + len(rel['ref2'][1].split()):rel['ref2'][0] + len(
                                      rel['ref2'][1].split()) + 10])

            before_text_n = ' '.join(
                before_text.replace(',', '').replace('.', '').replace(';', '').replace(' ', ' ').strip().split()[-5:])
            middle_text_n = middle_text.replace(',', '').replace('.', '').replace(';', '').replace(' ', ' ').strip()
            after_text_n = ' '.join(
                after_text.replace(',', '').replace('.', '').replace(';', '').replace(' ', ' ').strip().split()[:5])

            vector = []
            for key in dict_keys:
                if 'T1' in key:
                    if key[:-3] in before_text_n.split():
                        vector.append(1)
                    else:
                        vector.append(0)
                if 'T2' in key:
                    if key[:-3] in middle_text_n.split():
                        vector.append(1)
                    else:
                        vector.append(0)
                if 'T3' in key:

                    if key[:-3] in after_text_n.split():
                        vector.append(1)
                    else:
                        vector.append(0)

            vector += [len(before_text_n.split()), len(middle_text_n.split()), len(after_text_n.split())]


            #print vector
            if clf.predict(vector)[0]:
                # print clf.predict(vector), clf.predict_proba(vector)
                csv_line = "1|%d|%d|%s|%s [%s] %s [%s] %s|%s|%d|%d\n" % (clf.predict_proba(vector)[0][0]*100,clf.predict_proba(vector)[0][1]*100,
                                                                   act['date'], before_text, rel['ref1'][1], middle_text, rel['ref2'][1], after_text,
                                                                   text, t_id, act['id'])
            #
            # csv_line = "%d;%s;%s;%s;%s;%d;%d;%d;%d;%d;%d;%s;%d;%s;%d;%s\n" %\
            #            (count,
            #             before_text_n,
            #             middle_text_n,
            #             after_text_n,
            #             act['AKTETYPE'],
            #             len(before_text_n.split()),
            #             len(middle_text_n.split()),
            #             len(after_text_n.split()),
            #             0,
            #             0,
            #             0,
            #             '',
            #             t_id,
            #             act['id'],
            #             index,
            #             '')
            #print csv_line
                count += 1
                fd.write(csv_line)
