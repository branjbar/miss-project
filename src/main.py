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
    
def feature_set_construct():
    """
        constructs the feature sets for all standard dutch names and inserts that into the feature table
    """
    from modules import basic
    from modules import featureExtraction

    db = basic.do_connect()
    records = basic.get_dutch_names(db)
    for record in records:
        id = record[0]
        name = record[1]
        standard = record[2]
        document_type = record[3]
        f_list = featureExtraction.extract_feature(name, standard)
        #print name, standard, f_list
        basic.insert_features(db, id, name, standard, document_type, f_list)



if __name__ == '__main__':
    from interface import main_Interface
    main_Interface.main()