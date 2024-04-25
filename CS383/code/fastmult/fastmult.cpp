/*******************************************************************************
 * Name          : fastmult.cpp
 * Author        : Aidan Fischer
 * Pledge        : I pledge my honor that I have abided by the Stevens Honor System.
 * Date          : November 16, 2020
 * Description   : Implements the Fast Multiplication algorithm.
 ******************************************************************************/

//My own timings:
//1000x1000 (suggested test case): ~0.145 - 0.16s
//50000x50000 (maximum input size): ~70 - 80s

#include <iostream>
#include <utility>
#include <cmath>
#include <unordered_map>
#include <algorithm>

using namespace std;

pair<string, string> prepad(const string& a, const string& b);
string unpad(const string& a);
string add(const string& a, const string& b);
string subtract(const string& a, const string& b);
string multiply(const string& a, const string& b);

inline pair<string, string> prepad(const string& a, const string& b){
    string tempa = a;
    string tempb = b;
    size_t sizea = tempa.size();
    size_t sizeb = tempb.size();
    //Pad to same length
    if(sizea < sizeb){
        tempa = string(sizeb - sizea, '0') + tempa;
        sizea = sizeb;
    }else{
        tempb = string(sizea - sizeb, '0') + tempb;
        sizeb = sizea;
    }

    //Pad to power of 2;
    int required_zeros = pow(2,ceil(log(sizea)/log(2))) - sizea;
    return pair<string, string>(string(required_zeros,'0') + tempa, string(required_zeros,'0') + tempb);
}

inline string unpad(const string& a){
    //Unpad leading 0s,.
    string temp = a;
    int index = 0;
    while(temp[index] == '0'){
        ++index;
    }
    temp = temp.substr(index);
    return temp == "" ? "0" : temp;
}

string add(const string& a, const string& b){
    //Need to add from right to left.
    //This function works even if they aren't the same length.
    //Allows negative numbers.
    if(a[0] == '-' || b[0] == '-'){
        if(a[0] == '-' && b[0] == '-'){
            return "-" + add(a.substr(1),b.substr(1));
        }else if(a[0] == '-'){
            return subtract(b,a.substr(1));
        }else if(b[0] == '-'){
            return subtract(a,b.substr(1));
        }
    }

    auto ait = a.crbegin();
    auto bit = b.crbegin();
    string res = "";
    char carry = '0';
    while(ait != a.crend() || bit != b.crend()){
        char sum = ((ait != a.crend() ? *ait : '0') + (bit != b.crend() ? *bit : '0') - '`' + carry); //` is 96 in ASCII, which is 2 * 48 = 2 * '0'
        bool sumover = sum > 57;
        carry = sumover ? '1' : '0';
        res += (char)(sumover ? sum - 10 : sum);
        if(ait != a.crend()){
            ++ait;
        }
        if(bit != b.crend()){
            ++bit;
        }
    }
    if(carry == '1'){
        res += carry;
    }
    reverse(res.begin(), res.end());
    return res;
}

string subtract(const string& a, const string& b){
    //This is a bit more complicated than addition, because we may need to carry multiple times (i.e. 1000 - 1).
    //Allows negative numbers.
    if(a[0] == '-' || b[0] == '-'){
        if(a[0] == '-' && b[0] == '-'){
            return subtract(b.substr(1), a.substr(1));
        }else if(a[0] == '-'){
            return "-" + add(a.substr(1),b);
        }else if(b[0] == '-'){
            return add(a,b.substr(1));
        }
    }

    auto ait = a.crbegin();
    auto bit = b.crbegin();
    string res = "";
    char carry = '0';
    while(ait != a.crend() || bit != b.crend()){
        char currenta = ait != a.crend() ? *ait : '0';
        //If carry is '1', that means the previous step needed a carry.
        char innera = carry == '1' ? (currenta != '0' ? currenta - 1 : '9') : currenta;
        char innerb = bit != b.crend() ? *bit : '0';

        //If the carry needs to be "forwarded", that is, if it needs to be taken from a further place value, as in 1000-1
        carry = carry == '1' ? (currenta == '0' ? '1' : '0') : '0';

        char difference = (innera - innerb + '0');

        if(difference < 48){
            carry = '1';
            //Add the carry in. For example, 4 - 8 -> 52 - 56 + 48 = 52 - 8 = 44 -> 44 + 10 = 54 -> 6
            difference += 10;
        }

        res += difference;
        if(ait != a.crend()){
            ++ait;
        }
        if(bit != b.crend()){
            ++bit;
        }
    }

    if(carry == '1'){
        return "-" + subtract(b, a);
    }

    reverse(res.begin(), res.end());
    return res;
}

string multiply(const string& a, const string& b){
    //Base case
    if(a.size() <= 2 && b.size() <= 2){
        if(a.size() == 1 && b.size() == 1){
            return to_string((a[0]-'0')*(b[0]-'0'));
        }else if(a.size() == 2 && b.size() == 1 && a[0] == '-'){
            return "-" + to_string((a[1]-'0')*(b[0]-'0'));;
        }else if(a.size() == 1 && b.size() == 2 && b[0] == '-'){
            return "-" + to_string((a[0]-'0')*(b[1]-'0'));
        }else if(a.size() == 2 && b.size() == 2 && a[0] == '-' && b[0] == '-'){
            return to_string((a[1]-'0')*(b[1]-'0'));
        }
    }
    string newa, newb;

    //Make a and b the same length
    if(a.size()!=b.size()){
        pair<string,string> padded = prepad(a, b);
        newa = padded.first;
        newb = padded.second;
    } else {
        newa = a;
        newb = b;
    }

    //Round the split length up so we don't end up with empty strings that'll result in segmentation faults. Strings of length 1 would result in empty strings still,
    //but strings of length 1 are taken care of in the base case, and if either is greater than length 1, then they are made to be the same length (of greater tham 1)
    //above.
    int split_length = ceil((double)newa.size()/2);

    string a1 = newa.substr(0,split_length);
    string a0 = newa.substr(split_length);
    string b1 = newb.substr(0,split_length);
    string b0 = newb.substr(split_length);

    string c2 = multiply(a1, b1);
    string c0 = multiply(a0, b0);
    string c1 = subtract(multiply(add(a1, a0), add(b1, b0)), add(c2, c0));

    //Handle the "multiplication" by a power of 10 necessary for c2 and c1. Since we aren't requiring the strings be a length of a power of 2, then a1/b1 and a0/b0 might
    //have different lengths. However, since we make sure they are equal length, they are off by at most one. The lengths of a1 and b1 are equal, and the lengths of a0 and
    //b0 are equal. Therefore, if a1 and a0 are not of equal size, then the power of 10 we must multiply by is reduced by 1. (For c2, since it is mulitplied by that power of 10
    //twice, this reduces it by 2 for c2). We are sure its reduced by one, because the effect of the ceil on the split_length makes sure that a0/b0 are either equal in length to
    //a1/b1 (in which case the reduction by 1 doesn't take effect) or shorter than them by 1 (which means the power of 10 that is on a1/b1 is reduced by 1 because of that).
    string zeros = string(split_length - (a1.size() != a0.size() ? 1 : 0), '0');

    return add(add(c2 + zeros + zeros, c1 + zeros), c0);
}

int main(int argc, char* const argv[]){
    string a, b;
    if(argc != 3){
        cerr << "Usage: " << argv[0] << " <integer> <integer>" << endl;
        return 1;
    }
    a = argv[1];
    b = argv[2];
    string k;
    cout << unpad(multiply(a,b)) << endl;
}

