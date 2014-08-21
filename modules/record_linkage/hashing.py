from modules.basic_modules.basic import run_query

__author__ = 'bijan'


query = "select first_name, last_name, register_id from all_persons_new limit 100000"

cur = run_query(query)
hashing_table_first_name = {}
hashing_table_last_name = {}
count = 0
for c in cur:
    d_id = c[2]
    try:
        first_name = c[0].split()[0]
        hashing_table_first_name[first_name] = hashing_table_first_name.get(first_name,[]) + [d_id]
        hashing_table_first_name[first_name] = list(set(hashing_table_first_name[first_name]))
    except:
        pass
    try:
        last_name = c[1].split()[-1]
        hashing_table_last_name[last_name] = hashing_table_last_name.get(last_name,[]) + [d_id]
        hashing_table_last_name[last_name] = list(set(hashing_table_last_name[last_name]))
    except:
        pass


print hashing_table_first_name
# print hashing_table_last_name

