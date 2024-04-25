import java.util.Arrays;
import java.util.List;
import java.util.ArrayList;
import java.util.Random;

public class Customer implements Runnable {
    private Bakery bakery;
    private Random rnd;
    private List<BreadType> shoppingCart;
    private int shopTime;
    private int checkoutTime;

    /**
     * Initialize a customer object and randomize its shopping cart
     */
    public Customer(Bakery bakery) {
        this.bakery = bakery;
        this.rnd = new Random();
        this.shoppingCart = new ArrayList<BreadType>();
        this.shopTime = rnd.nextInt(1250) + 250;
        this.checkoutTime = rnd.nextInt(500) + 250;
    }

    /**
     * Run tasks for the customer
     */
    public void run(){
        try {
            System.out.println("Customer " + hashCode() + " has started shopping.");
            this.fillShoppingCart();
            System.out.println("Customer " + hashCode() + " is checking out.");
            bakery.cashiers.acquire();
            Thread.sleep(this.checkoutTime);
            bakery.salesAccess.acquire();
            bakery.addSales(this.getItemsValue());
            bakery.salesAccess.release(); 
            bakery.cashiers.release();
            System.out.println("Customer " + hashCode() + " is finished shopping.");
        } catch(InterruptedException ie){
            ie.printStackTrace();
        }
    }

    /**
     * Return a string representation of the customer
     */
    public String toString() {
        return "Customer " + hashCode() + ": shoppingCart=" + Arrays.toString(shoppingCart.toArray()) + ", shopTime=" + shopTime + ", checkoutTime=" + checkoutTime;
    }

    /**
     * Add a bread item to the customer's shopping cart
     */
    private boolean addItem(BreadType bread) {
        // do not allow more than 3 items, chooseItems() does not call more than 3 times
        if (shoppingCart.size() >= 3) {
            return false;
        }
        System.out.println("Customer " + hashCode() + " is taking " + bread.toString().toLowerCase() +  " from stock.");
        try {
            Thread.sleep(this.shopTime);
        } catch (InterruptedException ie) {
            ie.printStackTrace();
        }
        bakery.takeBread(bread);
        shoppingCart.add(bread);
        return true;
    }

    /**
     * Fill the customer's shopping cart with 1 to 3 random breads
     */
    private void fillShoppingCart() throws InterruptedException {
        int itemCnt = 1 + rnd.nextInt(3);
        while (itemCnt > 0) {
            int chosenBread = rnd.nextInt(BreadType.values().length);
            bakery.shelfAccess[chosenBread].acquire();
            addItem(BreadType.values()[chosenBread]);
            bakery.shelfAccess[chosenBread].release();
            itemCnt--;
        }
    }

    /**
     * Calculate the total value of the items in the customer's shopping cart
     */
    private float getItemsValue() {
        float value = 0;
        for (BreadType bread : shoppingCart) {
            value += bread.getPrice();
        }
        return value;
    }
}