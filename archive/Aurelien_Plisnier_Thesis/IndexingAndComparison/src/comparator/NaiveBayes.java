package comparator;

import java.io.BufferedReader;
import java.io.BufferedWriter;
import java.io.FileNotFoundException;
import java.io.FileReader;
import java.io.IOException;
import java.util.Hashtable;

import org.apache.commons.math3.util.Precision;
import org.joda.time.DateTime;
import org.joda.time.Duration;

import data.CoupleData;
import data.PersonData;
import data.PlaceCoordinatesConverter;

public class NaiveBayes {

	private Hashtable<Integer, Double> matchDeltaKM;
	private Hashtable<Integer, Double> nonMatchDeltaKM;
	private Hashtable<Integer, Double> matchDeltaYears;
	private Hashtable<Integer, Double> matchDeltaYearsMin;
	private Hashtable<Integer, Double> matchDeltaYearsMax;
	private Hashtable<Integer, Double> nonMatchDeltaYears;
	private Hashtable<Integer, Double> matchFNdist;
	private Hashtable<Integer, Double> nonMatchFNdist;
	private Hashtable<Integer, Double> matchLNdist;
	private Hashtable<Integer, Double> nonMatchLNdist;
	private Hashtable<Integer, Double> matchPatDist;
	private Hashtable<Integer, Double> nonMatchPatDist;
	private Hashtable<Integer, Double> matchDeltaKMBP;
	
	private double threshold;

	public NaiveBayes(String matchingType, double threshold){
		this.threshold = threshold;

		//Hashtables containing the prob distribibutions.
		if(matchingType.equals("PP")){ //Parents to parents
			matchDeltaKM = new Hashtable<Integer, Double>();
			this.fillHashTable(matchDeltaKM, "stats/PP/geoDist.csv");

			nonMatchDeltaKM = new Hashtable<Integer, Double>();
			this.fillHashTable(nonMatchDeltaKM, "stats/PP/new/NonMatchGeoDist.csv");

			matchDeltaYears = new Hashtable<Integer, Double>();
			this.fillHashTable(matchDeltaYears, "stats/PP/DeltaYearBirths.csv");

			nonMatchDeltaYears = new Hashtable<Integer, Double>();
			this.fillHashTable(nonMatchDeltaYears, "stats/PP/new/NonMatchDeltaYears.csv");

			matchFNdist = new Hashtable<Integer, Double>();
			this.fillHashTable(matchFNdist, "stats/PP/FNdist.csv");

			nonMatchFNdist = new Hashtable<Integer, Double>();
			this.fillHashTable(nonMatchFNdist, "stats/PP/new/NonMatchFNdist.csv");

			matchLNdist = new Hashtable<Integer, Double>();
			this.fillHashTable(matchLNdist, "stats/PP/LNdist.csv");

			nonMatchLNdist = new Hashtable<Integer, Double>();
			this.fillHashTable(nonMatchLNdist, "stats/PP/new/NonMatchLNdist.csv");

			matchPatDist = new Hashtable<Integer, Double>();
			this.fillHashTable(matchPatDist, "stats/PP/Patdist.csv");

			nonMatchPatDist = new Hashtable<Integer, Double>();
			this.fillHashTable(nonMatchPatDist, "stats/PP/nonMatchesPatDist.csv");

			//System.out.println(nonMatchDeltaYears);
		}

		if(matchingType.equals("MP")){ //Newlyweds to parents
			matchDeltaKM = new Hashtable<Integer, Double>();
			this.fillHashTable(matchDeltaKM, "stats/MP/geoDistances.csv");

			nonMatchDeltaKM = new Hashtable<Integer, Double>();
			this.fillHashTable(nonMatchDeltaKM, "stats/PP/new/NonMatchGeoDist.csv");

			matchDeltaYearsMin = new Hashtable<Integer, Double>();
			this.fillHashTable(matchDeltaYearsMin, "stats/MP/deltaMin.csv");

			matchDeltaYearsMax = new Hashtable<Integer, Double>();
			this.fillHashTable(matchDeltaYearsMax, "stats/MP/deltaMax.csv");

			nonMatchDeltaYears = new Hashtable<Integer, Double>();
			this.fillHashTable(nonMatchDeltaYears, "stats/PP/new/NonMatchDeltaYears.csv");

			matchFNdist = new Hashtable<Integer, Double>();
			this.fillHashTable(matchFNdist, "stats/PP/FNdist.csv");

			nonMatchFNdist = new Hashtable<Integer, Double>();
			this.fillHashTable(nonMatchFNdist, "stats/PP/new/NonMatchFNdist.csv");

			matchLNdist = new Hashtable<Integer, Double>();
			this.fillHashTable(matchLNdist, "stats/PP/LNdist.csv");

			nonMatchLNdist = new Hashtable<Integer, Double>();
			this.fillHashTable(nonMatchLNdist, "stats/PP/new/NonMatchLNdist.csv");

			matchPatDist = new Hashtable<Integer, Double>();
			this.fillHashTable(matchPatDist, "stats/PP/Patdist.csv");

			nonMatchPatDist = new Hashtable<Integer, Double>();
			this.fillHashTable(nonMatchPatDist, "stats/PP/nonMatchesPatDist.csv");

		}

		if(matchingType.equals("BMP")){ //Newborns to parents
			matchDeltaKMBP = new Hashtable<Integer, Double>();
			this.fillHashTable(matchDeltaKMBP, "stats/BMP/geoDistanceMatchesBMP.csv");			

			matchDeltaKM = new Hashtable<Integer, Double>();
			this.fillHashTable(matchDeltaKM, "stats/BMP/geoDistanceMatchesBMP.csv");

			nonMatchDeltaKM = new Hashtable<Integer, Double>();
			this.fillHashTable(nonMatchDeltaKM, "stats/PP/new/NonMatchGeoDist.csv");

			matchDeltaYears = new Hashtable<Integer, Double>();
			this.fillHashTable(matchDeltaYears, "stats/BMP/deltaYearMatchesBMP.csv");

			nonMatchDeltaYears = new Hashtable<Integer, Double>();
			this.fillHashTable(nonMatchDeltaYears, "stats/BMP/nonMatchesDeltaYear.csv");

			matchFNdist = new Hashtable<Integer, Double>();
			this.fillHashTable(matchFNdist, "stats/PP/FNdist.csv");

			nonMatchFNdist = new Hashtable<Integer, Double>();
			this.fillHashTable(nonMatchFNdist, "stats/PP/new/NonMatchFNdist.csv");

			matchLNdist = new Hashtable<Integer, Double>();
			this.fillHashTable(matchLNdist, "stats/PP/LNdist.csv");

			nonMatchLNdist = new Hashtable<Integer, Double>();
			this.fillHashTable(nonMatchLNdist, "stats/PP/new/NonMatchLNdist.csv");

			matchPatDist = new Hashtable<Integer, Double>();
			this.fillHashTable(matchPatDist, "stats/PP/Patdist.csv");

			nonMatchPatDist = new Hashtable<Integer, Double>();
			this.fillHashTable(nonMatchPatDist, "stats/PP/nonMatchesPatDist.csv");

		}
	}

	//Reads Excel files containing prob distributions. !! Hardcoded to the format of my files
	private void fillHashTable(Hashtable<Integer, Double> table, String filePath){
		BufferedReader br;
		String line;
		String[] curLine;
		try {
			br = new BufferedReader(new FileReader(filePath));
			line = br.readLine(); 
			curLine = new String[6];
			while(line != null) {			
				if(!line.isEmpty()){
					curLine = line.split(";");
					if(curLine.length == 6){ 		
						if(!curLine[0].isEmpty() && !curLine[3].isEmpty()){
							if(this.isNumeric(curLine[0]) && this.isNumeric(curLine[3])){
								System.out.println("0 : " + Integer.parseInt(curLine[0]) + " , 3 : " + Double.parseDouble(curLine[3].replace(',', '.')));
								table.put(Integer.parseInt(curLine[0]), Double.parseDouble(curLine[3].replace(',', '.')));
							}

						}
					}
				}
				line = br.readLine();
			}

		} catch (FileNotFoundException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		} catch (IOException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		}
	}


	private boolean isNumeric(String str)  
	{  
		try  
		{  
			Double.parseDouble(str.replace(',', '.'));  
		}  
		catch(NumberFormatException nfe)  
		{  
			return false;  
		}  
		return true;  
	}


	//Compute sim score for pair of parents and classify the pair according to the score and the threshold.
	public void comparisonPP(CoupleData couple1, CoupleData couple2, BufferedWriter bw, PlaceCoordinatesConverter pCC) throws IOException{

		if(couple1.getRecordID() == couple2.getRecordID()) return;

		String man1FirstName =  couple1.getNames().get(0).toLowerCase();
		String man1LastName = couple1.getNames().get(1).toLowerCase();
		String man1Patronymic = couple1.getManPat();
		String woman1FirstName =  couple1.getNames().get(2).toLowerCase();
		String woman1LastName = couple1.getNames().get(3).toLowerCase();
		String woman1Patronymic = couple1.getWomanPat();

		String man2FirstName =  couple2.getNames().get(0).toLowerCase();
		String man2LastName = couple2.getNames().get(1).toLowerCase();
		String man2Patronymic = couple2.getManPat();
		String woman2FirstName =  couple2.getNames().get(2).toLowerCase();
		String woman2LastName = couple2.getNames().get(3).toLowerCase();
		String woman2Patronymic = couple2.getWomanPat();

		String date1String = couple1.getDate();
		String date2String = couple2.getDate();

		int distFFN = -1, distFLN = -1, distMFN = -1, distMLN = -1, geoDist = -1, deltaYears = -1, distFPat = -1, distMPat = -1;
		double probMatchDistFFN, probMatchDistFLN, probMatchDistMFN, probMatchDistMLN, probMatchGeoDist, probMatchDeltaYears, probMatchDistFPat, probMatchDistMPat;
		double probNonMatchDistFFN, probNonMatchDistFLN, probNonMatchDistMFN, probNonMatchDistMLN, probNonMatchGeoDist, probNonMatchDeltaYears, probNonMatchDistFPat, probNonMatchDistMPat;

		if(!date1String.isEmpty() && !date2String.isEmpty() && date1String.split("-").length == 3 && date2String.split("-").length == 3){

			String year1String = date1String.split("-")[0].replaceAll("[^0-9]", "");
			String year2String = date2String.split("-")[0].replaceAll("[^0-9]", "");
			String month1String = date1String.split("-")[1].replaceAll("[^0-9]", "");
			String month2String = date2String.split("-")[1].replaceAll("[^0-9]", "");
			String day1String = date1String.split("-")[2].replaceAll("[^0-9]", "");
			String day2String = date2String.split("-")[2].replaceAll("[^0-9]", "");

			//Date score
			if(!year1String.isEmpty() && !year2String.isEmpty() && !month1String.isEmpty() && !month2String.isEmpty() && !day1String.isEmpty() && !day2String.isEmpty()){
				int year1 = Integer.parseInt(year1String);
				int year2 = Integer.parseInt(year2String);
				int month1 = Integer.parseInt(month1String);
				int month2 = Integer.parseInt(month2String);
				int day1 = Integer.parseInt(day1String);
				int day2 = Integer.parseInt(day2String);
				if (!(year1 < 1550 || year2 < 1550 || year1 > 1850 || year2 > 1850 || month1 < 1 || month2 < 1 || month1 > 12 || month2 > 12 || day1 < 1 || day2 < 1 || day1 > 31 || day2 > 31)){
					if (month1 == 2 && day1 > 28) day1 = 28;
					if (month2 == 2 && day2 > 28) day2 = 28;
					if ((month1 == 4 || month1 == 6 || month1 == 9 || month1 == 11) && day1 > 30) day1 = 30;
					if ((month2 == 4 || month2 == 6 || month2 == 9 || month2 == 11) && day2 > 30) day2 = 30;
					DateTime date1 = new DateTime(year1, month1, day1, 0, 0, 0, 0);
					DateTime date2 = new DateTime(year2, month2, day2, 0, 0, 0, 0);
					int deltaDays = Math.abs((int) new Duration(date1, date2).getStandardDays());
					if(deltaDays < 274 && deltaDays != 0){ // If the two births are less than 9 months away, both couples can't be the same. Except for twins, so dates should be the same.
						return;
					}
				}
			}

			if(!year1String.isEmpty() && !year2String.isEmpty()){
				deltaYears = Math.abs(Integer.parseInt(year1String) - Integer.parseInt(year2String));
				if(deltaYears > 38) return;
				probMatchDeltaYears = matchDeltaYears.get(deltaYears);
				probNonMatchDeltaYears = nonMatchDeltaYears.get(deltaYears);
			}
			else {
				probNonMatchDeltaYears = 1;
				probMatchDeltaYears = 1;
			}
		} else{
			probNonMatchDeltaYears = 1;
			probMatchDeltaYears = 1;
		}

		//Place score
		int geoDistance = PairwiseComparison.geoDistance(couple1.getPlace(), couple2.getPlace(), pCC);
		if(geoDistance != -1){
			geoDist = (int)Precision.round((double) geoDistance, -1);
			if(geoDist > 120){
				probMatchGeoDist = 1;
				probNonMatchGeoDist = 1;
			}
			else {
				probMatchGeoDist = matchDeltaKM.get(geoDist);
				probNonMatchGeoDist = nonMatchDeltaKM.get(geoDist);
			}
		} else{
			probMatchGeoDist = 1;
			probNonMatchGeoDist = 1;
		}

		//Men Patronymic Score
		if(man1Patronymic != null && man2Patronymic != null && !man1Patronymic.isEmpty() && !man2Patronymic.isEmpty()){
			distFPat = LevenshteinDistance.LevenshteinDistance(man1Patronymic.toLowerCase(), man2Patronymic.toLowerCase());
			if(distFPat > 14){
				probMatchDistFPat = 1;
				probNonMatchDistFPat = 1;
			}
			else {
				probMatchDistFPat = matchPatDist.get(distFPat);
				probNonMatchDistFPat = nonMatchPatDist.get(distFPat);
			}		
		} else {
			probMatchDistFPat = 1;
			probNonMatchDistFPat = 1;
		}

		//Women Patronymic Score
		if(woman1Patronymic != null && woman2Patronymic != null && !woman1Patronymic.isEmpty() && !woman2Patronymic.isEmpty()){
			distMPat = LevenshteinDistance.LevenshteinDistance(woman1Patronymic.toLowerCase(), woman2Patronymic.toLowerCase());
			if(distMPat > 14){
				probMatchDistMPat = 1;
				probNonMatchDistMPat = 1;
			}
			else {
				probMatchDistMPat = matchPatDist.get(distMPat);
				probNonMatchDistMPat = nonMatchPatDist.get(distMPat);
			}			
		} else {
			probMatchDistMPat = 1;
			probNonMatchDistMPat = 1;
		}

		//Men first name score
		distFFN = LevenshteinDistance.LevenshteinDistance(man1FirstName, man2FirstName);
		if(distFFN > 17){ // Not available in stats, so we use a neutral value
			probMatchDistFFN = 1;
			probNonMatchDistFFN = 1;
		}
		else {
			probMatchDistFFN = matchFNdist.get(distFFN);
			probNonMatchDistFFN = nonMatchFNdist.get(distFFN);
		}


		//Men last name score
		distFLN = LevenshteinDistance.LevenshteinDistance(man1LastName, man2LastName);
		if(distFLN > 24){
			probMatchDistFLN = 1;
			probNonMatchDistFLN = 1;
		}
		else {
			probMatchDistFLN = matchLNdist.get(distFLN);
			probNonMatchDistFLN = nonMatchLNdist.get(distFLN);
		}

		//Women first name score
		distMFN = LevenshteinDistance.LevenshteinDistance(woman1FirstName, woman2FirstName);
		if(distMFN > 17){
			probMatchDistMFN = 1;
			probNonMatchDistMFN = 1;
		}
		else {
			probMatchDistMFN = matchFNdist.get(distMFN);
			probNonMatchDistMFN = nonMatchFNdist.get(distMFN);
		}


		//Women last name score
		distMLN = LevenshteinDistance.LevenshteinDistance(woman1LastName, woman2LastName);
		if(distMLN > 24){
			probMatchDistMLN = 1;
			probNonMatchDistMLN = 1;
		}
		else {
			probMatchDistMLN = matchLNdist.get(distMLN);
			probNonMatchDistMLN = nonMatchLNdist.get(distMLN);
		}


		//Global score.
		float score = (float) ((float)(probMatchDistFFN * probMatchDistFLN * probMatchDistMFN * probMatchDistMLN * probMatchGeoDist * probMatchDeltaYears * probMatchDistFPat * probMatchDistMPat)/(probNonMatchDistFFN * probNonMatchDistFLN * probNonMatchDistMFN * probNonMatchDistMLN * probNonMatchGeoDist * probNonMatchDeltaYears * probNonMatchDistFPat * probNonMatchDistMPat));

		//Threshold based comparison.
		if(score < this.threshold){
			return;
		}		
		else{
			//bw.write(couple1.getRecordID() + "," + couple2.getRecordID() + "," + score + "," + distFFN + "," + distFPat + "," + distFLN + "," + distMFN + "," + distMPat + "," + distMLN + "," + geoDist + "," + deltaYears + "\n");
			bw.write(couple1.getRecordID() + "," + couple2.getRecordID() + "," + score + "\n");
		}

	}

	//Compute sim score for pair of newlyweds and parents and classify the pair according to the score and the threshold.
	public void comparisonMP(CoupleData newlyweds, CoupleData parents, BufferedWriter bw, PlaceCoordinatesConverter pCC) throws IOException{

		String man1FirstName =  newlyweds.getNames().get(0).toLowerCase();
		String man1LastName = newlyweds.getNames().get(1).toLowerCase();
		String man1Patronymic = newlyweds.getManPat();
		String woman1FirstName =  newlyweds.getNames().get(2).toLowerCase();
		String woman1LastName = newlyweds.getNames().get(3).toLowerCase();
		String woman1Patronymic = newlyweds.getWomanPat();

		String man2FirstName =  parents.getNames().get(0).toLowerCase();
		String man2LastName = parents.getNames().get(1).toLowerCase();
		String man2Patronymic = parents.getManPat();
		String woman2FirstName =  parents.getNames().get(2).toLowerCase();
		String woman2LastName = parents.getNames().get(3).toLowerCase();
		String woman2Patronymic = parents.getWomanPat();

		String date1String = newlyweds.getDate();
		String date2String = parents.getDate();

		int minYearBirth, maxYearBirth, yearMarriage;

		int distFFN = -1, distFLN = -1, distMFN = -1, distMLN = -1, geoDist = -1, deltaYearsMin = -1, deltaYearsMax = -1, distFPat = -1, distMPat = -1;
		double probMatchDistFFN, probMatchDistFLN, probMatchDistMFN, probMatchDistMLN, probMatchGeoDist, probMatchDeltaYearsMin, probMatchDeltaYearsMax, probMatchDistFPat, probMatchDistMPat;
		double probNonMatchDistFFN, probNonMatchDistFLN, probNonMatchDistMFN, probNonMatchDistMLN, probNonMatchGeoDist, probNonMatchDeltaYearsMin, probNonMatchDeltaYearsMax, probNonMatchDistFPat, probNonMatchDistMPat;

		if(!date1String.isEmpty() && !date2String.isEmpty()){
			String minYearBirthString = date2String.split(";")[0].replaceAll("[^0-9]", "");
			String maxYearBirthString = date2String.split(";")[1].replaceAll("[^0-9]", "");
			String yearMarriageString = date1String.split("-")[0].replaceAll("[^0-9]", "");

			//System.out.println("min: " + minYearBirthString + " ;max: " +maxYearBirthString + " ; marriage: " + yearMarriageString);

			if(!minYearBirthString.isEmpty() && !maxYearBirthString.isEmpty() && !yearMarriageString.isEmpty()){
				minYearBirth = Integer.parseInt(minYearBirthString);
				maxYearBirth = Integer.parseInt(maxYearBirthString);
				yearMarriage = Integer.parseInt(yearMarriageString);

				//System.out.println("min: " + minYearBirth + " ;max: " + maxYearBirth + " ; marriage: " + yearMarriage);

				if (!(minYearBirth < 1550 || maxYearBirth < 1550 || minYearBirth > 1850 || maxYearBirth > 1850 || yearMarriage < 1550 || yearMarriage > 1850)){

					if(minYearBirth < yearMarriage || maxYearBirth > yearMarriage + 38){ //Birth should take place after marriage. Also, last birth should not take place too long after marriage.
						return;
					} else{
						deltaYearsMin = minYearBirth - yearMarriage;
						deltaYearsMax = maxYearBirth - yearMarriage;

						//System.out.println(deltaYears);
						if(deltaYearsMin <= 33){
							probMatchDeltaYearsMin = matchDeltaYearsMin.get(deltaYearsMin);
							probNonMatchDeltaYearsMin = nonMatchDeltaYears.get(deltaYearsMin);		
						} else {
							probMatchDeltaYearsMin = 1;
							probNonMatchDeltaYearsMin = 1;
						}

						if(deltaYearsMax <= 36 && maxYearBirth > minYearBirth){
							probMatchDeltaYearsMax = matchDeltaYearsMax.get(deltaYearsMax);
							probNonMatchDeltaYearsMax = nonMatchDeltaYears.get(deltaYearsMax);
						} else {
							probMatchDeltaYearsMax = 1;
							probNonMatchDeltaYearsMax = 1;
						}
					}
				} else return;
			} else {
				probMatchDeltaYearsMin= 1;
				probNonMatchDeltaYearsMin= 1;
				probMatchDeltaYearsMax= 1;
				probNonMatchDeltaYearsMax= 1;
			}
		} else {
			probMatchDeltaYearsMin= 1;
			probNonMatchDeltaYearsMin= 1;
			probMatchDeltaYearsMax= 1;
			probNonMatchDeltaYearsMax= 1;
		}

		//Place score
		int geoDistance = -1; geoDist = -1;
		if(newlyweds.getPlace() != null && parents.getPlace() != null) {
			geoDistance = PairwiseComparison.geoDistance(newlyweds.getPlace(), parents.getPlace(), pCC);
			if(geoDistance != -1){
				geoDist = (int)Precision.round((double) geoDistance, -1);
				if(geoDist > 120 || geoDist == -1){
					probMatchGeoDist = 1;
					probNonMatchGeoDist = 1;
				}
				else {
					probMatchGeoDist = matchDeltaKM.get(geoDist);
					probNonMatchGeoDist = nonMatchDeltaKM.get(geoDist);
				}
			} else{
				probMatchGeoDist = 1;
				probNonMatchGeoDist = 1;
			}
		}else{
			probMatchGeoDist = 1;
			probNonMatchGeoDist = 1;
		}

		//Men patronymic score
		if(man1Patronymic != null && man2Patronymic != null && !man1Patronymic.isEmpty() && !man2Patronymic.isEmpty()){
			distFPat = LevenshteinDistance.LevenshteinDistance(man1Patronymic.toLowerCase(), man2Patronymic.toLowerCase());
			if(distFPat > 14){
				probMatchDistFPat = 1;
				probNonMatchDistFPat = 1;
			}
			else {
				probMatchDistFPat = matchPatDist.get(distFPat);
				probNonMatchDistFPat = nonMatchPatDist.get(distFPat);
			}		
		} else {
			probMatchDistFPat = 1;
			probNonMatchDistFPat = 1;
		}

		//Women patronymic score
		if(woman1Patronymic != null && woman2Patronymic != null && !woman1Patronymic.isEmpty() && !woman2Patronymic.isEmpty()){
			distMPat = LevenshteinDistance.LevenshteinDistance(woman1Patronymic.toLowerCase(), woman2Patronymic.toLowerCase());
			if(distMPat > 14){
				probMatchDistMPat = 1;
				probNonMatchDistMPat = 1;
			}
			else {
				probMatchDistMPat = matchPatDist.get(distMPat);
				probNonMatchDistMPat = nonMatchPatDist.get(distMPat);
			}			
		} else {
			probMatchDistMPat = 1;
			probNonMatchDistMPat = 1;
		}

		//Men first name score.
		distFFN = LevenshteinDistance.LevenshteinDistance(man1FirstName, man2FirstName);
		if(distFFN > 17){ // Not available in stats, so we use a neutral value
			probMatchDistFFN = 1;
			probNonMatchDistFFN = 1;
		}
		else {
			probMatchDistFFN = matchFNdist.get(distFFN);
			probNonMatchDistFFN = nonMatchFNdist.get(distFFN);
		}


		//Men last name score
		distFLN = LevenshteinDistance.LevenshteinDistance(man1LastName, man2LastName);
		if(distFLN > 24){
			probMatchDistFLN = 1;
			probNonMatchDistFLN = 1;
		}
		else {
			probMatchDistFLN = matchLNdist.get(distFLN);
			probNonMatchDistFLN = nonMatchLNdist.get(distFLN);
		}

		//Women first name score
		distMFN = LevenshteinDistance.LevenshteinDistance(woman1FirstName, woman2FirstName);
		if(distMFN > 17){
			probMatchDistMFN = 1;
			probNonMatchDistMFN = 1;
		}
		else {
			probMatchDistMFN = matchFNdist.get(distMFN);
			probNonMatchDistMFN = nonMatchFNdist.get(distMFN);
		}

		//Women last name score
		distMLN = LevenshteinDistance.LevenshteinDistance(woman1LastName, woman2LastName);
		if(distMLN > 24){
			probMatchDistMLN = 1;
			probNonMatchDistMLN = 1;
		}
		else {
			probMatchDistMLN = matchLNdist.get(distMLN);
			probNonMatchDistMLN = nonMatchLNdist.get(distMLN);
		}


		float score = (float) ((float)(probMatchDistFFN * probMatchDistFLN * probMatchDistMFN * probMatchDistMLN * probMatchGeoDist * probMatchDeltaYearsMin  * probMatchDistFPat * probMatchDistMPat)/(probNonMatchDistFFN * probNonMatchDistFLN * probNonMatchDistMFN * probNonMatchDistMLN * probNonMatchGeoDist * probNonMatchDeltaYearsMin  * probNonMatchDistFPat * probNonMatchDistMPat));

		if(score < threshold){
			//if(score < 50000){
			return;
		}		
		else{
			bw.write(newlyweds.getRecordID() + "," + parents.getRecordID() + "," + score + "," + deltaYearsMin + "," + geoDist + "," + distFFN + "," + distFPat + "," + distFLN + "," + distMFN + "," + distMPat + "," + distMLN + "\n");
			//bw.write(";" + newlyweds.getRecordID() + "," + parents.getRecordID() + "," + score + "\n");
			//bw.write(";" + couple1.getRecordID() + "," + couple2.getRecordID() + "," + score + "," + scoreJulia + "," + probMatchDistFFN + "," + probMatchDistFPat + "," + probMatchDistFLN + "," + probNonMatchDistFFN + "," + probNonMatchDistFPat + "," + probNonMatchDistFLN + "," + probMatchDistMFN + "," + probMatchDistMPat + "," + probMatchDistMLN + "," + probNonMatchDistMFN + "," + probNonMatchDistMPat + "," + probNonMatchDistMLN + "," + probMatchGeoDist + "," + probNonMatchGeoDist + "," + probMatchDeltaYears + "," + probNonMatchDeltaYears); 
		}
		//bw.write(";" + couple1.getRecordID() + "," + couple2.getRecordID() + "," + score);

	}

	public void comparisonBMP(PersonData child, PersonData parent, BufferedWriter bw, PlaceCoordinatesConverter pCC) throws IOException{

		char parentGender = parent.getGender();
		char childGender = child.getGender();
		int parentYear = parent.getYear();
		int childYear = child.getYear();
		String parentFirstName =  parent.getNames().get(0).toLowerCase();
		String childFirstName = child.getNames().get(0).toLowerCase();
		String parentPat = parent.getPatronymic().toLowerCase();
		String childPat = child.getPatronymic().toLowerCase();
		String parentLastName =  parent.getNames().get(1).toLowerCase();
		String childLastName = child.getNames().get(1).toLowerCase();
		String parentPlaceOfBirth = parent.getPlaceOfBirth();
		String childPlace = child.getPlace();
		String parentPlace = parent.getPlace();

		int distFN = -1, distLN = -1, geoDist = -1, deltaYears = -1, distPat = -1, distPlaceOfBirth = -1;
		double probMatchDistFN, probMatchDistLN, probMatchGeoDist, probMatchDeltaYears, probMatchDistPat;
		double probNonMatchDistFN, probNonMatchDistLN, probNonMatchGeoDist, probNonMatchDeltaYears, probNonMatchDistPat;

		//FILTER ON GENDER (If available)
		if(childGender != 'u' && childGender != parentGender){
			return;
		}

		//FILTER ON DATE 
		//System.out.println(parent.getMaxYear());
		if ((parentYear < childYear + 12) || (parentGender == 'v' && parent.getMaxYear() > childYear + 60) || (parentGender == 'm' && parent.getMaxYear() > childYear + 99)) {
			return;
			//probMatchDeltaYears = 1;
			//probNonMatchDeltaYears = 1;
		} else{

			deltaYears = parentYear - childYear;
			//System.out.println(deltaYears);
			probMatchDeltaYears = matchDeltaYears.get(deltaYears);
			probNonMatchDeltaYears = nonMatchDeltaYears.get(deltaYears);
		}

		//FILTER ON PLACE 
		if (childPlace == null || childPlace.isEmpty() || parentPlace == null || parentPlace.isEmpty()) {
			probMatchGeoDist = 1;
			probNonMatchGeoDist = 1;
		} else{
			geoDist = (int)Precision.round((double) PairwiseComparison.geoDistance(childPlace.toLowerCase(), parentPlace.toLowerCase(), pCC), -1);
			if(geoDist > 120){
				probMatchGeoDist = 1;
				probNonMatchGeoDist = 1;
			}
			else {
				probMatchGeoDist = matchDeltaKM.get(geoDist);
				probNonMatchGeoDist = nonMatchDeltaKM.get(geoDist);
			}
		}
		if(parentPlaceOfBirth != null && !parentPlaceOfBirth.isEmpty()){
			distPlaceOfBirth = (int)Precision.round((double) PairwiseComparison.geoDistance(childPlace.toLowerCase(), parentPlaceOfBirth.toLowerCase(), pCC), -1);
			if(distPlaceOfBirth <= 120){
				probMatchGeoDist = probMatchGeoDist * matchDeltaKMBP.get(distPlaceOfBirth);
				probNonMatchGeoDist = probNonMatchGeoDist * nonMatchDeltaKM.get(distPlaceOfBirth);
			}
		}

		//PATRONYMIC
		if(childPat != null && parentPat != null && !childPat.isEmpty() && !parentPat.isEmpty()){
			distPat = LevenshteinDistance.LevenshteinDistance(childPat.toLowerCase(), parentPat.toLowerCase());
			if(distPat > 14){
				probMatchDistPat = 1;
				probNonMatchDistPat = 1;
			}
			else {
				probMatchDistPat = matchPatDist.get(distPat);
				probNonMatchDistPat = nonMatchPatDist.get(distPat);
			}		
		} else {
			probMatchDistPat = 1;
			probNonMatchDistPat = 1;
		}

		//FIRST NAME
		distFN = LevenshteinDistance.LevenshteinDistance(childFirstName, parentFirstName);
		if(distFN > 17){ // Not available in stats, so we use a neutral value
			probMatchDistFN = 1;
			probNonMatchDistFN = 1;
		}
		else {
			probMatchDistFN = matchFNdist.get(distFN);
			probNonMatchDistFN = nonMatchFNdist.get(distFN);
		}

		//LAST NAME
		distLN = LevenshteinDistance.LevenshteinDistance(childLastName, parentLastName);
		if(distLN > 24){
			probMatchDistLN = 1;
			probNonMatchDistLN = 1;
		}
		else {
			probMatchDistLN = matchLNdist.get(distLN);
			probNonMatchDistLN = nonMatchLNdist.get(distLN);
		}

		//SCORE COMPUTATION
		float score = (float) ((float)(probMatchDistFN * probMatchDistLN * probMatchGeoDist * probMatchDeltaYears * probMatchDistPat)/(probNonMatchDistFN * probNonMatchDistLN * probNonMatchGeoDist * probNonMatchDeltaYears * probNonMatchDistPat));


		//COMPARE SCORE TO THRESHOLD
		if(score < threshold){
			return;
		}		
		else{
			//System.out.println(childYear + "  ,  " + parentYear + "    ,   " + parent.getMaxYear() + "     ,   " + deltaYears + ";" + child.getRecordID() + "," + parent.getRecordID() + "," + score + "," + deltaYears + "," + geoDist + "," + distFN + "," + distLN + "," + distPat);
			//System.out.println(";" + child.getRecordID() + "," + parent.getRecordID() + "," + score + "," + deltaYears + "," + geoDist + "," + distFN + "," + distLN + "," + distPat); 3550
			if(deltaYears != -1 && geoDist != -1 && score > 1) bw.write(child.getRecordID() + "," + parent.getRecordID() + ","  + child.getPersonID() + "," + parent.getPersonID() + "," + score + "\n");
			// bw.write(child.getRecordID() + "," + parent.getRecordID() + ","  + child.getPersonID() + "," + parent.getPersonID() + "," + score + "," + deltaYears + "," + geoDist + "," + distFN + "," + distLN + "," + distPat + "\n"); //bw.write(";" + child.getRecordID() + "," + parent.getRecordID() + "," + child.getPersonID() + "," + parent.getPersonID() + "," + score);
		} 
	}

}
