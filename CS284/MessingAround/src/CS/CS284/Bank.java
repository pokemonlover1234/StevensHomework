package CS.CS284;

public class Bank {
	private double balance;
	public Bank(double balance){
		this.balance = balance;
	}
	public Bank() {
		this.balance = 0;
	}
	
	public static void main(String[] args) {
		Bank testBank = new Bank(15);
		System.out.println(testBank);
		testBank.deposit(10);
		System.out.println(testBank);
		testBank.withdraw(20);
		System.out.println(testBank);
	}
	public void setBalance(double balance) {
		this.balance = balance;
	}
	public double getBalance() {
		return this.balance;
	}
	public String toString() {
		return "Bal: " + this.balance;
	}
	public void deposit(double amount) {
		this.balance += amount;
	}
	public void withdraw(double amount) {
		if(this.balance < amount) {
			System.out.println("Insufficient funds to withdraw");
		}else {
			this.balance -= amount;
		}
	}
}

