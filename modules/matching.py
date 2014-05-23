__author__ = 'Bijan'


from modules import basic
import time
db = basic.do_connect()

query = "select id, block_key, document_id from all_persons_features limit 1000000"
cur = basic.run_query(db, query)



block_dict = {}
t = time.time()
for block_row in cur.fetchall():

    if block_dict.get(block_row[1]):
        block_dict[block_row[1]].append([block_row[0],block_row[2]])
    else:
        if block_row:
            block_dict[block_row[1]] = [[block_row[0],block_row[2]]]

print 'elapsed time: ', time.time() - t
print len(block_dict)


t = time.time()
doc_dict = {}
for b in block_dict.keys():
    if b:
        for doc1 in block_dict[b]:
            for doc2 in block_dict[b]:
                if not doc1 is doc2:
                    key = str(doc1[1]) + '_' + str(doc2[1])
                    if doc_dict.get(key) and not b in doc_dict[key]:
                        doc_dict[key].append(b)
                        print (doc1[0], doc2[0]),'<-', b
                    else:
                        doc_dict[key] = [b]


print 'elapsed time: ', time.time() - t
print len(doc_dict)
# print doc_dict
