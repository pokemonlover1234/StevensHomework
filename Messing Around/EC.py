# Implements elliptic curves mod p

from argparse import ArgumentTypeError


class EC():
    def __init__(self, p, a, b):
        self.p = p
        self.a = a
        self.b = b
        # Define point and zero classes
        # Defined in here to allow for
        # usage of EC parameters
        # Define Point type for this curve
        class Point():
            def __init__(self, x, y):
                self.x = x % p
                self.y = y % p

            def __neg__(self):
                return Point(self.x, -self.y % p)
            
            def __add__(self, other):
                # Case 5
                if isinstance(self, Zero):
                    if isinstance(other, Zero):
                        return Zero()
                    return Point(other.x, other.y)
                elif isinstance(other, Zero):
                    if isinstance(self, Zero):
                        return Zero()
                    return Point(self.x, self.y)
                elif self.x == other.x:
                    # Case 3
                    if self.y == 0 and other.y == 0:
                        return Zero()
                    # Case 4
                    elif not self.y == other.y:
                        return Zero()
                    # Case 2
                    else:
                        gamma = (3 * self.x ** 2 + a) * pow(2 * self.y, -1, p)
                        newx = gamma ** 2 - self.x - other.x
                        newy = gamma * (self.x - newx) - self.y
                        return Point(newx, newy)
                # Case 1
                else:
                    gamma = (other.y - self.y) * pow(other.x - self.x, -1, p)
                    newx = gamma ** 2 - self.x - other.x
                    newy = gamma * (self.x - newx) - self.y
                    return Point(newx, newy)

            def __sub__(self, other):
                return self + -other

            def __str__(self):
                if isinstance(self, Zero):
                    return "𝓞"
                else:
                    return f"({self.x},{self.y})"
            
            def __rmul__(self, other):
                if not isinstance(other, int):
                    raise TypeError("Must multiply point by an integer")
                # here other is an int.
                if other == 0:
                    return Zero
                start = Point(self.x, self.y)
                if other < 0:
                    start = -start
                final = Point(start.x, start.y)
                if abs(other) == 1:
                    return start
                for i in range(abs(other) - 1):
                    final += start
                return final
            
            def __repr__(self):
                return str(self)

        # Define special element "Zero"
        class Zero(Point):
            def __init__(self):
                pass
        self.Point = Point
        self.Zero = Zero

    # Allow a point to be created using 
    # an instance ec of EC like ec(x, y)
    # if zero is True, returns a Zero instance
    # and ignores x and y. 
    # Makes sure x and y are valid for this EC
    def __call__(self, x, y, zero=False):
        if zero:
            return self.Zero()
        if not (y ** 2) % self.p == (x ** 3 + self.a * x + self.b) % self.p:
            raise ValueError("The provided x and y values do not construct a valid point for this elliptic curve")
        return self.Point(x, y)
