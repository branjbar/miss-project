package tree;

import java.io.BufferedWriter;
import java.io.IOException;
import java.util.ArrayList;
import java.util.List;

import comparator.NaiveBayes;

import data.Data;
import data.PersonData;
import data.PlaceCoordinatesConverter;

public class Node {
	private List<Data> data;
	private List<Node> children;

	public Node(){
		this.data = new ArrayList<Data>();
		this.children = new ArrayList<Node>();
		this.children.add(null); this.children.add(null);
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
	public void addRecord(Data data) {
		this.data.add(data);	
		//System.out.println("Adding data: ");
		//data.display();
	}
	
	public void getData(List<Data> result){
		for (Data d : this.data) result.add(d);
	}
	
	public void display(){
		for (Data d:this.data)
			d.display();
		for(int i = 0; i < 2; i++){	
			if(this.children.get(i) != null){
				System.out.println("Child # " + i);
				this.children.get(i).display();
			}
		}
	}
	
	
	//Returns the amount of stored records.
	public int getSize(){
		return this.data.size();
	}

	public void compareRecords(Data child, BufferedWriter bw, PlaceCoordinatesConverter pCC, NaiveBayes comparator, String type) throws IOException {
		for(Data d : this.data) d.compareRecords(child, bw, pCC, comparator, type); 
		
	}
}