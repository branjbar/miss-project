package automata;


import java.io.BufferedWriter;
import java.io.IOException;

import org.apache.lucene.index.IndexReader;
import org.apache.lucene.index.Term;
import org.apache.lucene.search.AutomatonQuery;
import org.apache.lucene.search.Collector;
import org.apache.lucene.search.SearcherFactory;
import org.apache.lucene.util.automaton.Automaton;
import org.apache.lucene.util.automaton.LevenshteinAutomata;
import org.apache.lucene.util.automaton.Operations;

import data.PersonData;
import data.PlaceCoordinatesConverter;

public class AutomataIndexing {

	private Automaton strUnion;
	private int maxDistance;

	public AutomataIndexing(int maxDistance){
		this.strUnion = null;
		this.maxDistance = maxDistance;
	}

	public void storeRecord(PersonData data) {
		//For each record, we make a levenshtein automaton with max error of 2 for the first name and for the last name. We concatenate both automata.
		//The global automaton is the union of all automata.
		if (this.strUnion == null) {
			this.strUnion = Operations.concatenate(new LevenshteinAutomata(data.getNames().get(0), true).toAutomaton(maxDistance), new LevenshteinAutomata(data.getNames().get(1), true).toAutomaton(maxDistance));
		}
		else {
			this.strUnion = Operations.union(this.strUnion, Operations.concatenate(new LevenshteinAutomata(data.getNames().get(0), true).toAutomaton(maxDistance), new LevenshteinAutomata(data.getNames().get(1), true).toAutomaton(maxDistance)));
		}
	}
	
	//Not working.
	public void findMatches(PersonData data, BufferedWriter bw, int groupID, PlaceCoordinatesConverter pCC){
		Term term = new Term(data.getNames().get(0)+data.getNames().get(1));
		AutomatonQuery query = new AutomatonQuery(term, this.strUnion);
		
		SearcherFactory searcherFactory = new SearcherFactory();
		IndexReader reader = null;
		Collector results = null;
		try {
			searcherFactory.newSearcher(reader).search(query, results);
		} catch (IOException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		}
		System.out.println(results.toString());
	}
}
