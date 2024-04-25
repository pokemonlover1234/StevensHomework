/*******************************************************************************
 * Name          : powergrid.cpp
 * Author        : Aidan Fischer
 * Pledge        : I pledge my honor that I have abided by the Stevens Honor System.
 * Date          : December 10, 2020
 * Description   : Implements Kruskal's algorithm to solve the power grid problem.
 ******************************************************************************/

#include <fstream>
#include <vector>
#include <sstream>
#include <iostream>
#include <algorithm>
#include <string>

using namespace std;


//Define Nodes as they pertain to Kruskal's algorithm. These also hold the street name
//These also act as a vertex, in the context of the powergrid problem.
class KruskalNode {
    public:
    KruskalNode *parent;
    int vertex;

    KruskalNode(int vertex) : parent{nullptr}, vertex{vertex} { }

    bool operator!=(const KruskalNode& b){
        return this->vertex != b.vertex;
    }
    //Kruskal methods
    KruskalNode* find(){
        KruskalNode* xRoot = this;
        while(xRoot->parent){
            xRoot = xRoot->parent;
        }   
        return xRoot;
    }
    //kUnion = kruskal union
    void kUnion(KruskalNode* y){
        y->find()->parent = find();
    }  
};

//Define an edge between two vertices, which in the context
//of the problem, is a street.
class Street{
    public:
    KruskalNode* v1;
    KruskalNode* v2;
    long long distance;
    string name;
    Street(KruskalNode* v1, KruskalNode* v2, long long distance, string name) : 
                 v1{v1}, v2{v2}, distance{distance}, name{name} { }
};

//Since we are working with heap pointers, the sort call in kruskal
//needs a custom sorting predicate
bool sortByDistance(Street* a, Street* b){
    return a->distance < b->distance;
}
//For the output
bool sortByStreet(Street* a, Street* b){
    for(long unsigned int i = 0; i < min(a->name.size(), b->name.size()); i++){
        if(a->name[i] < b->name[i]){
            return true;
        }else if(a->name[i] > b->name[i]){
            return false;
        }
    }
    //If they are equal up to the length of the shortest name
    //i.e. apple and applesauce, alphabetical order puts the 
    //shorter string first.
    return a->name.size() < b->name.size();
}

//Execute kruskal
vector<Street*>* kruskal(vector<Street*>* town){
    vector<Street*>* MST = new vector<Street*>();
    sort(town->begin(), town->end(), sortByDistance);
    for(auto edge = town->begin(); edge != town->end(); edge++){
        if((*edge)->v1->find() != (*edge)->v2->find()){
            MST->push_back(*edge);
            (*edge)->v1->kUnion((*edge)->v2);
        }else{
            continue;
        }
    }
    
    return MST;
}


//Source: https://stackoverflow.com/a/46931770
//Splits a string by a provided delimiter character.
vector<string> split (const string &s, char delim) {
    vector<string> result;
    stringstream ss (s);
    string item;

    while (getline (ss, item, delim)) {
        result.push_back (item);
    }

    return result;
}
//Check if the MST contains every node.
bool allNodesInSolution(vector<Street*>* solution, int vertexCount){
    vector<bool>* nodePresent = new vector<bool>();
    for(int i = 0; i < vertexCount; i++){
        nodePresent->push_back(false);
    }
    for(auto street : *solution){
        nodePresent->at(street->v1->vertex - 1) = true;
        nodePresent->at(street->v2->vertex - 1) = true;
    }
    bool res = true;
    for(bool k : *nodePresent){
        res &= k;
    }
    delete nodePresent;
    return res;
}

int main(int argc, char *argv[]){
    if(argc != 2){
        cerr << "Usage: " << argv[0] << " <input file>" << endl;
        return 1;
    }
    string filename = argv[1];

    ifstream edges(filename);
    int vertices;

    if(edges){
        istringstream iss;
        string line;
        int linenum = 1;
        getline(edges, line);
        iss.str(line);
        if(!(iss >> vertices) || vertices < 1 || vertices > 1000 || to_string(vertices).size() != line.size()){
            cerr << "Error: Invalid number of vertices '" << line << "' on line " << linenum << "." << endl;
            return 1;
        }
        //Use this to make sure we don't make duplicate KruskalNodes for each 
        vector<Street*>* town = new vector<Street*>();
        vector<KruskalNode*>* nodes = new vector<KruskalNode*>();
        for(int i = 1; i <= vertices; ++i){
            nodes->push_back(new KruskalNode(i));
        }

        while(getline(edges, line)){
            linenum++;
            int v1, v2;
            long long distance;
            istringstream iss1, iss2, iss3;
            vector<string> components = split(line, ',');
            if(components.size() != 4){
                cerr << "Error: Invalid edge data '" << line << "' on line " << linenum << "." << endl;
                for(auto entry: *nodes){
                    delete entry;
                }
                for(auto entry: *town){
                    delete entry;
                }
                delete nodes;
                delete town;
                return 1;
            }
            iss1.str(components.at(0));
            iss2.str(components.at(1));
            iss3.str(components.at(2));
            if(!(iss1 >> v1) || v1 < 1 || v1 > vertices || to_string(v1).size() != components.at(0).size()){
                cerr << "Error: Starting vertex '" << components.at(0) << "' on line " << linenum << " is not among valid values 1-" << vertices << "." << endl;
                for(auto entry: *nodes){
                    delete entry;
                }
                for(auto entry: *town){
                    delete entry;
                }
                delete nodes;
                delete town;
                return 1;
            }
            if(!(iss2 >> v2) || v2 < 1 || v2 > vertices || to_string(v2).size() != components.at(1).size()){
                cerr << "Error: Ending vertex '" << components.at(1) << "' on line " << linenum << " is not among valid values 1-" << vertices << "." << endl;
                for(auto entry: *nodes){
                    delete entry;
                }
                for(auto entry: *town){
                    delete entry;
                }
                delete nodes;
                delete town;
                return 1;
            }
            if(!(iss3 >> distance) || distance < 1 || to_string(distance).size() != components.at(2).size()){
                cerr << "Error: Invalid edge weight '" << components.at(2) << "' on line " << linenum << "." << endl;
                for(auto entry: *nodes){
                    delete entry;
                }
                for(auto entry: *town){
                    delete entry;
                }
                delete nodes;
                delete town;
                return 1;
            }
            //Data is valid, populate town.
            town->push_back(new Street(nodes->at(v1-1), nodes->at(v2-1), distance, components.at(3)));
        }
        vector<Street*>* solution = kruskal(town);
        sort(solution->begin(), solution->end(), sortByStreet);
        if(!allNodesInSolution(solution, vertices)){
            cout << "No solution." << endl;
            for(auto entry: *nodes){
                delete entry;
            }
            for(auto entry: *town){
                delete entry;
            }
            delete nodes;
            delete town;
            delete solution;
            return 0;
        }
        long long total = 0;
        for(auto street: *solution){
            total += street->distance;
        }
        cout << "Total wire length (meters): " << total << endl;
        for(auto street: *solution){
            cout << street->name << " [" << street->distance << "]" << endl;
        }
        for(auto entry: *nodes){
            delete entry;
        }
        for(auto entry: *town){
            delete entry;
        }
        delete nodes;
        delete town;
        delete solution;
    }else{
        cerr << "Error: Cannot open file '" << filename << "'." << endl; 
        return 1;
    }
    return 0;
}