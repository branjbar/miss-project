
-- Query to group the matches based on roles and docuemnt types
SELECT 
    score,
    role1,
    rol2,
    type1,
    type2,
    substring(docu2.date, 7, 12) - substring(docu1.date, 7, 12) as age,
    COUNT(*)
FROM
    (SELECT 
        *
    FROM
        links_based.miss_matches
    WHERE
        score = 2) AS T1
        inner join
    all_documents as docu1
        inner join
    all_documents as docu2
where
    docu2.id = doc2 and docu1.id = doc1
group by role1 , rol2 , type1 , type2
order by count(*) desc;
