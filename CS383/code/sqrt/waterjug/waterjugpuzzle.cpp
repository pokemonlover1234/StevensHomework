/*******************************************************************************
 * Name        : waterjugpuzzle.cpp
 * Author      : Aidan Fischer
 * Date        : October 6th, 2020
 * Description : Solves generic 3 water jug puzzles with jugs of varying capacity.
 * Pledge      : I pledge my honor that I have abided by the Stevens Honor System.
 ******************************************************************************/

#include <iostream>
#include <sstream>
#include <deque>

using namespace std;

//Note to self, and anyone else who reads this and cares
//My comments and readability whitespace make up a lot of this source file
//Taking those out, I have ~170-180 lines of actual source
//In the lecture, Professor Borowski said a cleverly (I think that was the word?)
//implemented solution would be around 150, so I think I did well, at least in that
//regard. (The passing test script and valgrind tests I ran seem to agree with that assessment.)
//Will my grade tho? Guess I'll find out!

// Struct to represent state of water in the jugs.
// From provided state.cpp
struct State {
    int a, b, c;
    string directions;
    State *parent;
    State(int _a, int _b, int _c, string _directions) : 
        a{_a}, b{_b}, c{_c}, directions{_directions}, parent{nullptr} { }
    
    // String representation of state in tuple form.
    string to_string() {
        ostringstream oss;
        oss << "(" << a << ", " << b << ", " << c << ")";
        return oss.str();
    }
};

//Generalized input assigner, taking necessary values as input for that generalization. t
//is the type of the input, whether it be a goal or a capacity
bool assign_input(int &assigner, char * const value, string name, string t, bool printerr){
    istringstream iss(value);
    
    if(!(iss >> assigner)){
        //We only want to output an error for the first problem.
        if(printerr){
            cerr << "Error: Invalid " << t << " '" << value << "' for jug " << name << "." << endl;
        }
        return false;
    }

    if((assigner <= 0 && t == "capacity") || (assigner < 0 && t == "goal")){
        if(printerr){
            cerr << "Error: Invalid " << t << " '" << value << "' for jug " << name << "." << endl;
        }
        return false;
    }

    return true;
}

bool validate_capacity(string name, int cap, int goal, bool printerr){
    //Goal cannot exceed the capacity of the jug.
    if(goal > cap){
        if(printerr){
            cerr << "Error: Goal cannot exceed capacity of jug " << name << "." << endl;
        }
        return false;
    }
    return true;
}

void pour(bool **seen_states, deque <State*> &bfs_queue, int step, State *process, State goal, int ca, int cb, int cc, bool &solfound, deque <State*> &cleanup_queue){
    //A generalized pour function, to prevent duplication of code.
    //Step is the step we are processing from the order in the next comment block, indexed from 0

    //Processing in order:
    //Pour C->A
    //Pour B->A
    //Pour C->B
    //Pour A->B
    //Pour B->C
    //Pour A->C

    //For each of these, we need to pour from the source until it is empty, or the target is full.
    //We also cannot pour if the source is empty and/or the target is full.

    //If we can pour, then we do so by creating a new state that represents the result of the pour, 
    //with "process" as parent and the direction as directions, and check if it's the solution. If it 
    //is, return it. If it isn't, add it to the stack and seen_states.

    //General pour result: x is current jug, y is other.
    //Untouched jug: x.val -> x.val
    //Source jug: x.val -> max(0, x.val-(y.cap-y.val)), y is target
    //Above empties x until either y is full or x is empty. y.cap-y.val is the empty space in y.
    //Target jug: x.val -> min(x.cap,x.val+y.val), y is source.
    //Fill x until it is full or y becomes empty.
    //Proof by exhaustion this always works

    //Possibility 1: Source fills target to capacity
    //Source change
    //x.val -> max(0, x.val-(y.cap-y.val)) 
    //If source has enough to fill target, then x.val-(y.cap-y.val) >= 0, so x.val -> x.val-(y.cap-y.val), the expected result.
    //Target change
    //x.val -> min(x.cap, x.val+y.val)
    //If target was filled to capacity, we know x.val+y.val >= x.cap, so x.val -> x.cap, the expected result.

    //Possibility 2: Source doesn't fill target
    //Source change
    //x.val -> max(0, x.val-(y.cap-y.val))
    //If source doesn't have enough to fill target, x.val-(y.cap-y.val) < 0, therefore x.val -> 0, the expected result.
    //Target change
    //x.val -> min(x.cap, x.val+y.val)
    //If source doesn't have enough to fill target, x.val+y.val < x.cap, therefore x.val -> x.val + y.val, the expected result.

    //A map of step to respective indexes for u,s,t -> a,b,c
    //Each entry is {index of untouched in abc, index of source in abc, index of target in abc}
    int map [6][3] = {{1,2,0},{2,1,0},{0,2,1},{2,0,1},{0,1,2},{1,0,2}};

    //List of current values.
    int abc [3] = {process->a, process->b, process->c};

    //u = untouched, s=source, t=target
    int ust [3];

    //List of capacities.
    int cap [3] = {ca, cb, cc};

    //List of letters, for use with directions construction.
    char letters [3] = {'A','B','C'};

    //x, y = What we are changing, what it depends on. 
    //xcap, ycap = the capacities.
    int x, y, xcap, ycap;
    //Make sure you can actually pour!!
    if(abc[map[step][1]] == 0 || abc[map[step][2]] == cap[map[step][2]]){
        return;
    }

    //The actually pouring operation.

    //Set untouched's new value
    ust[0] = abc[map[step][0]];
    //Set source's new value. x=source, y=target
    x = abc[map[step][1]];
    y = abc[map[step][2]];
    ycap = cap[map[step][2]];
    ust[1] = max(0,x-(ycap-y));
    //Set target's new value. x=target, y=source
    x = abc[map[step][2]];
    y = abc[map[step][1]];
    xcap = cap[map[step][2]];
    ust[2] = min(xcap,x+y);

    //We also need to construct the directions.
    string gallons = " gallon";
    if(ust[2] - abc[map[step][2]] > 1) gallons += "s";
    string directions = "Pour " + to_string(ust[2] - abc[map[step][2]]) + gallons + " from " + letters[map[step][1]] + " to " +
                        letters[map[step][2]] + ". ";

    //Create the new state, check if solution, etc.
    //First, update abc with new values.

    abc[map[step][0]] = ust[0];
    abc[map[step][1]] = ust[1];
    abc[map[step][2]] = ust[2];

    //Now, make the state
    State *new_state = new State(abc[0],abc[1],abc[2],directions);
    new_state->parent = process;
    //Check if it's the solution
    if(new_state->to_string() == goal.to_string()){
        //If it is, set the solution found flag.
        solfound = true;
        //Add it to the queue, so get_solution can find it.
        bfs_queue.push_back(new_state);
        cleanup_queue.push_back(new_state);
        return;
    //Otherwise add it to the queue and seen_states, unless it's already been seen. If it has, clean it up.
    } else {
        if(seen_states[abc[0]][abc[1]]){
            delete new_state;
            return;
        }
        seen_states[abc[0]][abc[1]] = true;
        bfs_queue.push_back(new_state);
        cleanup_queue.push_back(new_state);
        return;
    }
}

State get_solution(bool **seen_states, deque <State*> bfs_queue, int ca, int cb, int cc, int ga, int gb, int gc, deque <State*> &cleanup_queue){
    State goal(ga, gb, gc, "Goal State");
    bool solfound = false;
    solfound = goal.to_string() == bfs_queue.front()->to_string();
    
    while(!bfs_queue.empty()){
        State * process = bfs_queue.front();
        bfs_queue.pop_front();
        //Begin the algorithm. Note that if the solution is found, it won't process further steps.
        //If it did, the queue won't have the solution as it's last entry.

        //pour is implemented above. It's a clever method of deduplicating the pouring code.
        if(!solfound) pour(seen_states, bfs_queue, 0, process, goal, ca, cb, cc, solfound, cleanup_queue);
        if(!solfound) pour(seen_states, bfs_queue, 1, process, goal, ca, cb, cc, solfound, cleanup_queue);
        if(!solfound) pour(seen_states, bfs_queue, 2, process, goal, ca, cb, cc, solfound, cleanup_queue);
        if(!solfound) pour(seen_states, bfs_queue, 3, process, goal, ca, cb, cc, solfound, cleanup_queue);
        if(!solfound) pour(seen_states, bfs_queue, 4, process, goal, ca, cb, cc, solfound, cleanup_queue);
        if(!solfound) pour(seen_states, bfs_queue, 5, process, goal, ca, cb, cc, solfound, cleanup_queue);
        if(solfound){
            return *bfs_queue.back();
        }
    }
    State nosol(-1,-1,-1,"NOSOL");
    return nosol;
}

int main(int argc, char * const argv[]) {
    int ca, cb, cc, ga, gb, gc;

    if(argc != 7){
        cerr << "Usage: " << argv[0] << " <cap A> <cap B> <cap C> <goal A> <goal B> <goal C>" << endl;
        return 1;
    }

    //Run the assignment function on all inputs, and assign the proper values if validation passes
    bool printerr = true;
    printerr &= assign_input(ca, argv[1], "A", "capacity", printerr);
    printerr &= assign_input(cb, argv[2], "B", "capacity", printerr);
    printerr &= assign_input(cc, argv[3], "C", "capacity", printerr);
    printerr &= assign_input(ga, argv[4], "A", "goal", printerr);
    printerr &= assign_input(gb, argv[5], "B", "goal", printerr);
    printerr &= assign_input(gc, argv[6], "C", "goal", printerr);

    if(!printerr){
        return 1;
    }

    //Confirm goals do not exceed capacities.
    printerr = true;
    printerr &= validate_capacity("A", ca, ga, printerr);
    printerr &= validate_capacity("B", cb, gb, printerr);
    printerr &= validate_capacity("C", cc, gc, printerr);

    if(!printerr){
        return 1;
    }

    if(cc != ga + gb + gc){
        cerr << "Error: Total gallons in goal state must be equal to the capacity of jug C." << endl;
        return 1;
    }

    //If the input is valid, define the array that will store whether we've seen a state or not.
    //The number of rows should be ca + 1, number of columns be cb + 1

    bool **seen_states = new bool*[ca + 1];

    for(int i = 0; i < ca + 1; ++i){
        seen_states[i] = new bool[cb + 1];
        fill(seen_states[i], seen_states[i] + cb + 1, false);
    }

    //Define the queue to be used in BFS.

    deque <State*> *bfs_queue = new deque<State*>();

    //Define a queue to handle final cleanup of States.

    deque <State*> *cleanup_queue = new deque<State*>();

    //Define the initial state, and put it on the queue, and put it in seen_states.

    State *start_state = new State(0, 0, cc, "Initial state. ");

    seen_states[0][0] = true;

    bfs_queue->push_back(start_state);
    cleanup_queue->push_back(start_state);

    //Solve the puzzle.

    State end_state = get_solution(seen_states, *bfs_queue, ca, cb, cc, ga, gb, gc, *cleanup_queue);

    //Print the solution

    deque <State> *res_queue = new deque<State>();

    if(end_state.directions == "NOSOL"){
        //No solution
        cout << "No solution." << endl;
    } else {
        res_queue->push_back(end_state);
        while(end_state.parent != nullptr){
            end_state = *end_state.parent;
            res_queue->push_back(end_state);
        }
    }

    while(!res_queue->empty()){
        State cur = res_queue->back();
        res_queue->pop_back();
        cout << cur.directions << cur.to_string() << endl;
    }

    //Clean up the heap.

    for(int i = 0; i < ca + 1; ++i){
        delete [] seen_states[i];
    }

    while(!cleanup_queue->empty()){
        delete cleanup_queue->front();
        cleanup_queue->pop_front();
    }

    delete [] seen_states;
    delete bfs_queue;
    delete res_queue;
    delete cleanup_queue;

    return 0;
}
