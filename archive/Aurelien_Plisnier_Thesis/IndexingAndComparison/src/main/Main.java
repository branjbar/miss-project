package main;


import java.io.IOException;
import java.sql.SQLException;

import tree.TreeLevenshtein;
import data.DbHandler;

public class Main {

	public static void main(String[] args) {		
		int errorMaxOnFN = 1, errorMaxOnLN = 1;
		TreeLevenshtein tree = new TreeLevenshtein(errorMaxOnFN, errorMaxOnLN);
		try {
			new DbHandler().preparePPMatching(tree); // Parents to parents
			//new DbHandler().prepareMPmatching(tree); // Newlyweds to parents
			//new DbHandler().prepareBPMmatching(tree); // Newborns to parents
			
		} catch (ClassNotFoundException e1) {
			// TODO Auto-generated catch block
			e1.printStackTrace();
		} catch (SQLException e1) {
			// TODO Auto-generated catch block
			e1.printStackTrace();
		}  
		System.out.println("Looking for Matches");
		try {
			new DbHandler().performPPMatching(tree); // Parents to parents
			//new DbHandler().performMPMatching(tree); // Newlyweds to parents
			//new DbHandler().performBPMMatching(tree); // Newborns to parents
		} catch (IOException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		} catch (ClassNotFoundException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		} catch (SQLException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		} 
	
	}  
}