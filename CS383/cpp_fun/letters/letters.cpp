#include <vector>
#include <iostream>

using namespace std;

char beginchar = '0';
char endchar = '9';
int len = 8;


//This program will all strings containing chars between beginchar and endchar in lexicographic order, up to and including strings of length len. 
//Does about 16384 - 32768, or 2^14 - 2^15, strings per second on my machine when putting output in a file.

inline bool notallchars(string k, char ch){
    for(auto c : k){
        if(c != ch){
            return true;
        }
    }
    return false;
}

inline string tostring(vector<char>* charlist){
    string res = "";
    for(auto i = charlist->begin(); i != charlist->end(); i++){
        res.push_back(*i);
    }
    return res;
}

inline void reset(vector<char>* charlist){
    for(auto i = charlist->begin(); i != charlist->end(); i++){
        *i = beginchar;
    }
}

int main(){
    vector<char>* charlist = new vector<char>();
    charlist->push_back(beginchar);
    bool increase = true;
    vector<char>::reverse_iterator it;
    for(int i = 1; i <= len; i++){
        while(notallchars(tostring(charlist), endchar)){
            increase = true;
            it = charlist->rbegin();
            //Special personal fun condition, where if the begin char and end char are 0 and 9, make it only print valid base 10 numbers (no beginning with 0!)
            //However, for this case it would just be faster to increment integers and print, but this can (technically) go to strings of arbitrary length, tho
            //it would take exponential time to do so.
            if(((beginchar == '0' && endchar == '9') && (charlist->at(0) != '0' || charlist->size() == 1)) || (!(beginchar == '0' && endchar == '9'))){
                cout << tostring(charlist) << endl;
            }
            while(it != charlist->rend()){
                if(*it == endchar && increase){
                    it++;
                    if(it == charlist->rend()){
                        break;
                    }
                    increase = *it == endchar;
                    if(*it == endchar){
                        it--;
                        *it = beginchar;
                        it++;
                        continue;
                    }
                    *it += 1;
                    it--;
                    *it = beginchar;
                    it++;
                }else if(increase){
                    *it += 1;
                    it++;
                    break;
                }else{
                    break;
                }
            }
        }
        cout << tostring(charlist) << endl;
        reset(charlist);
        charlist->push_back(beginchar);
    }
    return 0;
}
