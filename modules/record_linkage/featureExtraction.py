"""
Created on May 12, 2014

@author: Bijan

This file includes basic functions for extracting various features from the Dutch names:

    * f1: Boolean feature -- If first 2 letters of name and standard name are equal
    * f2: Boolean feature -- If last 2 letters of name and standard name are equal
    * f3: Boolean feature -- If size of name and standard name are equal
    * f4: Number feature -- absolute difference of name size and standard size
    * f5: Number feature--Number of longest first equal chars
    * f6: Number feature -- Number of longest last equal chars
    * f7: Boolean feature -- if soundex code of name and standard name is equal
    * f8: Boolean feature -- if metaphone code of name and standard name is equal
    * f9: Boolean feature -- if double-metaphone code of name and standard name is equal
    * f10:Number feature -- longest common chars between name and its standard name
    ** In future, we could extract more features such as bigrams, trigrams and other NLP related features from this dataset. For now, we just keep it simple.
    For example : ARINCK, AAFTINK  should be modeled as:

    0,0,0,1,1,1,?, ?, ?, 1


"""


def extract_feature(name, standard):
    """ (string, string) --> [boolean, boolean, boolean, int, int, int, boolean, boolean, boolean, int]
    extracts various features for each record (name, standard) and exports results in form of a list of booleans and integers.

    >>> extract_feature('ARINCK', 'AAFTINK')
     [0,0,0,1,1,1,?, ?, ?, 1]

    """
    if not name or not standard:
        return []

    f_list = [] # features list

    # f1: Boolean feature -- If first 2 letters of name and standard name are equal
    f_list.append(name[:2] == standard[:2])
    # f2: Boolean feature -- If last 2 letters of name and standard name are equal
    f_list.append(name[-2:] == standard[-2:])

    # f3: Boolean feature -- If size of name and standard name are equal
    f_list.append(len(name) == len(standard))

    # f4: Number feature -- absolute difference of name size and standard size
    f_list.append(abs(len(name) - len(standard)))

    # f5: Number feature--Number of longest first equal chars
    for i in xrange(1,len(name)+1):

        if not name[:i] == standard[:i]:
            break
    # print i, name, standard
    f_list.append(i-1)



    # f6: Number feature -- Number of longest last equal chars
    for i in range(len(name)):
        if not name[-i-1:] == standard[-i-1:]:
            break

    f_list.append(i)


    # f7: Boolean feature -- if soundex code of name and standard name is equal
    import jellyfish
    f_list.append(jellyfish.soundex(name) == jellyfish.soundex(standard))

    # f8: Boolean feature -- if metaphone code of name and standard name is equal

    f_list.append(jellyfish.metaphone(name) == jellyfish.metaphone(standard))

    # f9: Boolean feature -- if double-metaphone code of name and standard name is equal
    from preModules import metaphone
    dm_flag = False # a flag that shows whether two words have any common double-metaphone or not
    for dm1 in metaphone.doublemetaphone(name):
        for dm2 in metaphone.doublemetaphone(standard):
            if dm1 and dm2 and dm1 == dm2:
                dm_flag = True
                break

    f_list.append(dm_flag)

    # f10: Number feature -- longest common chars between name and its standard name
    from modules.basic_modules.basic import longest_common_substring
    f_list.append(len(longest_common_substring(name, standard)))

    return f_list


