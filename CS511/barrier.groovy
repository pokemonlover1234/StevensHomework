class AutoResetBarrier {
    int waiting = 0;
    int threads;
    Barrier(int threads){
        this.threads = threads;
    }

    synchronized void waitAtBarrier(){
        waiting++;
        if(waiting == threads){
            System.out.println("Notifying all");
            notifyAll();
            waiting = 0;
        } else{
            System.out.println(waiting + " waiting.")
            wait();
        }
    }
}

Barrier barrier = new Barrier(10);

100.times{
    Thread.start {
        barrier.waitAtBarrier();
    }
}