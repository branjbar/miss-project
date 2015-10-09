__author__ = 'bijan'

"""
CREATE TABLE `all_persons_2015` (
  `id` int(11) DEFAULT '0',
  `uuid` varchar(90) DEFAULT '0',
  `gender` varchar(90) DEFAULT '0',
  `first_name` varchar(90) DEFAULT NULL,
  `prefix` varchar(45) DEFAULT NULL,
  `last_name` varchar(45) DEFAULT NULL,
  `date_1` varchar(45) DEFAULT NULL,
  `place_1` varchar(45) DEFAULT NULL,
  `date_2` varchar(45) DEFAULT NULL,
  `place_2` varchar(90) DEFAULT NULL,
  `role` int(11) DEFAULT NULL,
  `register_id` varchar(45) DEFAULT NULL,
  `register_type` varchar(45) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;


CREATE TABLE `all_documents_2015` (
  `id` int(11) NOT NULL,
  `uuid` varchar(90) DEFAULT NULL,
  `type_text` varchar(45) DEFAULT NULL,
  `date` varchar(45) DEFAULT NULL,
  `municipality` varchar(45) DEFAULT NULL,
  `reference_ids` text,
  PRIMARY KEY (`id`)
)



"""


def add_to_sql(person_id, doc_id, dict, doc_type):
    """
    turns a simple dictionary to a sql
    :param dict:
    :param doc_type:
    :return:
    """
    xml_1_sql = open('sql_bs_%s_persons.sql' % doc_type, 'a')
    xml_2_sql = open('sql_bs_%s_documents.sql' % doc_type, 'a')

    if doc_type == 'birth':
        query = """
            INSERT INTO `all_persons_2015` (`id`, `uuid`, gender, `first_name`, `prefix`, `last_name`, `date_1`,  `place_1`, `role`, `register_id`, `register_type`)
            VALUES (%d,"%s","%s", "%s","%s","%s","%s", "%s", %d, %d, "%s");
            """ % (
            person_id, dict['child']['uuid'], dict['child']['gender'], dict['child']['first_name'].replace('"', "'"),
            dict['child']['prefix'].replace('"', "'"), dict['child']['last_name'].replace('"', "'"), dict['date'], dict['municipality'].replace('"', "'"), 1,
            doc_id, 'birth')
        person_id += 1
        query += """
                INSERT INTO `all_persons_2015` (id, uuid, gender, `first_name`, prefix, `last_name`, date_1,  `place_1`, role, `register_id`, `register_type`)
                VALUES (%d,"%s","%s", "%s","%s","%s","%s", "%s", %d, %d, "%s");
                """ % (person_id, dict['father']['uuid'], "male", dict['father']['first_name'].replace('"', "'"),
                       dict['father']['prefix'].replace('"', "'"), dict['father']['last_name'].replace('"', "'"),
                       dict['date'], dict['municipality'].replace('"', "'"), 5, doc_id, 'birth')
        person_id += 1
        query += """
                INSERT INTO `all_persons_2015` (id, uuid, gender, `first_name`, prefix, `last_name`, date_1,  `place_1`, role, `register_id`, `register_type`)
                VALUES (%d,"%s","%s", "%s","%s","%s","%s", "%s", %d, %d, "%s");
                """ % (person_id, dict['mother']['uuid'], "male", dict['mother']['first_name'].replace('"', "'"),
                       dict['mother']['prefix'].replace('"', "'"), dict['mother']['last_name'].replace('"', "'"),
                       dict['date'], dict['municipality'].replace('"', "'"), 5, doc_id, 'birth')

        query_document = """
                INSERT INTO `all_documents_2015` (id, uuid, `type_text`, date, `municipality`, reference_ids)
                VALUES (%d,"%s","%s","%s","%s","%s");
                """ % (doc_id, dict['uuid'], 'birth', dict['date'], dict['municipality'].replace('"', "'"),
                       ','.join([str(person_id - 2), str(person_id - 1), str(person_id)]))

    if doc_type == 'death':
        query = """
            INSERT INTO `all_persons_2015`
                (`id`, `uuid`, gender, `first_name`, `prefix`, `last_name`, `date_1`,  `place_1`, `role`, `register_id`, `register_type`)
            VALUES
                (%d,"%s","%s", "%s","%s","%s","%s", "%s", %d, %d, "%s"),
            """ % (
            person_id, dict['child']['uuid'], dict['child']['gender'], dict['child']['first_name'].replace('"', "'"),
            dict['child']['prefix'].replace('"', "'"), dict['child']['last_name'].replace('"', "'"), dict['date'], dict['municipality'].replace('"', "'"), 1,
            doc_id, 'death')
        person_id += 1
        query += """
                 (%d,"%s","%s", "%s","%s","%s","%s", "%s", %d, %d, "%s"),
                """ % (person_id, dict['father']['uuid'], "male", dict['father']['first_name'].replace('"', "'"),
                       dict['father']['prefix'].replace('"', "'"), dict['father']['last_name'].replace('"', "'"),
                       dict['date'], dict['municipality'].replace('"', "'"), 4, doc_id, 'death')
        person_id += 1
        query += """
                 (%d,"%s","%s", "%s","%s","%s","%s", "%s", %d, %d, "%s"),
                """ % (person_id, dict['mother']['uuid'], "male", dict['mother']['first_name'].replace('"', "'"),
                       dict['mother']['prefix'].replace('"', "'"), dict['mother']['last_name'].replace('"', "'"),
                       dict['date'], dict['municipality'].replace('"', "'"), 4, doc_id, 'death')
        person_id += 1
        query += """
                 (%d,"%s","%s", "%s","%s","%s","%s", "%s", %d, %d, "%s");
                """ % (person_id, dict['relative']['uuid'], "male", dict['relative']['first_name'].replace('"', "'"),
                       dict['relative']['prefix'].replace('"', "'"), dict['relative']['last_name'].replace('"', "'"),
                       dict['date'], dict['municipality'].replace('"', "'"), 6, doc_id, 'death')

        query_document = """
                INSERT INTO `all_documents_2015` (id, uuid, `type_text`, date, `municipality`, reference_ids)
                VALUES (%d,"%s","%s","%s","%s","%s");
                """ % (doc_id, dict['uuid'], 'death', dict['date'], dict['municipality'].replace('"', "'"),
                       ','.join([str(person_id - 3), str(person_id - 2), str(person_id - 1), str(person_id)]))


    if doc_type == 'marriage':
        query = """
                INSERT INTO `all_persons_2015` (`id`, `uuid`, gender, `first_name`, `prefix`, `last_name`, `date_1`, `place_1`,
                `date_2`, `place_2`, `role`, `register_id`, `register_type`)
                VALUES (%d,"%s","%s","%s","%s","%s","%s","%s", "%s", "%s", %d, %d, "%s");
                """ % (person_id, dict['groom']['uuid'], 'male', dict['groom']['first_name'].replace('"', "'"),
                       dict['groom']['prefix'].replace('"', "'"), dict['groom']['last_name'].replace('"', "'"),
                       dict['date'], dict['municipality'].replace('"', "'"), dict['groom']['date'], dict['groom']['place'].replace('"', "'"), 1, doc_id,
                       'marriage')

        person_id += 1
        query += """
                INSERT INTO `all_persons_2015` (`id`, `uuid`, gender, `first_name`, `prefix`, `last_name`, `date_1`, `place_1`,
                `date_2`, `place_2`, `role`, `register_id`, `register_type`)
                VALUES (%d,"%s","%s","%s","%s","%s","%s","%s", "%s", "%s", %d, %d, "%s");
                """ % (person_id, dict['bride']['uuid'], 'female', dict['bride']['first_name'].replace('"', "'"),
                       dict['bride']['prefix'].replace('"', "'"), dict['bride']['last_name'].replace('"', "'"),
                       dict['date'], dict['municipality'].replace('"', "'"), dict['bride']['date'], dict['bride']['place'].replace('"', "'"), 1, doc_id,
                       'marriage')

        person_id += 1
        query += """
                INSERT INTO `all_persons_2015` (id, uuid, gender,  `first_name`, prefix, `last_name`, date_1, place_1, role, `register_id`, `register_type`)
                VALUES (%d,"%s","%s","%s","%s","%s","%s", "%s", %d, %d, "%s");
                """ % (
            person_id, dict['groom']['father']['uuid'], 'male', dict['groom']['father']['first_name'].replace('"', "'"),
            dict['groom']['father']['prefix'].replace('"', "'"), dict['groom']['father']['last_name'].replace('"', "'"),
            dict['date'], dict['municipality'].replace('"', "'"), 2, doc_id, 'marriage')

        person_id += 1
        query += """
                INSERT INTO `all_persons_2015` (id, uuid, gender,  `first_name`, prefix, `last_name`, date_1, place_1, role, `register_id`, `register_type`)
                VALUES (%d,"%s","%s","%s","%s","%s","%s", "%s",  %d, %d, "%s");
                """ % (
            person_id, dict['groom']['mother']['uuid'], 'female', dict['groom']['mother']['first_name'].replace('"', "'"),
            dict['groom']['mother']['prefix'].replace('"', "'"), dict['groom']['mother']['last_name'].replace('"', "'"),
            dict['date'], dict['municipality'].replace('"', "'"), 2, doc_id, 'marriage')

        person_id += 1
        query += """
                INSERT INTO `all_persons_2015` (id, uuid, gender,  `first_name`, prefix, `last_name`, date_1, place_1, role, `register_id`, `register_type`)
                VALUES (%d,"%s","%s","%s","%s","%s","%s", "%s",  %d, %d, "%s");
                """ % (
            person_id, dict['bride']['father']['uuid'], 'male', dict['bride']['father']['first_name'].replace('"', "'"),
            dict['bride']['father']['prefix'].replace('"', "'"), dict['bride']['father']['last_name'].replace('"', "'"),
            dict['date'], dict['municipality'].replace('"', "'"), 2, doc_id, 'marriage')

        person_id += 1
        query += """
                INSERT INTO `all_persons_2015` (id, uuid, gender,  `first_name`, prefix, `last_name`, date_1, place_1, role, `register_id`, `register_type`)
                VALUES (%d,"%s","%s","%s","%s","%s","%s", "%s", %d, %d, "%s");
                """ % (
            person_id, dict['bride']['mother']['uuid'], 'female', dict['bride']['mother']['first_name'].replace('"', "'"),
            dict['bride']['mother']['prefix'].replace('"', "'"), dict['bride']['mother']['last_name'].replace('"', "'"),
            dict['date'], dict['municipality'].replace('"', "'"), 3, doc_id, 'marriage')

        query_document = """
                INSERT INTO `all_documents_2015` (id, uuid,  `type_text`, date, `municipality`, reference_ids)
                VALUES (%d,"%s","%s","%s","%s","%s");
                """ % (doc_id, dict['uuid'], 'marriage', dict['date'], dict['municipality'].replace('"', "'"), ','.join(
                [str(person_id - 5), str(person_id - 4), str(person_id - 3), str(person_id - 2), str(person_id - 1),
                 str(person_id)]))

    xml_1_sql.write(query.encode('utf-8').replace('\\', ''))
    xml_2_sql.write(query_document.encode('utf-8').replace('\\', ''))
