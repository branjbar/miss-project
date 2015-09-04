
import javax.xml.parsers.SAXParser;  
import javax.xml.parsers.SAXParserFactory;  

import org.xml.sax.Attributes;  
import org.xml.sax.SAXException;  
import org.xml.sax.helpers.DefaultHandler;  

public class TrouwParser extends DefaultHandler{  

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
				boolean bridegroomFieldTag = false;
				boolean brideFieldTag = false;
				boolean previousWifeFieldTag = false;
				boolean previousHusbandFieldTag = false;
				boolean witnessFieldTag = false;

				String registerID = "";
				String place = "";
				String dateRecord = "";

				String bridegroomFirstName = "";
				String bridegroomPatronymic = "";
				String bridegroomInsertion = "";
				String bridegroomSurname = "";
				String bridegroomAlias = "";
				String bridegroomSex = "m";
				String bridegroomBirthPlace = "";
				String bridegroomLivingPlace = "";
				String bridegroomAge = "-1";
				String bridegroomDateOfBirth = "0000-00-00";
				String bridegroomMisc = "";

				String brideFirstName = "";
				String bridePatronymic = "";
				String brideInsertion = "";
				String brideSurname = "";
				String brideAlias = "";
				String brideSex = "v";
				String brideBirthPlace = "";
				String brideLivingPlace = "";
				String brideAge = "-1";
				String brideDateOfBirth = "0000-00-00";
				String brideMisc = "";

				String previousWifeFirstName = "";
				String previousWifePatronymic = "";
				String previousWifeInsertion = "";
				String previousWifeSurname = "";
				String previousWifeAlias = "";
				String previousWifeSex = "v";
				String previousWifeBirthPlace = "";
				String previousWifeLivingPlace = "";
				String previousWifeAge = "-1";
				String previousWifeDateOfBirth = "0000-00-00";
				String previousWifeMisc = "";

				String previousHusbandFirstName = "";
				String previousHusbandPatronymic = "";
				String previousHusbandInsertion = "";
				String previousHusbandSurname = "";
				String previousHusbandAlias = "";
				String previousHusbandSex = "v";
				String previousHusbandBirthPlace = "";
				String previousHusbandLivingPlace = "";
				String previousHusbandAge = "-1";
				String previousHusbandDateOfBirth = "0000-00-00";
				String previousHusbandMisc = "";

				String witnessFirstName = "";
				String witnessPatronymic = "";
				String witnessInsertion = "";
				String witnessSurname = "";
				String witnessAlias = "";
				String witnessSex = "v";
				String witnessBirthPlace = "";
				String witnessLivingPlace = "";
				String witnessAge = "-1";
				String witnessDateOfBirth = "0000-00-00";
				String witnessMisc = "";

				boolean previousWifeIsset = false;
				boolean previousHusbandIsset = false;
				boolean witnessIsset = false;


				// this method is called every time the parser gets an open tag '<'  
				// identifies which tag is being open at time by assigning an open flag  
				public void startElement(String uri, String localName, String qName, Attributes attributes) throws SAXException {

					//Depth counter
					if (qName.equalsIgnoreCase("RECORD")) recordDepth ++;

					//bridegroom
					if (qName.equalsIgnoreCase("FIELD") && attributes.getValue(0).equalsIgnoreCase("Bruidegom")){
						bridegroomFieldTag = true;
						brideFieldTag = false;
						previousWifeFieldTag = false;
						previousHusbandFieldTag = false;
						witnessFieldTag = false;
					}

					//bride
					if (qName.equalsIgnoreCase("FIELD") && attributes.getValue(0).equalsIgnoreCase("Bruid")){
						bridegroomFieldTag = false;
						brideFieldTag = true;
						previousWifeFieldTag = false;
						previousHusbandFieldTag = false;
						witnessFieldTag = false;
					}

					//previous wife
					if (qName.equalsIgnoreCase("FIELD") && attributes.getValue(0).equalsIgnoreCase("Eerdere vrouw")){
						bridegroomFieldTag = false;
						brideFieldTag = false;
						previousWifeFieldTag = true;
						previousHusbandFieldTag = false;
						witnessFieldTag = false;
					}

					//previous husband
					if (qName.equalsIgnoreCase("FIELD") && attributes.getValue(0).equalsIgnoreCase("Eerdere man")){
						bridegroomFieldTag = false;
						brideFieldTag = false;
						previousWifeFieldTag = false;
						previousHusbandFieldTag = true;
						witnessFieldTag = false;
					}

					//witness
					if (qName.equalsIgnoreCase("FIELD") && attributes.getValue(0).equalsIgnoreCase("Getuige")){
						bridegroomFieldTag = false;
						brideFieldTag = false;
						previousWifeFieldTag = false;
						previousHusbandFieldTag = false;
						witnessFieldTag = true;
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

					/*****************************BRIDEGROOM********************************************************************/

					//bridegroomFirstName
					if (qName.equalsIgnoreCase("FIELD") && attributes.getValue(0).equalsIgnoreCase("voornaam") && bridegroomFieldTag) positionFlag = 5;
					if (qName.equalsIgnoreCase("VALUE") && positionFlag == 5) positionFlag = 6;

					//bridegroomPatronymic
					if (qName.equalsIgnoreCase("FIELD") && attributes.getValue(0).equalsIgnoreCase("patroniem") && bridegroomFieldTag) positionFlag = 7;
					if (qName.equalsIgnoreCase("VALUE") && positionFlag == 7) positionFlag = 8;

					//bridegroomInsertion
					if (qName.equalsIgnoreCase("FIELD") && attributes.getValue(0).equalsIgnoreCase("tussenvoegsel") && bridegroomFieldTag) positionFlag = 9;
					if (qName.equalsIgnoreCase("VALUE") && positionFlag == 9) positionFlag = 10;

					//bridegroomSurname
					if (qName.equalsIgnoreCase("FIELD") && attributes.getValue(0).equalsIgnoreCase("geslachtsnaam") && bridegroomFieldTag) positionFlag = 11;
					if (qName.equalsIgnoreCase("VALUE") && positionFlag == 11) positionFlag = 12;

					//bridegroomAlias
					if (qName.equalsIgnoreCase("FIELD") && attributes.getValue(0).equalsIgnoreCase("alias") && bridegroomFieldTag) positionFlag = 13;
					if (qName.equalsIgnoreCase("VALUE") && positionFlag == 13) positionFlag = 14; 

					//bridegroom birth place
					if (qName.equalsIgnoreCase("FIELD") && attributes.getValue(0).equalsIgnoreCase("plaats_geboorte") && bridegroomFieldTag) positionFlag = 15;
					if (qName.equalsIgnoreCase("VALUE") && positionFlag == 15) positionFlag = 16; 

					//bridegroom living place
					if (qName.equalsIgnoreCase("FIELD") && attributes.getValue(0).equalsIgnoreCase("plaats_wonen") && bridegroomFieldTag) positionFlag = 17;
					if (qName.equalsIgnoreCase("VALUE") && positionFlag == 17) positionFlag = 18;

					//bridegroom age
					if (qName.equalsIgnoreCase("FIELD") && attributes.getValue(0).equalsIgnoreCase("leeftijd") && bridegroomFieldTag) positionFlag = 19;
					if (qName.equalsIgnoreCase("VALUE") && positionFlag == 19) positionFlag = 20;

					//bridegroom misc
					if (qName.equalsIgnoreCase("FIELD") && attributes.getValue(0).equalsIgnoreCase("diversen") && bridegroomFieldTag) positionFlag = 21;
					if (qName.equalsIgnoreCase("VALUE") && positionFlag == 21) positionFlag = 22;


					/*****************************BRIDE*************************************************************************/

					//brideFirstName
					if (qName.equalsIgnoreCase("FIELD") && attributes.getValue(0).equalsIgnoreCase("voornaam") && brideFieldTag) positionFlag = 23;
					if (qName.equalsIgnoreCase("VALUE") && positionFlag == 23) positionFlag = 24;

					//bridePatronymic
					if (qName.equalsIgnoreCase("FIELD") && attributes.getValue(0).equalsIgnoreCase("patroniem") && brideFieldTag) positionFlag = 25;
					if (qName.equalsIgnoreCase("VALUE") && positionFlag == 25) positionFlag = 26;

					//brideInsertion
					if (qName.equalsIgnoreCase("FIELD") && attributes.getValue(0).equalsIgnoreCase("tussenvoegsel") && brideFieldTag) positionFlag = 27;
					if (qName.equalsIgnoreCase("VALUE") && positionFlag == 27) positionFlag = 28;

					//brideSurname
					if (qName.equalsIgnoreCase("FIELD") && attributes.getValue(0).equalsIgnoreCase("geslachtsnaam") && brideFieldTag) positionFlag = 29;
					if (qName.equalsIgnoreCase("VALUE") && positionFlag == 29) positionFlag = 30;

					//brideAlias
					if (qName.equalsIgnoreCase("FIELD") && attributes.getValue(0).equalsIgnoreCase("alias") && brideFieldTag) positionFlag = 31;
					if (qName.equalsIgnoreCase("VALUE") && positionFlag == 31) positionFlag = 32; 

					//bride birth place
					if (qName.equalsIgnoreCase("FIELD") && attributes.getValue(0).equalsIgnoreCase("plaats_geboorte") && brideFieldTag) positionFlag = 33;
					if (qName.equalsIgnoreCase("VALUE") && positionFlag == 33) positionFlag = 34; 

					//bride living place
					if (qName.equalsIgnoreCase("FIELD") && attributes.getValue(0).equalsIgnoreCase("plaats_wonen") && brideFieldTag) positionFlag = 35;
					if (qName.equalsIgnoreCase("VALUE") && positionFlag == 35) positionFlag = 36;

					//bride age
					if (qName.equalsIgnoreCase("FIELD") && attributes.getValue(0).equalsIgnoreCase("leeftijd") && brideFieldTag) positionFlag = 37;
					if (qName.equalsIgnoreCase("VALUE") && positionFlag == 37) positionFlag = 38;

					//bride misc
					if (qName.equalsIgnoreCase("FIELD") && attributes.getValue(0).equalsIgnoreCase("diversen") && brideFieldTag) positionFlag = 39;
					if (qName.equalsIgnoreCase("VALUE") && positionFlag == 39) positionFlag = 40;

					/*****************************PREVIOUS WIFE*******************************************************************/

					//previousWifeFirstName
					if (qName.equalsIgnoreCase("FIELD") && attributes.getValue(0).equalsIgnoreCase("voornaam") && previousWifeFieldTag) positionFlag = 41;
					if (qName.equalsIgnoreCase("VALUE") && positionFlag == 41) positionFlag = 42;

					//previousWifePatronymic
					if (qName.equalsIgnoreCase("FIELD") && attributes.getValue(0).equalsIgnoreCase("patroniem") && previousWifeFieldTag) positionFlag = 43;
					if (qName.equalsIgnoreCase("VALUE") && positionFlag == 43) positionFlag = 44;

					//previousWifeInsertion
					if (qName.equalsIgnoreCase("FIELD") && attributes.getValue(0).equalsIgnoreCase("tussenvoegsel") && previousWifeFieldTag) positionFlag = 45;
					if (qName.equalsIgnoreCase("VALUE") && positionFlag == 45) positionFlag = 46;

					//previousWifeSurname
					if (qName.equalsIgnoreCase("FIELD") && attributes.getValue(0).equalsIgnoreCase("geslachtsnaam") && previousWifeFieldTag) positionFlag = 47;
					if (qName.equalsIgnoreCase("VALUE") && positionFlag == 47) positionFlag = 48;

					//previousWifeAlias
					if (qName.equalsIgnoreCase("FIELD") && attributes.getValue(0).equalsIgnoreCase("alias") && previousWifeFieldTag) positionFlag = 49;
					if (qName.equalsIgnoreCase("VALUE") && positionFlag == 49) positionFlag = 50; 

					//previousWife misc
					if (qName.equalsIgnoreCase("FIELD") && attributes.getValue(0).equalsIgnoreCase("diversen") && previousWifeFieldTag) positionFlag = 51;
					if (qName.equalsIgnoreCase("VALUE") && positionFlag == 51) positionFlag = 52;


					/*****************************PREVIOUS HUSBAND*******************************************************************/

					//previousHusbandFirstName
					if (qName.equalsIgnoreCase("FIELD") && attributes.getValue(0).equalsIgnoreCase("voornaam") && previousHusbandFieldTag) positionFlag = 53;
					if (qName.equalsIgnoreCase("VALUE") && positionFlag == 53) positionFlag = 54;

					//previousHusbandPatronymic
					if (qName.equalsIgnoreCase("FIELD") && attributes.getValue(0).equalsIgnoreCase("patroniem") && previousHusbandFieldTag) positionFlag = 55;
					if (qName.equalsIgnoreCase("VALUE") && positionFlag == 55) positionFlag = 56;

					//previousHusbandInsertion
					if (qName.equalsIgnoreCase("FIELD") && attributes.getValue(0).equalsIgnoreCase("tussenvoegsel") && previousHusbandFieldTag) positionFlag = 57;
					if (qName.equalsIgnoreCase("VALUE") && positionFlag == 57) positionFlag = 58;

					//previousHusbandSurname
					if (qName.equalsIgnoreCase("FIELD") && attributes.getValue(0).equalsIgnoreCase("geslachtsnaam") && previousHusbandFieldTag) positionFlag = 59;
					if (qName.equalsIgnoreCase("VALUE") && positionFlag == 59) positionFlag = 60;

					//previousHusbandAlias
					if (qName.equalsIgnoreCase("FIELD") && attributes.getValue(0).equalsIgnoreCase("alias") && previousHusbandFieldTag) positionFlag = 61;
					if (qName.equalsIgnoreCase("VALUE") && positionFlag == 61) positionFlag = 62; 

					//previousHusband misc
					if (qName.equalsIgnoreCase("FIELD") && attributes.getValue(0).equalsIgnoreCase("diversen") && previousHusbandFieldTag) positionFlag = 63;
					if (qName.equalsIgnoreCase("VALUE") && positionFlag == 63) positionFlag = 64;

					/*****************************WITNESS*******************************************************************/

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

					/*****************************BRIDEGROOM********************************************************************/

					//bridegroomFirstName
					if (positionFlag == 6) bridegroomFirstName = new String(ch, start, length); 

					//bridegroomPatronymic
					if (positionFlag == 8) bridegroomPatronymic = new String(ch, start, length); 

					//bridegroomInsertion
					if (positionFlag == 10) bridegroomInsertion = new String(ch, start, length); 

					//bridegroomSurname
					if (positionFlag == 12) bridegroomSurname = new String(ch, start, length); 

					//bridegroomAlias
					if (positionFlag == 14) bridegroomAlias = new String(ch, start, length); 

					//bridegroom birth place
					if (positionFlag == 16) bridegroomBirthPlace = new String(ch, start, length); 

					//bridegroom living place
					if (positionFlag == 18) bridegroomLivingPlace = new String(ch, start, length); 

					//bridegroom age
					if (positionFlag == 20) bridegroomAge = new String(ch, start, length); 

					//bridegroom misc
					if (positionFlag == 22) bridegroomMisc = new String(ch, start, length); 

					/*****************************BRIDE*************************************************************************/

					//brideFirstName
					if (positionFlag == 24) brideFirstName = new String(ch, start, length); 

					//bridePatronymic
					if (positionFlag == 26) bridePatronymic = new String(ch, start, length); 

					//brideInsertion
					if (positionFlag == 28) brideInsertion = new String(ch, start, length); 

					//brideSurname
					if (positionFlag == 30) brideSurname = new String(ch, start, length); 

					//brideAlias
					if (positionFlag == 32) brideAlias = new String(ch, start, length); 

					//bride birth place
					if (positionFlag == 34) brideBirthPlace = new String(ch, start, length); 

					//bride living place
					if (positionFlag == 36) brideLivingPlace = new String(ch, start, length); 

					//bride age
					if (positionFlag == 38) brideAge = new String(ch, start, length); 

					//bride misc
					if (positionFlag == 40) brideMisc = new String(ch, start, length);

					/*****************************PREVIOUS WIFE*******************************************************************/

					//previousWifeFirstName
					if (positionFlag == 42) {
						previousWifeFirstName = new String(ch, start, length);
						previousWifeIsset = true;
					}

					//previousWifePatronymic
					if (positionFlag == 44){
						previousWifePatronymic = new String(ch, start, length); 
						previousWifeIsset = true;
					}

					//previousWifeInsertion
					if (positionFlag == 46){
						previousWifeInsertion = new String(ch, start, length); 
						previousWifeIsset = true;
					}

					//previousWifeSurname
					if (positionFlag == 48){
						previousWifeSurname = new String(ch, start, length);
						previousWifeIsset = true;
					}

					//previousWifeAlias
					if (positionFlag == 50){
						previousWifeAlias = new String(ch, start, length);
						previousWifeIsset = true;
					}

					//previousWife misc
					if (positionFlag == 52){
						previousWifeMisc = new String(ch, start, length);
						previousWifeIsset = true;
					}

					/*****************************PREVIOUS HUSBAND*******************************************************************/

					//previousHusbandFirstName
					if (positionFlag == 54){
						previousHusbandFirstName = new String(ch, start, length); 
						previousHusbandIsset = true;
					}

					//previousHusbandPatronymic
					if (positionFlag == 56){
						previousHusbandPatronymic = new String(ch, start, length); 
						previousHusbandIsset = true;
					}

					//previousHusbandInsertion
					if (positionFlag == 58){
						previousHusbandInsertion = new String(ch, start, length); 
						previousHusbandIsset = true;
					}

					//previousHusbandSurname
					if (positionFlag == 60){
						previousHusbandSurname = new String(ch, start, length); 
						previousHusbandIsset = true;
					}

					//previousHusbandAlias
					if (positionFlag == 62){
						previousHusbandAlias = new String(ch, start, length);
						previousHusbandIsset = true;
					}

					//previousHusband misc
					if (positionFlag == 64){
						previousHusbandMisc = new String(ch, start, length);
						previousHusbandIsset = true;
					}

					/*****************************WITNESS*******************************************************************/

					//witnessFirstName
					if (positionFlag == 66){
						witnessFirstName = new String(ch, start, length); 
						witnessIsset = true;
					}

					//witnessPatronymic
					if (positionFlag == 68){
						witnessPatronymic = new String(ch, start, length); 
						witnessIsset = true;
					}

					//witnessInsertion
					if (positionFlag == 70){
						witnessInsertion = new String(ch, start, length); 
						witnessIsset = true;
					}

					//witnessSurname
					if (positionFlag == 72){
						witnessSurname = new String(ch, start, length); 
						witnessIsset = true;
					}

					//witnessAlias
					if (positionFlag == 74){
						witnessAlias = new String(ch, start, length);
						witnessIsset = true;
					}

					//witness misc
					if (positionFlag == 76){
						witnessMisc = new String(ch, start, length);
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

							/*****************************BRIDEGROOM********************************************************************/

							String query = "INSERT INTO person (FirstName, Patronymic, Insertion, Surname, Alias, Sex, BirthPlace, LivingPlace, Age, DateOfBirth, Miscellaneous)"
									+ " VALUES ('" + bridegroomFirstName.replace("'", "''").replace("\\", "")
									+ "','" + bridegroomPatronymic.replace("'", "''").replace("\\", "")
									+ "','" + bridegroomInsertion.replace("'", "''").replace("\\", "")
									+ "','" + bridegroomSurname.replace("'", "''").replace("\\", "")
									+ "','" + bridegroomAlias.replace("'", "''").replace("\\", "")
									+ "','" + bridegroomSex
									+ "','" + bridegroomBirthPlace.replace("'", "''").replace("\\", "")
									+ "','" + bridegroomLivingPlace.replace("'", "''").replace("\\", "")
									+ "','" + bridegroomAge
									+ "','" + bridegroomDateOfBirth 
									+ "','" + bridegroomMisc.replace("'", "''").replace("\\", "") 
									+ "');";
							database.runQuery(query);

							bridegroomFirstName = "";
							bridegroomPatronymic = "";
							bridegroomInsertion = "";
							bridegroomSurname = "";
							bridegroomAlias = "";
							bridegroomSex = "";
							bridegroomBirthPlace = "";
							bridegroomLivingPlace = "";
							bridegroomAge = "-1";
							bridegroomDateOfBirth = "0000-00-00";
							bridegroomMisc = "";

							query = "SET @bridegroomID = LAST_INSERT_ID(); ";
							database.runQuery(query);

							/*****************************BRIDE********************************************************************/

							query = "INSERT INTO person (FirstName, Patronymic, Insertion, Surname, Alias, Sex, BirthPlace, LivingPlace, Age, DateOfBirth, Miscellaneous)"
									+ " VALUES ('" + brideFirstName.replace("'", "''").replace("\\", "")
									+ "','" + bridePatronymic.replace("'", "''").replace("\\", "")
									+ "','" + brideInsertion.replace("'", "''").replace("\\", "")
									+ "','" + brideSurname.replace("'", "''").replace("\\", "")
									+ "','" + brideAlias.replace("'", "''").replace("\\", "")
									+ "','" + brideSex
									+ "','" + brideBirthPlace.replace("'", "''").replace("\\", "")
									+ "','" + brideLivingPlace.replace("'", "''").replace("\\", "")
									+ "','" + brideAge
									+ "','" + brideDateOfBirth 
									+ "','" + brideMisc.replace("'", "''").replace("\\", "") 
									+ "');";
							database.runQuery(query);

							brideFirstName = "";
							bridePatronymic = "";
							brideInsertion = "";
							brideSurname = "";
							brideAlias = "";
							brideSex = "";
							brideBirthPlace = "";
							brideLivingPlace = "";
							brideAge = "-1";
							brideDateOfBirth = "0000-00-00";
							brideMisc = "";

							query = "SET @brideID = LAST_INSERT_ID(); ";
							database.runQuery(query);

							/*****************************PREVIOUS WIFE********************************************************************/

							if(previousWifeIsset){
								query = "INSERT INTO person (FirstName, Patronymic, Insertion, Surname, Alias, Sex, BirthPlace, LivingPlace, Age, DateOfBirth, Miscellaneous)"
										+ " VALUES ('" + previousWifeFirstName.replace("'", "''").replace("\\", "")
										+ "','" + previousWifePatronymic.replace("'", "''").replace("\\", "")
										+ "','" + previousWifeInsertion.replace("'", "''").replace("\\", "")
										+ "','" + previousWifeSurname.replace("'", "''").replace("\\", "")
										+ "','" + previousWifeAlias.replace("'", "''").replace("\\", "")
										+ "','" + previousWifeSex
										+ "','" + previousWifeBirthPlace.replace("'", "''").replace("\\", "")
										+ "','" + previousWifeLivingPlace.replace("'", "''").replace("\\", "")
										+ "','" + previousWifeAge
										+ "','" + previousWifeDateOfBirth 
										+ "','" + previousWifeMisc.replace("'", "''").replace("\\", "") 
										+ "');";
								database.runQuery(query);
								
								previousWifeIsset = false;

								previousWifeFirstName = "";
								previousWifePatronymic = "";
								previousWifeInsertion = "";
								previousWifeSurname = "";
								previousWifeAlias = "";
								previousWifeSex = "";
								previousWifeBirthPlace = "";
								previousWifeLivingPlace = "";
								previousWifeAge = "-1";
								previousWifeDateOfBirth = "0000-00-00";
								previousWifeMisc = "";

								query = "SET @previousWifeID = LAST_INSERT_ID(); ";
								database.runQuery(query);
							} else {query = "SET @previousWifeID = -1; "; database.runQuery(query);} 

							/*****************************PREVIOUS HUSBAND********************************************************************/

							if(previousHusbandIsset){
								query = "INSERT INTO person (FirstName, Patronymic, Insertion, Surname, Alias, Sex, BirthPlace, LivingPlace, Age, DateOfBirth, Miscellaneous)"
										+ " VALUES ('" + previousHusbandFirstName.replace("'", "''").replace("\\", "")
										+ "','" + previousHusbandPatronymic.replace("'", "''").replace("\\", "")
										+ "','" + previousHusbandInsertion.replace("'", "''").replace("\\", "")
										+ "','" + previousHusbandSurname.replace("'", "''").replace("\\", "")
										+ "','" + previousHusbandAlias.replace("'", "''").replace("\\", "")
										+ "','" + previousHusbandSex
										+ "','" + previousHusbandBirthPlace.replace("'", "''").replace("\\", "")
										+ "','" + previousHusbandLivingPlace.replace("'", "''").replace("\\", "")
										+ "','" + previousHusbandAge
										+ "','" + previousHusbandDateOfBirth 
										+ "','" + previousHusbandMisc.replace("'", "''").replace("\\", "") 
										+ "');";
								database.runQuery(query);
								
								previousHusbandIsset = false;

								previousHusbandFirstName = "";
								previousHusbandPatronymic = "";
								previousHusbandInsertion = "";
								previousHusbandSurname = "";
								previousHusbandAlias = "";
								previousHusbandSex = "";
								previousHusbandBirthPlace = "";
								previousHusbandLivingPlace = "";
								previousHusbandAge = "-1";
								previousHusbandDateOfBirth = "0000-00-00";
								previousHusbandMisc = "";

								query = "SET @previousHusbandID = LAST_INSERT_ID(); ";
								database.runQuery(query);
							} else {query = "SET @previousHusbandID = -1; "; database.runQuery(query);} 

							/*****************************WITNESS********************************************************************/

							if(witnessIsset){
								query = "INSERT INTO person (FirstName, Patronymic, Insertion, Surname, Alias, Sex, BirthPlace, LivingPlace, Age, DateOfBirth, Miscellaneous)"
										+ " VALUES ('" + witnessFirstName.replace("'", "''").replace("\\", "")
										+ "','" + witnessPatronymic.replace("'", "''").replace("\\", "")
										+ "','" + witnessInsertion.replace("'", "''").replace("\\", "")
										+ "','" + witnessSurname.replace("'", "''").replace("\\", "")
										+ "','" + witnessAlias.replace("'", "''").replace("\\", "")
										+ "','" + witnessSex
										+ "','" + witnessBirthPlace.replace("'", "''").replace("\\", "")
										+ "','" + witnessLivingPlace.replace("'", "''").replace("\\", "")
										+ "','" + witnessAge
										+ "','" + witnessDateOfBirth 
										+ "','" + witnessMisc.replace("'", "''").replace("\\", "") 
										+ "');";
								database.runQuery(query);
								
								witnessIsset = false;

								witnessFirstName = "";
								witnessPatronymic = "";
								witnessInsertion = "";
								witnessSurname = "";
								witnessAlias = "";
								witnessSex = "";
								witnessBirthPlace = "";
								witnessLivingPlace = "";
								witnessAge = "-1";
								witnessDateOfBirth = "0000-00-00";
								witnessMisc = "";

								query = "SET @witnessID = LAST_INSERT_ID(); ";
								database.runQuery(query);
							} else {query = "SET @witnessID = -1; "; database.runQuery(query);}

							/*****************************RECORD********************************************************************/

							query = "INSERT INTO marriage_record (Register_ID, Place, DateRecord, Bridegroom_ID, Bride_ID , PreviousWife_ID, PreviousHusband_ID, Witness_ID) "
									+ "VALUES ('" + registerID
									+ "','" + place.replace("'", "''").replace("\\", "")
									+ "','" + dateRecord
									+ "', @bridegroomID" 
									+ ", @brideID"
									+ ", @previousWifeID" 
									+ ", @previousHusbandID"
									+ ", @witnessID"
									+ ");";
							database.runQuery(query);
							database.close();

							registerID = "";
							place = "";
							dateRecord = "";							
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