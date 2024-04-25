/*
Quiz 5C - 15 Oct 2021

Name1: Aidan Fischer 
Name2: No partner
Pledge: I pledge my honor that I have abided by the Stevens Honor System.

 */
import java.util.concurrent.locks.*;

class PizzaShop {
    int s=0; 
    int l=0; 
    // variables here
    ReentrantLock lock = new ReentrantLock();
    Condition small = lock.newCondition();
    Condition large = lock.newCondition();
    void purchaseLargePizza() {
	lock.lock();
	try {
	    // complete
        while(l == 0 && s <= 1){
            large.await();
        }
        if(l == 0){
            s -= 2;
        }else{
            l--;
        }
        printState("purchase lp")
	} finally {
            lock.unlock();
	}
	
    }

    void purchaseSmallPizza() {
	lock.lock();
	try {
	    // complete
	    while(s == 0){
            small.await();
        }
        s--;
	    printState("purchase sp");
	} finally {
            lock.unlock();
	}
    }

    void bakeSmallPizza() {
	lock.lock();
	try {
	    // complete
	    s++;
        small.signalAll();
        //Because people wanting large pizzas can also purchase small pizzas, signal them too.
        large.signalAll();
	    printState("bake sp");
	} finally {
            lock.unlock();
	}
    }

    void bakeLargePizza() {
	lock.lock();
	try {
	    // complete
	    l++;
        large.signalAll();
	    printState("bake lp");
	} finally {
            lock.unlock();
	}
    }

    
    void printState(String str) {
	lock.lock();
	try {
	    println str+"-> large: "+l+", small: "+s;
	} finally {
            lock.unlock();
	}
    }
}

PizzaShop p = new PizzaShop();


30.times{
    int id = it;
    Thread.start { // Passenger Train going South
	p.purchaseLargePizza();
    }
}

10.times{
    int id = it;
    sleep(100);
    Thread.start { // Passenger Train going South
	p.purchaseSmallPizza();
    }
}

Thread.start { // Baker
    Random r = new Random();
    70.times {
	sleep(10);
	if (r.nextInt(2)==0) {
	    p.bakeSmallPizza();
    } else {
	    p.bakeLargePizza();
	}
    }
}


