package data;

import java.io.BufferedWriter;
import java.io.IOException;
import java.util.List;

import comparator.NaiveBayes;

public interface Data {
	public List<String> getNames();
	public int getRecordID();
	public String getPlace();
	public void display();
	public Boolean equals(Data d);
	public void compareRecords(Data child, BufferedWriter bw, PlaceCoordinatesConverter pCC, NaiveBayes comparator, String type) throws IOException;
	
}
