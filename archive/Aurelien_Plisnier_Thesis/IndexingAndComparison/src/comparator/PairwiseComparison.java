package comparator;

import java.io.BufferedWriter;
import java.io.IOException;
import java.util.List;

import org.apache.commons.math3.util.Precision;
import org.joda.time.DateTime;
import org.joda.time.Duration;

import com.wcohen.ss.Jaro;

import data.CoupleData;
import data.PersonData;
import data.PlaceCoordinatesConverter;


// That class can be used to generate pairs for stats computation based on arbitrary criteria: we just have to force high similarity on every attributes but the ones we're seeking stats for. (cf information excess principle)
public class PairwiseComparison {

	public static void pairwiseComparisonNP(PersonData child, PersonData parent, BufferedWriter bw, PlaceCoordinatesConverter pCC) throws IOException{
		//FILTER ON GENDER (If available)
		char parentGender = parent.getGender();
		char childGender = child.getGender();
		int parentYear = parent.getYear();
		int childYear = child.getYear();
		String parentFirstName =  parent.getNames().get(0).toLowerCase();
		String childFirstName = child.getNames().get(0).toLowerCase();
		String parentLastName =  parent.getNames().get(1).toLowerCase();
		String parentPat = parent.getPatronymic().toLowerCase();
		String childPat = child.getPatronymic().toLowerCase();
		String childLastName = child.getNames().get(1).toLowerCase();
		String childPlace = child.getPlace();
		String parentPlaceOfBirth = parent.getPlaceOfBirth();

		if(childGender != 'u' && childGender != parentGender){
			//System.out.println("Gender rejected: " + child.getGender() + ", " + parentGender);
			return;
		}

		//FILTER ON DATE: ensure dates are consistent
		if (parentYear < child.getYear() + 12) {
			//System.out.println("Year rejected: " + child.getYear() + ", " + parentYear);
			return;
		}
		if (parentGender == 'v' && parent.getMaxYear() > childYear + 50){
			//System.out.println("Year rejected: " + child.getYear() + ", " + parentYear);
			return;
		}
		if (parentGender == 'm' && parent.getMaxYear() > childYear + 80){
			//System.out.println("Year rejected: " + child.getYear() + ", " + parentYear);
			return;
		}

		//PAIRWISE COMPARISON (Simple edit distance)
		int fnDist = LevenshteinDistance.LevenshteinDistance(childFirstName, parentFirstName);
		int lnDist = LevenshteinDistance.LevenshteinDistance(childLastName, parentLastName);	

		//int score = LevenshteinDistance.LevenshteinDistance(child.getNames().get(0), parent.getNames().get(0)) + LevenshteinDistance.LevenshteinDistance(child.getNames().get(1), parent.getNames().get(1));

		//FILTER ON SIMILARITY SCORE Thresholds set using probability distributions on first name and last name.
		if (fnDist > 4 || lnDist > 3) {
			//System.out.println("Score rejected: " + firstNameScore + " " + lastNameScore + " " + parent.getNames());
			return;
		}
		
		float dateScore = 0;
		int deltaYear = parentYear - childYear;
		if(parentGender == 'v') dateScore = 1 - (float)Math.abs(20-deltaYear)/30;
		if(parentGender == 'm') dateScore = 1 - (float)Math.abs(20-deltaYear)/60;
		float firstNameScore = 1 - (float)fnDist/Math.max(childFirstName.length(), parentFirstName.length());
		float lastNameScore = 1 - (float)lnDist/Math.max(childLastName.length(), parentLastName.length());
		float globalScore = (firstNameScore + lastNameScore + dateScore)/3;
		
		float patScore = 0;
		int patDist = -1;
		if(childPat != null && parentPat != null && !childPat.isEmpty() && !parentPat.isEmpty()){
			patDist = LevenshteinDistance.LevenshteinDistance(childPat, parentPat);
			patScore = 1 - (float)patDist/Math.max(childPat.length(), parentPat.length());
			globalScore = (3 * globalScore + patScore)/4;
		}
		
		int distPlaceOfBirth = -1;
		if(parentPlaceOfBirth != null && !parentPlaceOfBirth.isEmpty()){
			distPlaceOfBirth = (int)Precision.round((double) PairwiseComparison.geoDistance(childPlace, parentPlaceOfBirth, pCC), -1);
			if(distPlaceOfBirth <= 10){
				if (patScore == 0) globalScore = (3 * globalScore + 1)/4;
				else globalScore = (4 * globalScore + 1)/5;
			}
		}
		
		//else System.out.println("JW Accepted: " + score);

		//GEOGRAPHICAL DISTANCE

		int geoDistance = PairwiseComparison.geoDistance(parent.getPlace(), child.getPlace(), pCC);

		//STORE RESULTS
		bw.write(";" + child.getRecordID() + "," + parent.getRecordID() + "," + child.getPersonID() + "," + parent.getPersonID() + "," + globalScore + "," + deltaYear + "," + geoDistance + "," + distPlaceOfBirth + "," + fnDist + "," + lnDist + "," + patDist);

	}

	public static int geoDistance(String placeA, String placeB, PlaceCoordinatesConverter pCC){
		if (placeA.isEmpty() || placeB.isEmpty()) return -1;
		List<Double> coordinatesA = pCC.getCoordinates(placeA);
		List<Double> coordinatesB = pCC.getCoordinates(placeB);
		if (coordinatesA == null || coordinatesB == null) return -1;
		return PairwiseComparison.distFrom(coordinatesA.get(0), coordinatesA.get(1), coordinatesB.get(0), coordinatesB.get(1));		
	}

	//Compute geoDistance
	private static int distFrom(double lat1, double lng1, double lat2, double lng2) {
		double earthRadius = 6371; //kilometers
		double dLat = Math.toRadians(lat2-lat1);
		double dLng = Math.toRadians(lng2-lng1);
		double a = Math.sin(dLat/2) * Math.sin(dLat/2) +
				Math.cos(Math.toRadians(lat1)) * Math.cos(Math.toRadians(lat2)) *
				Math.sin(dLng/2) * Math.sin(dLng/2);
		double c = 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1-a));
		int dist = (int) (earthRadius * c);

		return dist;
	}
	/*
	//Returns JaroWinkler similarity score between names of 2 people
	private float jaroWinkler(Data child){
		float firstNameWeight = (float)1/3;
		float lastNameWeight = (float)2/3;

		float firstNamesJW = new JaroWinklerDistance().getDistance(child.getNames().get(0), this.names.get(0));
		float lastNamesJW = new JaroWinklerDistance().getDistance(child.getNames().get(1), this.names.get(1));
		float score = firstNameWeight * firstNamesJW + lastNameWeight * lastNamesJW;

		/*System.out.println("JW between " + child.getNames().get(0) + " and " + this.names.get(0) + " : " + firstNamesJW);
		System.out.println("JW between " + child.getNames().get(1) + " and " + this.names.get(1) + " : " + lastNamesJW);
		System.out.println("Global Score: " + score); */

	public static void pairwiseComparisonNPWithMetadata(PersonData child, PersonData parent, BufferedWriter bw, PlaceCoordinatesConverter pCC) throws IOException{


		char parentGender = parent.getGender();
		char childGender = child.getGender();
		int parentYear = parent.getYear();
		int childYear = child.getYear();
		String parentFirstName =  parent.getNames().get(0).toLowerCase();
		String childFirstName = child.getNames().get(0).toLowerCase();
		String parentLastName =  parent.getNames().get(1).toLowerCase();
		String childLastName = child.getNames().get(1).toLowerCase();

		//FILTER ON GENDER (If available)
		if(childGender != 'u' && childGender != parentGender){
			return;
		}

		//FILTER ON DATE
		if (parentYear < child.getYear() + 12) {
			return;
		}
		if (parentGender == 'v' && parentYear > childYear + 50){
			return;
		}
		if (parentGender == 'm' && parentYear > childYear + 100){
			return;
		}

		//PAIRWISE COMPARISON (Simple edit distance)

		float firstNameScore = 1 - (float)LevenshteinDistance.LevenshteinDistance(childFirstName, parentFirstName)/Math.max(childFirstName.length(), parentFirstName.length());
		float lastNameScore = 1 - (float)LevenshteinDistance.LevenshteinDistance(childLastName, parentLastName)/Math.max(childLastName.length(), parentLastName.length());
		float globalScore = (firstNameScore + lastNameScore)/2;

		//int score = LevenshteinDistance.LevenshteinDistance(child.getNames().get(0), parent.getNames().get(0)) + LevenshteinDistance.LevenshteinDistance(child.getNames().get(1), parent.getNames().get(1));

		//FILTER ON SIMILARITY SCORE
		if (firstNameScore < 0.81 || lastNameScore < 0.81) {
			return;
		}
		//else System.out.println("JW Accepted: " + score);

		//GEOGRAPHICAL DISTANCE

		int geoDistance = PairwiseComparison.geoDistance(parent.getPlace(), child.getPlace(), pCC);

		//STORE RESULTS

		//System.out.println("Writing Potential Match...");
		//bw.write(", (" + groupID + ", 0," + parent.getRecordID() + "," + parent.getPersonID() + "," + String.format(Locale.ENGLISH, "%.3f", globalScore) + "," + geoDistance + ") \n"); // String.format("%.3f", score) if score is a float
		//bw.write("\n");

	}

	public static boolean jaroPairwiseComparison(PersonData parent, PersonData child) {
		//FILTER ON GENDER (If available)
		char parentGender = parent.getGender();
		char childGender = child.getGender();
		int parentYear = parent.getYear();
		int childYear = child.getYear();
		String parentFirstName =  parent.getNames().get(0);
		String childFirstName = child.getNames().get(0);
		String parentLastName =  parent.getNames().get(1);
		String childLastName = child.getNames().get(1);

		if(childGender != 'u' && childGender != parentGender){
			//System.out.println("Gender rejected: " + child.getGender() + ", " + parentGender);
			return false;
		}

		//FILTER ON DATE
		if (parentYear < child.getYear() + 12) {
			//System.out.println("Year rejected: " + child.getYear() + ", " + parentYear);
			return false;
		}
		if (parentGender == 'v' && parentYear > childYear + 50){
			//System.out.println("Year rejected: " + child.getYear() + ", " + parentYear);
			return false;
		}
		if (parentGender == 'm' && parentYear > childYear + 100){
			//System.out.println("Year rejected: " + child.getYear() + ", " + parentYear);
			return false;
		}

		//PAIRWISE COMPARISON (Simple edit distance)

		double firstNameScore = new Jaro().score(parentFirstName, childFirstName);
		double lastNameScore = new Jaro().score(parentLastName, childLastName);

		//int score = LevenshteinDistance.LevenshteinDistance(child.getNames().get(0), parent.getNames().get(0)) + LevenshteinDistance.LevenshteinDistance(child.getNames().get(1), parent.getNames().get(1));

		//FILTER ON SIMILARITY SCORE
		if (firstNameScore < 0.75 || lastNameScore < 0.75) {
			//System.out.println("Score rejected: " + firstNameScore + " " + lastNameScore + " " + parent.getNames());
			return false;
		}

		return true;
	}

	public static void pairwiseComparisonPPWithMetadata(CoupleData couple1, CoupleData couple2, BufferedWriter bw, PlaceCoordinatesConverter pCC) throws IOException {


		String man1FirstName =  couple1.getNames().get(0).toLowerCase();
		String man1LastName = couple1.getNames().get(1).toLowerCase();
		String woman1FirstName =  couple1.getNames().get(2).toLowerCase();
		String woman1LastName = couple1.getNames().get(3).toLowerCase();

		String man2FirstName =  couple2.getNames().get(0).toLowerCase();
		String man2LastName = couple2.getNames().get(1).toLowerCase();
		String woman2FirstName =  couple2.getNames().get(2).toLowerCase();
		String woman2LastName = couple2.getNames().get(3).toLowerCase();

		String date1String = couple1.getDate();
		String date2String = couple2.getDate();

		//FILTER ON DATE
		if(!date1String.isEmpty() && !date2String.isEmpty() && date1String.split("-").length == 3 && date2String.split("-").length == 3){
			String year1String = date1String.split("-")[0].replaceAll("[^0-9]", "");
			String year2String = date2String.split("-")[0].replaceAll("[^0-9]", "");
			String month1String = date1String.split("-")[1].replaceAll("[^0-9]", "");
			String month2String = date2String.split("-")[1].replaceAll("[^0-9]", "");
			String day1String = date1String.split("-")[2].replaceAll("[^0-9]", "");
			String day2String = date2String.split("-")[2].replaceAll("[^0-9]", "");


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
					if(deltaDays > 38 * 365){ // A woman cannot have a child before her 12 nor after her 50. So if two births are more than 38 years away it can't be the same couple.
						return;
					}
				}
			}
		}

		//PAIRWISE COMPARISON (Simple edit distance)

		float firstNameScoreMen = 1 - (float)LevenshteinDistance.LevenshteinDistance(man1FirstName, man2FirstName)/Math.max(man1FirstName.length(), man2FirstName.length());
		float lastNameScoreMen = 1 - (float)LevenshteinDistance.LevenshteinDistance(man1LastName, man2LastName)/Math.max(man1LastName.length(), man2LastName.length());
		float firstNameScoreWomen = 1 - (float)LevenshteinDistance.LevenshteinDistance(woman1FirstName, woman2FirstName)/Math.max(woman1FirstName.length(), woman2FirstName.length());
		float lastNameScoreWomen = 1 - (float)LevenshteinDistance.LevenshteinDistance(woman1LastName, woman2LastName)/Math.max(woman1LastName.length(), woman2LastName.length());

		//FILTER ON SIMILARITY SCORE
		if (firstNameScoreMen < 0.76 || lastNameScoreMen < 0.66 || firstNameScoreWomen < 0.76 || lastNameScoreWomen < 0.66) {
			//System.out.println("FN men :" + firstNameScoreMen + "LN men: " + lastNameScoreMen + "FN women: " + firstNameScoreWomen + "LN women: " + lastNameScoreWomen);
			return;
		}

		//STORE RESULTS

		bw.write(";1," + couple1.getRecordID() + ",0," + couple2.getRecordID());
		//bw.write(",(1, " + couple1.getRecordID() + ", 0, " + couple2.getRecordID() + ") \n");
	}

	public static void pairwiseComparisonMPWithMetadata(CoupleData couple1, CoupleData couple2, BufferedWriter bw, PlaceCoordinatesConverter pCC) throws IOException {

		String man1FirstName =  couple1.getNames().get(0).toLowerCase();
		String man1Pat = couple1.getManPat();
		String man1LastName = couple1.getNames().get(1).toLowerCase();
		String woman1FirstName =  couple1.getNames().get(2).toLowerCase();
		String woman1Pat = couple1.getWomanPat();
		String woman1LastName = couple1.getNames().get(3).toLowerCase();

		String man2FirstName =  couple2.getNames().get(0).toLowerCase();
		String man2Pat = couple2.getManPat();
		String man2LastName = couple2.getNames().get(1).toLowerCase();
		String woman2FirstName =  couple2.getNames().get(2).toLowerCase();
		String woman2Pat = couple2.getWomanPat();
		String woman2LastName = couple2.getNames().get(3).toLowerCase();

		int minYearBirth = 0, maxYearBirth = 0, yearMarriage = 0;
		int deltaYear = -1, distFPat = -1, distMPat = -1;
		float globalScore = 0, dateScore = 0;;
		
		String date1String = couple1.getDate();
		String date2String = couple2.getDate();

		//System.out.println(date1String + "  2 " + date2String);
		
		//PAIRWISE COMPARISON (Simple edit distance)
		int distFFN = LevenshteinDistance.LevenshteinDistance(man1FirstName, man2FirstName);
		int distFLN = LevenshteinDistance.LevenshteinDistance(man1LastName, man2LastName);
		int distMFN = LevenshteinDistance.LevenshteinDistance(woman1FirstName, woman2FirstName);
		int distMLN = LevenshteinDistance.LevenshteinDistance(woman1LastName, woman2LastName);

		float firstNameScoreMen = 1 - (float)distFFN/Math.max(man1FirstName.length(), man2FirstName.length());
		float lastNameScoreMen = 1 - (float)distFLN/Math.max(man1LastName.length(), man2LastName.length());
		float firstNameScoreWomen = 1 - (float)distMFN/Math.max(woman1FirstName.length(), woman2FirstName.length());
		float lastNameScoreWomen = 1 - (float)distMLN/Math.max(woman1LastName.length(), woman2LastName.length());
		
		globalScore = (firstNameScoreMen + lastNameScoreMen + firstNameScoreWomen + lastNameScoreWomen)/4;

		//FILTER ON DATE
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
					}
					else {
						deltaYear = minYearBirth - yearMarriage;
						dateScore = 1 - (float)Math.abs(1-deltaYear)/38;
					}
				}
			}
		}
		globalScore = (4 * globalScore + dateScore)/5;
		
		float patFScore = 0;
		boolean patFContribution = false;
		int patFDist = -1;
		if(man1Pat != null && man2Pat != null && !man1Pat.isEmpty() && !man2Pat.isEmpty()){
			patFDist = LevenshteinDistance.LevenshteinDistance(man1Pat.toLowerCase(), man2Pat.toLowerCase());
			patFScore = 1 - (float)patFDist/Math.max(man1Pat.length(), man2Pat.length());
			globalScore = (5 * globalScore + patFScore)/6;
			patFContribution = true;
		}
		
		float patMScore = 0;
		boolean patMContribution = false;
		int patMDist = -1;
		if(woman1Pat != null && woman2Pat != null && !woman1Pat.isEmpty() && !woman2Pat.isEmpty()){
			patMDist = LevenshteinDistance.LevenshteinDistance(woman1Pat.toLowerCase(), woman2Pat.toLowerCase());
			patMScore = 1 - (float)patMDist/Math.max(woman1Pat.length(), woman2Pat.length());
			if(!patFContribution) globalScore = (5 * globalScore + patMScore)/6;
			else globalScore = (6 * globalScore + patMScore)/7;
			patMContribution = true;
		}
		
		int geoDist = -1;
		String place1 = couple1.getPlace();
		String place2 = couple2.getPlace();
		if(place1 != null && !place1.isEmpty() && place2 != null && !place2.isEmpty()){
			geoDist = (int)Precision.round((double) PairwiseComparison.geoDistance(place1, place2, pCC), -1);
			if(geoDist <= 10){
				if(patFContribution && patMContribution) globalScore = (7 * globalScore + 1)/8;
				else if (!patFContribution && !patMContribution) globalScore = (5 * globalScore + 1)/6;
				else globalScore = (6 * globalScore + 1)/7;
			}
		}



		//FILTER ON SIMILARITY SCORE
		/*if (firstNameScoreMen < 0.66 || lastNameScoreMen < 0.55 || firstNameScoreWomen < 0.66 || lastNameScoreWomen < 0.55) {
			metadata.incrementEditDistanceFilterImpact();
			//System.out.println("FN men :" + firstNameScoreMen + "LN men: " + lastNameScoreMen + "FN women: " + firstNameScoreWomen + "LN women: " + lastNameScoreWomen);
			return;
		}*/

		//STORE RESULTS

		if(globalScore > 0.83) bw.write(";" + couple1.getRecordID() + "," + couple2.getRecordID() + ","  + globalScore);
		//bw.write(";" + couple1.getRecordID() + "," + couple2.getRecordID() + ","  + globalScore + "," + deltaYear + "," + geoDist + "," + distFFN + "," + distFPat + "," + distFLN + "," + distMFN + "," + distMPat + "," + distMLN);

	}

	public static void pairwiseComparisonPPforStatistics(PersonData father1, PersonData father2, BufferedWriter bw, PlaceCoordinatesConverter pCC) throws IOException{

		String man1FirstName =  father1.getNames().get(0).toLowerCase();
		String man1LastName = father1.getNames().get(1).toLowerCase();

		String man2FirstName =  father2.getNames().get(0).toLowerCase();
		String man2LastName = father2.getNames().get(1).toLowerCase();

		String place1 = father1.getPlace().toLowerCase();
		String place2 = father2.getPlace().toLowerCase();

		int year1 = father1.getYear();
		int year2 = father2.getYear();

		if(father1.getRecordID() == father2.getRecordID()) return;

		//FILTER ON DATE
		if(Math.abs(year1 - year2) > 10 || year1 < 1550 || year2 < 1550 || year1 > 1850 || year2 > 1850){
			return;

		}

		float firstNameScoreMen = 1 - (float)LevenshteinDistance.LevenshteinDistance(man1FirstName, man2FirstName)/Math.max(man1FirstName.length(), man2FirstName.length());
		float lastNameScoreMen = 1 - (float)LevenshteinDistance.LevenshteinDistance(man1LastName, man2LastName)/Math.max(man1LastName.length(), man2LastName.length());

		//FILTER ON SIMILARITY SCORE
		if (firstNameScoreMen < 0.90 || lastNameScoreMen < 0.90) {
			//System.out.println("FN men :" + firstNameScoreMen + "LN men: " + lastNameScoreMen + "FN women: " + firstNameScoreWomen + "LN women: " + lastNameScoreWomen);
			return;
		}

		float placeScore = 1 - (float)LevenshteinDistance.LevenshteinDistance(place1, place2)/Math.max(place1.length(), place2.length());

		if (placeScore < 0.90 || place1.isEmpty() || place2.isEmpty()) {
			//metadata.incrementEditDistanceFilterImpact();
			//System.out.println("FN men :" + firstNameScoreMen + "LN men: " + lastNameScoreMen + "FN women: " + firstNameScoreWomen + "LN women: " + lastNameScoreWomen);
			return;
		} 

		bw.write(";" + father1.getRecordID() + "," + father2.getRecordID());
	}

	public static void getDatesStatsPP(CoupleData couple1, CoupleData couple2, BufferedWriter bw) throws IOException {

		String man1FirstName =  couple1.getNames().get(0).toLowerCase();
		String man1LastName = couple1.getNames().get(1).toLowerCase();
		String woman1FirstName =  couple1.getNames().get(2).toLowerCase();
		String woman1LastName = couple1.getNames().get(3).toLowerCase();

		String man2FirstName =  couple2.getNames().get(0).toLowerCase();
		String man2LastName = couple2.getNames().get(1).toLowerCase();
		String woman2FirstName =  couple2.getNames().get(2).toLowerCase();
		String woman2LastName = couple2.getNames().get(3).toLowerCase();

		String place1 = couple1.getPlace().toLowerCase();
		String place2 = couple2.getPlace().toLowerCase();

		//PAIRWISE COMPARISON (Simple edit distance)

		float firstNameScoreMen = 1 - (float)LevenshteinDistance.LevenshteinDistance(man1FirstName, man2FirstName)/Math.max(man1FirstName.length(), man2FirstName.length());
		float lastNameScoreMen = 1 - (float)LevenshteinDistance.LevenshteinDistance(man1LastName, man2LastName)/Math.max(man1LastName.length(), man2LastName.length());
		float firstNameScoreWomen = 1 - (float)LevenshteinDistance.LevenshteinDistance(woman1FirstName, woman2FirstName)/Math.max(woman1FirstName.length(), woman2FirstName.length());
		float lastNameScoreWomen = 1 - (float)LevenshteinDistance.LevenshteinDistance(woman1LastName, woman2LastName)/Math.max(woman1LastName.length(), woman2LastName.length());

		//FILTER ON SIMILARITY SCORE
		if (firstNameScoreMen < 0.90 || lastNameScoreMen < 0.90 || firstNameScoreWomen < 0.90 || lastNameScoreWomen < 0.90) {
			//System.out.println("FN men :" + firstNameScoreMen + "LN men: " + lastNameScoreMen + "FN women: " + firstNameScoreWomen + "LN women: " + lastNameScoreWomen);
			return;
		}

		float placeScore = 1 - (float)LevenshteinDistance.LevenshteinDistance(place1, place2)/Math.max(place1.length(), place2.length());

		if (placeScore < 0.90 || place1.isEmpty() || place2.isEmpty()) {
			//metadata.incrementEditDistanceFilterImpact();
			//System.out.println("FN men :" + firstNameScoreMen + "LN men: " + lastNameScoreMen + "FN women: " + firstNameScoreWomen + "LN women: " + lastNameScoreWomen);
			return;
		}

		//STORE RESULTS

		bw.write(";" + couple1.getRecordID() + "," + couple2.getRecordID());
		//bw.write(",(1, " + couple1.getRecordID() + ", 0, " + couple2.getRecordID() + ") \n");

	}

	public static void getPlacesStatsPP(CoupleData couple1, CoupleData couple2, BufferedWriter bw, PlaceCoordinatesConverter pCC) throws IOException {	
		if(couple1.getPlace() == null || couple1.getPlace().isEmpty() || couple2.getPlace() == null || couple2.getPlace().isEmpty()) return;

		String man1FirstName =  couple1.getNames().get(0).toLowerCase();
		String man1LastName = couple1.getNames().get(1).toLowerCase();
		String woman1FirstName =  couple1.getNames().get(2).toLowerCase();
		String woman1LastName = couple1.getNames().get(3).toLowerCase();

		String man2FirstName =  couple2.getNames().get(0).toLowerCase();
		String man2LastName = couple2.getNames().get(1).toLowerCase();
		String woman2FirstName =  couple2.getNames().get(2).toLowerCase();
		String woman2LastName = couple2.getNames().get(3).toLowerCase();

		String date1String = couple1.getDate();
		String date2String = couple2.getDate();

		String place1 = couple1.getPlace().toLowerCase();
		String place2 = couple2.getPlace().toLowerCase();

		//PAIRWISE COMPARISON (Simple edit distance)

		float firstNameScoreMen = 1 - (float)LevenshteinDistance.LevenshteinDistance(man1FirstName, man2FirstName)/Math.max(man1FirstName.length(), man2FirstName.length());
		float lastNameScoreMen = 1 - (float)LevenshteinDistance.LevenshteinDistance(man1LastName, man2LastName)/Math.max(man1LastName.length(), man2LastName.length());
		float firstNameScoreWomen = 1 - (float)LevenshteinDistance.LevenshteinDistance(woman1FirstName, woman2FirstName)/Math.max(woman1FirstName.length(), woman2FirstName.length());
		float lastNameScoreWomen = 1 - (float)LevenshteinDistance.LevenshteinDistance(woman1LastName, woman2LastName)/Math.max(woman1LastName.length(), woman2LastName.length());

		//FILTER ON SIMILARITY SCORE
		if (firstNameScoreMen < 0.90 || lastNameScoreMen < 0.90 || firstNameScoreWomen < 0.90 || lastNameScoreWomen < 0.90) {
			//System.out.println("FN men :" + firstNameScoreMen + "LN men: " + lastNameScoreMen + "FN women: " + firstNameScoreWomen + "LN women: " + lastNameScoreWomen);
			return;
		}

		//FILTER ON DATE
		if(!date1String.isEmpty() && !date2String.isEmpty() && date1String.split("-").length == 3 && date2String.split("-").length == 3){
			String year1String = date1String.split("-")[0].replaceAll("[^0-9]", "");
			String year2String = date2String.split("-")[0].replaceAll("[^0-9]", "");
			String month1String = date1String.split("-")[1].replaceAll("[^0-9]", "");
			String month2String = date2String.split("-")[1].replaceAll("[^0-9]", "");
			String day1String = date1String.split("-")[2].replaceAll("[^0-9]", "");
			String day2String = date2String.split("-")[2].replaceAll("[^0-9]", "");


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
					if(deltaDays > 10 * 365){ // A woman cannot have a child before her 12 nor after her 50. So if two births are more than 38 years away it can't be the same couple.
						return;
					}
				} else {
					return;
				}
			} else {
				return;
			}
		} else {
			return;
		}


		//STORE RESULTS
		int geoDistance = PairwiseComparison.geoDistance(place1, place2, pCC);
		if(geoDistance != -1){
			bw.write(";" + couple1.getRecordID() + "," + couple2.getRecordID() + "," + geoDistance + "," + (int)Precision.round((double) geoDistance, -1));
		}
		//bw.write(",(1, " + couple1.getRecordID() + ", 0, " + couple2.getRecordID() + ") \n");

	}

	public static void getDatesStatsMP(CoupleData parents, CoupleData newlyweds, BufferedWriter bw) throws IOException {

		String man1FirstName =  parents.getNames().get(0).toLowerCase();
		String man1LastName = parents.getNames().get(1).toLowerCase();
		String woman1FirstName =  parents.getNames().get(2).toLowerCase();
		String woman1LastName = parents.getNames().get(3).toLowerCase();

		String man2FirstName =  newlyweds.getNames().get(0).toLowerCase();
		String man2LastName = newlyweds.getNames().get(1).toLowerCase();
		String woman2FirstName =  newlyweds.getNames().get(2).toLowerCase();
		String woman2LastName = newlyweds.getNames().get(3).toLowerCase();

		int minYearBirth = 0, maxYearBirth = 0, yearMarriage = 0;
		int deltaMin = -1, deltaMax = -1;

		String date1String = parents.getDate();
		String date2String = newlyweds.getDate();

		if(parents.getPlace() == null || newlyweds.getPlace() == null) return;
		String place1 = parents.getPlace().toLowerCase();
		String place2 = newlyweds.getPlace().toLowerCase();

		//System.out.println(date1String + "  2 " + date2String);

		float placeScore = 1 - (float)LevenshteinDistance.LevenshteinDistance(place1, place2)/Math.max(place1.length(), place2.length());

		if (placeScore < 0.90 || place1.isEmpty() || place2.isEmpty()) {
			//metadata.incrementEditDistanceFilterImpact();
			//System.out.println("FN men :" + firstNameScoreMen + "LN men: " + lastNameScoreMen + "FN women: " + firstNameScoreWomen + "LN women: " + lastNameScoreWomen);
			return;
		}

		//PAIRWISE COMPARISON (Simple edit distance)

		float firstNameScoreMen = 1 - (float)LevenshteinDistance.LevenshteinDistance(man1FirstName, man2FirstName)/Math.max(man1FirstName.length(), man2FirstName.length());
		float lastNameScoreMen = 1 - (float)LevenshteinDistance.LevenshteinDistance(man1LastName, man2LastName)/Math.max(man1LastName.length(), man2LastName.length());
		float firstNameScoreWomen = 1 - (float)LevenshteinDistance.LevenshteinDistance(woman1FirstName, woman2FirstName)/Math.max(woman1FirstName.length(), woman2FirstName.length());
		float lastNameScoreWomen = 1 - (float)LevenshteinDistance.LevenshteinDistance(woman1LastName, woman2LastName)/Math.max(woman1LastName.length(), woman2LastName.length());

		//FILTER ON SIMILARITY SCORE
		if (firstNameScoreMen < 0.90 || lastNameScoreMen < 0.90 || firstNameScoreWomen < 0.90 || lastNameScoreWomen < 0.90) {
			//System.out.println("FN men :" + firstNameScoreMen + "LN men: " + lastNameScoreMen + "FN women: " + firstNameScoreWomen + "LN women: " + lastNameScoreWomen);
			return;
		}

		//FILTER ON DATE
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
					}else{
						deltaMin = minYearBirth - yearMarriage;
						deltaMax = maxYearBirth - yearMarriage;
					} 
				} else return;
			} else return;
		} else return;



		//STORE RESULTS

		//System.out.println("Match found : " + man1FirstName + " " + man1LastName + " and " + woman1FirstName + " " + woman1LastName + " with " + man2FirstName + " " + man2LastName + " and " +  woman2FirstName + " " + woman2LastName+ " Year marriage is: " + yearMarriage + " and min year birth is " + minYearBirth + " and max year birth is " + maxYearBirth);
		bw.write(";" + parents.getRecordID() + "," + newlyweds.getRecordID() + "," + deltaMin + "," + deltaMax);
		//bw.write(",(1, " + couple1.getRecordID() + ", 0, " + couple2.getRecordID() + ") \n");

	}

	public static void getPlacesStatsMP(CoupleData newlyweds, CoupleData parents, BufferedWriter bw, PlaceCoordinatesConverter pCC) throws IOException {

		String man1FirstName =  parents.getNames().get(0).toLowerCase();
		String man1LastName = parents.getNames().get(1).toLowerCase();
		String woman1FirstName =  parents.getNames().get(2).toLowerCase();
		String woman1LastName = parents.getNames().get(3).toLowerCase();

		String man2FirstName =  newlyweds.getNames().get(0).toLowerCase();
		String man2LastName = newlyweds.getNames().get(1).toLowerCase();
		String woman2FirstName =  newlyweds.getNames().get(2).toLowerCase();
		String woman2LastName = newlyweds.getNames().get(3).toLowerCase();

		int minYearBirth = 0, maxYearBirth = 0, yearMarriage = 0;

		String date1String = parents.getDate();
		String date2String = newlyweds.getDate();

		if(parents.getPlace() == null || newlyweds.getPlace() == null) return;
		String place1 = newlyweds.getPlace().toLowerCase();
		String place2 = parents.getPlace().toLowerCase();

		//PAIRWISE COMPARISON (Simple edit distance)

		float firstNameScoreMen = 1 - (float)LevenshteinDistance.LevenshteinDistance(man1FirstName, man2FirstName)/Math.max(man1FirstName.length(), man2FirstName.length());
		float lastNameScoreMen = 1 - (float)LevenshteinDistance.LevenshteinDistance(man1LastName, man2LastName)/Math.max(man1LastName.length(), man2LastName.length());
		float firstNameScoreWomen = 1 - (float)LevenshteinDistance.LevenshteinDistance(woman1FirstName, woman2FirstName)/Math.max(woman1FirstName.length(), woman2FirstName.length());
		float lastNameScoreWomen = 1 - (float)LevenshteinDistance.LevenshteinDistance(woman1LastName, woman2LastName)/Math.max(woman1LastName.length(), woman2LastName.length());

		//FILTER ON SIMILARITY SCORE
		if (firstNameScoreMen < 0.90 || lastNameScoreMen < 0.90 || firstNameScoreWomen < 0.90 || lastNameScoreWomen < 0.90) {
			//System.out.println("FN men :" + firstNameScoreMen + "LN men: " + lastNameScoreMen + "FN women: " + firstNameScoreWomen + "LN women: " + lastNameScoreWomen);
			return;
		}

		//FILTER ON DATE
		if(!date1String.isEmpty() && !date2String.isEmpty()){
			String minYearBirthString = date1String.split(";")[0].replaceAll("[^0-9]", "");
			String maxYearBirthString = date1String.split(";")[1].replaceAll("[^0-9]", "");
			String yearMarriageString = date2String.split("-")[0].replaceAll("[^0-9]", "");

			//System.out.println("min: " + minYearBirthString + " ;max: " +maxYearBirthString + " ; marriage: " + yearMarriageString);

			if(!minYearBirthString.isEmpty() && !maxYearBirthString.isEmpty() && !yearMarriageString.isEmpty()){
				minYearBirth = Integer.parseInt(minYearBirthString);
				maxYearBirth = Integer.parseInt(maxYearBirthString);
				yearMarriage = Integer.parseInt(yearMarriageString);

				//System.out.println("min: " + minYearBirth + " ;max: " + maxYearBirth + " ; marriage: " + yearMarriage);

				if (!(minYearBirth < 1550 || maxYearBirth < 1550 || minYearBirth > 1850 || maxYearBirth > 1850 || yearMarriage < 1550 || yearMarriage > 1850)){

					if(minYearBirth < yearMarriage || maxYearBirth > yearMarriage + 30){ //Birth should take place after marriage. Also, last birth should not take place too long after marriage.
						return;
					}
				} else return;
			} else return;
		} else return;
	


		//STORE RESULTS
		int geoDistance = PairwiseComparison.geoDistance(place1, place2, pCC);
		if(geoDistance != -1){
			bw.write(";" + parents.getRecordID() + "," + newlyweds.getRecordID() + "," + geoDistance + "," + (int)Precision.round((double) geoDistance, -1));
		}

	}

	public static void getDatesStatsBMP(PersonData child, PersonData parent, BufferedWriter bw, PlaceCoordinatesConverter pCC) throws IOException {
		
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
		//String parentPlaceOfBirth = parent.getPlaceOfBirth().toLowerCase();
		String childPlace = child.getPlace().toLowerCase();
		String parentPlace = parent.getPlace().toLowerCase();
		
		//FILTER ON BIRTHPLACE (discarded: redundant with filter on place)
		//if(parentPlaceOfBirth == null || parentPlaceOfBirth.isEmpty() || PairwiseComparison.geoDistance(childPlace, parentPlaceOfBirth.toLowerCase(), pCC) > 5) return;
		
		//FILTER ON GENDER (If available)
		if(childGender != 'u' && childGender != parentGender){
			//System.out.println("Gender Impact: " + childGender + " " + parentGender);
			return;
		}

		//FILTER ON DATE (Even though we are looking for similarity stats on dates, we still force biologically possible dates for matches)
		if (parentYear < 1550 || childYear < 1550 || parentYear > 1850 || childYear > 1850 || parent.getMaxYear() < 1550 || parent.getMaxYear() > 1850) return;
		if (parentYear < childYear + 12) {
			return;
		}
		if (parentGender == 'v' && parent.getMaxYear() > childYear + 60){
			return;
		}
		if (parentGender == 'm' && parent.getMaxYear() > childYear + 100){
			return;
		}
		
		//FILTER ON PLACE
		
		//float placeScore = 1 - (float)LevenshteinDistance.LevenshteinDistance(childPlace, parentPlace)/Math.max(childPlace.length(), parentPlace.length());
		if (PairwiseComparison.geoDistance(childPlace, parentPlace, pCC) > 30 || childPlace.isEmpty() || parentPlace.isEmpty()) {
			//System.out.println("Places Impact: " + childPlace + " " + parentPlace);
			return;
		} 

		//PAIRWISE COMPARISON (Simple edit distance)

		float firstNameScore = 1 - (float)LevenshteinDistance.LevenshteinDistance(childFirstName, parentFirstName)/Math.max(childFirstName.length(), parentFirstName.length());
		float lastNameScore = 1 - (float)LevenshteinDistance.LevenshteinDistance(childLastName, parentLastName)/Math.max(childLastName.length(), parentLastName.length());
		
		//FILTER ON NAMES
		if(firstNameScore < 0.90 || lastNameScore < 0.90){
			return;
		}
		if(!childPat.isEmpty() && !parentPat.isEmpty()){
			float patScore = 1 - (float)LevenshteinDistance.LevenshteinDistance(childPat, parentPat)/Math.max(childPat.length(), parentPat.length());
			if(patScore < 0.90){
				return;
			}
		}
		
		//The two records are matching, we can save delta year for stats computation
		int deltaYear = parentYear - childYear;
		//System.out.println("ParentYear = " + parentYear + " , childYear = " + childYear + " , deltayear = " + deltaYear + " , parent gender = " + parentGender);
		bw.write(";" + child.getRecordID() + "," + parent.getRecordID() + "," + deltaYear+ "," + parentGender);
		
	}
	
	public static void getPlacesStatsBMP(PersonData child, PersonData parent, BufferedWriter bw, PlaceCoordinatesConverter pCC) throws IOException {
		
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
		String childPlace = child.getPlace().toLowerCase();
		String parentPlace = parent.getPlace().toLowerCase();
		
		//FILTER ON BIRTHPLACE (discarded: introduces a bias)
		//if(parentPlaceOfBirth == null || parentPlaceOfBirth.isEmpty() || PairwiseComparison.geoDistance(childPlace, parentPlaceOfBirth.toLowerCase(), pCC) > 5) return;
		
		//FILTER ON GENDER (If available)
		if(childGender != 'u' && childGender != parentGender){
			return;
		}

		//FILTER ON DATE (Even though we are looking for similarity stats on dates, we still force biologically possible dates for matches)
		if (parentYear < 1550 || childYear < 1550 || parentYear > 1850 || childYear > 1850 || parent.getMaxYear() < 1550 || parent.getMaxYear() > 1850) return;
		if (parentYear < childYear + 12) {
			return;
		}
		if (parentGender == 'v' && parent.getMaxYear() > childYear + 40){
			return;
		}
		if (parentGender == 'm' && parent.getMaxYear() > childYear + 60){
			return;
		}

		//PAIRWISE COMPARISON (Simple edit distance)

		float firstNameScore = 1 - (float)LevenshteinDistance.LevenshteinDistance(childFirstName, parentFirstName)/Math.max(childFirstName.length(), parentFirstName.length());
		float lastNameScore = 1 - (float)LevenshteinDistance.LevenshteinDistance(childLastName, parentLastName)/Math.max(childLastName.length(), parentLastName.length());
		
		//FILTER ON NAMES
		if(firstNameScore < 0.90 || lastNameScore < 0.90){
			return;
		}
		if(!childPat.isEmpty() && !parentPat.isEmpty()){
			float patScore = 1 - (float)LevenshteinDistance.LevenshteinDistance(childPat, parentPat)/Math.max(childPat.length(), parentPat.length());
			if(patScore < 0.90){
				return;
			}
		}
		
		
		//STORE RESULTS
		int geoDistance = PairwiseComparison.geoDistance(childPlace, parentPlace, pCC);
		if(geoDistance != -1){
			bw.write(";" + child.getRecordID() + "," + parent.getRecordID() + "," + geoDistance + "," + (int)Precision.round((double) geoDistance, -1) + "," + parentGender);
		}
		
	}
}
