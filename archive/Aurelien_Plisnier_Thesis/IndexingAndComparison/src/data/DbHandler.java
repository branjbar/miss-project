package data;

import java.io.BufferedReader;
import java.io.BufferedWriter;
import java.io.FileNotFoundException;
import java.io.FileReader;
import java.io.FileWriter;
import java.io.IOException;
import java.sql.Connection;
import java.sql.DriverManager;
import java.sql.ResultSet;
import java.sql.SQLException;
import java.sql.Statement;
import java.util.ArrayList;
import java.util.Hashtable;
import java.util.List;

import org.apache.commons.math3.util.Precision;

import com.microsoft.sqlserver.jdbc.SQLServerDataSource;

import comparator.LevenshteinDistance;
import comparator.NaiveBayes;
import comparator.PairwiseComparison;
import bitVector.BitVector;
import tree.TreeLevenshtein;

public class DbHandler {

	private Connection connection;

	public DbHandler() throws ClassNotFoundException, SQLException{
		//MySQL connection string
		/*
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
		} */

		//SQL Server connection string
		String url ="jdbc:sqlserver://RogerH;loginTimeout=7200;databaseName=thesis_miss;integratedSecurity=true;lockTimeout=-1";
		Class.forName("com.microsoft.sqlserver.jdbc.SQLServerDriver");
		this.connection = DriverManager.getConnection(url);

		//SQLServerDataSource d = new SQLServerDataSource();
	}

	//Newborn to parent
	public void prepareBPMmatching(TreeLevenshtein tree) {
		List<String> man = new ArrayList<String>();
		List<String> woman = new ArrayList<String>();
		Statement statement = null;
		try {
			statement = this.connection.createStatement();
		} catch (SQLException e) {
			System.out.println("Error making statement.");
			e.printStackTrace();
		}
		ResultSet result = null;
		try {
			result = statement.executeQuery("SELECT record.Record_ID, convert(int, replace(LEFT(record.[DateRecord],4), '-', '')), record.Place, " +
					"man.FirstName, man.Patronymic, man.Surname, man.Entity_ID, man.standardFirstName, groom.BirthPlace, groom.LivingPlace, " +
					"woman.FirstName, woman.Patronymic, woman.Surname, woman.Entity_ID, woman.standardFirstName, bride.BirthPlace, bride.LivingPlace, man.person_id, woman.person_id " +
					"FROM [thesis_miss].[dbo].[birth_record] record," +
					"[thesis_miss].[dbo].[person] man left join [thesis_miss].[dbo].[person] groom on man.Entity_ID = groom.Entity_ID AND (groom.LivingPlace <> '' OR groom.BirthPlace <> ''), " +
					"[thesis_miss].[dbo].[person] woman left join [thesis_miss].[dbo].[person] bride on woman.Entity_ID = bride.Entity_ID AND (bride.LivingPlace <> '' OR bride.BirthPlace <> '') " +
					"WHERE man.Person_ID = record.Father_ID " +
					"AND woman.Person_ID = record.Mother_ID " +
					"AND man.FirstName <> '' and man.Surname <> '' and woman.FirstName <> '' and woman.Surname <> '' " +
					"AND woman.surname not like 'NN' AND woman.Surname not like 'N.N.' AND man.surname not like 'NN' AND man.Surname not like 'N.N.' " +
					"ORDER BY  man.Entity_ID desc, woman.Entity_ID desc, convert(int, replace(LEFT(record.[DateRecord],4), '-', ''))");
		} catch (SQLException e) {
			System.out.println("Error executing query.");
			e.printStackTrace();
		}
		try {
			int counter = 0;

			int curEntity = -1;
			int prevEntity = -1;
			int year = -1, minYear = -1, maxYear = -1;
			int recordID = -1, manID = -1, womanID = -1;
			boolean store = false;

			String manStandardFN = null, manLN = null, manFN = null, womanStandardFN = null, womanLN = null, womanFN = null, place = null, manPat = null, womanPat = null, manPlaceOfBirth = null, womanPlaceOfBirth = null;
			while (result.next()){

				if(counter%10000 == 0) System.out.println(counter);
				counter++;

				prevEntity = curEntity;
				curEntity = result.getInt(7);

				//EntityID
				if((prevEntity != -1 && prevEntity != curEntity) || (result.getString(7) == null && manLN != null)){ // Starting new entity, prev one has to be treated.
					if(manStandardFN == null || manStandardFN.isEmpty()) man.add(manFN); // If standard first name not set, we use the person's first name
					else man.add(manStandardFN);
					man.add(manLN); // Surname
					if(womanStandardFN == null || womanStandardFN.isEmpty()) woman.add(womanFN); // If standard first name not set, we use the person's first name
					else woman.add(womanStandardFN);
					woman.add(womanLN);

					if(store){
						PersonData manData = new PersonData(man, recordID, minYear, place, 'm');
						manData.setPatronymic(manPat);
						manData.setPlaceOfBirth(manPlaceOfBirth);
						manData.setMaxYear(maxYear);
						manData.setPersonID(manID);
						PersonData womanData = new PersonData(woman, recordID, minYear, place, 'v');
						womanData.setPatronymic(womanPat);
						womanData.setPlaceOfBirth(womanPlaceOfBirth);
						womanData.setMaxYear(maxYear);
						womanData.setPersonID(womanID);

						tree.storeRecord(manData);
						tree.storeRecord(womanData);
					}

					//Cleaning buffers
					store = false;
					man = new ArrayList<String>();
					woman = new ArrayList<String>();
					year = -1;
					recordID = -1; minYear = -1; maxYear = -1; manID = -1; womanID = -1;
					manStandardFN = null; manLN = null; manFN = null; womanStandardFN = null; womanLN = null; womanFN = null; place = null; manPat = null; womanPat = null; manPlaceOfBirth = null; womanPlaceOfBirth = null;

					//Treating new entity

					year = result.getInt(2);
					if(year < 1811 && year > 1550){
						store = true;
						if(minYear == -1){
							minYear = year;
							maxYear = year;
							place = result.getString(3);
							recordID = result.getInt(1);
							manID = result.getInt(18);
							womanID = result.getInt(19);
							manPat = result.getString(5);
							womanPat = result.getString(12);
							if(manStandardFN == null || manStandardFN.isEmpty()) manStandardFN = result.getString(8);
							if(manFN == null || manFN.isEmpty()) manFN = result.getString(4);
							if(manLN == null || manLN.isEmpty()) manLN = result.getString(6);
							if(manPlaceOfBirth == null || manPlaceOfBirth.isEmpty()) manPlaceOfBirth = result.getString(9);
							if(manPlaceOfBirth == null || manPlaceOfBirth.isEmpty()) manPlaceOfBirth = result.getString(10);

							if(womanStandardFN == null || womanStandardFN.isEmpty()) womanStandardFN = result.getString(15);
							if(womanFN == null || womanFN.isEmpty()) womanFN = result.getString(11);
							if(womanLN == null || womanLN.isEmpty()) womanLN = result.getString(13);
							if(womanPlaceOfBirth == null || womanPlaceOfBirth.isEmpty()) womanPlaceOfBirth = result.getString(16);
							if(womanPlaceOfBirth == null || womanPlaceOfBirth.isEmpty()) womanPlaceOfBirth = result.getString(17);
						}
						else{
							if(year < minYear){
								place = result.getString(3);
								recordID = result.getInt(1);
								manID = result.getInt(18);
								womanID = result.getInt(19);
								manPat = result.getString(5);
								womanPat = result.getString(12);
								minYear = year;
								if(manStandardFN == null || manStandardFN.isEmpty()) manStandardFN = result.getString(8);
								if(manFN == null || manFN.isEmpty()) manFN = result.getString(4);
								if(manLN == null || manLN.isEmpty()) manLN = result.getString(6);
								if(manPlaceOfBirth == null || manPlaceOfBirth.isEmpty()) manPlaceOfBirth = result.getString(9);
								if(manPlaceOfBirth == null || manPlaceOfBirth.isEmpty()) manPlaceOfBirth = result.getString(10);

								if(womanStandardFN == null || womanStandardFN.isEmpty()) womanStandardFN = result.getString(15);
								if(womanFN == null || womanFN.isEmpty()) womanFN = result.getString(11);
								if(womanLN == null || womanLN.isEmpty()) womanLN = result.getString(13);
								if(womanPlaceOfBirth == null || womanPlaceOfBirth.isEmpty()) womanPlaceOfBirth = result.getString(16);
								if(womanPlaceOfBirth == null || womanPlaceOfBirth.isEmpty()) womanPlaceOfBirth = result.getString(17);
							}
							maxYear = Math.max(year, maxYear);						 
						}
					}

				}
				//Treating current entity
				else{
					year = result.getInt(2);
					if(year < 1811 && year > 1550){
						store = true;
						if(minYear == -1){
							minYear = year;
							maxYear = year;
							place = result.getString(3);
							recordID = result.getInt(1);
							manID = result.getInt(18);
							womanID = result.getInt(19);
							manPat = result.getString(5);
							womanPat = result.getString(12);
							if(manStandardFN == null || manStandardFN.isEmpty()) manStandardFN = result.getString(8);
							if(manFN == null || manFN.isEmpty()) manFN = result.getString(4);
							if(manLN == null || manLN.isEmpty()) manLN = result.getString(6);
							if(manPlaceOfBirth == null || manPlaceOfBirth.isEmpty()) manPlaceOfBirth = result.getString(9);
							if(manPlaceOfBirth == null || manPlaceOfBirth.isEmpty()) manPlaceOfBirth = result.getString(10);

							if(womanStandardFN == null || womanStandardFN.isEmpty()) womanStandardFN = result.getString(15);
							if(womanFN == null || womanFN.isEmpty()) womanFN = result.getString(11);
							if(womanLN == null || womanLN.isEmpty()) womanLN = result.getString(13);
							if(womanPlaceOfBirth == null || womanPlaceOfBirth.isEmpty()) womanPlaceOfBirth = result.getString(16);
							if(womanPlaceOfBirth == null || womanPlaceOfBirth.isEmpty()) womanPlaceOfBirth = result.getString(17);
						}
						else{
							if(year < minYear){
								place = result.getString(3);
								recordID = result.getInt(1);
								manID = result.getInt(18);
								womanID = result.getInt(19);
								manPat = result.getString(5);
								womanPat = result.getString(12);
								minYear = year;
								if(manStandardFN == null || manStandardFN.isEmpty()) manStandardFN = result.getString(8);
								if(manFN == null || manFN.isEmpty()) manFN = result.getString(4);
								if(manLN == null || manLN.isEmpty()) manLN = result.getString(6);
								if(manPlaceOfBirth == null || manPlaceOfBirth.isEmpty()) manPlaceOfBirth = result.getString(9);
								if(manPlaceOfBirth == null || manPlaceOfBirth.isEmpty()) manPlaceOfBirth = result.getString(10);

								if(womanStandardFN == null || womanStandardFN.isEmpty()) womanStandardFN = result.getString(15);
								if(womanFN == null || womanFN.isEmpty()) womanFN = result.getString(11);
								if(womanLN == null || womanLN.isEmpty()) womanLN = result.getString(13);
								if(womanPlaceOfBirth == null || womanPlaceOfBirth.isEmpty()) womanPlaceOfBirth = result.getString(16);
								if(womanPlaceOfBirth == null || womanPlaceOfBirth.isEmpty()) womanPlaceOfBirth = result.getString(17);
							}
							maxYear = Math.max(year, maxYear);						 
						}							
					}
				}
			}
		} catch (SQLException e) {
			System.out.println("Error parsing query result.");
			e.printStackTrace();
		}
		this.close();
	}

	//Newborn to parent
	public void performBPMMatching(TreeLevenshtein tree) throws IOException {
		PlaceCoordinatesConverter PCC = new PlaceCoordinatesConverter();

		Statement statement = null;
		NaiveBayes comparator = new NaiveBayes("BMP", 1);

		BufferedWriter bw = new BufferedWriter(new FileWriter("BMPCandidates.csv"));

		List<String> child;
		try {
			statement = this.connection.createStatement();
		} catch (SQLException e) {
			System.out.println("Error making statement.");
			e.printStackTrace();
		}
		ResultSet result = null;
		try {
			result = statement.executeQuery("SELECT record.Record_ID, child.FirstName, child.patronymic, child.Surname, child.standardFirstName, child.sex, record.DateRecord, record.place, child.person_id "
					+ "FROM birth_record record, person child "
					+ "WHERE child.Person_ID = record.Child_ID and child.FirstName <> '' and child.Surname <> '' and child.oldValue IS NULL " // oldValue is set to "stillborn" in case of the child died at birth.
					+ "AND child.surname not like 'NN' AND child.Surname not like 'N.N.'");
					//+ "AND child.firstname in (select FirstName from [thesis_miss].[dbo].[person] group by FirstName having count(*) < 2000)"// only for stats computation: we select people with unpopular first name
					//+ "AND child.surname in (select surname from [thesis_miss].[dbo].[person] group by surname having count(*) < 2000)");
		} catch (SQLException e) {
			System.out.println("Error executing query.");
			e.printStackTrace();
		}
		try {
			int i = 0;
			int recordID, year;
			char gender;
			String yearString;

			//bw.write("DocID_A,DocID_B,Child_ID,Parent_ID,Score,DeltaYear,DeltaKM,DistFN,DistLN,DistPat\n"); 
			bw.write("DocID_A,DocID_B,Child_ID,Parent_ID,Score\n");
			
			while (result.next()){
				if(i % 1000 == 0) System.out.println(i);
				//System.out.println(i);
				i ++;

				child = new ArrayList<String>();
				if(result.getString(5) == null || result.getString(5).isEmpty()) child.add(result.getString(2)); // If Standard first name not available, we use first name
				else child.add(result.getString(5)); // If available, we use standard first name.			
				child.add(result.getString(4)); // LN
				recordID = result.getInt(1);
				if (result.getString(6) == null || result.getString(6).isEmpty()) gender = 'u'; // If gender not available, it is set to unknown
				else gender = result.getString(6).charAt(0);
				year = -1;
				yearString = result.getString(7).split("-")[0].replaceAll("[^0-9]", ""); 
				if(!yearString.isEmpty()) year = Integer.parseInt(yearString);

				PersonData childData = new PersonData(child, recordID, year, result.getString(8), gender);
				childData.setPatronymic(result.getString(3));
				childData.setPersonID(result.getInt(9));

				tree.treeTraversalPerson(new BitVector(childData), 0, tree.getRoot(), 0, 0, 0, 0, bw, childData, PCC, comparator, "BMP"); // Indexing metadata


			}
			//this.displayMetadata(metadatas); // Indexing metadata
		} catch (SQLException e) {
			System.out.println("Error parsing query result.");
			e.printStackTrace();
		}
		bw.close();
		this.close();
	}

	public void preparePPMatching(TreeLevenshtein tree) {
		List<String> father;
		List<String> mother;
		Statement statement = null;
		try {
			statement = this.connection.createStatement();
		} catch (SQLException e) {
			System.out.println("Error making statement.");
			e.printStackTrace();
		}
		ResultSet result = null;
		try {
			result = statement.executeQuery("SELECT record.Record_ID, father.FirstName, father.Surname, mother.FirstName, mother.Surname, father.standardFirstName, mother.standardFirstName, record.daterecord, record.Place, father.Patronymic, mother.Patronymic FROM birth_record record, person father, person mother WHERE father.Person_ID = record.Father_ID AND mother.Person_ID = record.Mother_ID and father.FirstName <> '' and father.Surname <> '' and mother.FirstName <> '' and mother.Surname <> ''"
					+ " AND mother.surname not like 'NN' AND mother.Surname not like 'N.N.' AND father.surname not like 'NN' AND father.Surname not like 'N.N.'");
		} catch (SQLException e) {
			System.out.println("Error executing query.");
			e.printStackTrace();
		}
		try {
			while (result.next()){
				father = new ArrayList<String>();
				mother = new ArrayList<String>();
				if(result.getString(6) == null || result.getString(6).isEmpty()) father.add(result.getString(2)); // If standard first name not set, we use the person's first name
				else father.add(result.getString(6));
				father.add(result.getString(3)); // Surname
				if(result.getString(7) == null || result.getString(7).isEmpty()) mother.add(result.getString(4)); // If standard first name not set, we use the person's first name
				else  mother.add(result.getString(7));
				mother.add(result.getString(5));
				CoupleData data = new CoupleData(father, mother, result.getInt(1), result.getString(8), result.getString(9));
				if(!result.getString(10).isEmpty()) data.setManPat(result.getString(10));
				if(!result.getString(11).isEmpty()) data.setWomanPat(result.getString(11));
				tree.storeRecord(data);

			}
		} catch (SQLException e) {
			System.out.println("Error parsing query result.");
			e.printStackTrace();
		}
		this.close();

	}



	//Also used to compute stats on date and place
	public void performPPMatching(TreeLevenshtein tree) throws IOException {
		PlaceCoordinatesConverter PCC = new PlaceCoordinatesConverter();

		List<String> father;
		List<String> mother;
		Statement statement = null;
		NaiveBayes comparator = new NaiveBayes("PP", 300000);
		BufferedWriter bw = new BufferedWriter(new FileWriter("PPCandidates.csv"));
		try {
			statement = this.connection.createStatement();
		} catch (SQLException e) {
			System.out.println("Error making statement.");
			e.printStackTrace();
		}
		ResultSet result = null;
		try {
			result = statement.executeQuery("SELECT record.Record_ID, father.FirstName, father.Surname, mother.FirstName, mother.Surname, father.standardFirstName, mother.standardFirstName, record.daterecord, record.Place, father.Patronymic, mother.Patronymic FROM birth_record record, person father, person mother WHERE father.Person_ID = record.Father_ID AND mother.Person_ID = record.Mother_ID and father.FirstName <> '' and father.Surname <> '' and mother.FirstName <> '' and mother.Surname <> ''"
					+ " AND mother.surname not like 'NN' AND mother.Surname not like 'N.N.' AND father.surname not like 'NN' AND father.Surname not like 'N.N.'");
		} catch (SQLException e) {
			System.out.println("Error executing query.");
			e.printStackTrace();
		}
		try {
			int i = 0;

			//bw.write("DocID_A,DocID_B,Score,DistFFN,DistFPat,DistFLN,DistMFN,DistMPat,DistMLN,GeoDist,DeltaYears\n"); 
			bw.write("DocID_A,DocID_B,Score\n");

			while (result.next()){
				i ++;
				if(i%1000 == 0) System.out.println(i);
		
				father = new ArrayList<String>();
				mother = new ArrayList<String>();
				if(result.getString(6) == null || result.getString(6).isEmpty()) father.add(result.getString(2)); // If standard first name not set, we use the person's first name
				else father.add(result.getString(6));
				father.add(result.getString(3)); // Surname
				if(result.getString(7) == null || result.getString(7).isEmpty()) mother.add(result.getString(4)); // If standard first name not set, we use the person's first name
				else  mother.add(result.getString(7));
				mother.add(result.getString(5));
				CoupleData data = new CoupleData(father, mother, result.getInt(1), result.getString(8), result.getString(9));
				if(!result.getString(10).isEmpty()) data.setManPat(result.getString(10));
				if(!result.getString(11).isEmpty()) data.setWomanPat(result.getString(11));

				tree.treeTraversalCouple(new BitVector(data), 0, tree.getRoot(), 0, 0, 0, 0, 0, 0, 0, 0, bw, data, PCC, comparator, "PP"); // Indexing metadata



				//tree.treeTraversalCouple(new BitVector(data), 0, tree.getRoot(), 0, 0, 0, 0, bw, data, PCC);

			}
		} catch (SQLException e) {
			System.out.println("Error parsing query result.");
			e.printStackTrace();
		}
		bw.close(); 
		this.close();

	}

	//Can also be used to prepare date and place stats retrieval for PM matching
	public void prepareMPmatching(TreeLevenshtein tree) {
		List<String> father = new ArrayList<String>();
		List<String> mother = new ArrayList<String>();
		Statement statement = null;
		try {
			statement = this.connection.createStatement();
		} catch (SQLException e) {
			System.out.println("Error making statement.");
			e.printStackTrace();
		}
		ResultSet result = null;
		try {
			result = statement.executeQuery("SELECT R.DateRecord, R.Record_ID, F.FirstName, F.Surname, F.Entity_ID, F.standardFirstName, M.FirstName, M.Surname, M.Entity_ID, M.standardFirstName, R.Place, F.Patronymic, M.Patronymic " +
					"FROM [thesis_miss].[dbo].[birth_record] R, [thesis_miss].[dbo].[person] F, [thesis_miss].[dbo].[person] M " +
					"WHERE F.Person_ID = R.Father_ID " +
					"AND M.Person_ID = R.Mother_ID " +
					//"AND M.Entity_ID is not null " +
					//"AND F.Entity_ID is not null " +
					"AND F.FirstName <> '' and F.Surname <> '' and M.FirstName <> '' and M.Surname <> ''"
					+ " AND M.surname not like 'NN' AND M.Surname not like 'N.N.' AND F.surname not like 'NN' AND F.Surname not like 'N.N.' " +
					"ORDER BY F.Entity_ID desc, M.Entity_ID desc");
		} catch (SQLException e) {
			System.out.println("Error executing query.");
			e.printStackTrace();
		}
		try {
			int minYear = -1;
			int maxYear = -1;
			int curEntity = -1;
			int prevEntity = -1;
			int year = -1;
			int recordID = -1;
			boolean store = false;

			int counter = 0;
			String yearString = null, fatherStandardFN = null, fatherLN = null, fatherFN = null, motherStandardFN = null, motherLN = null, motherFN = null, firstPlace = null, manPat = null, womanPat = null;
			while (result.next()){
				if(counter%10000 == 0) System.out.println(counter);
				counter++;

				prevEntity = curEntity;
				curEntity = result.getInt(5);


				if((prevEntity != -1 && prevEntity != curEntity) || (result.getString(5) == null && fatherLN != null)){ // Starting new entity, prev one has to be treated.
					//counter ++;
					if(fatherStandardFN == null || fatherStandardFN.isEmpty()) father.add(fatherFN); // If standard first name not set, we use the person's first name
					else father.add(fatherStandardFN);
					father.add(fatherLN); // Surname
					if(motherStandardFN == null || motherStandardFN.isEmpty()) mother.add(motherFN); // If standard first name not set, we use the person's first name
					else mother.add(motherStandardFN);
					mother.add(motherLN);

					//System.out.println("Storing record: " + father + " " + recordID + " " + minYear+";"+maxYear);
					if(store){
						CoupleData couple = new CoupleData(father, mother, recordID, minYear+";"+maxYear, firstPlace);
						couple.setManPat(manPat);
						couple.setWomanPat(womanPat);
						tree.storeRecord(couple);
					}
					//System.out.println("Storing record: " + father + " " + recordID + " " + minYear+";"+maxYear);

					//Cleaning buffers
					store = false;
					father = new ArrayList<String>();
					mother = new ArrayList<String>();
					minYear = -1;
					maxYear = -1;
					recordID = -1;
					yearString = null; fatherStandardFN = null; fatherLN = null; fatherFN = null; motherStandardFN = null; motherLN = null; motherFN = null; firstPlace = null; manPat = null; womanPat = null;

					//Treating new entity

					year = -1;
					yearString = result.getString(1).split("-")[0].replaceAll("[^0-9]", ""); 
					if (!yearString.isEmpty()){
						store = true;
						year = Integer.parseInt(yearString);
						if(minYear == -1){
							minYear = year;
							maxYear = year;
							firstPlace = result.getString(11);
							recordID = result.getInt(2);
							manPat = result.getString(12);
							womanPat = result.getString(13);
							if(fatherStandardFN == null || fatherStandardFN.isEmpty()) fatherStandardFN = result.getString(6);
							if(fatherFN == null || fatherFN.isEmpty()) fatherFN = result.getString(3);
							if(fatherLN == null || fatherLN.isEmpty()) fatherLN = result.getString(4);
							if(motherStandardFN == null || motherStandardFN.isEmpty()) motherStandardFN = result.getString(10);
							if(motherFN == null || motherFN.isEmpty()) motherFN = result.getString(7);
							if(motherLN == null || motherLN.isEmpty()) motherLN = result.getString(8);
						}
						else{
							if(year < minYear){
								minYear = year;
								firstPlace = result.getString(11);
								recordID = result.getInt(2);
								manPat = result.getString(12);
								womanPat = result.getString(13);
								if(fatherStandardFN == null || fatherStandardFN.isEmpty()) fatherStandardFN = result.getString(6);
								if(fatherFN == null || fatherFN.isEmpty()) fatherFN = result.getString(3);
								if(fatherLN == null || fatherLN.isEmpty()) fatherLN = result.getString(4);
								if(motherStandardFN == null || motherStandardFN.isEmpty()) motherStandardFN = result.getString(10);
								if(motherFN == null || motherFN.isEmpty()) motherFN = result.getString(7);
								if(motherLN == null || motherLN.isEmpty()) motherLN = result.getString(8);
							}
							maxYear = Math.max(year, maxYear);						 
						}	
					}

				}
				//Treating current entity
				else{
					recordID = result.getInt(2);
					manPat = result.getString(12);
					womanPat = result.getString(13);
					if(fatherStandardFN == null || fatherStandardFN.isEmpty()) fatherStandardFN = result.getString(6);
					if(fatherFN == null || fatherFN.isEmpty()) fatherFN = result.getString(3);
					if(fatherLN == null || fatherLN.isEmpty()) fatherLN = result.getString(4);
					if(motherStandardFN == null || motherStandardFN.isEmpty()) motherStandardFN = result.getString(10);
					if(motherFN == null || motherFN.isEmpty()) motherFN = result.getString(7);
					if(motherLN == null || motherLN.isEmpty()) motherLN = result.getString(8);
					year = -1;
					yearString = result.getString(1).split("-")[0].replaceAll("[^0-9]", ""); 
					if (!yearString.isEmpty()){
						store = true;
						year = Integer.parseInt(yearString);
						if(minYear == -1){
							minYear = year;
							maxYear = year;
							recordID = result.getInt(2);
							manPat = result.getString(12);
							womanPat = result.getString(13);
							if(fatherStandardFN == null || fatherStandardFN.isEmpty()) fatherStandardFN = result.getString(6);
							if(fatherFN == null || fatherFN.isEmpty()) fatherFN = result.getString(3);
							if(fatherLN == null || fatherLN.isEmpty()) fatherLN = result.getString(4);
							if(motherStandardFN == null || motherStandardFN.isEmpty()) motherStandardFN = result.getString(10);
							if(motherFN == null || motherFN.isEmpty()) motherFN = result.getString(7);
							if(motherLN == null || motherLN.isEmpty()) motherLN = result.getString(8);
						}
						else{
							if(year < minYear){
								minYear = year;
								firstPlace = result.getString(11);
								recordID = result.getInt(2);
								manPat = result.getString(12);
								womanPat = result.getString(13);
								if(fatherStandardFN == null || fatherStandardFN.isEmpty()) fatherStandardFN = result.getString(6);
								if(fatherFN == null || fatherFN.isEmpty()) fatherFN = result.getString(3);
								if(fatherLN == null || fatherLN.isEmpty()) fatherLN = result.getString(4);
								if(motherStandardFN == null || motherStandardFN.isEmpty()) motherStandardFN = result.getString(10);
								if(motherFN == null || motherFN.isEmpty()) motherFN = result.getString(7);
								if(motherLN == null || motherLN.isEmpty()) motherLN = result.getString(8);
							}
							maxYear = Math.max(year, maxYear);
						}	
					}
				}
			}
		} catch (SQLException e) {
			System.out.println("Error parsing query result.");
			e.printStackTrace();
		}
		this.close();

	}

	//Also used to compute stats on date and place
	public void performMPMatching(TreeLevenshtein tree) throws IOException {
		NaiveBayes comparator = new NaiveBayes("MP", 50000);
		PlaceCoordinatesConverter PCC = new PlaceCoordinatesConverter();
		List<String> groom;
		List<String> bride;
		Statement statement = null;
		BufferedWriter bw = new BufferedWriter(new FileWriter("CandidatesMP.csv")); 

		try {
			statement = this.connection.createStatement();
		} catch (SQLException e) {
			System.out.println("Error making statement.");
			e.printStackTrace();
		}
		ResultSet result = null;
		try {
			result = statement.executeQuery("SELECT record.Record_ID, groom.FirstName, groom.Surname, bride.FirstName, bride.Surname, groom.standardFirstName, bride.standardFirstName, record.daterecord, record.Place FROM [thesis_miss].[dbo].[marriage_record] record, [thesis_miss].[dbo].[person] groom, [thesis_miss].[dbo].[person] bride WHERE groom.Person_ID = record.Bridegroom_ID AND bride.Person_ID = record.Bride_ID and groom.FirstName <> '' and groom.Surname <> '' and bride.FirstName <> '' and bride.Surname <> ''"
					+ " AND groom.surname not like 'NN' AND groom.Surname not like 'N.N.' AND bride.surname not like 'NN' AND bride.Surname not like 'N.N.' ");
		} catch (SQLException e) {
			System.out.println("Error executing query.");
			e.printStackTrace();
		}
		try {
			int i = 0;

			bw.write("DocID_A,DocID_B,Score\n");
			//bw.write("DocID_A,DocID_B,Score,deltaYear,GeoDist,DistFFN,DistFPat,DistFLN,DistMFN,DistMPat,DistMLN\n");

			while (result.next()){
				if(i%1000 == 0) System.out.println(i);
				i ++;
					
				groom = new ArrayList<String>();
				bride = new ArrayList<String>();
				if(result.getString(6) == null || result.getString(6).isEmpty()) groom.add(result.getString(2)); // If standard first name not set, we use the person's first name
				else groom.add(result.getString(6));
				groom.add(result.getString(3)); // Surname
				if(result.getString(7) == null || result.getString(7).isEmpty()) bride.add(result.getString(4)); // If standard first name not set, we use the person's first name
				else  bride.add(result.getString(7));
				bride.add(result.getString(5));

				CoupleData data = new CoupleData(groom, bride, result.getInt(1), result.getString(8), result.getString(9));

				tree.treeTraversalCouple(new BitVector(data), 0, tree.getRoot(), 0, 0, 0, 0, 0, 0, 0, 0, bw, data, PCC, comparator, "MP"); // Indexing metadata
			}
		} catch (SQLException e) {
			System.out.println("Error parsing query result.");
			e.printStackTrace();
		}
		bw.close(); 
		this.close();

	}
	
	private void close(){
		try {
			this.connection.close();
		} catch (SQLException e) {
			System.out.println("Error closing connection to DB.");
			e.printStackTrace();
		}
	}


}



/*
//Effort to find statistical data about true matches. Couples will be matched only based on father's data which have an unpopular first name.
//By doing so, statistical data about mother's data can be collected.
//Launch this method after "addParentsToTree" (where the part in which mothers are added is commented).
public void fetchFatherssAndSearchPotentialMatches(TreeLevenshtein tree) throws IOException{
	List<String> father;
	Statement statement = null;
	BufferedWriter bw = new BufferedWriter(new FileWriter("statsMothers.txt")); 
	try {
		statement = this.connection.createStatement();
	} catch (SQLException e) {
		System.out.println("Error making statement.");
		e.printStackTrace();
	}
	ResultSet result = null;
	try {
		result = statement.executeQuery("SELECT record.Record_ID, father.FirstName, father.Surname, father.standardFirstName, record.daterecord, record.place FROM birth_record record, person father WHERE father.Person_ID = record.Father_ID AND father.FirstName <> '' AND father.Surname <> ''"
				+ "AND father.firstname in (" // We select names with low popularity
				+ "select FirstName from [thesis_miss].[dbo].[person],[thesis_miss].[dbo].[birth_record] record where Person_ID = Father_ID group by FirstName having count(*) < 500)");
	} catch (SQLException e) {
		System.out.println("Error executing query.");
		e.printStackTrace();
	}
	try {
		int i = 0;
		int recordID, year;
		String yearString;

		List<TreeTraversalCounter> metadatas = new ArrayList<TreeTraversalCounter>(); // Indexing metadata

		//bw.write("INSERT INTO P_P_Candidates (Role_A, DocID_A, Role_B, DocID_B) VALUES \n"); 
		bw.write("DocID_A,DocID_B"); 

		while (result.next()){
			i ++;
			if(i%10000 == 0) System.out.println(i);

			year = -1;
			yearString = result.getString(5).split("-")[0].replaceAll("[^0-9]", ""); 
			if (!yearString.isEmpty()) year = Integer.parseInt(yearString);	 		
			father = new ArrayList<String>();
			if(result.getString(4) == null || result.getString(4).isEmpty()) father.add(result.getString(2)); // If standard first name not set, we use the person's first name
			else father.add(result.getString(4));
			father.add(result.getString(3)); // Surname

			//PersonData data = new PersonData(father, 'D', result.getInt(1), -1, year, 'm', result.getString(6));

			//if (i == 1) bw.write("(-1, -1, -1, -1) \n");   
			//bw.write("");

			TreeTraversalCounter metadata = new TreeTraversalCounter(0, 0, 0, 0, 0); // Indexing metadata
			//tree.treeTraversalPersonWithMetada(new BitVector(data), 0, tree.getRoot(), 0, 0, 0, 0, bw, data, null, metadata);
			metadatas.add(metadata); // Indexing metadata 



			//tree.treeTraversalCouple(new BitVector(data), 0, tree.getRoot(), 0, 0, 0, 0, bw, data, PCC);

		}
		this.displayMetadata(metadatas); // Indexing metadata
	} catch (SQLException e) {
		System.out.println("Error parsing query result.");
		e.printStackTrace();
	}
	bw.close(); 
	this.close();
} */


/*
public void computeFeatures() throws IOException{
	BufferedReader br;
	String line;
	String[] curLine;
	BufferedWriter bw = new BufferedWriter(new FileWriter("LabeledSetPPfeatures.csv"));
	bw.write("DocID_A,DocID_B,Score,DistFFN,DistFPat,DistFLN,DistMFN,DistMPat,DistMLN,GeoDist,DeltaYears\n");

	br = new BufferedReader(new FileReader("LabeledSetforFeatures.csv"));
	line = br.readLine(); 
	line = br.readLine(); 
	curLine = new String[25];
	while(line != null) {			
		if(!line.isEmpty()){
			curLine = line.split(";");
			if(curLine.length == 25){ 	
				int distFFN = LevenshteinDistance.LevenshteinDistance(curLine[6].toLowerCase(), curLine[16].toLowerCase());
				int distFPat = -1; if(!curLine[7].isEmpty() && !curLine[17].isEmpty()) distFPat = LevenshteinDistance.LevenshteinDistance(curLine[7].toLowerCase(), curLine[17].toLowerCase());
				int distFLN = LevenshteinDistance.LevenshteinDistance(curLine[9].toLowerCase(), curLine[19].toLowerCase());
				int distMFN = LevenshteinDistance.LevenshteinDistance(curLine[10].toLowerCase(), curLine[20].toLowerCase());
				int distMPat = -1; if(!curLine[11].isEmpty() && !curLine[11].isEmpty()) distFPat = LevenshteinDistance.LevenshteinDistance(curLine[11].toLowerCase(), curLine[11].toLowerCase());
				int distMLN = LevenshteinDistance.LevenshteinDistance(curLine[13].toLowerCase(), curLine[23].toLowerCase());
				int geoDist = (int)Precision.round((double) PairwiseComparison.geoDistance(curLine[5], curLine[15], new PlaceCoordinatesConverter()), -1);
				int deltaYears = Math.abs(Integer.parseInt(curLine[4].split("-")[0].replaceAll("[^0-9]", "")) - Integer.parseInt(curLine[14].split("-")[0].replaceAll("[^0-9]", "")));
				bw.write(curLine[0] + "," + curLine[1] + "," + curLine[2] + "," + distFFN + "," + distFPat + "," + distFLN + "," + distMFN + "," + distMPat + "," + distMLN + "," + geoDist + "," + deltaYears + "\n");
			}
			line = br.readLine(); 
		}
	}
	bw.close();
	br.close();
} */


/*
public void computeStatistics(){
	Statement statement = null;
	PlaceCoordinatesConverter PCC = new PlaceCoordinatesConverter();
	String query = "Select R1.Place, M1.FirstName, M1.Patronymic, M1.Insertion, M1.Surname, R2.Place, M2.FirstName, M2.Patronymic, M2.Insertion, M2.Surname " +
			"from [thesis_miss].[dbo].[statsMothers] P, [thesis_miss].[dbo].[birth_record] R1, [thesis_miss].[dbo].[person] M1, [thesis_miss].[dbo].[birth_record] R2, [thesis_miss].[dbo].[person] M2 " +
			"where P.DocID_A = R1.Record_ID AND P.DocID_B = R2.Record_ID AND R1.Mother_ID = M1.Person_ID AND R2.Mother_ID = M2.Person_ID";

	try {
		statement = this.connection.createStatement();
	} catch (SQLException e) {
		System.out.println("Error making statement.");
		e.printStackTrace();
	}
	ResultSet result = null;
	try {
		result = statement.executeQuery(query);
	} catch (SQLException e) {
		System.out.println("Error executing query.");
		e.printStackTrace();
	}

	try {
		int i = 0;
		float avgPlaceLevScore = 0, avgFNLevScore = 0, avgInsertLevScore = 0, avgPatLevScore = 0, avgLNLevScore = 0, avgPlaceDistance = 0;
		int placeCounter = 0, FNCounter = 0, insertCounter = 0, patCounter = 0, LNCounter = 0;

		while (result.next()){
			i ++;
			if(i%10000 == 0) System.out.println(i);

			if (!result.getString(1).isEmpty() && !result.getString(6).isEmpty()){
				avgPlaceLevScore += 1 - (float)LevenshteinDistance.LevenshteinDistance(result.getString(1).toLowerCase(), result.getString(6).toLowerCase())/Math.max(result.getString(1).length(), result.getString(6).length());
				avgPlaceDistance += (float) Math.abs(PairwiseComparison.geoDistance(result.getString(1), result.getString(6), PCC));
				placeCounter ++;
			}

			if (!result.getString(2).isEmpty() && !result.getString(7).isEmpty()){
				avgFNLevScore += 1 - (float)LevenshteinDistance.LevenshteinDistance(result.getString(2).toLowerCase(), result.getString(7).toLowerCase())/Math.max(result.getString(2).length(), result.getString(7).length());
				FNCounter ++;
			}

			if (!result.getString(4).isEmpty() && !result.getString(9).isEmpty()){
				avgInsertLevScore += 1 - (float)LevenshteinDistance.LevenshteinDistance(result.getString(4).toLowerCase(), result.getString(9).toLowerCase())/Math.max(result.getString(4).length(), result.getString(9).length());
				insertCounter ++;
			}

			if (!result.getString(3).isEmpty() && !result.getString(8).isEmpty()){
				avgPatLevScore += 1 - (float)LevenshteinDistance.LevenshteinDistance(result.getString(3).toLowerCase(), result.getString(8).toLowerCase())/Math.max(result.getString(8).length(), result.getString(6).length());
				patCounter ++;
			}

			if (!result.getString(5).isEmpty() && !result.getString(10).isEmpty()){
				avgLNLevScore += 1 - (float)LevenshteinDistance.LevenshteinDistance(result.getString(5).toLowerCase(), result.getString(10).toLowerCase())/Math.max(result.getString(5).length(), result.getString(10).length());
				LNCounter ++;
			}
			/*if (!result.getString(1).isEmpty() && !result.getString(6).isEmpty()) System.out.println("avgPlaceLevScore: " + avgPlaceLevScore + " counter: " + placeCounter + " just added: " + (1-(float)LevenshteinDistance.LevenshteinDistance(result.getString(1).toLowerCase(), result.getString(6).toLowerCase())/Math.max(result.getString(1).length(), result.getString(6).length())) + " places are: " + result.getString(1) + " and " + result.getString(6));
			if (!result.getString(1).isEmpty() && !result.getString(6).isEmpty()) System.out.println("avgPlaceDistance: " + avgPlaceDistance + " counter: " + placeCounter + " just added: " + (float) Math.abs(PairwiseComparison.geoDistance(result.getString(1), result.getString(6), PCC)) + " places are: " + result.getString(1) + " and " + result.getString(6));
			if (!result.getString(2).isEmpty() && !result.getString(7).isEmpty()) System.out.println("avgFNLevScore: " + avgFNLevScore + " counter: " + FNCounter + " just added: " +  (1-(float)LevenshteinDistance.LevenshteinDistance(result.getString(2).toLowerCase(), result.getString(7).toLowerCase())/Math.max(result.getString(2).length(), result.getString(7).length())) + " names are: " + result.getString(2) + " and " + result.getString(7));
			if (!result.getString(4).isEmpty() && !result.getString(9).isEmpty()) System.out.println("avgInsertLevScore: " + avgInsertLevScore + " counter: " + insertCounter + " just added: " + (1-(float)LevenshteinDistance.LevenshteinDistance(result.getString(4).toLowerCase(), result.getString(9).toLowerCase())/Math.max(result.getString(4).length(), result.getString(9).length())) + " names are: " + result.getString(4) + " and " + result.getString(9));
			if (!result.getString(3).isEmpty() && !result.getString(8).isEmpty()) System.out.println("avgPatLevScore: " + avgPatLevScore + " counter: " + patCounter + " just added: " + (1-(float)LevenshteinDistance.LevenshteinDistance(result.getString(3).toLowerCase(), result.getString(8).toLowerCase())/Math.max(result.getString(8).length(), result.getString(6).length())) + " names are: " + result.getString(6) + " and " + result.getString(8));
			if (!result.getString(5).isEmpty() && !result.getString(10).isEmpty()) System.out.println("avgLNLevScore: " + avgLNLevScore + " counter: " + LNCounter + " just added: " + (1-(float)LevenshteinDistance.LevenshteinDistance(result.getString(5).toLowerCase(), result.getString(10).toLowerCase())/Math.max(result.getString(5).length(), result.getString(10).length())) + " names are: " + result.getString(5) + " and " + result.getString(10));
			System.out.println("====================================================================================="); */

		/*}

		avgPlaceLevScore = avgPlaceLevScore / placeCounter;
		avgFNLevScore = avgFNLevScore / FNCounter;
		avgInsertLevScore = avgInsertLevScore / insertCounter;
		avgPatLevScore = avgPatLevScore / patCounter;
		avgLNLevScore = avgLNLevScore / LNCounter;
		avgPlaceDistance = avgPlaceDistance / placeCounter;

		System.out.println("avgPlaceLevScore: " + avgPlaceLevScore);
		System.out.println("avgPlaceDistance: " + avgPlaceDistance);
		System.out.println("avgFNLevScore: " + avgFNLevScore);
		System.out.println("avgInsertLevScore: " + avgInsertLevScore);
		System.out.println("avgPatLevScore: " + avgPatLevScore);
		System.out.println("avgLNLevScore: " + avgLNLevScore);

	} catch (SQLException e) {
		System.out.println("Error parsing query result.");
		e.printStackTrace();
	}
}


public void collectStatsAboutAlreadyMatchedPP() throws IOException, SQLException{	
	Statement statement = null;
	String query = "SELECT R1.Record_ID, R2.Record_ID, R1.DateRecord as Date1, R1.Place as Place1, F1.FirstName as F1FN, F1.Patronymic as F1Pat, F1.Insertion as F1Insert, F1.Surname as F1LN, M1.FirstName as M1FN, M1.Patronymic as M1Pat, M1.Insertion as M1Insert, M1.Surname as M1LN, " + 
			"R2.DateRecord as Date2, R2.Place as Place2, F2.FirstName as F2FN, F2.Patronymic as F2Pat, F2.Insertion as F2Insert, F2.Surname as F2LN, M2.FirstName as M2FN, M2.Patronymic as M2Pat, M2.Insertion as M2Insert, M2.Surname as M2LN " +
			"from [thesis_miss].[dbo].[birth_record] R1, [thesis_miss].[dbo].[person] F1, [thesis_miss].[dbo].[person] M1 " +
			", [thesis_miss].[dbo].[birth_record] R2, [thesis_miss].[dbo].[person] F2, [thesis_miss].[dbo].[person] M2 " + 
			"where F1.Entity_ID = F2.Entity_ID AND M1.Entity_ID = M2.Entity_ID AND R1.Father_ID = F1.Person_ID AND R1.Mother_ID = M1.Person_ID " + 
			"AND R2.Father_ID = F2.Person_ID AND R2.Mother_ID = M2.Person_ID AND R1.Record_ID <> R2.Record_ID " +
			"AND M1.Surname <> 'N.N.' and M1.Surname <> 'NN' and M1.Surname <> '' AND M1.FirstName <> '' " +
			"AND M2.Surname <> 'N.N.' and M2.Surname <> 'NN' and M2.Surname <> '' AND M2.FirstName <> '' " +
			"AND F1.Surname <> 'N.N.' and F1.Surname <> 'NN' and F1.Surname <> '' AND F1.FirstName <> '' " +	
			"AND F2.Surname <> 'N.N.' and F2.Surname <> 'NN' and F2.Surname <> '' AND F2.FirstName <> '' " +
			"AND R1.DateRecord <> '' AND R2.DateRecord <> '' AND R1.Place <> '' AND R2.Place <> ''";
	
	BufferedWriter bw = new BufferedWriter(new FileWriter("statsPostMatchPP.txt"));
	bw.write("DocID_A,DocID_B,DistFFN,DistFPat,DistFLN,DistMFN,DistMPat,DistMLN,GeoDist,DeltaYears");
	
	try {
		statement = this.connection.createStatement();
	} catch (SQLException e) {
		System.out.println("Error making statement.");
		e.printStackTrace();
	}
	ResultSet result = null;
	try {
		result = statement.executeQuery(query);
	} catch (SQLException e) {
		System.out.println("Error executing query.");
		e.printStackTrace();
	}
	
	int i = 0;
	while (result.next()){
		i ++;
		if(i%10000 == 0) System.out.println(i);
		
		int distFFN = LevenshteinDistance.LevenshteinDistance(result.getString(5).toLowerCase(), result.getString(15).toLowerCase());
		int distFPat = -1; if(!result.getString(6).isEmpty() && !result.getString(16).isEmpty()) distFPat = LevenshteinDistance.LevenshteinDistance(result.getString(6).toLowerCase(), result.getString(16).toLowerCase());
		int distFLN = LevenshteinDistance.LevenshteinDistance(result.getString(8).toLowerCase(), result.getString(18).toLowerCase());
		int distMFN = LevenshteinDistance.LevenshteinDistance(result.getString(9).toLowerCase(), result.getString(19).toLowerCase());
		int distMPat = -1; if(!result.getString(10).isEmpty() && !result.getString(20).isEmpty()) distFPat = LevenshteinDistance.LevenshteinDistance(result.getString(10).toLowerCase(), result.getString(20).toLowerCase());
		int distMLN = LevenshteinDistance.LevenshteinDistance(result.getString(12).toLowerCase(), result.getString(22).toLowerCase());
		int geoDist = (int)Precision.round((double) PairwiseComparison.geoDistance(result.getString(4), result.getString(14), new PlaceCoordinatesConverter()), -1);
		int deltaYears = Math.abs(Integer.parseInt(result.getString(3).split("-")[0].replaceAll("[^0-9]", "")) - Integer.parseInt(result.getString(13).split("-")[0].replaceAll("[^0-9]", "")));
		bw.write(";" + result.getInt(1) + "," + result.getInt(2) + "," + distFFN + "," + distFPat + "," + distFLN + "," + distMFN + "," + distMPat + "," + distMLN + "," + geoDist + "," + deltaYears);		
	}
	
	bw.close();
	this.close();
	
}

public void collectStatsAboutAlreadyMatchedMP() throws IOException, SQLException{	
	Statement statement = null;
	String query = "SELECT marriage.Record_ID, birth.Record_ID, marriage.DateRecord as dateMarriage, marriage.Place as placeMarriage, groom.FirstName as GFN, groom.Patronymic as GPat, groom.Insertion as GInsert, groom.Surname as GLN, " +
			"bride.FirstName as BFN, bride.Patronymic as BPat, bride.Insertion as BInsert, bride.Surname as BLN, " +
			"birth.DateRecord as dateBirth, birth.Place as placeBirth,father.FirstName as FFN, father.Patronymic as FPat, father.Insertion as FInsert, father.Surname as FLN, " +
			"mother.FirstName as MFN, mother.Patronymic as MPat, mother.Insertion as MInsert, mother.Surname as MLN " +
			"from [thesis_miss].[dbo].[birth_record] birth, [thesis_miss].[dbo].[marriage_record] marriage, " + 
			"[thesis_miss].[dbo].[person] groom, [thesis_miss].[dbo].[person] bride, [thesis_miss].[dbo].[person] father, [thesis_miss].[dbo].[person] mother " +
			"WHERE marriage.Bridegroom_ID = groom.Person_ID AND marriage.Bride_ID = bride.Person_ID " +
			"AND birth.Father_ID = father.Person_ID AND birth.Mother_ID = mother.Person_ID " +
			"AND father.Entity_ID_raw = groom.Entity_ID_raw AND mother.Entity_ID_raw = bride.Entity_ID_raw " +
			"AND bride.Surname <> 'N.N.' and bride.Surname <> 'NN' and bride.Surname <> '' AND bride.FirstName <> '' " + 
			"AND mother.Surname <> 'N.N.' and mother.Surname <> 'NN' and mother.Surname <> '' AND mother.FirstName <> '' " + 
			"AND groom.Surname <> 'N.N.' and groom.Surname <> 'NN' and groom.Surname <> '' AND groom.FirstName <> '' " + 
			"AND father.Surname <> 'N.N.' and father.Surname <> 'NN' and father.Surname <> '' AND father.FirstName <> '' " + 
			"AND marriage.DateRecord <> '' AND birth.DateRecord <> '' AND marriage.Place <> '' AND birth.Place <> ''";
	
	BufferedWriter bw = new BufferedWriter(new FileWriter("statsPostMatchMP_raw.txt"));
	bw.write("DocID_A,DocID_B,DistFFN,DistFPat,DistFLN,DistMFN,DistMPat,DistMLN,GeoDist,DeltaYears");
	
	try {
		statement = this.connection.createStatement();
	} catch (SQLException e) {
		System.out.println("Error making statement.");
		e.printStackTrace();
	}
	ResultSet result = null;
	try {
		result = statement.executeQuery(query);
	} catch (SQLException e) {
		System.out.println("Error executing query.");
		e.printStackTrace();
	}
	
	int i = 0;
	while (result.next()){
		i ++;
		if(i%10000 == 0) System.out.println(i);
		
		int distFFN = LevenshteinDistance.LevenshteinDistance(result.getString(5).toLowerCase(), result.getString(15).toLowerCase());
		int distFPat = -1; if(!result.getString(6).isEmpty() && !result.getString(16).isEmpty()) distFPat = LevenshteinDistance.LevenshteinDistance(result.getString(6).toLowerCase(), result.getString(16).toLowerCase());
		int distFLN = LevenshteinDistance.LevenshteinDistance(result.getString(8).toLowerCase(), result.getString(18).toLowerCase());
		int distMFN = LevenshteinDistance.LevenshteinDistance(result.getString(9).toLowerCase(), result.getString(19).toLowerCase());
		int distMPat = -1; if(!result.getString(10).isEmpty() && !result.getString(20).isEmpty()) distFPat = LevenshteinDistance.LevenshteinDistance(result.getString(10).toLowerCase(), result.getString(20).toLowerCase());
		int distMLN = LevenshteinDistance.LevenshteinDistance(result.getString(12).toLowerCase(), result.getString(22).toLowerCase());
		int geoDist = (int)Precision.round((double) PairwiseComparison.geoDistance(result.getString(4), result.getString(14), new PlaceCoordinatesConverter()), -1);
		int deltaYears = Math.abs(Integer.parseInt(result.getString(3).split("-")[0].replaceAll("[^0-9]", "")) - Integer.parseInt(result.getString(13).split("-")[0].replaceAll("[^0-9]", "")));
		bw.write(";" + result.getInt(1) + "," + result.getInt(2) + "," + distFFN + "," + distFPat + "," + distFLN + "," + distMFN + "," + distMPat + "," + distMLN + "," + geoDist + "," + deltaYears);		
	}
	
	bw.close();
	this.close();
	
}

public void collectStatsAboutAlreadyMatchedBMP() throws IOException, SQLException{	
	Statement statement = null;
	String query = "SELECT P1.[DocID_A],P1.[DocID_B],P1.[Child_ID],P1.[Parent_ID], " +
			"convert(real, P1.[Score]) as Score, " +
			"birth.DateRecord as birthDate, birth.Place as birthPlace, child.FirstName as CFN, child.Patronymic as CPat, child.Surname as CLN, " +
			"parenting.DateRecord as parentingDate, parenting.Place as parentingPlace, parent.FirstName as PFN, parent.Patronymic as PPat, parent.Surname as PLN " +
			"FROM [thesis_miss].[dbo].[BMPCandidates-incomplete] P1, [thesis_miss].[dbo].[person] child, " +
			"[thesis_miss].[dbo].[birth_record] birth, [thesis_miss].[dbo].[person] parent, [thesis_miss].[dbo].[birth_record] parenting " +
			"WHERE  convert(real, [Score]) IN " +
			"(SELECT max(convert(real, [Score])) " + 
			"FROM [thesis_miss].[dbo].[BMPCandidates-incomplete] P2 " + 
			"WHERE P1.DocID_A = P2.DocID_A) " +
			"AND convert(real, [Score]) IN " +
			"(SELECT max(convert(real, [Score])) " + 
			"FROM [thesis_miss].[dbo].[BMPCandidates-incomplete] P2 " +
			"WHERE P1.DocID_B = P2.DocID_B) " +
			"AND child.Person_ID = birth.Child_ID AND child.Person_ID = P1.[Child_ID] " +
			"AND parent.Person_ID =  P1.[Parent_ID] AND parenting.Record_ID = P1.DocID_B " +
			"order by P1.[DocID_A] ";
	
	BufferedWriter bw = new BufferedWriter(new FileWriter("statsPostMatchBMP.txt"));
	bw.write("DocID_A,DocID_B,Child_ID,Parent_ID,DistFN,DistLN,GeoDist,DeltaYears");
	
	try {
		statement = this.connection.createStatement();
	} catch (SQLException e) {
		System.out.println("Error making statement.");
		e.printStackTrace();
	}
	ResultSet result = null;
	try {
		result = statement.executeQuery(query);
	} catch (SQLException e) {
		System.out.println("Error executing query.");
		e.printStackTrace();
	}
	
	int i = 0;
	while (result.next()){
		i ++;
		if(i%10000 == 0) System.out.println(i);
		
		int distFN = LevenshteinDistance.LevenshteinDistance(result.getString(8).toLowerCase(), result.getString(13).toLowerCase());
		int distLN = LevenshteinDistance.LevenshteinDistance(result.getString(10).toLowerCase(), result.getString(15).toLowerCase());
		int geoDist = (int)Precision.round((double) PairwiseComparison.geoDistance(result.getString(7), result.getString(12), new PlaceCoordinatesConverter()), -1);
		int deltaYears = Math.abs(Integer.parseInt(result.getString(6).split("-")[0].replaceAll("[^0-9]", "")) - Integer.parseInt(result.getString(11).split("-")[0].replaceAll("[^0-9]", "")));
		bw.write(";" + result.getInt(1) + "," + result.getInt(2) + "," + result.getInt(3) + "," + result.getInt(4) + "," + distFN + "," + distLN + "," + geoDist + "," + deltaYears);		
	}
	
	bw.close();
	this.close();
	
} */
