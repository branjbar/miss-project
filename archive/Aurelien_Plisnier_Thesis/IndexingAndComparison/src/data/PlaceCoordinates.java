package data;

public class PlaceCoordinates {
	
	private String place;
	private double latitude, longitude;
	
	public PlaceCoordinates(String place, double latitude, double longitude){
		this.place = place;
		this.latitude = latitude;
		this.longitude = longitude;
	}
	
	public String getPlace(){
		return this.place;
	}
	
	public double getLatitude(){
		return this.latitude;
	}

	public double getLongitude(){
		return this.longitude;
	}
}
