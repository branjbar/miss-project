package indexing;

import java.util.ArrayList;
import java.util.List;

import data.Record;

//A node of the tree. Has pointers to child nodes and to stored records (if leaf)
public class Node {
	private List<Record> data;
	private List<Node> children;

	public Node(){
		this.data = new ArrayList<Record>();
		this.children = new ArrayList<Node>();
		this.children.add(null); this.children.add(null); // Dirty. Avoiding null pointer exception in binary tree.
	}

	//Get the child corresponding to given label.
	public Node getChild(Boolean edgeLabel) {
		int label = (edgeLabel) ? 1 : 0;
		return this.children.get(label);
	}

	//Add a child
	public void addChild(Node child, Boolean edgeLabel){
		int label = (edgeLabel) ? 1 : 0;
		this.children.set(label, child);
	}

	//Add data
	public void addRecord(Record data) {
		this.data.add(data);	
	}

	//Fetch data from node.
	public void fetchData(List<Record> result) {
		for (Record d : this.data) result.add(d);
	}

}
