import java.util.Map;
import java.util.concurrent.ConcurrentHashMap;
import java.util.concurrent.Executors;
import java.util.concurrent.ExecutorService;
import java.util.concurrent.Semaphore;
import java.util.concurrent.TimeUnit;
import java.util.Random;

public class Bakery implements Runnable {
    private static final int TOTAL_CUSTOMERS = 200;
    private static final int ALLOWED_CUSTOMERS = 50;
    private static final int FULL_BREAD = 20;
    private Map<BreadType, Integer> availableBread;
    private ExecutorService executor;
    private float sales = 0;
    public Semaphore salesAccess;
    public Semaphore[] shelfAccess;
    public Semaphore cashiers;

    /**
     * Remove a loaf from the available breads and restock if necessary
     */
    public void takeBread(BreadType bread) {
        int breadLeft = availableBread.get(bread);
        if (breadLeft > 0) {
            availableBread.put(bread, breadLeft - 1);
        } else {
            System.out.println("No " + bread.toString() + " bread left! Restocking...");
            // restock by preventing access to the bread stand for some time
            try {
                Thread.sleep(1000);
            } catch (InterruptedException ie) {
                ie.printStackTrace();
            }
            availableBread.put(bread, FULL_BREAD - 1);
        }
    }

    /**
     * Add to the total sales
     */
    public void addSales(float value) {
        sales += value;
    }

    /**
     * Run all customers in a fixed thread pool
     */
    public void run() {
        salesAccess = new Semaphore(1, true);
        shelfAccess = new Semaphore[] {new Semaphore(1, true), new Semaphore(1, true), new Semaphore(1, true)};
        cashiers = new Semaphore(4, true);
        availableBread = new ConcurrentHashMap<BreadType, Integer>();
        availableBread.put(BreadType.RYE, FULL_BREAD);
        availableBread.put(BreadType.SOURDOUGH, FULL_BREAD);
        availableBread.put(BreadType.WONDER, FULL_BREAD);

        ExecutorService executorService = Executors.newFixedThreadPool(ALLOWED_CUSTOMERS);

        Random random = new Random();
        for(int i = 0; i < TOTAL_CUSTOMERS; i++){
            try {
                Thread.sleep(random.nextInt(100));
            } catch (InterruptedException ie) {
                ie.printStackTrace();
            }
            executorService.execute(new Customer(this));
        }

        executorService.shutdown();
        try {
            executorService.awaitTermination(1, TimeUnit.HOURS);
        } catch (InterruptedException ie) {
            ie.printStackTrace();
        }
        System.out.println("Total sales: $" + sales);
    }
}