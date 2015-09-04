package indexing;

import java.util.ArrayList;
import java.util.List;

import data.Record;

//BitVector built from a record.
public class BitVector {
	private List<Boolean> vector;

	public BitVector(Record data){
		List<String> inputString = new ArrayList<String>();
		inputString.add(data.getFirstName().toLowerCase());
		inputString.add(data.getLastName().toLowerCase());
		this.vector = new ArrayList<Boolean>();

		//Building the vector: it will be the concatenation of first name's subvector and last name's subvector.
		for(String name:inputString){ //The letter-vector position was hardcoded. It is taken from Marijn's paper. He devised it using simulated annealing.

			//Pos 0: E or G
			if (name.matches(".*g.*|.*e.*")) this.vector.add(true); else this.vector.add(false);

			//Pos 1: A or L or Q or H or J or X or ,
			if (name.matches(".*a.*|.*l.*|.*q.*|.*h.*|.*j.*|.*x.*|.*,.*")) this.vector.add(true); else this.vector.add(false);

			//Pos 2: R or P or V
			if (name.matches(".*r.*|.*p.*|.*v.*")) this.vector.add(true); else this.vector.add(false);

			//Pos 3: N or space
			if (name.matches(".*n.*|.*\\s.*")) this.vector.add(true); else this.vector.add(false);

			//Pos 4: I or U or W
			if (name.matches(".*i.*|.*u.*|.*w.*")) this.vector.add(true); else this.vector.add(false);

			//Pos 5: D or F or C or M or Z
			if (name.matches(".*d.*|.*f.*|.*c.*|.*m.*|.*z.*")) this.vector.add(true); else this.vector.add(false);

			//Pos 6: T or S or Y
			if (name.matches(".*t.*|.*s.*|.*y.*")) this.vector.add(true); else this.vector.add(false);

			//Pos 7: O or B or K or other
			if (name.matches(".*o.*|.*b.*|.*k.*")) this.vector.add(true); else this.vector.add(false); 
		}
	}

	public Boolean get(int i) {
		return this.vector.get(i);
	}

	public int size() {
		return this.vector.size();
	}

	public void display() {
		System.out.println(this.vector);

	}
}