/*******************************************************************************
 * Name          : toposort.cpp
 * Author        : Brian S. Borowski
 * Version       : 1.0
 * Date          : October 13, 2020
 * Description   : Solves SPOJ's TOPOSORT problem.
 *                 https://www.spoj.com/problems/TOPOSORT/
 ******************************************************************************/
#include <algorithm>
#include <iostream>
#include <queue>
#include <vector>

using namespace std;

vector<int> toposort(vector<int> graph[], const size_t size) {
    int *indegree = new int[size];
    // Fill all the elements with 0, except for index 0, which is not used.
    fill(indegree + 1, indegree + size, 0);

    // Determine the indegree of each vertex.
    for (size_t row = 1; row < size; row++) {
        for (size_t col = 0; col < graph[row].size(); col++) {
            indegree[graph[row][col]]++;
        }
    }

    // Declare a min heap priority queue.
    priority_queue<int, vector<int>, greater<int>> q;
    for (size_t i = 1; i < size; i++) {
        if (indegree[i] == 0) {
            q.push(i);
        }
    }

    // Perform the core algorithm.
    vector<int> order;
    while (!q.empty()) {
        int vertex = q.top();
        q.pop();
        order.push_back(vertex);
        for (int adjacent: graph[vertex]) {
            indegree[adjacent]--;
            if (indegree[adjacent] == 0) {
                q.push(adjacent);
            }
        }
    }

    // Look for a cycle.
    for (size_t i = 1; i < size; i++) {
        if (indegree[i] > 0) {
            order.clear();
            break;
        }
    }

    delete [] indegree;
    return order;
}

int main() {
    // Configure fast input.
    ios::sync_with_stdio(false);
    cin.tie(NULL);
    size_t n, m;
    cin >> n >> m;

    // Make an adjacency list in a simple, straightforward manner.
    vector<int> *graph = new vector<int>[n + 1];
    while (m--) {
        int x, y;
        cin >> x >> y;
        graph[x].push_back(y);
    }
    vector<int> order = toposort(graph, n + 1);
    if (order.size() > 0) {
        for (int vertex: order) {
            cout << vertex << " "; // Trailing space is ok for this problem.
        }
    } else {
        cout << "Sandro fails.";
    }
    cout << endl;

    delete [] graph;
    return 0;
}
