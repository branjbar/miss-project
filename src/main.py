'''
Created on Feb 7, 2014

@author: Bijan
'''
def check_a_random_pair():
    
    from modules import basic
    db = basic.do_connect()
    
    ref1 = basic.get_person(db)
    ref2 = basic.get_person(db)
       
    score_0 = basic.get_match_score(db, ref1, ref2, 0)
    print ref1,'\n', ref2, '\nscore_0 is ', score_0  
    score_1 = basic.get_match_score(db, ref1, ref2, 1)
    print 'score_1 is ', score_1 
    score_2 = basic.get_match_score(db, ref1, ref2, 2)
    print 'score_2 is', score_2 


def do_matching():
    from modules import basic
    db = basic.do_connect()
    basic.do_matching(db)
    
    
if __name__ == '__main__':
    do_matching()
#     from modules import basic
#     db = basic.do_connect()
#     basic.generate_relations(db,'birth')
#     check_a_random_pair()

# import basic
# db = basic.do_connect()
# ref1 = basic.get_person(db,994429)
# ref2 = basic.get_person(db,323640)
# basic.get_match_score(db,ref1,ref2,0)
# basic.get_match_score(db,ref1,ref2,1)
# basic.get_match_score(db,ref1,ref2,2)


    