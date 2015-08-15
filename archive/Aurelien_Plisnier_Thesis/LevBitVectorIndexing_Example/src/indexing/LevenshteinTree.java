package indexing;

import java.util.List;

import data.Record;

public class LevenshteinTree {

	private Node root;
	private int errorMax;

	public LevenshteinTree(int errorMax){
		this.errorMax = errorMax;
		this.root = new Node();
	}

	//Tree construction method: we receive a record and put it into the tree, missing nodes are created.
	public void storeRecord(Record data){ 
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
	}

	//Recursive tree traversal method. Given a record's bit vector we search the tree for records stored in close by leafs.
	//Found records are stored in a List. e1 and e2 are the tree traversal error (CF Marijn's work), we show that max(e1, e2) is a lower bound for Lev distance.
	public void findCandidatePairs(BitVector path, int pos, Node cur, int e1, int e2, List<Record> result) {
		if(pos == path.size()){
			cur.fetchData(result); // If leaf: read the data
			return;
		}
		Node next = cur.getChild(path.get(pos)); // Explore right path
		if(next != null){
			findCandidatePairs(path, pos + 1, next, e1, e2, result); 
		}
		next = cur.getChild(!path.get(pos)); // Explore wrong path: we need to increment error
		int e1Prime = e1;
		int e2Prime = e2;

		if(path.get(pos)) e1Prime ++; // Bit to 1 in path and 0 in followed branch
		else e2Prime ++; // Bit to 0 in path and 1 in followed branch

		if(next != null && e1Prime <= this.errorMax && e2Prime <= this.errorMax){
			findCandidatePairs(path, pos + 1, next, e1Prime, e2Prime, result);
		}
	}

	public Node getRoot() {
		return root;
	}

}
