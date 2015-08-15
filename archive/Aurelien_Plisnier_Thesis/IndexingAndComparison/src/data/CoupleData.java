package data;

import java.io.BufferedWriter;
import java.io.IOException;
import java.util.List;

import comparator.NaiveBayes;

public class CoupleData implements Data{

	private List<String> names;
	private int recordID;
	private String place, date;
	
	private String manPat, womanPat; //Patronymics

	public CoupleData(List<String> father, List<String> mother, int recordID, String date, String place){
		this.names = father;
		this.names.addAll(mother);
		this.recordID = recordID;
		this.date = date;
		this.place = place;
		this.setManPat(null);
		this.setWomanPat(null);
	}

	
	
	public List<String> getNames() {
		return this.names;
	}

	public int getRecordID(){
		return this.recordID;
	}

	public String getDate(){
		return this.date;
	}

	public String getPlace(){
		return this.place;
	}

	public void display() {
		System.out.println("Names " + this.names);
		System.out.println("recordId " + this.recordID);	
		System.out.println("Date " + this.date);
	}

	//Comparing two datas
	public void compareRecords(Data couple, BufferedWriter bw, PlaceCoordinatesConverter pCC, NaiveBayes comparator, String type) throws IOException {
		if(type.equals("PP")) comparator.comparisonPP((CoupleData)couple, this, bw, pCC);
		if(type.equals("MP")) comparator.comparisonMP((CoupleData)couple, this, bw, pCC);
		
	}

	public Boolean equals(Data d) {
		return this.recordID == d.getRecordID();
	}


	//Patronymic
	public String getManPat() {
		return manPat;
	}



	public void setManPat(String manPat) {
		this.manPat = manPat;
	}



	public String getWomanPat() {
		return womanPat;
	}



	public void setWomanPat(String womanPat) {
		this.womanPat = womanPat;
	}
}
