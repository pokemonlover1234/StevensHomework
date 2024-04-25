import java.util.concurrent.Semaphore

int counter_mice = 0
int counter_cats = 0
Semaphore access_check = new Semaphore(1)
Semaphore counter_access = new Semaphore(1)
Semaphore feeding_lot = new Semaphore(1)

20.times{
    Thread.start{
        while(true){
            access_check.acquire();
            counter_access.acquire();
            if(counter_cats == 0){
                access_check.release();
                feeding_lot.acquire();
                break
            }
            counter_access.release();
            access_check.release();
        }
        counter_mice++;
        counter_access.release();
        counter_access.acquire();
        counter_mice--;
        counter_access.release();
        feeding_lot.release();
    }
}

20.times{
    Thread.start{
        while(true){
            access_check.acquire();
            counter_access.acquire();
            if(counter_mice == 0){
                access_check.release();
                feeding_lot.acquire();
                break
            }
            counter_access.release();
            access_check.release();
        }
        counter_cats++;
        counter_access.release();
        counter_access.acquire();
        counter_cats--;
        counter_access.release();
        feeding_lot.release();
    }
}
