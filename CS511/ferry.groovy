import java.util.concurrent.Semaphore;

int N = 20;

Semaphore[] permToBoard = [new Semaphore(0), new Semaphore(0)];
permToDisembark = new Semaphore(0);
permToLeave = new Semaphore(0);
permToReboard = new Semaphore(0);

Thread.start {
    int coast=0;
    while(true){
        println("Boarding")
        N.times {permToBoard[coast].release();}
        N.times {permToLeave.acquire();}
        println("Leaving")
        coast = 1 - coast;
        println("Arrived, Disembarking.")
        N.times {permToDisembark.release();}
        N.times {permToReboard.acquire();}
    }
}

100.times {
    Thread.start {
        permToBoard[0].acquire();
        permToLeave.release();
        permToDisembark.acquire();
        permToReboard.release();
    }
}

100.times {
    Thread.start {
        permToBoard[1].acquire();
        permToLeave.release();
        permToDisembark.acquire();
        permToReboard.release();
    }
}

return;