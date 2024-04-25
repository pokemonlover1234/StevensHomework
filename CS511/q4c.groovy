/*
Quiz 4C - 6 Oct 2021
Name - Aidan Fischer
No Partner
I pledge my honor that I have abided by the Stevens Honor System.
 */
import java.util.concurrent.Semaphore;



MAX_WEIGHTS = 10;
GYM_CAP = 50;

// // Declare semaphores here
// enter = new Semaphore(50);
// List<Semaphore> apparatus = [... , ..., ..., ...]

Semaphore enter = new Semaphore(GYM_CAP);
List<Semaphore> apparatus = [new Semaphore(1), new Semaphore(1), new Semaphore(1), new Semaphore(1)];
Semaphore weights = new Semaphore(MAX_WEIGHTS);
Semaphore grabWeight = new Semaphore(1);
// Due to how routine

def make_routine(int no_exercises) { // returns a random routine
    Random rand = new Random();
    int size = rand.nextInt(no_exercises);
    routine = [];

    size.times {
	  routine.add(new Tuple(rand.nextInt(4),rand.nextInt(MAX_WEIGHTS-1)+1));
    }
    return routine;
}

200.times {
    int id = it;
    Thread.start {  // Client
        // enter gym
        routine = make_routine(20);
        enter.acquire();
        
	    routine.size().times {
            // complete exercise on machine 
            grabWeight.acquire();
            routine[it][1].times {
                weights.acquire();
            }
            grabWeight.release();
            apparatus[routine[it][0]].acquire();
	        println "[$id] apparatus:"+routine[it][0] + ", weights:"+ routine[it][1];
            apparatus[routine[it][0]].release();
            routine[it][1].times {
                weights.release();
            }
	    }

        enter.release();
    }    
}

return ;
