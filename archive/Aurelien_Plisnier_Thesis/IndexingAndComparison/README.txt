Order of execution:

Main instantiates the indexer (Bit Vector Tree) and a database handler. Main orders the database handler to prepare the matching then to perform the matching.

DbHandler, to prepare the matching, fetches the records and add them to the bit vector tree.
	The tree instantiates a BitVector from the record it received and stores it	

To perform the matching, DbHandler fetches the records and give them to the bit vector tree so that it can be traversed.
	TreeLevenshtein performs a recursive traversal to find the correct leaves. 

When a leaf is found, it is asked to the node to compare the record at hand with all the records it contains.

Settings: the database connection string is in DhHandler's constructor. Sql queries are in DbHandlers methods.	