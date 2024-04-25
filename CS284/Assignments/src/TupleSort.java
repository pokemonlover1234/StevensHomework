import java.util.HashMap;

//Name: Aidan Fischer
//Pledge: I pledge my honor that I have abided by the Stevens Honor System
public class TupleSort {

	class Tuple implements Comparable<Tuple> {
		int[] tuple;

		public Tuple(int[] this_tuple) {
			this.tuple = this_tuple;
		}

		@Override
		public int compareTo(Tuple other_tuple) {
			/*
			 * return -1 if this tuple < other tuple return 1 if this tuple > other tuple
			 * return 0 if they are equal
			 */

			int i = 0;

			while (i < tuple.length && i < other_tuple.tuple.length) {
				if (tuple[i] == other_tuple.tuple[i]) {
					i++;
					continue;
				}
				if (tuple[i] > other_tuple.tuple[i]) {
					return 1;
				}
				if (tuple[i] < other_tuple.tuple[i]) {
					return -1;
				}

			}
			if (i == tuple.length && i < other_tuple.tuple.length) {
				return -1;
			} else if (i == other_tuple.tuple.length && i < tuple.length) {
				return 1;
			}

			return 0;
		}

		public String toString() {
			String result = "(";
			for (int i = 0; i < tuple.length; i++) {
				result += tuple[i];
				if (i != tuple.length - 1) {
					result += ",";
				}
			}
			result += ")";
			return result;
		}
	}

	public void insertion_sort(Tuple[] table) {
		for (int pos = 1; pos < table.length; pos++) {
			insertion_step(table, pos, 1);
		}
	}
	
	public void insertion_step(Tuple[] a, int this_idx, int stride) {
		Tuple this_val = a[this_idx];
		while (this_idx >= stride && this_val.compareTo(a[this_idx - stride]) < 0) {
			a[this_idx] = a[this_idx - stride];
			this_idx -= stride;
		}
		a[this_idx] = this_val;
	}

	public Tuple[] tuple_sort(Tuple[] array) {
		Tuple[] sort = array.clone();
		insertion_sort(sort);
		return sort;
	}

	public void print_tuple_array(Tuple[] array) {
		for (int i = 0; i < array.length; i++) {
			System.out.print(array[i]);
			if (i != array.length - 1) {
				System.out.print(", ");
			} else {
				System.out.println("");
			}
		}
	}

	public void test_tuple_sort() {
		TupleSort test = new TupleSort();

		Tuple[] test_tuple = new Tuple[5];
		test_tuple[0] = new Tuple(new int[] { 1, 2 });
		test_tuple[1] = new Tuple(new int[] { 2 });
		test_tuple[2] = new Tuple(new int[] { 1, 1, 1 });
		test_tuple[3] = new Tuple(new int[] { 1, 5, 0, 5 });
		test_tuple[4] = new Tuple(new int[] { 1, 5, -1 });

		System.out.println("Before sorting: ");
		this.print_tuple_array(test_tuple);

		Tuple[] sorted_tuple = this.tuple_sort(test_tuple);

		System.out.println("After sorting: ");
		this.print_tuple_array(sorted_tuple);
	}

	public static void main(String[] args) {
		TupleSort test = new TupleSort();
		test.test_tuple_sort();
	}
}
