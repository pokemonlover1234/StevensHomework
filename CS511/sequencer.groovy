
class ThreewaySequencer{
    int state = 1
    
    synchronized first(){
        while(state != 1){
            wait();
        }
        state = 2;
        notifyAll();
    }

    synchronized second(){
        while(state != 2){
            wait();
        }
        state = 3;
        notifyAll();
    }

    synchronized third(){
        while(state != 3){
            wait();
        }
        state = 1;
        notifyAll();
    }
}

tws = new ThreewaySequencer();

80.times{
    Thread.start {
        tws.first();
    }
}
80.times{
    Thread.start {
        tws.second();
    }
}
80.times{
    Thread.start {
        tws.third();
    }
}