/*******************************************************************************
 * Name        : sieve.cpp
 * Author      : Aidan Fischer
 * Date        : 9/14/2020
 * Description : Sieve of Eratosthenes
 * Pledge      : I pledge my honor that I have abided by the Stevens Honor System.
 ******************************************************************************/
#include <cmath>
#include <iomanip>
#include <iostream>
#include <sstream>

using namespace std;

class PrimesSieve {
public:
    PrimesSieve(int limit);

    ~PrimesSieve() {
        delete [] is_prime_;
    }

    int num_primes() const {
        return num_primes_;
    }

    void display_primes() const;

private:
    // Instance variables
    bool * const is_prime_;
    const int limit_;
    int num_primes_, max_prime_;

    // Method declarations
    int count_num_primes() const;
    void sieve();
    static int num_digits(int num);
};

PrimesSieve::PrimesSieve(int limit) :
        is_prime_{new bool[limit + 1]}, limit_{limit} {
            //Boolean arrays initialize randomly. Need to make sure every
            //entry is true before running the sieve.
            for(int i = 0; i <= limit; ++i){
                is_prime_[i] = true;
            }
    sieve();
}

void PrimesSieve::display_primes() const {
    // Set the max prime width and the number of primes per row accordingly, then
    // Define the output sequence depending on if all the primes can fit on one 
    // line or if multiple lines, and by extension right-alignment, are necessary
    cout << "Number of primes found: " << num_primes() << endl;
    cout << "Primes up to " << limit_ << ":" << endl;
    const int max_prime_width = num_digits(max_prime_),
              primes_per_row = 80 / (max_prime_width + 1);
    if(num_primes() > primes_per_row){
        int current_line_primes = 0;
        for(int i = 2; i <= limit_; i++){
            if(is_prime_[i]){
                if(current_line_primes == 0){
                    cout << setw(max_prime_width) << i;
                } else {
                    cout << setw(max_prime_width + 1) << i;
                }
                current_line_primes++;
                if(current_line_primes == primes_per_row){
                    current_line_primes = 0;
                    cout << endl;
                }
            }
        }
    } else {
        for(int i = 2; i <= limit_; i++){
            if(is_prime_[i]){
                cout << i;
                if(i != max_prime_){
                    cout << " ";
                }
            }
        }
    }
    

}

int PrimesSieve::count_num_primes() const {
    // Start at index 2 because that point represents the value 2 in the sieve.
    // Indexes 0 and 1 represent 0 and 1 and therefore are not prime.
    int count = 0;
    for(int i = 2; i <= limit_; i++){
        if(is_prime_[i]){
            count++;
        }
    }
    return count;
}

void PrimesSieve::sieve() {
    // Run the sieve of eratosthenes, removing all multiples of primes found that
    // have not yet been removed by the factors of previously discovered primes.
    for(int i = 2; i <= sqrt(limit_); ++i){
        if(is_prime_[i]){
            for(int j = pow(i, 2); j <= limit_; j += i){
                is_prime_[j] = false;
            }
        }
    }
    int max_prime = limit_;
    while(!is_prime_[max_prime]){
        max_prime--;
    }
    max_prime_ = max_prime;
    num_primes_ = count_num_primes();
}

int PrimesSieve::num_digits(int num) {
    // Start the count at one (all numbers have at least one digit), then
    // keep dividing by 10 and adding a digit until the number is less than
    // 10.
    int count = 1;
    while(num >= 10){
        count++;
        num /= 10;
    }
    return count;
}

int main() {
    cout << "**************************** " <<  "Sieve of Eratosthenes" <<
            " ****************************" << endl;
    cout << "Search for primes up to: ";
    string limit_str;
    cin >> limit_str;
    int limit;

    // Use stringstream for conversion. Don't forget to #include <sstream>
    istringstream iss(limit_str);

    // Check for error.
    if ( !(iss >> limit) ) {
        cerr << "Error: Input is not an integer." << endl;
        return 1;
    }
    if (limit < 2) {
        cerr << "Error: Input must be an integer >= 2." << endl;
        return 1;
    }

    cout << endl;
    PrimesSieve sieve = PrimesSieve(limit);
    sieve.display_primes();
    return 0;
}
