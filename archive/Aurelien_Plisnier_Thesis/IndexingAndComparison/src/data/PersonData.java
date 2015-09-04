package data;

import java.io.BufferedWriter;
import java.io.IOException;
import java.util.List;

import comparator.NaiveBayes;
import comparator.PairwiseComparison;

public class PersonData implements Data {

	private List<String> names;
	private int recordID, year;
	private String place, patronymic, placeOfBirth;
	private char gender;
	private int maxYear, personID;

	public PersonData(List<String> names, int recordID, int year, String place, char gender){
		this.names = names;
		this.recordID = recordID;
		this.year = year;
		this.place = place;
		this.gender = gender;

		//System.out.println(names);
	}

	public List<String> getNames() {
		return this.names;
	}


	public int getRecordID(){
		return this.recordID;
	}


	public int getYear(){
		return this.year;
	}

	public String getPlace(){
		return this.place;
	}

	public void display() {
		System.out.println("Names " + this.names);
		System.out.println("recordId " + this.recordID);	
		System.out.println("Year " + this.year);
	}

	public Boolean equals(Data d){
		return this.recordID == d.getRecordID();
	}

	public boolean jaroMatch(PersonData d) {
		return PairwiseComparison.jaroPairwiseComparison(d, this);
	}

	//Compare with other data
	public void compareRecords(Data child, BufferedWriter bw, PlaceCoordinatesConverter pCC, NaiveBayes comparator, String type) throws IOException {
		if(type.equals("BMP"))comparator.comparisonBMP((PersonData)child, this, bw, pCC);
	}

	public String getPatronymic() {
		return patronymic;
	}

	public void setPatronymic(String patronymic) {
		this.patronymic = patronymic;
	}

	public String getPlaceOfBirth() {
		return placeOfBirth;
	}

	public void setPlaceOfBirth(String placeOfBirth) {
		this.placeOfBirth = placeOfBirth;
	}

	public char getGender() {
		return gender;
	}

	public void setGender(char gender) {
		this.gender = gender;
	}

	public void setMaxYear(int maxYear) {
		this.maxYear = maxYear;
		
	}
	public int getMaxYear(){
		return this.maxYear;
	}

	public void setPersonID(int personID) {
		this.personID = personID;		
	}
	
	public int getPersonID(){
		return this.personID;
	}
}
