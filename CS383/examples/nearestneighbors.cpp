/**
 * What is a brute force algorithm?
 * A brute force algorithm is one that tests all possible candidates
 * for meeting a certain criterion.
 * It is not necessarily the best algorithm but often works well enough
 * for small input sizes.
 * It's tied closely to the concept of exhaustive search.
 *
 * Nearest-neighbor problem
 *
 * x
 *                     x
 *                             x
 *                         x
 *                                                x
 *                  x
 *     x
 *                                         x
 *
 * Imagine each x represents the GPS coordinates of a person. We want to
 * find the 2 people who are closest to one another.
 *
 * Here is the code we derived together:
 */
#include <cmath>
#include <iostream>
#include <limits>
#include <string>
#include <utility>

using namespace std;

struct Neighbor {
    float x, y;
    string name;

    Neighbor(float _x, float _y, string _name) : x{_x}, y{_y}, name{_name} { }
};

float distance(float x1, float y1, float x2, float y2) {
    float diff_x = x2 - x1, diff_y = y2 - y1;
    return diff_x*diff_x + diff_y*diff_y;
}

pair<Neighbor, Neighbor> nearest_neighbors(
                                    Neighbor neighbors[], const int length) {
    float min_distance = numeric_limits<float>::max();
    int nearest_indices[2];
    for (int i = 0; i < length - 1; i++) {
        for (int j = i + 1; j < length; j++) {
            float cur_distance = distance(neighbors[i].x, neighbors[i].y,
                                          neighbors[j].x, neighbors[j].y);
            if (cur_distance < min_distance) {
                min_distance = cur_distance;
                nearest_indices[0] = i;
                nearest_indices[1] = j;
            }
        }
    }
    return make_pair(neighbors[nearest_indices[0]],
                     neighbors[nearest_indices[1]]);
}

int main() {
    Neighbor neighbors[4] = {Neighbor(1, 1, "A"),
                             Neighbor(10.5, 111, "B"),
                             Neighbor(121, 111.1, "C"),
                             Neighbor(121.5, 111.2, "D")
                            };
    pair<Neighbor, Neighbor> result = nearest_neighbors(neighbors, 4);
    cout << result.first.name << ", " << result.second.name << endl;
    cout << "Distance: " << sqrt(distance(result.first.x, result.first.y,
                                          result.second.x, result.second.y))
         << endl;
    return 0;
}
