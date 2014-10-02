__author__ = 'bijan'

import solr


class Story():
    def __init__(self):
        """
        initializes the Solr connection
        :return:
        """
        self.s = solr.SolrConnection('http://localhost:8983/solr')
        self.commit_counter = 0
        self.commit_number = 0
        self.current_document_id = 2846095
