/*******************************************************************************
 * Name    : sqrt.cpp
 * Author  : Aidan Fischer
 * Version : 1.0
 * Date    : September 2, 2020
 * Description : Computes the sqrt of a number using Newton's method
 * Pledge : I pledge my honor that I have abided by the Stevens Honor System.
 ******************************************************************************/
#include <iostream>
#include <sstream>
#include <limits>
#include <iomanip>

using namespace std;

double sqrt(double num, double epsilon = 1e-7){
    double last_guess = 0;
    double next_guess = num;
    if(num < 0){
        return numeric_limits<double>::quiet_NaN();
    }else if(num == 0 || num == 1){
        return num;
    }else {
        while(abs(last_guess - next_guess) > epsilon){
            last_guess = next_guess;
            next_guess = (last_guess + num/last_guess) / 2;
        }
        return next_guess;
    }
}

int main(int argc, char* const argv[]){
    double num, epsilon;
    istringstream iss;

    if (argc != 2 && argc != 3){
        cerr << "Usage: " << argv[0] << " <value> [epsilon]" 
             << endl;
        return 1;
    }
    iss.str(argv[1]);
    if(!(iss >> num)){
        cerr << "Error: Value argument must be a double." 
             << endl;
        return 1;
    }
    iss.clear();
    if(argc == 3){
        iss.str(argv[2]);
        if(!(iss >> epsilon) || epsilon <= 0){
            cerr << "Error: Epsilon argument must be a positive double."
                 << endl;
            return 1;
        }
        cout << fixed << setprecision(8) << sqrt(num, epsilon) << endl;
        return 0;
    } else {
        cout << fixed << setprecision(8) << sqrt(num) << endl;
        return 0;
    }


}



