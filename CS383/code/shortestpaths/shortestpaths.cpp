/*******************************************************************************
 * Name          : shortestpaths.cpp
 * Author        : Aidan Fischer
 * Pledge        : I pledge my honor that I have abided by the Stevens Honor System.
 * Date          : November 25, 2020
 * Description   : Implements Floyd's algorithm.
 ******************************************************************************/

#include <iostream>
#include <sstream>
#include <fstream>
#include <iomanip>
#include <string>

long const INF = __LONG_MAX__;
int num_vertices = 0;

using namespace std;

void delete_array(long** arr, int length){
    for(int i = 0; i < length; i++){
        delete [] arr[i];
    }
    delete [] arr;
}

//Get the length of a long
int len(long val){
    int length = 0;
    while(val > 0){
        ++length;
        val /= 10;
    }
    return length == 0 ? 1 : length;
}

/**
 * Displays the matrix on the screen formatted as a table
 */
void display_table(long** const matrix, const string &label, const bool use_letters = false){
    cout << label << endl;
    long max_val = 0;
    for(int i = 0; i < num_vertices; i++){
        for(int j = 0; j < num_vertices; j++){
            long cell = matrix[i][j];
            if(cell < INF && cell > max_val){
                max_val = matrix[i][j];
            }
        }
    }
    long value = max(static_cast<long>(num_vertices), max_val);
    int max_cell_width = use_letters ? len(max_val) : len(value);
    cout << ' ';
    for(int j = 0; j < num_vertices; j++){
        cout << setw(max_cell_width + 1) << static_cast<char>(j + 'A');
    }
    cout << endl;
    for(int i = 0; i < num_vertices; i++){
        cout << static_cast<char>(i + 'A');
        for(int j = 0; j < num_vertices; j++){
            cout << " " << setw(max_cell_width);
            if(matrix[i][j] == INF){
                cout << "-";
            }else if(use_letters){
                cout << static_cast<char>(matrix[i][j] + 'A');
            }else{
                cout << matrix[i][j];
            }
        }
        cout << endl;
    }
    cout << endl;
}

string calculate_path(long** path, long** inter, int i, int j);

string calculate_path_secondary(long** path, long** inter, int i, int j){
    if(i == j){
        return "";
    }
    if(inter[i][j] != INF){
        return calculate_path_secondary(path, inter, i, inter[i][j]) + " -> " + calculate_path_secondary(path, inter, inter[i][j], j);
    }else{
        return string(1, static_cast<char>('A' + j));
    }
}

string calculate_path(long** path, long** inter, int i, int j){
    if(i == j){
        return string(1, static_cast<char>('A' + i));
    }
    if(inter[i][j] != INF){
        return calculate_path(path, inter, i, inter[i][j]) + " -> " + calculate_path_secondary(path, inter, inter[i][j], j);
    }else{
        return string(1, static_cast<char>('A' + i)) + " -> " + string(1, static_cast<char>('A' + j));
    }
}

void get_and_print_solution(long** const dist_matrix, int num_vertices){
    display_table(dist_matrix, "Distance matrix:");
    //Initialize path length and intermediate vertices tables
    long **path_matrix = new long*[num_vertices];
    for(int i = 0; i < num_vertices; i++){
        path_matrix[i] = new long[num_vertices];
        for(int j = 0; j < num_vertices; j++){
            path_matrix[i][j] = dist_matrix[i][j];
        }
    }
    long **inter_matrix = new long*[num_vertices];
    for(int i = 0; i < num_vertices; i++){
        inter_matrix[i] = new long[num_vertices];
        for(int j = 0; j < num_vertices; j++){
            inter_matrix[i][j] = INF;
        }
    }

    //Create a table for D_k+1 construction
    long **next_path_matrix = new long*[num_vertices];
    for(int i = 0; i < num_vertices; i++){
        next_path_matrix[i] = new long[num_vertices];
        for(int j = 0; j < num_vertices; j++){
            next_path_matrix[i][j] = path_matrix[i][j];
        }
    }

    for(int k = 0; k < num_vertices; k++){
        for(int i = 0; i < num_vertices; i++){
            for(int j = 0; j < num_vertices; j++){
                long sum = (path_matrix[i][k] == INF || path_matrix[k][j] == INF) ? INF : path_matrix[i][k] + path_matrix[k][j];
                next_path_matrix[i][j] = min(path_matrix[i][j], sum);
                //Intermediate vertex add
                if(sum < path_matrix[i][j]){
                    inter_matrix[i][j] = static_cast<long>(k);
                }
            }
        }
        //Delete old length table
        delete_array(path_matrix, num_vertices);
        path_matrix = next_path_matrix;
        next_path_matrix = new long*[num_vertices];
        for(int i = 0; i < num_vertices; i++){
            next_path_matrix[i] = new long[num_vertices];
            for(int j = 0; j < num_vertices; j++){
                next_path_matrix[i][j] = path_matrix[i][j];
            }
        }
    }
    delete_array(next_path_matrix, num_vertices);
    display_table(path_matrix, "Path lengths:");
    display_table(inter_matrix, "Intermediate vertices:", true);

    //Display paths

    for(int i = 0; i < num_vertices; i++){
        for(int j = 0; j < num_vertices; j++){
            cout << static_cast<char>('A' + i) << " -> " << static_cast<char>('A' + j) << ", distance: " << 
            (path_matrix[i][j] == INF ? "infinity" : to_string(path_matrix[i][j])) << ", path: " <<
            (path_matrix[i][j] == INF ? "none" : calculate_path(path_matrix, inter_matrix, i, j)) << endl;
        }
    }
    delete_array(path_matrix, num_vertices);
    delete_array(inter_matrix, num_vertices);

    return;
}

int main(int argc, char* const argv[]){
    if(argc != 2){
        cerr << "Usage: " << argv[0] << " <filename>" << endl;
        return 1;
    }
    string filename = argv[1];

    ifstream vertices(filename);

    if(vertices){
        istringstream iss;
        string line;
        int linenum = 1;
        getline(vertices, line);
        iss.str(line);
        if(!(iss >> num_vertices) || num_vertices < 1 || num_vertices > 26 || len(num_vertices) != static_cast<int>(line.length())){
            cerr << "Error: Invalid number of vertices '" << line << "' on line " << linenum << "." << endl;
            return 1;
        }
        char max_vertex = static_cast<char>('A' + num_vertices - 1);
        //Initializes distance matrix
        long **matrix = new long*[num_vertices];

        for(int i = 0; i < num_vertices; i++){
            matrix[i] = new long[num_vertices];
            for(int j = 0; j < num_vertices; j++){
                //Distance to same vertex is 0
                matrix[i][j] = i == j ? 0 : INF;
            }
        }

        ++linenum;
        while(getline(vertices, line)){
            string edge1;
            string edge2;
            string distance;
            string populator;
            istringstream linecheck(line);
            int step = 1;
            while(linecheck >> populator){
                edge1 = step == 1 ? populator : edge1;
                edge2 = step == 2 ? populator : edge2;
                distance = step == 3 ? populator : distance;
                ++step;
            }
            //Confirm line data is valid
            if(step != 4){
                cerr << "Error: Invalid edge data '" << line << "' on line " << linenum << "." << endl;
                delete_array(matrix, num_vertices);
                return 1;
            }
            //Confirm edges are valid
            if(edge1.length() != 1 || (edge1[0] > max_vertex || edge1[0] < 'A')){
                cerr << "Error: Starting vertex '" << edge1 << "' on line " << linenum <<
                " is not among valid values A-" << max_vertex << "." << endl;
                delete_array(matrix, num_vertices);
                return 1;
            }

            if(edge2.length() != 1 || (edge2[0] > max_vertex || edge2[0] < 'A')){
                cerr << "Error: Ending vertex '" << edge2 << "' on line " << linenum <<
                " is not among valid values A-" << max_vertex << "." << endl;
                delete_array(matrix, num_vertices);
                return 1;
            }
            long dist;
            //Validate weight
            istringstream weight(distance);
            if(!(weight >> dist) || dist <= 0 || len(dist) != static_cast<int>(distance.length())){
                cerr << "Error: Invalid edge weight '" << distance << "' on line " << linenum << "." << endl;
                delete_array(matrix, num_vertices);
                return 1;
            }
            //Line is valid, populate distance matrix
            matrix[edge1[0] - 'A'][edge2[0] - 'A'] = dist;
            linenum++;
        }
        vertices.close();
        get_and_print_solution(matrix, num_vertices);
        delete_array(matrix, num_vertices);
    }else{
        cerr << "Error: Cannot open file '" << filename << "'." << endl; 
        return 1;
    }
    return 0;
}