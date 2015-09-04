import javax.xml.parsers.SAXParser;  
import javax.xml.parsers.SAXParserFactory;  

import org.xml.sax.Attributes;  
import org.xml.sax.SAXException;  
import org.xml.sax.helpers.DefaultHandler;  

public class BegraafParser extends DefaultHandler{  

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

				boolean registerFieldTag = false;
				boolean plaatsFieldTag = false;
				boolean readPlaatsValueTag = false;
				boolean datumFieldTag = false;
				boolean readDatumValueTag = false;
				boolean overledeneFieldTag = false;
				boolean deceasedFirstNameFieldTag = false;
				boolean readDeceasedFirstNameValueTag = false;
				boolean relatieeFieldTag = false;
				boolean deceasedPatronymicFieldTag = false;
				boolean readDeceasedPatronymicValueTag = false;
				boolean deceasedInsertionFieldTag = false;
				boolean readDeceasedInsertionValueTag = false;
				boolean deceasedSurnameFieldTag = false;
				boolean readDeceasedSurnameValueTag = false;
				boolean deceasedAliasFieldTag = false;
				boolean readDeceasedAliasValueTag = false;
				boolean placeOfDeathFieldTag = false;
				boolean readPlaceOfDeathValueTag = false;
				boolean readDateOfDeathValueTag = false;
				boolean dateOfDeathFieldTag = false;
				boolean deceasedSexFieldTag = false;
				boolean readDeceasedSexValueTag = false;
				boolean deceasedAgeFieldTag = false;
				boolean readDeceasedAgeValueTag = false;
				boolean deceasedMiscFieldTag = false;
				boolean readDeceasedMiscValueTag = false;
				boolean overledeneEntityTag = false;
				boolean relatieFirstNameFieldTag = false;
				boolean readrelatieFirstNameValueTag = false;
				boolean relatiePatronymicFieldTag = false;
				boolean readrelatiePatronymicValueTag = false;
				boolean relatieInsertionFieldTag = false;
				boolean readrelatieInsertionValueTag = false;
				boolean relatieSurnameFieldTag = false;
				boolean readrelatieSurnameValueTag = false;
				boolean relatieAliasFieldTag = false;
				boolean readrelatieAliasValueTag = false;
				boolean relatieMiscFieldTag = false;
				boolean readrelatieMiscValueTag = false;
				boolean relatieTypeFieldTag = false;
				boolean readrelatieTypeValueTag = false;
				
				boolean vaderFirstNameFieldTag = false;
				boolean readvaderFirstNameValueTag = false;
				boolean vaderPatronymicFieldTag = false;
				boolean readvaderPatronymicValueTag = false;
				boolean vaderInsertionFieldTag = false;
				boolean readvaderInsertionValueTag = false;
				boolean vaderSurnameFieldTag = false;
				boolean readvaderSurnameValueTag = false;
				boolean vaderAliasFieldTag = false;
				boolean readvaderAliasValueTag = false;
				boolean vaderMiscFieldTag = false;
				boolean readvaderMiscValueTag = false;
				boolean vaderTypeFieldTag = false;
				boolean readvaderTypeValueTag = false;
				
				boolean moederFirstNameFieldTag = false;
				boolean readmoederFirstNameValueTag = false;
				boolean moederPatronymicFieldTag = false;
				boolean readmoederPatronymicValueTag = false;
				boolean moederInsertionFieldTag = false;
				boolean readmoederInsertionValueTag = false;
				boolean moederSurnameFieldTag = false;
				boolean readmoederSurnameValueTag = false;
				boolean moederAliasFieldTag = false;
				boolean readmoederAliasValueTag = false;
				boolean moederMiscFieldTag = false;
				boolean readmoederMiscValueTag = false;
				boolean moederTypeFieldTag = false;
				boolean readmoederTypeValueTag = false;
				
				boolean vaderFieldTag = false;
				boolean moederFieldTag = false;
				
				boolean readRegisterID = false;

				String registerID = "";
				String place = "";
				String dateRecord = "";
				String dateOfDeath = "0000-00-00";
				String placeOfDeath = "";

				String deceasedFirstName = "";
				String deceasedPatronymic = "";
				String deceasedInsertion = "";
				String deceasedSurname = "";
				String deceasedAlias = "";
				String deceasedSex = "";
				String deceasedBirthPlace = "";
				String deceasedLivingPlace = "";
				String deceasedAge = "-1";
				String deceasedDateOfBirth = "0000-00-00";
				String deceasedMisc = "";
				
				boolean relatieIsset = false;
				boolean vaderIsset = false;
				boolean moederIsset = false;
				
				String relatieFirstName = "";
				String relatiePatronymic = "";
				String relatieInsertion = "";
				String relatieSurname = "";
				String relatieAlias = "";
				String relatieSex = "";
				String relatieBirthPlace = "";
				String relatieLivingPlace = "";
				String relatieAge = "-1";
				String relatieDateOfBirth = "0000-00-00";
				String relatieMisc = "";
				
				String vaderFirstName = "";
				String vaderPatronymic = "";
				String vaderInsertion = "";
				String vaderSurname = "";
				String vaderAlias = "";
				String vaderSex = "";
				String vaderBirthPlace = "";
				String vaderLivingPlace = "";
				String vaderAge = "-1";
				String vaderDateOfBirth = "0000-00-00";
				String vaderMisc = "";
				
				String moederFirstName = "";
				String moederPatronymic = "";
				String moederInsertion = "";
				String moederSurname = "";
				String moederAlias = "";
				String moederSex = "";
				String moederBirthPlace = "";
				String moederLivingPlace = "";
				String moederAge = "-1";
				String moederDateOfBirth = "0000-00-00";
				String moederMisc = "";

				// this method is called every time the parser gets an open tag '<'  
				// identifies which tag is being open at time by assigning an open flag  
				public void startElement(String uri, String localName, String qName, Attributes attributes) throws SAXException {  
					
					//Depth counter
					if (qName.equalsIgnoreCase("RECORD")) recordDepth ++;
					
					//Deceased
					if (qName.equalsIgnoreCase("FIELD") && attributes.getValue(0).equalsIgnoreCase("Overledene")){
						overledeneFieldTag = true;
						relatieeFieldTag = false;
						vaderFieldTag = false;
						moederFieldTag = false;
					}
					
					//Relatie
					if (qName.equalsIgnoreCase("FIELD") && attributes.getValue(0).equalsIgnoreCase("Relatie")){
						overledeneFieldTag = false;
						relatieeFieldTag = true;
						vaderFieldTag = false;
						moederFieldTag = false;
					}
					
					//vader
					if (qName.equalsIgnoreCase("FIELD") && attributes.getValue(0).equalsIgnoreCase("vader")){
						overledeneFieldTag = false;
						relatieeFieldTag = false;
						vaderFieldTag = true;
						moederFieldTag = false;
					}
					
					//moeder
					if (qName.equalsIgnoreCase("FIELD") && attributes.getValue(0).equalsIgnoreCase("moeder")){
						overledeneFieldTag = false;
						relatieeFieldTag = false;
						vaderFieldTag = false;
						moederFieldTag = true;
					}

					//RegisterID
					if (qName.equalsIgnoreCase("FIELD") && attributes.getValue(0).equalsIgnoreCase("REGISTER")) registerFieldTag = true;
					if (qName.equalsIgnoreCase("ENTITY") && registerFieldTag) readRegisterID = true; 
					if (qName.equalsIgnoreCase("record") && readRegisterID) registerID = attributes.getValue(0);

					//Place
					if (qName.equalsIgnoreCase("FIELD") && attributes.getValue(0).equalsIgnoreCase("PLAATS")) plaatsFieldTag = true;
					if (qName.equalsIgnoreCase("VALUE") && plaatsFieldTag) readPlaatsValueTag = true;

					//Date
					if (qName.equalsIgnoreCase("FIELD") && attributes.getValue(0).equalsIgnoreCase("DATUM")) datumFieldTag = true;
					if (qName.equalsIgnoreCase("VALUE") && datumFieldTag) readDatumValueTag = true;

					//deceasedFirstName
					if (qName.equalsIgnoreCase("FIELD") && attributes.getValue(0).equalsIgnoreCase("voornaam") && overledeneFieldTag) deceasedFirstNameFieldTag = true;
					if (qName.equalsIgnoreCase("VALUE") && deceasedFirstNameFieldTag) readDeceasedFirstNameValueTag = true;
					
					//deceasedPatronymic
					if (qName.equalsIgnoreCase("FIELD") && attributes.getValue(0).equalsIgnoreCase("patroniem") && overledeneFieldTag) deceasedPatronymicFieldTag = true;
					if (qName.equalsIgnoreCase("VALUE") && deceasedPatronymicFieldTag) readDeceasedPatronymicValueTag = true;
					
					//deceasedInsertion
					if (qName.equalsIgnoreCase("FIELD") && attributes.getValue(0).equalsIgnoreCase("tussenvoegsel") && overledeneFieldTag) deceasedInsertionFieldTag = true;
					if (qName.equalsIgnoreCase("VALUE") && deceasedInsertionFieldTag) readDeceasedInsertionValueTag = true;
					
					//deceasedSurname
					if (qName.equalsIgnoreCase("FIELD") && attributes.getValue(0).equalsIgnoreCase("geslachtsnaam") && overledeneFieldTag) deceasedSurnameFieldTag = true;
					if (qName.equalsIgnoreCase("VALUE") && deceasedSurnameFieldTag) readDeceasedSurnameValueTag = true;
					
					//deceasedAlias
					if (qName.equalsIgnoreCase("FIELD") && attributes.getValue(0).equalsIgnoreCase("alias") && overledeneFieldTag) deceasedAliasFieldTag = true;
					if (qName.equalsIgnoreCase("VALUE") && deceasedAliasFieldTag) readDeceasedAliasValueTag = true;
					
					//placeOfDeath
					if (qName.equalsIgnoreCase("FIELD") && attributes.getValue(0).equalsIgnoreCase("plaats_overlijden") && overledeneFieldTag) placeOfDeathFieldTag = true;
					if (qName.equalsIgnoreCase("VALUE") && placeOfDeathFieldTag) readPlaceOfDeathValueTag = true;
					
					//dateOfDeath
					if (qName.equalsIgnoreCase("FIELD") && attributes.getValue(0).equalsIgnoreCase("datum_overlijden") && overledeneFieldTag) dateOfDeathFieldTag = true;
					if (qName.equalsIgnoreCase("VALUE") && dateOfDeathFieldTag) readDateOfDeathValueTag = true;
					
					//deceasedSex
					if (qName.equalsIgnoreCase("FIELD") && attributes.getValue(0).equalsIgnoreCase("geslacht") && overledeneFieldTag) deceasedSexFieldTag = true;
					if (qName.equalsIgnoreCase("VALUE") && deceasedSexFieldTag) readDeceasedSexValueTag = true;
					
					//deceasedAge
					if (qName.equalsIgnoreCase("FIELD") && attributes.getValue(0).equalsIgnoreCase("leeftijd") && overledeneFieldTag) deceasedAgeFieldTag = true;
					if (qName.equalsIgnoreCase("VALUE") && deceasedAgeFieldTag) readDeceasedAgeValueTag = true;
					
					//deceasedMisc
					if (qName.equalsIgnoreCase("FIELD") && attributes.getValue(0).equalsIgnoreCase("diversen") && overledeneFieldTag) deceasedMiscFieldTag = true;
					if (qName.equalsIgnoreCase("VALUE") && deceasedMiscFieldTag) readDeceasedMiscValueTag = true;
					
					//relatieFirstName
					if (qName.equalsIgnoreCase("FIELD") && attributes.getValue(0).equalsIgnoreCase("voornaam") && relatieeFieldTag) relatieFirstNameFieldTag = true;
					if (qName.equalsIgnoreCase("VALUE") && relatieFirstNameFieldTag) readrelatieFirstNameValueTag = true;
					
					//relatiePatronymic
					if (qName.equalsIgnoreCase("FIELD") && attributes.getValue(0).equalsIgnoreCase("patroniem") && relatieeFieldTag) relatiePatronymicFieldTag = true;
					if (qName.equalsIgnoreCase("VALUE") && relatiePatronymicFieldTag) readrelatiePatronymicValueTag = true;
					
					//relatieInsertion
					if (qName.equalsIgnoreCase("FIELD") && attributes.getValue(0).equalsIgnoreCase("tussenvoegsel") && relatieeFieldTag) relatieInsertionFieldTag = true;
					if (qName.equalsIgnoreCase("VALUE") && relatieInsertionFieldTag) readrelatieInsertionValueTag = true;
					
					//relatieSurname
					if (qName.equalsIgnoreCase("FIELD") && attributes.getValue(0).equalsIgnoreCase("geslachtsnaam") && relatieeFieldTag) relatieSurnameFieldTag = true;
					if (qName.equalsIgnoreCase("VALUE") && relatieSurnameFieldTag) readrelatieSurnameValueTag = true;
					
					//relatieAlias
					if (qName.equalsIgnoreCase("FIELD") && attributes.getValue(0).equalsIgnoreCase("alias") && relatieeFieldTag) relatieAliasFieldTag = true;
					if (qName.equalsIgnoreCase("VALUE") && relatieAliasFieldTag) readrelatieAliasValueTag = true;
					
					//relatieMisc
					if (qName.equalsIgnoreCase("FIELD") && attributes.getValue(0).equalsIgnoreCase("diversen") && relatieeFieldTag) relatieMiscFieldTag = true;
					if (qName.equalsIgnoreCase("VALUE") && relatieMiscFieldTag) readrelatieMiscValueTag = true;
					
					//relatieType
					if (qName.equalsIgnoreCase("FIELD") && attributes.getValue(0).equalsIgnoreCase("relatietype") && relatieeFieldTag) relatieTypeFieldTag = true;
					if (qName.equalsIgnoreCase("VALUE") && relatieTypeFieldTag) readrelatieTypeValueTag = true;
					
					//vaderFirstName
					if (qName.equalsIgnoreCase("FIELD") && attributes.getValue(0).equalsIgnoreCase("voornaam") && vaderFieldTag) vaderFirstNameFieldTag = true;
					if (qName.equalsIgnoreCase("VALUE") && vaderFirstNameFieldTag) readvaderFirstNameValueTag = true;
					
					//vaderPatronymic
					if (qName.equalsIgnoreCase("FIELD") && attributes.getValue(0).equalsIgnoreCase("patroniem") && vaderFieldTag) vaderPatronymicFieldTag = true;
					if (qName.equalsIgnoreCase("VALUE") && vaderPatronymicFieldTag) readvaderPatronymicValueTag = true;
					
					//vaderInsertion
					if (qName.equalsIgnoreCase("FIELD") && attributes.getValue(0).equalsIgnoreCase("tussenvoegsel") && vaderFieldTag) vaderInsertionFieldTag = true;
					if (qName.equalsIgnoreCase("VALUE") && vaderInsertionFieldTag) readvaderInsertionValueTag = true;
					
					//vaderSurname
					if (qName.equalsIgnoreCase("FIELD") && attributes.getValue(0).equalsIgnoreCase("geslachtsnaam") && vaderFieldTag) vaderSurnameFieldTag = true;
					if (qName.equalsIgnoreCase("VALUE") && vaderSurnameFieldTag) readvaderSurnameValueTag = true;
					
					//vaderAlias
					if (qName.equalsIgnoreCase("FIELD") && attributes.getValue(0).equalsIgnoreCase("alias") && vaderFieldTag) vaderAliasFieldTag = true;
					if (qName.equalsIgnoreCase("VALUE") && vaderAliasFieldTag) readvaderAliasValueTag = true;
					
					//vaderMisc
					if (qName.equalsIgnoreCase("FIELD") && attributes.getValue(0).equalsIgnoreCase("diversen") && vaderFieldTag) vaderMiscFieldTag = true;
					if (qName.equalsIgnoreCase("VALUE") && vaderMiscFieldTag) readvaderMiscValueTag = true;
					
					//vaderType
					if (qName.equalsIgnoreCase("FIELD") && attributes.getValue(0).equalsIgnoreCase("relatietype") && vaderFieldTag) vaderTypeFieldTag = true;
					if (qName.equalsIgnoreCase("VALUE") && vaderTypeFieldTag) readvaderTypeValueTag = true;
					
					//moederFirstName
					if (qName.equalsIgnoreCase("FIELD") && attributes.getValue(0).equalsIgnoreCase("voornaam") && moederFieldTag) moederFirstNameFieldTag = true;
					if (qName.equalsIgnoreCase("VALUE") && moederFirstNameFieldTag) readmoederFirstNameValueTag = true;
					
					//moederPatronymic
					if (qName.equalsIgnoreCase("FIELD") && attributes.getValue(0).equalsIgnoreCase("patroniem") && moederFieldTag) moederPatronymicFieldTag = true;
					if (qName.equalsIgnoreCase("VALUE") && moederPatronymicFieldTag) readmoederPatronymicValueTag = true;
					
					//moederInsertion
					if (qName.equalsIgnoreCase("FIELD") && attributes.getValue(0).equalsIgnoreCase("tussenvoegsel") && moederFieldTag) moederInsertionFieldTag = true;
					if (qName.equalsIgnoreCase("VALUE") && moederInsertionFieldTag) readmoederInsertionValueTag = true;
					
					//moederSurname
					if (qName.equalsIgnoreCase("FIELD") && attributes.getValue(0).equalsIgnoreCase("geslachtsnaam") && moederFieldTag) moederSurnameFieldTag = true;
					if (qName.equalsIgnoreCase("VALUE") && moederSurnameFieldTag) readmoederSurnameValueTag = true;
					
					//moederAlias
					if (qName.equalsIgnoreCase("FIELD") && attributes.getValue(0).equalsIgnoreCase("alias") && moederFieldTag) moederAliasFieldTag = true;
					if (qName.equalsIgnoreCase("VALUE") && moederAliasFieldTag) readmoederAliasValueTag = true;
					
					//moederMisc
					if (qName.equalsIgnoreCase("FIELD") && attributes.getValue(0).equalsIgnoreCase("diversen") && moederFieldTag) moederMiscFieldTag = true;
					if (qName.equalsIgnoreCase("VALUE") && moederMiscFieldTag) readmoederMiscValueTag = true;
					
					//moederType
					if (qName.equalsIgnoreCase("FIELD") && attributes.getValue(0).equalsIgnoreCase("relatietype") && moederFieldTag) moederTypeFieldTag = true;
					if (qName.equalsIgnoreCase("VALUE") && moederTypeFieldTag) readmoederTypeValueTag = true;

				}  

				// prints data stored in between '<' and '>' tags  
				public void characters(char ch[], int start, int length) throws SAXException {

					//Place
					if (readPlaatsValueTag) place = new String(ch, start, length); 

					//Date
					if (readDatumValueTag) dateRecord = new String(ch, start, length); 
					
					//Deceased first name
					if (readDeceasedFirstNameValueTag) deceasedFirstName = new String(ch, start, length); 
					
					//deceasedPatronymic
					if (readDeceasedPatronymicValueTag) deceasedPatronymic = new String(ch, start, length); 
					
					//deceasedInsertion
					if (readDeceasedInsertionValueTag) deceasedInsertion = new String(ch, start, length);
					
					//deceasedSurname
					if (readDeceasedSurnameValueTag) deceasedSurname = new String(ch, start, length);
					
					//deceasedAlias
					if (readDeceasedAliasValueTag) deceasedAlias = new String(ch, start, length);
					
					//placeOfDeath
					if (readPlaceOfDeathValueTag) placeOfDeath = new String(ch, start, length);
					
					//dateOfDeath
					if (readDateOfDeathValueTag) dateOfDeath = new String(ch, start, length);
					
					//deceasedSex
					if (readDeceasedSexValueTag) deceasedSex = new String(ch, start, length);
					
					//deceasedAge
					if (readDeceasedAgeValueTag) deceasedAge = new String(ch, start, length);
					
					//deceasedMisc
					if (readDeceasedMiscValueTag) deceasedMisc = new String(ch, start, length);
					
					//relatie first name
					if (readrelatieFirstNameValueTag) {
						relatieIsset = true;
						relatieFirstName = new String(ch, start, length); 
					}
					
					//relatiePatronymic
					if (readrelatiePatronymicValueTag){
						relatieIsset = true;
						relatiePatronymic = new String(ch, start, length); 
					}
					
					//relatieInsertion
					if (readrelatieInsertionValueTag){
						relatieIsset = true;
						relatieInsertion = new String(ch, start, length);
					}
					
					//relatieSurname
					if (readrelatieSurnameValueTag){
						relatieIsset = true;
						relatieSurname = new String(ch, start, length);
					}
					
					//relatieAlias
					if (readrelatieAliasValueTag){
						relatieIsset = true;
						relatieAlias = new String(ch, start, length);
					}
					
					//relatieMisc
					if (readrelatieMiscValueTag){
						relatieIsset = true;
						relatieMisc = new String(ch, start, length);
					}
					
					//relatieType
					if (readrelatieTypeValueTag){
						relatieIsset = true;
						relatieMisc = relatieMisc + " ; relation type : " + new String(ch, start, length);
					}
					
					//vader first name
					if (readvaderFirstNameValueTag) {
						vaderIsset = true;
						vaderFirstName = new String(ch, start, length); 
					}
					
					//vaderPatronymic
					if (readvaderPatronymicValueTag){
						vaderIsset = true;
						vaderPatronymic = new String(ch, start, length); 
					}
					
					//vaderInsertion
					if (readvaderInsertionValueTag){
						vaderIsset = true;
						vaderInsertion = new String(ch, start, length);
					}
					
					//vaderSurname
					if (readvaderSurnameValueTag){
						vaderIsset = true;
						vaderSurname = new String(ch, start, length);
					}
					
					//vaderAlias
					if (readvaderAliasValueTag){
						vaderIsset = true;
						vaderAlias = new String(ch, start, length);
					}
					
					//vaderMisc
					if (readvaderMiscValueTag){
						vaderIsset = true;
						vaderMisc = new String(ch, start, length);
					}
					
					//vaderType
					if (readvaderTypeValueTag){
						vaderIsset = true;
						vaderMisc = vaderMisc + " ; relation type : " + new String(ch, start, length);
					}
					
					//moeder first name
					if (readmoederFirstNameValueTag) {
						moederIsset = true;
						moederFirstName = new String(ch, start, length); 
					}
					
					//moederPatronymic
					if (readmoederPatronymicValueTag){
						moederIsset = true;
						moederPatronymic = new String(ch, start, length); 
					}
					
					//moederInsertion
					if (readmoederInsertionValueTag){
						moederIsset = true;
						moederInsertion = new String(ch, start, length);
					}
					
					//moederSurname
					if (readmoederSurnameValueTag){
						moederIsset = true;
						moederSurname = new String(ch, start, length);
					}
					
					//moederAlias
					if (readmoederAliasValueTag){
						moederIsset = true;
						moederAlias = new String(ch, start, length);
					}
					
					//moederMisc
					if (readmoederMiscValueTag){
						moederIsset = true;
						moederMisc = new String(ch, start, length);
					}
					
					//moederType
					if (readmoederTypeValueTag){
						moederIsset = true;
						moederMisc = moederMisc + " ; relation type : " + new String(ch, start, length);
					}


				}  

				// calls by the parser whenever '>' end tag is found in xml   
				// makes tags flag to 'close'  
				public void endElement(String uri, String localName, String qName) throws SAXException { 

					//Tags
					if (registerFieldTag) registerFieldTag = false;
					if (plaatsFieldTag) plaatsFieldTag = false;
					if (readPlaatsValueTag) readPlaatsValueTag = false;
					if (datumFieldTag) datumFieldTag = false;
					if (readDatumValueTag) readDatumValueTag = false;
					if (relatieeFieldTag) overledeneFieldTag = false;
					if (deceasedFirstNameFieldTag) deceasedFirstNameFieldTag = false;
					if (readDeceasedFirstNameValueTag) readDeceasedFirstNameValueTag = false;
					if (deceasedPatronymicFieldTag) deceasedPatronymicFieldTag = false;
					if (readDeceasedPatronymicValueTag) readDeceasedPatronymicValueTag = false;
					if (deceasedInsertionFieldTag) deceasedInsertionFieldTag = false;
					if (readDeceasedInsertionValueTag) readDeceasedInsertionValueTag = false;
					if (deceasedSurnameFieldTag) deceasedSurnameFieldTag = false;
					if (readDeceasedSurnameValueTag) readDeceasedSurnameValueTag = false;
					if (deceasedAliasFieldTag) deceasedAliasFieldTag = false;
					if (readDeceasedAliasValueTag) readDeceasedAliasValueTag = false;
					if (placeOfDeathFieldTag) placeOfDeathFieldTag = false; 
					if (readPlaceOfDeathValueTag) readPlaceOfDeathValueTag = false;
					if (deceasedSexFieldTag) deceasedSexFieldTag = false;
					if (readDeceasedSexValueTag) readDeceasedSexValueTag = false;
					if (deceasedAgeFieldTag) deceasedAgeFieldTag = false;
					if (readDeceasedAgeValueTag) readDeceasedAgeValueTag = false;
					if (deceasedMiscFieldTag) deceasedMiscFieldTag = false;
					if (readDeceasedMiscValueTag) readDeceasedMiscValueTag = false;
					if (overledeneEntityTag) overledeneEntityTag = false;
					if (readRegisterID) readRegisterID = false;
					
					if (relatieFirstNameFieldTag) relatieFirstNameFieldTag = false;
					if (readrelatieFirstNameValueTag) readrelatieFirstNameValueTag = false;
					if (relatiePatronymicFieldTag) relatiePatronymicFieldTag = false;
					if (readrelatiePatronymicValueTag) readrelatiePatronymicValueTag = false;
					if (relatieInsertionFieldTag) relatieInsertionFieldTag = false;
					if (readrelatieInsertionValueTag) readrelatieInsertionValueTag = false;
					if (relatieSurnameFieldTag) relatieSurnameFieldTag = false;
					if (readrelatieSurnameValueTag) readrelatieSurnameValueTag = false;
					if (relatieAliasFieldTag) relatieAliasFieldTag = false;
					if (readrelatieAliasValueTag) readrelatieAliasValueTag = false;
					if (relatieMiscFieldTag) relatieMiscFieldTag = false;
					if (readrelatieMiscValueTag) readrelatieMiscValueTag = false;
					if (relatieTypeFieldTag) relatieTypeFieldTag = false;
					if (readrelatieTypeValueTag) readrelatieTypeValueTag = false;
					
					if (vaderFirstNameFieldTag) vaderFirstNameFieldTag = false;
					if (readvaderFirstNameValueTag) readvaderFirstNameValueTag = false;
					if (vaderPatronymicFieldTag) vaderPatronymicFieldTag = false;
					if (readvaderPatronymicValueTag) readvaderPatronymicValueTag = false;
					if (vaderInsertionFieldTag) vaderInsertionFieldTag = false;
					if (readvaderInsertionValueTag) readvaderInsertionValueTag = false;
					if (vaderSurnameFieldTag) vaderSurnameFieldTag = false;
					if (readvaderSurnameValueTag) readvaderSurnameValueTag = false;
					if (vaderAliasFieldTag) vaderAliasFieldTag = false;
					if (readvaderAliasValueTag) readvaderAliasValueTag = false;
					if (vaderMiscFieldTag) vaderMiscFieldTag = false;
					if (readvaderMiscValueTag) readvaderMiscValueTag = false;
					if (vaderTypeFieldTag) vaderTypeFieldTag = false;
					if (readvaderTypeValueTag) readvaderTypeValueTag = false;
					
					if (moederFirstNameFieldTag) moederFirstNameFieldTag = false;
					if (readmoederFirstNameValueTag) readmoederFirstNameValueTag = false;
					if (moederPatronymicFieldTag) moederPatronymicFieldTag = false;
					if (readmoederPatronymicValueTag) readmoederPatronymicValueTag = false;
					if (moederInsertionFieldTag) moederInsertionFieldTag = false;
					if (readmoederInsertionValueTag) readmoederInsertionValueTag = false;
					if (moederSurnameFieldTag) moederSurnameFieldTag = false;
					if (readmoederSurnameValueTag) readmoederSurnameValueTag = false;
					if (moederAliasFieldTag) moederAliasFieldTag = false;
					if (readmoederAliasValueTag) readmoederAliasValueTag = false;
					if (moederMiscFieldTag) moederMiscFieldTag = false;
					if (readmoederMiscValueTag) readmoederMiscValueTag = false;
					if (moederTypeFieldTag) moederTypeFieldTag = false;
					if (readmoederTypeValueTag) readmoederTypeValueTag = false;

					//SQL
					if (qName.equalsIgnoreCase("RECORD")) {
						//Depth counter
						recordDepth--; 
						if (recordDepth == 0){ // A full record is read: SQL INSERT
							DbHandler database = new DbHandler();
							
							String query = "INSERT INTO person (FirstName, Patronymic, Insertion, Surname, Alias, Sex, BirthPlace, LivingPlace, Age, DateOfBirth, Miscellaneous)"
									+ " VALUES ('" + deceasedFirstName.replace("'", "''").replace("\\", "")
									+ "','" + deceasedPatronymic.replace("'", "''").replace("\\", "")
									+ "','" + deceasedInsertion.replace("'", "''").replace("\\", "")
									+ "','" + deceasedSurname.replace("'", "''").replace("\\", "")
									+ "','" + deceasedAlias.replace("'", "''").replace("\\", "")
									+ "','" + deceasedSex
									+ "','" + deceasedBirthPlace.replace("'", "''").replace("\\", "")
									+ "','" + deceasedLivingPlace.replace("'", "''").replace("\\", "")
									+ "','" + deceasedAge
									+ "','" + deceasedDateOfBirth 
									+ "','" + deceasedMisc.replace("'", "''").replace("\\", "") 
									+ "');";
							database.runQuery(query);
							
							deceasedFirstName = "";
							deceasedPatronymic = "";
							deceasedInsertion = "";
							deceasedSurname = "";
							deceasedAlias = "";
							deceasedSex = "";
							deceasedBirthPlace = "";
							deceasedLivingPlace = "";
							deceasedAge = "-1";
							deceasedDateOfBirth = "0000-00-00";
							deceasedMisc = "";
									
							query = "SET @deceasedID = LAST_INSERT_ID(); ";
							database.runQuery(query);
							
							if(relatieIsset){
								 query = "INSERT INTO person (FirstName, Patronymic, Insertion, Surname, Alias, Sex, BirthPlace, LivingPlace, Age, DateOfBirth, Miscellaneous)"
										+ " VALUES ('" + relatieFirstName.replace("'", "''").replace("\\", "")
										+ "','" + relatiePatronymic.replace("'", "''").replace("\\", "")
										+ "','" + relatieInsertion.replace("'", "''").replace("\\", "")
										+ "','" + relatieSurname.replace("'", "''").replace("\\", "")
										+ "','" + relatieAlias.replace("'", "''").replace("\\", "")
										+ "','" + relatieSex
										+ "','" + relatieBirthPlace.replace("'", "''").replace("\\", "")
										+ "','" + relatieLivingPlace.replace("'", "''").replace("\\", "")
										+ "','" + relatieAge
										+ "','" + relatieDateOfBirth 
										+ "','" + relatieMisc.replace("'", "''").replace("\\", "")
										+ "');";
								database.runQuery(query);
								relatieIsset = false;
								
								relatieFirstName = "";
								relatiePatronymic = "";
								relatieInsertion = "";
								relatieSurname = "";
								relatieAlias = "";
								relatieSex = "";
								relatieBirthPlace = "";
								relatieLivingPlace = "";
								relatieAge = "-1";
								relatieDateOfBirth = "0000-00-00";
								relatieMisc = "";
										
								query = "SET @relatieID = LAST_INSERT_ID(); ";
								database.runQuery(query);
							} else {query = "SET @relatieID = -1; "; database.runQuery(query);}
							
							if(vaderIsset){
								 query = "INSERT INTO person (FirstName, Patronymic, Insertion, Surname, Alias, Sex, BirthPlace, LivingPlace, Age, DateOfBirth, Miscellaneous)"
										+ " VALUES ('" + vaderFirstName.replace("'", "''").replace("\\", "")
										+ "','" + vaderPatronymic.replace("'", "''").replace("\\", "")
										+ "','" + vaderInsertion.replace("'", "''").replace("\\", "")
										+ "','" + vaderSurname.replace("'", "''").replace("\\", "")
										+ "','" + vaderAlias.replace("'", "''").replace("\\", "")
										+ "','" + vaderSex
										+ "','" + vaderBirthPlace.replace("'", "''").replace("\\", "")
										+ "','" + vaderLivingPlace.replace("'", "''").replace("\\", "")
										+ "','" + vaderAge
										+ "','" + vaderDateOfBirth 
										+ "','" + vaderMisc.replace("'", "''").replace("\\", "") 
										+ "');";
								database.runQuery(query);
								vaderIsset = false;
								
								vaderFirstName = "";
								vaderPatronymic = "";
								vaderInsertion = "";
								vaderSurname = "";
								vaderAlias = "";
								vaderSex = "";
								vaderBirthPlace = "";
								vaderLivingPlace = "";
								vaderAge = "-1";
								vaderDateOfBirth = "0000-00-00";
								vaderMisc = "";
										
								query = "SET @vaderID = LAST_INSERT_ID(); ";
								database.runQuery(query);
							} else {query = "SET @vaderID = -1; "; database.runQuery(query);}
							
							if(moederIsset){
								 query = "INSERT INTO person (FirstName, Patronymic, Insertion, Surname, Alias, Sex, BirthPlace, LivingPlace, Age, DateOfBirth, Miscellaneous)"
										+ " VALUES ('" + moederFirstName.replace("'", "''").replace("\\", "")
										+ "','" + moederPatronymic.replace("'", "''").replace("\\", "")
										+ "','" + moederInsertion.replace("'", "''").replace("\\", "")
										+ "','" + moederSurname.replace("'", "''").replace("\\", "")
										+ "','" + moederAlias.replace("'", "''").replace("\\", "")
										+ "','" + moederSex
										+ "','" + moederBirthPlace.replace("'", "''").replace("\\", "")
										+ "','" + moederLivingPlace.replace("'", "''").replace("\\", "")
										+ "','" + moederAge
										+ "','" + moederDateOfBirth 
										+ "','" + moederMisc.replace("'", "''").replace("\\", "") 
										+ "');";
								database.runQuery(query);
								
								moederIsset = false;
								
								moederFirstName = "";
								moederPatronymic = "";
								moederInsertion = "";
								moederSurname = "";
								moederAlias = "";
								moederSex = "";
								moederBirthPlace = "";
								moederLivingPlace = "";
								moederAge = "-1";
								moederDateOfBirth = "0000-00-00";
								moederMisc = "";
										
								query = "SET @moederID = LAST_INSERT_ID(); ";
								database.runQuery(query);
							} else {query = "SET @moederID = -1; "; database.runQuery(query);}
									
							query = "INSERT INTO death_record (Register_ID, Place, DateRecord, DateOfDeath, PlaceOfDeath , Deceased_ID, Father_ID, Mother_ID, Relation_ID) "
									+ "VALUES ('" + registerID
									+ "','" + place.replace("'", "''").replace("\\", "")
									+ "','" + dateRecord
									+ "','" + dateOfDeath
									+ "','" + placeOfDeath.replace("'", "''").replace("\\", "")
									+ "', @deceasedID" 
									+ ", @vaderID"
									+ ", @moederID" 
									+ ", @relatieID" 
									+ ");";
							database.runQuery(query);
							database.close();
							
							registerID = "";
							place = "";
							dateRecord = "";
							dateOfDeath = "0000-00-00";
							placeOfDeath = "";
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