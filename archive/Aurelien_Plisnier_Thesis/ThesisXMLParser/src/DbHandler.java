

import java.sql.Connection;
import java.sql.DriverManager;
import java.sql.SQLException;
import java.sql.Statement;

import com.mysql.jdbc.PreparedStatement;


/**
 * Gere la connexion et les requetes a la base de donnees.
 */
public class DbHandler {

	private Connection connection;

	public DbHandler(){
		String url = "jdbc:mysql://localhost:3306/";
		String dbName = "thesis_miss";
		String driver = "com.mysql.jdbc.Driver";
		String userName = "root";
		String password = "";
		try {
			Class.forName(driver).newInstance();
			this.connection = DriverManager.getConnection(url+dbName,userName,password);
		} catch (Exception e) {
			System.out.println("Error establishing connection to DB.");
			e.printStackTrace();
		}
	}

	
	public void close(){
		try {
			this.connection.close();
		} catch (SQLException e) {
			System.out.println("Error closing connection to DB.");
			e.printStackTrace();
		}
	}

	public void runQuery(String query) {
		PreparedStatement statement = null;
		try {
			statement = (PreparedStatement) this.connection.prepareStatement(query);
		} catch (SQLException e) {
			System.out.println("Error making statement.");
			e.printStackTrace();
		}
		try {			
			statement.execute();
		} catch (SQLException e) {
			System.out.println("Error upating database. Query is \n" + query);
			e.printStackTrace();
		}

	}
}

