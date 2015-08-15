package tree;

import java.io.BufferedWriter;
import java.io.IOException;

import bitVector.BitVector;

import comparator.NaiveBayes;

import data.Data;
import data.PlaceCoordinatesConverter;

public class TreeLevenshtein {

	private Node root;
	private int errorMaxOnFN, errorMaxOnLN;

	public TreeLevenshtein(int errorMaxOnFN, int errorMaxOnLN){
		this.root = new Node();
		this.errorMaxOnFN = errorMaxOnFN;
		this.errorMaxOnLN = errorMaxOnLN;
	}

	//Tree construction method.
	public void storeRecord(Data data){ 
		BitVector vect = new BitVector(data);

		//Init cur node and prev node
		Node cur = this.root;
		Node prev = null;

		for(int i = 0; i < vect.size(); i++){
			prev = cur;
			cur = cur.getChild(vect.get(i)); //returns null if child does not exist

			if(cur == null){ //If null, we need to create the child
				cur = new Node();
				prev.addChild(cur, vect.get(i));
			}
		}
		cur.addRecord(data);
		//cur.display();//If we're on a leaf, store the data in current node.
	}

	public Node getRoot() {
		return this.root;
	}

	
	//Indexing metadata.
	public void treeTraversalPerson(BitVector path, int pos, Node cur, int e1FN, int e2FN, int e1LN, int e2LN, BufferedWriter bw, Data child, PlaceCoordinatesConverter pCC, NaiveBayes comparator, String type) throws IOException{

		if(pos == path.size()){
			cur.compareRecords(child, bw, pCC, comparator, type); // If leaf: read the data
			return;
		}
		Node next = cur.getChild(path.get(pos));
		if(next != null){
			treeTraversalPerson(path, pos + 1, next, e1FN, e2FN, e1LN, e2LN, bw, child, pCC, comparator, type); // Explore right path
		}
		next = cur.getChild(!path.get(pos));
		
		//e1 is the amount of bits to 1 in path while 0 in visited branch, e2 is the amount of bits to 0 in path while 1 in visited branch.
		int e1FNPrime = e1FN, e2FNPrime = e2FN, e1LNPrime = e1LN, e2LNPrime = e2LN;
		if(path.get(pos) && pos < path.size()/2) e1FNPrime++; // P(pos) = 1 and Q(pos) = 0 FN
		else if(!path.get(pos) && pos < path.size()/2) e2FNPrime++; // P(pos) = 0 and Q(pos) = 1 FN
		else if(path.get(pos)) e1LNPrime++; // P(pos) = 1 and Q(pos) = 0 LN
		else e2LNPrime++; // P(pos) = 0 and Q(pos) = 1 LN
		
		if(next != null && e1FNPrime <= this.errorMaxOnFN && e2FNPrime <= this.errorMaxOnFN && e1LNPrime <= this.errorMaxOnLN && e2LNPrime <= this.errorMaxOnLN){
			treeTraversalPerson(path, pos + 1, next, e1FNPrime, e2FNPrime, e1LNPrime, e2LNPrime, bw, child, pCC, comparator, type); // Explore wrong path (first subvector)
		}
	}

	public void treeTraversalCouple(BitVector path, int pos, Node cur, int e1FNP1, int e2FNP1, int e1LNP1, int e2LNP1, int e1FNP2, int e2FNP2, int e1LNP2, int e2LNP2, BufferedWriter bw, Data data, PlaceCoordinatesConverter pCC, NaiveBayes comparator, String type) throws IOException {
		if(pos == path.size()){
			cur.compareRecords(data, bw, pCC, comparator, type); // If leaf: read the data
			return;
		}
		Node next = cur.getChild(path.get(pos));
		if(next != null){
			treeTraversalCouple(path, pos + 1, next, e1FNP1, e2FNP1, e1LNP1, e2LNP1, e1FNP2, e2FNP2, e1LNP2, e2LNP2, bw, data, pCC, comparator, type); // Explore right path
		}
		next = cur.getChild(!path.get(pos));
		
		//e1 is the amount of bits to 1 in path while 0 in visited branch, e2 is the amount of bits to 0 in path while 1 in visited branch.
		int e1FNP1Prime = e1FNP1, e2FNP1Prime = e2FNP1, e1LNP1Prime = e1LNP1, e2LNP1Prime = e2LNP1, e1FNP2Prime = e1FNP2, e2FNP2Prime = e2FNP2, e1LNP2Prime = e1LNP2, e2LNP2Prime = e2LNP2;
		if(pos < path.size()/4){ // FN P1
			if(path.get(pos)) e1FNP1Prime ++;
			else e2FNP1Prime ++;
		}
		else if(pos < path.size()/2){ //LN P1
			if(path.get(pos)) e1LNP1Prime ++;
			else e2LNP1Prime ++;
		}
		else if(pos < 3*path.size()/4){// FN P2
			if(path.get(pos)) e1FNP2Prime ++;
			else e2FNP2Prime ++;
		}
		else { // LN P2
			if(path.get(pos)) e1LNP2Prime ++;
			else e2LNP2Prime ++;
		}
		
		if(next != null && e1FNP1Prime <= this.errorMaxOnFN && e2FNP1Prime <= this.errorMaxOnFN && e1FNP2Prime <= this.errorMaxOnFN && e2FNP2Prime <= this.errorMaxOnFN && e1LNP1Prime <= this.errorMaxOnLN && e2LNP1Prime <= this.errorMaxOnLN && e1LNP2Prime <= this.errorMaxOnLN && e2LNP2Prime <= this.errorMaxOnLN){
			treeTraversalCouple(path, pos + 1, next, e1FNP1Prime, e2FNP1Prime, e1LNP1Prime, e2LNP1Prime, e1FNP2Prime, e2FNP2Prime, e1LNP2Prime, e2LNP2Prime, bw, data, pCC, comparator, type); // Explore wrong path (first subvector)
		}
		
	}
}