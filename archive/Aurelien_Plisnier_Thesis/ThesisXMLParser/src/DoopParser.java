import java.util.ArrayList;
import java.util.List;

import javax.xml.parsers.SAXParser;  
import javax.xml.parsers.SAXParserFactory;  

import org.xml.sax.Attributes;  
import org.xml.sax.SAXException;  
import org.xml.sax.helpers.DefaultHandler;  

public class DoopParser extends DefaultHandler{  

	public void parse(String path){  
		try {  
			// obtain and configure a SAX based parser  
			SAXParserFactory saxParserFactory = SAXParserFactory.newInstance();  

			// obtain object for SAX parser  
			SAXParser saxParser = saxParserFactory.newSAXParser();  

			// default handler for SAX handler class  
			// all three methods are written in handler's body  
			DefaultHandler defaultHandler = new DefaultHandler(){  

				int recordDepth = 0;

				int positionFlag = -1;

				boolean childFieldTag = false;
				boolean fatherFieldTag = false;
				boolean motherFieldTag = false;
				boolean witnessFieldTag = false;

				String registerID = "";
				String place = "";
				String dateRecord = "";

				String childFirstName = "";
				String childPatronymic = "";
				String childInsertion = "";
				String childSurname = "";
				String childAlias = "";
				String childSex = "";
				String childBirthPlace = "";
				String childLivingPlace = "";
				String childAge = "-1";
				String childDateOfBirth = "0000-00-00";
				String childMisc = "";

				String fatherFirstName = "";
				String fatherPatronymic = "";
				String fatherInsertion = "";
				String fatherSurname = "";
				String fatherAlias = "";
				String fatherSex = "m";
				String fatherBirthPlace = "";
				String fatherLivingPlace = "";
				String fatherAge = "-1";
				String fatherDateOfBirth = "0000-00-00";
				String fatherMisc = "";

				String motherFirstName = "";
				String motherPatronymic = "";
				String motherInsertion = "";
				String motherSurname = "";
				String motherAlias = "";
				String motherSex = "v";
				String motherBirthPlace = "";
				String motherLivingPlace = "";
				String motherAge = "-1";
				String motherDateOfBirth = "0000-00-00";
				String motherMisc = "";

				int witnessCount = 0;
				List<String> witnessFirstName = new ArrayList<String>();
				List<String> witnessPatronymic = new ArrayList<String>();
				List<String> witnessInsertion = new ArrayList<String>();
				List<String> witnessSurname = new ArrayList<String>();
				List<String> witnessAlias = new ArrayList<String>();
				List<String> witnessSex = new ArrayList<String>();
				List<String> witnessBirthPlace = new ArrayList<String>();
				List<String> witnessLivingPlace = new ArrayList<String>();
				List<String> witnessAge = new ArrayList<String>();
				List<String> witnessDateOfBirth = new ArrayList<String>();
				List<String> witnessMisc = new ArrayList<String>();

				boolean witnessIsset = false;
				boolean fatherIsset = false;
				boolean motherIsset = false;


				// this method is called every time the parser gets an open tag '<'  
				// identifies which tag is being open at time by assigning an open flag  
				public void startElement(String uri, String localName, String qName, Attributes attributes) throws SAXException {

					//Depth counter
					if (qName.equalsIgnoreCase("RECORD")) recordDepth ++;

					//child
					if (qName.equalsIgnoreCase("FIELD") && attributes.getValue(0).equalsIgnoreCase("Kind")){
						childFieldTag = true;
						fatherFieldTag = false;
						motherFieldTag = false;
						witnessFieldTag = false;
					}

					//father
					if (qName.equalsIgnoreCase("FIELD") && attributes.getValue(0).equalsIgnoreCase("Vader")){
						childFieldTag = false;
						fatherFieldTag = true;
						motherFieldTag = false;
						witnessFieldTag = false;
					}

					//mother
					if (qName.equalsIgnoreCase("FIELD") && attributes.getValue(0).equalsIgnoreCase("Moeder")){
						childFieldTag = false;
						fatherFieldTag = false;
						motherFieldTag = true;
						witnessFieldTag = false;
					}

					//witness
					if (qName.equalsIgnoreCase("FIELD") && attributes.getValue(0).equalsIgnoreCase("Getuige")){
						childFieldTag = false;
						fatherFieldTag = false;
						motherFieldTag = false;
						witnessFieldTag = true;
					}

					if (qName.equalsIgnoreCase("record") && witnessFieldTag){
						witnessCount++;

						witnessFirstName.add("");
						witnessPatronymic.add("");
						witnessInsertion.add("");
						witnessSurname.add("");
						witnessAlias.add("");
						witnessSex.add("");
						witnessBirthPlace.add("");
						witnessLivingPlace.add("");
						witnessAge.add("-1");
						witnessDateOfBirth.add("0000-00-00");
						witnessMisc.add("");
					}

					/*****************************RECORD************************************************************************/

					//RegisterID
					if (qName.equalsIgnoreCase("FIELD") && attributes.getValue(0).equalsIgnoreCase("REGISTER")) positionFlag = 0;
					if (qName.equalsIgnoreCase("ENTITY") && positionFlag==0) positionFlag = 100; 
					if (qName.equalsIgnoreCase("record") && positionFlag==100) registerID = attributes.getValue(0);

					//Place
					if (qName.equalsIgnoreCase("FIELD") && attributes.getValue(0).equalsIgnoreCase("PLAATS")) positionFlag = 1;
					if (qName.equalsIgnoreCase("VALUE") && positionFlag == 1) positionFlag = 2;

					//Date
					if (qName.equalsIgnoreCase("FIELD") && attributes.getValue(0).equalsIgnoreCase("DATUM")) positionFlag = 3;
					if (qName.equalsIgnoreCase("VALUE") && positionFlag == 3) positionFlag = 4;

					/*****************************CHILD*************************************************************************/

					//childFirstName
					if (qName.equalsIgnoreCase("FIELD") && attributes.getValue(0).equalsIgnoreCase("voornaam") && childFieldTag) positionFlag = 5;
					if (qName.equalsIgnoreCase("VALUE") && positionFlag == 5) positionFlag = 6;

					//childPatronymic
					if (qName.equalsIgnoreCase("FIELD") && attributes.getValue(0).equalsIgnoreCase("patroniem") && childFieldTag) positionFlag = 7;
					if (qName.equalsIgnoreCase("VALUE") && positionFlag == 7) positionFlag = 8;

					//childInsertion
					if (qName.equalsIgnoreCase("FIELD") && attributes.getValue(0).equalsIgnoreCase("tussenvoegsel") && childFieldTag) positionFlag = 9;
					if (qName.equalsIgnoreCase("VALUE") && positionFlag == 9) positionFlag = 10;

					//childSurname
					if (qName.equalsIgnoreCase("FIELD") && attributes.getValue(0).equalsIgnoreCase("geslachtsnaam") && childFieldTag) positionFlag = 11;
					if (qName.equalsIgnoreCase("VALUE") && positionFlag == 11) positionFlag = 12;

					//childAlias
					if (qName.equalsIgnoreCase("FIELD") && attributes.getValue(0).equalsIgnoreCase("alias") && childFieldTag) positionFlag = 13;
					if (qName.equalsIgnoreCase("VALUE") && positionFlag == 13) positionFlag = 14; 

					//child birth place
					if (qName.equalsIgnoreCase("FIELD") && attributes.getValue(0).equalsIgnoreCase("plaats_geboorte") && childFieldTag) positionFlag = 15;
					if (qName.equalsIgnoreCase("VALUE") && positionFlag == 15) positionFlag = 16; 

					//child sex
					if (qName.equalsIgnoreCase("FIELD") && attributes.getValue(0).equalsIgnoreCase("geslacht") && childFieldTag) positionFlag = 17;
					if (qName.equalsIgnoreCase("VALUE") && positionFlag == 17) positionFlag = 18;

					//child age
					if (qName.equalsIgnoreCase("FIELD") && attributes.getValue(0).equalsIgnoreCase("leeftijd") && childFieldTag) positionFlag = 19;
					if (qName.equalsIgnoreCase("VALUE") && positionFlag == 19) positionFlag = 20;

					//child misc
					if (qName.equalsIgnoreCase("FIELD") && attributes.getValue(0).equalsIgnoreCase("diversen") && childFieldTag) positionFlag = 21;
					if (qName.equalsIgnoreCase("VALUE") && positionFlag == 21) positionFlag = 22;


					/*****************************FATHER************************************************************************/

					//fatherFirstName
					if (qName.equalsIgnoreCase("FIELD") && attributes.getValue(0).equalsIgnoreCase("voornaam") && fatherFieldTag) positionFlag = 23;
					if (qName.equalsIgnoreCase("VALUE") && positionFlag == 23) positionFlag = 24;

					//fatherPatronymic
					if (qName.equalsIgnoreCase("FIELD") && attributes.getValue(0).equalsIgnoreCase("patroniem") && fatherFieldTag) positionFlag = 25;
					if (qName.equalsIgnoreCase("VALUE") && positionFlag == 25) positionFlag = 26;

					//fatherInsertion
					if (qName.equalsIgnoreCase("FIELD") && attributes.getValue(0).equalsIgnoreCase("tussenvoegsel") && fatherFieldTag) positionFlag = 27;
					if (qName.equalsIgnoreCase("VALUE") && positionFlag == 27) positionFlag = 28;

					//fatherSurname
					if (qName.equalsIgnoreCase("FIELD") && attributes.getValue(0).equalsIgnoreCase("geslachtsnaam") && fatherFieldTag) positionFlag = 29;
					if (qName.equalsIgnoreCase("VALUE") && positionFlag == 29) positionFlag = 30;

					//fatherAlias
					if (qName.equalsIgnoreCase("FIELD") && attributes.getValue(0).equalsIgnoreCase("alias") && fatherFieldTag) positionFlag = 31;
					if (qName.equalsIgnoreCase("VALUE") && positionFlag == 31) positionFlag = 32; 

					//father misc
					if (qName.equalsIgnoreCase("FIELD") && attributes.getValue(0).equalsIgnoreCase("diversen") && fatherFieldTag) positionFlag = 39;
					if (qName.equalsIgnoreCase("VALUE") && positionFlag == 39) positionFlag = 40;

					/*****************************MOTHER************************************************************************/

					//motherFirstName
					if (qName.equalsIgnoreCase("FIELD") && attributes.getValue(0).equalsIgnoreCase("voornaam") && motherFieldTag) positionFlag = 41;
					if (qName.equalsIgnoreCase("VALUE") && positionFlag == 41) positionFlag = 42;

					//motherPatronymic
					if (qName.equalsIgnoreCase("FIELD") && attributes.getValue(0).equalsIgnoreCase("patroniem") && motherFieldTag) positionFlag = 43;
					if (qName.equalsIgnoreCase("VALUE") && positionFlag == 43) positionFlag = 44;

					//motherInsertion
					if (qName.equalsIgnoreCase("FIELD") && attributes.getValue(0).equalsIgnoreCase("tussenvoegsel") && motherFieldTag) positionFlag = 45;
					if (qName.equalsIgnoreCase("VALUE") && positionFlag == 45) positionFlag = 46;

					//motherSurname
					if (qName.equalsIgnoreCase("FIELD") && attributes.getValue(0).equalsIgnoreCase("geslachtsnaam") && motherFieldTag) positionFlag = 47;
					if (qName.equalsIgnoreCase("VALUE") && positionFlag == 47) positionFlag = 48;

					//motherAlias
					if (qName.equalsIgnoreCase("FIELD") && attributes.getValue(0).equalsIgnoreCase("alias") && motherFieldTag) positionFlag = 49;
					if (qName.equalsIgnoreCase("VALUE") && positionFlag == 49) positionFlag = 50; 

					//mother misc
					if (qName.equalsIgnoreCase("FIELD") && attributes.getValue(0).equalsIgnoreCase("diversen") && motherFieldTag) positionFlag = 51;
					if (qName.equalsIgnoreCase("VALUE") && positionFlag == 51) positionFlag = 52;

					/*****************************WITNESS************************************************************************/

					//witnessFirstName
					if (qName.equalsIgnoreCase("FIELD") && attributes.getValue(0).equalsIgnoreCase("voornaam") && witnessFieldTag) positionFlag = 65;
					if (qName.equalsIgnoreCase("VALUE") && positionFlag == 65) positionFlag = 66;

					//witnessPatronymic
					if (qName.equalsIgnoreCase("FIELD") && attributes.getValue(0).equalsIgnoreCase("patroniem") && witnessFieldTag) positionFlag = 67;
					if (qName.equalsIgnoreCase("VALUE") && positionFlag == 67) positionFlag = 68;

					//witnessInsertion
					if (qName.equalsIgnoreCase("FIELD") && attributes.getValue(0).equalsIgnoreCase("tussenvoegsel") && witnessFieldTag) positionFlag = 69;
					if (qName.equalsIgnoreCase("VALUE") && positionFlag == 69) positionFlag = 70;

					//witnessSurname
					if (qName.equalsIgnoreCase("FIELD") && attributes.getValue(0).equalsIgnoreCase("geslachtsnaam") && witnessFieldTag) positionFlag = 71;
					if (qName.equalsIgnoreCase("VALUE") && positionFlag == 71) positionFlag = 72;

					//witnessAlias
					if (qName.equalsIgnoreCase("FIELD") && attributes.getValue(0).equalsIgnoreCase("alias") && witnessFieldTag) positionFlag = 73;
					if (qName.equalsIgnoreCase("VALUE") && positionFlag == 73) positionFlag = 74; 

					//witness misc
					if (qName.equalsIgnoreCase("FIELD") && attributes.getValue(0).equalsIgnoreCase("diversen") && witnessFieldTag) positionFlag = 75;
					if (qName.equalsIgnoreCase("VALUE") && positionFlag == 75) positionFlag = 76;

				}  

				// prints data stored in between '<' and '>' tags  
				public void characters(char ch[], int start, int length) throws SAXException {

					/*****************************RECORD************************************************************************/

					//Place
					if (positionFlag == 2) place = new String(ch, start, length); 

					//Date
					if (positionFlag == 4) dateRecord = new String(ch, start, length); 

					/*****************************CHILD*************************************************************************/

					//childFirstName
					if (positionFlag == 6) childFirstName = new String(ch, start, length); 

					//childPatronymic
					if (positionFlag == 8) childPatronymic = new String(ch, start, length); 

					//childInsertion
					if (positionFlag == 10) childInsertion = new String(ch, start, length); 

					//childSurname
					if (positionFlag == 12) childSurname = new String(ch, start, length); 

					//childAlias
					if (positionFlag == 14) childAlias = new String(ch, start, length); 

					//child birth place
					if (positionFlag == 16) childBirthPlace = new String(ch, start, length); 

					//child living place
					if (positionFlag == 18) childSex = new String(ch, start, length); 

					//child age
					if (positionFlag == 20) childAge = new String(ch, start, length); 

					//child misc
					if (positionFlag == 22) childMisc = new String(ch, start, length); 

					/*****************************FATHER*************************************************************************/

					//fatherFirstName
					if (positionFlag == 24){
						fatherFirstName = new String(ch, start, length); 
						fatherIsset = true;
					}

					//fatherPatronymic
					if (positionFlag == 26){
						fatherPatronymic = new String(ch, start, length);
						fatherIsset = true;
					}

					//fatherInsertion
					if (positionFlag == 28){
						fatherInsertion = new String(ch, start, length); 
						fatherIsset = true;
					}

					//fatherSurname
					if (positionFlag == 30){
						fatherSurname = new String(ch, start, length); 
						fatherIsset = true;
					}

					//fatherAlias
					if (positionFlag == 32){
						fatherAlias = new String(ch, start, length); 
						fatherIsset = true;
					}

					//father misc
					if (positionFlag == 40){
						fatherMisc = new String(ch, start, length);
						fatherIsset = true;
					}

					/*****************************MOTHER************************************************************************/

					//motherFirstName
					if (positionFlag == 42){
						motherFirstName = new String(ch, start, length); 
						motherIsset = true;
					}

					//motherPatronymic
					if (positionFlag == 44){
						motherPatronymic = new String(ch, start, length); 
						motherIsset = true;
					}

					//motherInsertion
					if (positionFlag == 46){
						motherInsertion = new String(ch, start, length); 
						motherIsset = true;
					}

					//motherSurname
					if (positionFlag == 48){
						motherSurname = new String(ch, start, length); 
						motherIsset = true;
					}

					//motherAlias
					if (positionFlag == 50){
						motherAlias = new String(ch, start, length);
						motherIsset = true;
					}

					//mother misc
					if (positionFlag == 52){
						motherMisc = new String(ch, start, length);
						motherIsset = true;
					}

					/*****************************WITNESS*******************************************************************/

					//witnessFirstName
					if (positionFlag == 66){
						witnessFirstName.set(witnessCount-1, new String(ch, start, length)); 
						witnessIsset = true;
					}

					//witnessPatronymic
					if (positionFlag == 68){
						witnessPatronymic.set(witnessCount-1, new String(ch, start, length));
						witnessIsset = true;
					}

					//witnessInsertion
					if (positionFlag == 70){
						witnessInsertion.set(witnessCount-1, new String(ch, start, length));
						witnessIsset = true;
					}

					//witnessSurname
					if (positionFlag == 72){
						witnessSurname.set(witnessCount-1, new String(ch, start, length));
						witnessIsset = true;
					}

					//witnessAlias
					if (positionFlag == 74){
						witnessAlias.set(witnessCount-1, new String(ch, start, length));
						witnessIsset = true;
					}

					//witness misc
					if (positionFlag == 76){
						witnessMisc.set(witnessCount-1, new String(ch, start, length));
						witnessIsset = true;
					}
				}  

				// calls by the parser whenever '>' end tag is found in xml   
				// makes tags flag to 'close'  
				public void endElement(String uri, String localName, String qName) throws SAXException { 

					//Tags
					positionFlag = -1;

					//SQL
					if (qName.equalsIgnoreCase("RECORD")) {
						//Depth counter
						recordDepth--; 
						if (recordDepth == 0){ // A full record is read: SQL INSERT
							DbHandler database = new DbHandler();
							//witnessCount = 0;

							/*****************************CHILD********************************************************************/

							String query = "INSERT INTO person (FirstName, Patronymic, Insertion, Surname, Alias, Sex, BirthPlace, LivingPlace, Age, DateOfBirth, Miscellaneous)"
									+ " VALUES ('" + childFirstName.replace("'", "''").replace("\\", "")
									+ "','" + childPatronymic.replace("'", "''").replace("\\", "")
									+ "','" + childInsertion.replace("'", "''").replace("\\", "")
									+ "','" + childSurname.replace("'", "''").replace("\\", "")
									+ "','" + childAlias.replace("'", "''").replace("\\", "")
									+ "','" + childSex
									+ "','" + childBirthPlace.replace("'", "''").replace("\\", "")
									+ "','" + childLivingPlace.replace("'", "''").replace("\\", "")
									+ "','" + childAge
									+ "','" + childDateOfBirth 
									+ "','" + childMisc.replace("'", "''").replace("\\", "")
									+ "');";
							database.runQuery(query);

							childFirstName = "";
							childPatronymic = "";
							childInsertion = "";
							childSurname = "";
							childAlias = "";
							childSex = "";
							childBirthPlace = "";
							childLivingPlace = "";
							childAge = "-1";
							childDateOfBirth = "0000-00-00";
							childMisc = "";

							query = "SET @childID = LAST_INSERT_ID(); ";
							database.runQuery(query);

							/*****************************FATHER********************************************************************/
							if (fatherIsset){
								query = "INSERT INTO person (FirstName, Patronymic, Insertion, Surname, Alias, Sex, BirthPlace, LivingPlace, Age, DateOfBirth, Miscellaneous)"
										+ " VALUES ('" + fatherFirstName.replace("'", "''").replace("\\", "")
										+ "','" + fatherPatronymic.replace("'", "''").replace("\\", "")
										+ "','" + fatherInsertion.replace("'", "''").replace("\\", "")
										+ "','" + fatherSurname.replace("'", "''").replace("\\", "")
										+ "','" + fatherAlias.replace("'", "''").replace("\\", "")
										+ "','" + fatherSex
										+ "','" + fatherBirthPlace.replace("'", "''").replace("\\", "")
										+ "','" + fatherLivingPlace.replace("'", "''").replace("\\", "")
										+ "','" + fatherAge
										+ "','" + fatherDateOfBirth 
										+ "','" + fatherMisc.replace("'", "''").replace("\\", "") 
										+ "');";
								database.runQuery(query);
								fatherIsset = false;
								fatherFirstName = "";
								fatherPatronymic = "";
								fatherInsertion = "";
								fatherSurname = "";
								fatherAlias = "";
								fatherSex = "";
								fatherBirthPlace = "";
								fatherLivingPlace = "";
								fatherAge = "-1";
								fatherDateOfBirth = "0000-00-00";
								fatherMisc = "";

								query = "SET @fatherID = LAST_INSERT_ID(); ";
								database.runQuery(query);}
							else { query = "SET @fatherID = -1; "; database.runQuery(query);}

							/*****************************MOTHER********************************************************************/
							if(motherIsset){
								query = "INSERT INTO person (FirstName, Patronymic, Insertion, Surname, Alias, Sex, BirthPlace, LivingPlace, Age, DateOfBirth, Miscellaneous)"
										+ " VALUES ('" + motherFirstName.replace("'", "''").replace("\\", "")
										+ "','" + motherPatronymic.replace("'", "''").replace("\\", "")
										+ "','" + motherInsertion.replace("'", "''").replace("\\", "")
										+ "','" + motherSurname.replace("'", "''").replace("\\", "")
										+ "','" + motherAlias.replace("'", "''").replace("\\", "")
										+ "','" + motherSex
										+ "','" + motherBirthPlace.replace("'", "''").replace("\\", "")
										+ "','" + motherLivingPlace.replace("'", "''").replace("\\", "")
										+ "','" + motherAge
										+ "','" + motherDateOfBirth 
										+ "','" + motherMisc.replace("'", "''").replace("\\", "")
										+ "');";
								database.runQuery(query);
								motherIsset = false;
								motherFirstName = "";
								motherPatronymic = "";
								motherInsertion = "";
								motherSurname = "";
								motherAlias = "";
								motherSex = "";
								motherBirthPlace = "";
								motherLivingPlace = "";
								motherAge = "-1";
								motherDateOfBirth = "0000-00-00";
								motherMisc = "";

								query = "SET @motherID = LAST_INSERT_ID(); ";
								database.runQuery(query);
							}else { query = "SET @motherID = -1; "; database.runQuery(query);}

							/*****************************RECORD********************************************************************/

							query = "INSERT INTO birth_record (Register_ID, Place, DateRecord, Child_ID, Father_ID , Mother_ID) "
									+ "VALUES ('" + registerID
									+ "','" + place.replace("'", "''").replace("\\", "")
									+ "','" + dateRecord
									+ "', @childID" 
									+ ", @fatherID"
									+ ", @motherID" 
									+ ");";
							database.runQuery(query);

							query = "SET @recordID = LAST_INSERT_ID(); ";
							database.runQuery(query);



							registerID = "";
							place = "";
							dateRecord = "";

							/*****************************WITNESS********************************************************************/
							if(witnessIsset){
								for(int i = 0; i < witnessCount; i++){
									query = "INSERT INTO person (FirstName, Patronymic, Insertion, Surname, Alias, Sex, BirthPlace, LivingPlace, Age, DateOfBirth, Miscellaneous)"
											+ " VALUES ('" + witnessFirstName.get(i).replace("'", "''").replace("\\", "")
											+ "','" + witnessPatronymic.get(i).replace("'", "''").replace("\\", "")
											+ "','" + witnessInsertion.get(i).replace("'", "''").replace("\\", "")
											+ "','" + witnessSurname.get(i).replace("'", "''").replace("\\", "")
											+ "','" + witnessAlias.get(i).replace("'", "''").replace("\\", "")
											+ "','" + witnessSex.get(i)
											+ "','" + witnessBirthPlace.get(i).replace("'", "''").replace("\\", "")
											+ "','" + witnessLivingPlace.get(i).replace("'", "''").replace("\\", "")
											+ "','" + witnessAge.get(i)
											+ "','" + witnessDateOfBirth.get(i) 
											+ "','" + witnessMisc.get(i).replace("'", "''").replace("\\", "")
											+ "');";
									database.runQuery(query);

									query = "SET @witnessID = LAST_INSERT_ID(); ";
									database.runQuery(query);

									query = "INSERT INTO witnesses_record (Record_ID, Person_ID)"
											+ " VALUES (@recordID, @witnessID);";
									database.runQuery(query);
								}

								witnessFirstName = new ArrayList<String>();
								witnessPatronymic = new ArrayList<String>();
								witnessInsertion = new ArrayList<String>();
								witnessSurname = new ArrayList<String>();
								witnessAlias = new ArrayList<String>();
								witnessSex = new ArrayList<String>();
								witnessBirthPlace = new ArrayList<String>();
								witnessLivingPlace = new ArrayList<String>();
								witnessAge = new ArrayList<String>();
								witnessDateOfBirth = new ArrayList<String>();
								witnessMisc = new ArrayList<String>();

								witnessCount = 0;
								witnessIsset = false;
							} 
							database.close();
						}
					}

				}  
			};  

			// parse the XML specified in the given path and uses supplied  
			// handler to parse the document  
			// this calls startElement(), endElement() and character() methods  
			// accordingly  
			saxParser.parse(path, defaultHandler);  
		} catch (Exception e) {  
			e.printStackTrace();  
		}  
	}

}  