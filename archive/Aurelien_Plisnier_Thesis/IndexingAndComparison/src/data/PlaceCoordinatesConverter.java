package data;

import java.io.BufferedReader;
import java.io.FileReader;
import java.util.ArrayList;
import java.util.List;

public class PlaceCoordinatesConverter {

	private List<PlaceCoordinates> places;

	public PlaceCoordinatesConverter(){
		BufferedReader br = null;  
		places = new ArrayList<PlaceCoordinates>();
		try{  
			br = new BufferedReader(new FileReader("municipality_gps_bijan.csv"));  

			String line = br.readLine();   
			//List<String> couple;
			String[] curLine = new String[4];


			while(line != null) {   
				if(!line.isEmpty()){
					curLine = line.split(",");
					if(!this.isNumeric(curLine[2]));
					else if(this.isNumeric(curLine[1])){
						this.places.add(new PlaceCoordinates(curLine[0], Double.parseDouble(curLine[1]), Double.parseDouble(curLine[2])));
					}
					else {
						this.places.add(new PlaceCoordinates(curLine[0], Double.parseDouble(curLine[2]), Double.parseDouble(curLine[3])));
						this.places.add(new PlaceCoordinates(curLine[1], Double.parseDouble(curLine[2]), Double.parseDouble(curLine[3])));
					}
				}

				line = br.readLine(); 
			}  


			br.close();  
		}  
		catch(Exception e){  
			System.out.println("Exception caught : " + e);  
		}  
	}

	private boolean isNumeric(String str)  
	{  
		try  
		{  
			Double.parseDouble(str);  
		}  
		catch(NumberFormatException nfe)  
		{  
			return false;  
		}  
		return true;  
	}
	
	public List<Double> getCoordinates(String place){
		List<Double> result = new ArrayList<Double>();
		for(PlaceCoordinates PC : this.places){
			if(PC.getPlace().toLowerCase().contains(place.toLowerCase())){
				result.add(PC.getLatitude());
				result.add(PC.getLongitude());
				return result;
			}
		}
		return null;
	}

}
