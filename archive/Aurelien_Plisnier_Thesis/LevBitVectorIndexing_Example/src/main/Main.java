package main;

import java.util.ArrayList;
import java.util.List;

import indexing.BitVector;
import indexing.LevenshteinTree;
import data.Record;

public class Main {
	
	public static void main(String[] args) {
		//A bunch of example records
		Record r1 = new Record(1, "Stefan", "Eppe");
		Record r2 = new Record(2, "Stephan", "Hepper");
		Record r3 = new Record(3, "Stephanus", "Keppler");
		Record r4 = new Record(4, "Stefan", "Eppe");
		
		//Will contain candidate matches
		List<Record> result = new ArrayList<Record>();
		
		//Indexing tree
		LevenshteinTree tree = new LevenshteinTree(2); // Error of 2.
		
		//Building the tree
		tree.storeRecord(r1);
		tree.storeRecord(r2);
		tree.storeRecord(r3);
		
		//Looking for matches
		tree.findCandidatePairs(new BitVector(r4), 0, tree.getRoot(), 0, 0, result);
		
		//Display results
		System.out.println("Source record is :");
		r4.display();	
		System.out.println("Candidate matches are :");
		for(Record d : result) d.display();
		
	}

}
