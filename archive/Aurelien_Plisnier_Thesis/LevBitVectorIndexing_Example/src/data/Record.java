package data;

//Data type representing records to match. Here we just consider an ID and 2 names.
public class Record {
	
	private int ID;
	private String firstName, lastName;
	
	public Record(int ID, String firstName, String lastName){
		this.setID(ID);
		this.setFirstName(firstName);
		this.setLastName(lastName);
	}

	public int getID() {
		return ID;
	}

	public void setID(int iD) {
		ID = iD;
	}

	public String getFirstName() {
		return firstName;
	}

	public void setFirstName(String firstName) {
		this.firstName = firstName;
	}

	public String getLastName() {
		return lastName;
	}

	public void setLastName(String lastName) {
		this.lastName = lastName;
	}
	
	public void display(){
		System.out.println("ID = " + ID + ", first name = " + firstName + ", last name = " + lastName);
	}

}
