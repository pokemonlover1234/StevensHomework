
public class Frequency {
	 int[] arr;
	 
	 public Frequency(int[] arr) {
		 int length = arr.length;
		 this.arr = new int[length];
		 for (int i = 0; i < length; i++) {
			 this.arr[i] = arr[i];
		 }
	 }
	 public int countOf(int num) {
		 int count = 0;
		 for (int i = 0; i < arr.length; i++) {
			 if(num == arr[i]) {
				 count++;
			 }
		 }
		 return count;
	 }
	 
	 public static void main(String[] args) {
		 int[] nums = {1,2,1,1,2,3,4,3,4,4};
		 Frequency stuff = new Frequency(nums); 
		 System.out.println(stuff.countOf(1));
		 System.out.println(stuff.countOf(2));
		 System.out.println(stuff.countOf(3));
		 System.out.println(stuff.countOf(4));
	 }
}
