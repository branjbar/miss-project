"""
 DecisionTreeClassifier take as input two arrays: an array X of size [n_samples, n_features]  and an array Y of integer values, size [n_samples]
"""

import csv

x = []
y = []
with open('weka_file_generated_V_2.csv', 'rb') as csvfile:
    spamreader = csv.reader(csvfile, delimiter=',', quotechar=",")
    header = True
    for row in spamreader:
        if header:
            header_cells = []
            for c in row[:-4] + [row[-1]]:
                header_cells.append(c.replace("'", ''))

            header = False
        else:
            this_row = []
            for c in row[:-4] + [row[-1]]:
                try:
                    this_row.append(int(c.replace("'", '')))
                except:
                    if c == "'negative'":
                        y.append(0)
                    else:
                        y.append(1)

            x.append(this_row)

from sklearn import tree
clf = tree.DecisionTreeClassifier(criterion='entropy', splitter='best', max_depth=4, min_samples_split=2,
                                  min_samples_leaf=1, max_features=None, random_state=None, min_density=None,
                                  compute_importances=None, max_leaf_nodes=None)
clf = clf.fit(x, y)
number_of_samples = len(y)
# from sklearn import cross_validation
# print "Doing Cross Validation ..."
# print cross_validation.cross_val_score(clf, x, y, cv=10)
#
with open("iris.dot", 'w') as f:
    f = tree.export_graphviz(clf, out_file=f)


import fileinput
import re

for line in fileinput.input("iris.dot", inplace=True):
    for index, h in enumerate(header_cells):
        line = line.replace('X[%d] <= 0.5000' % index, "if '%s' doens't exist / exists" % h)
        line = line.replace('X[%d]' % index, "if '%s'" % h)
    if '.]' in line:
        searching = re.search('(.*)\[(.*?)\. (.*?)\.', line)
        c1 = int(searching.group(2))
        c2 = int(searching.group(3))
        color = hex(int(220 - 220 * (c1 + c2)/number_of_samples))[2:]
        if len(color) == 1:
            color = '0' + color
        if c1 > c2:
            line = line[:-4] + ', style="filled", fillcolor="#FF%s%s"];' % (color, color)
        else:
            line = line[:-4] + ', style="filled", fillcolor="#%sFF%s"];' % (color, color)
    #
    # if 'samples' in line:
    #     searching = re.search('(.*)samples = (.*?)"', line)
    #     line = line.replace(searching.group(2), "%.2f\%" % (int(searching.group(2))/number_of_samples))
    #     # line = line.replace(searching.group(2)[:-8], str(int(searching.group(2)[:-8])/1.0/number_of_samples))

    print line