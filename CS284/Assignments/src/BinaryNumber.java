//Aidan Fischer
//I pledge my honor that I have abided by the Stevens Honor System

public class BinaryNumber {
	private int data[];
	private int length;
	//Create an empty BinaryNumber with all zeros
	BinaryNumber(int length){
		if(length<0) {
			throw new IllegalArgumentException("Length of Binary Number must be nonnegative");
		}
		this.length = length;
		this.data = new int[length];
	}
	//Create a new BinaryNumber populated with bits.
	BinaryNumber(String str) {
		this.data = new int[str.length()];
		this.length = str.length();
		for(int i=0;i<str.length();i++) {
			if(!str.substring(i, i+1).equals("1") && !str.substring(i, i+1).equals("0")) {
				System.out.println(str.substring(i,i+1));
				throw new IllegalArgumentException("Binary Number string must contain only 0s and 1s");
			}
			this.data[i] = Character.getNumericValue(str.charAt(i));
		}
	}
	//Public getters
	public int getLength() {
		return this.length;
	}
	public int[] getInnerArray() {
		return this.data.clone();
	}
	//Get a digit from the inner array
	public int getDigit(int index) {
		if(index>=this.length||index<0) {
			throw new IllegalArgumentException("Index out of bounds. Must be greater than or equal to 0 and less than " + this.length);
		}
		return this.data[index];
	}
	//Convert the represented Binary Number to decimal
	public int toDecimal() {
		int dec = 0;
		for(int i=0;i<this.length;i++) {
			dec += Math.pow(2, this.length-i-1)*this.data[i];
		}
		return dec;
	}
	//Prepend zeros to the internal array to allow for operations that go beyond the length of the number
	public void prepend(int amount) {
		if(amount < 0) {
			throw new IllegalArgumentException("Cannot prepend negative amount of 0s");
		}
		int[] newArr = new int[this.length+amount];
		for(int i = 0;i < this.length;i++) {
			newArr[i+amount] = this.data[i];
		}
		this.data = newArr;
		this.length = this.data.length;
	}
	//Implement bitShifting left or right, adding or removing factors of 2
	public void bitShift(int direction, int amount) {
		if(amount <= 0) {
			throw new IllegalArgumentException("In bit shift operation, amount to be shifted must be nonnegative. Object not modified.");
		}
		if(direction == -1) {
			this.prepend(amount);
			for(int i=amount;i<this.length;i++) {
				this.data[i-amount] = this.data[i];
			}
			for(int i = this.length-1;i>this.length-1-amount;i--) {
				this.data[i] = 0;
			}
		}else if(direction == 1) {
			if(amount > this.length) {
				throw new IllegalArgumentException("Cannot bitshift right by more than length of number.");
			}
			int[] newArr = new int[this.length-amount];
			for(int i = 0; i < this.length-amount;i++) {
				newArr[i] = this.data[i];
			}
			this.data = newArr;
			this.length = this.data.length;
		}else {
			throw new IllegalArgumentException("Direction only valid as positive or negative one. Object not modified.");
		}
	}
	//Bitwise-or two BinaryNumbers, ORing each bit and returning the result
	//Same for bwand, which is bitwise and, but AND each bit
	public static int[] bwor(BinaryNumber bn1, BinaryNumber bn2) {
		if(bn1.getLength()!=bn2.getLength()) {
			throw new IllegalArgumentException("Numbers must be of same length.");
		}
		int[] result = new int[bn1.getLength()];
		for(int i = 0; i < bn1.getLength(); i++) {
			result[i] = bn1.getInnerArray()[i]|bn2.getInnerArray()[i];
		}
		return result;
	}
	public static int[] bwand(BinaryNumber bn1, BinaryNumber bn2) {
		if(bn1.getLength()!=bn2.getLength()) {
			throw new IllegalArgumentException("Numbers must be of same length.");
		}
		int[] result = new int[bn1.getLength()];
		for(int i = 0; i < bn1.getLength(); i++) {
			result[i] = bn1.getInnerArray()[i]&bn2.getInnerArray()[i];
		}
		return result;
	}
	//Add a binary number to the current instance and have the current instance store the result.
	public void add(BinaryNumber aBinaryNumber) {
		if(aBinaryNumber.getLength() < this.length) {
			aBinaryNumber.prepend(this.length - aBinaryNumber.getLength());
		}
		if(aBinaryNumber.getLength() > this.length) {
			this.prepend(aBinaryNumber.getLength() - this.length);
		}
		int[] result = new int[this.length];
		int val;
		int carry = 0;
		for(int i = this.length-1; i >= 0; i--) {
			val = carry + aBinaryNumber.getInnerArray()[i] + this.data[i];
			if(val == 0) {
				result[i] = 0;
				carry = 0;
			}else if(val == 1){
				result[i] = 1;
				carry = 0;
			}else if(val == 2) {
				result[i] = 0;
				carry = 1;
			}else if(val == 3) {
				result[i] = 1;
				carry = 1;
			}else {
				throw new IllegalStateException("Impossible overcarry when adding. Perhaps there are some nonbinary digits in the binary (should be impossible). Addition aborted");
			}
		}
		this.data=result;
		if(carry == 1) {
			this.prepend(1);
			this.data[0] = 1;
		}
	}
	public String toString() {
		String str = "";
		for(int i = 0;i<this.length;i++) {
			str += this.data[i];
		}
		return str;
	}
}
