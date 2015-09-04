
public class Main {
	
	public static void main(String args[]){
		
		
		new DoopParser().parse("../../../../../wamp/www/thesis/DTB-D.xml"); // You may want to change this...
		System.out.println("Doop OK");
		new BegraafParser().parse("../../../../../wamp/www/thesis/DTB-B.xml");
		System.out.println("Begraaf OK");
		new TrouwParser().parse("../../../../../wamp/www/thesis/DTB-T.xml");
		System.out.println("Trouw OK");
		DbHandler database = new DbHandler();
		
		database.runQuery("OPTIMIZE TABLE witnesses_record");
		database.runQuery("OPTIMIZE TABLE person");
		database.runQuery("OPTIMIZE TABLE birth_record");
		database.runQuery("OPTIMIZE TABLE marriage_record");
		database.runQuery("OPTIMIZE TABLE death_record");
		
		database.close();
		
		System.out.println("SUCCESS !");
	}

}
