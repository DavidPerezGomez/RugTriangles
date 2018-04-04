import sys
import math
from enum import Enum
import random
import itertools


class Union():
    """Abstract (and vague) representation of the line that connects two points"""

    def __init__(self, name, type):
        self.name = name
        self.type = type

    def __eq__(self, other):
        return self.name == other.name and self.type == other.type


class UnionType(Enum):
    ORTHOGONAL = 'orthogonal' # vertical/horizontal
    DIAGONAL = 'diagonal' # diagonal


class Unions(Union):
    """Enum of the unions (connecting lines) that will be used"""

    ALPHA = Union('α', UnionType.ORTHOGONAL) # vertical
    BETA = Union('β', UnionType.ORTHOGONAL) # horizontal
    GAMMA = Union('γ', UnionType.DIAGONAL) # top to bottom, left to right
    DELTA = Union('𝛿', UnionType.DIAGONAL) # top to bottom, right to left
    DEFAULT = Union('none', None)


class Triangle():
    """Represents a triangle, three points"""

    def __init__(self, a, b, c):
        self.points = (a, b, c)

    def __str__(self):
        return '{}-{}-{}'.format(self.points[0], self.points[1], self.points[2])

    def is_valid(self, parity):
        """Returns wether the three point form a valid triangle for a given parity or not.
        A triangle is considered valid if:
        a) all of its points are different
        b) all of its points are conected by lines to each of the other points
        c) at least one of the three lines is of a different type (orthogonal/diagonal) from the other two"""
        # even parity (True) -> (0,0) does have a diagonal coming out of it
        # odd parity (False) -> (0,0) does not have a diagonal coming out of it
        a = self.points[0]
        b = self.points[1]
        c = self.points[2]
        # are the points different?
        if a != b and a != c and b != c:
            ab = a.get_union_with(b, parity)
            bc = b.get_union_with(c, parity)
            ca = c.get_union_with(a, parity)
            # are the point all connected to one another?
            if not ab.type is None and not bc.type is None and not ca.type is None:
                # is there at least one connection different from the other two?
                return ab.type != ca.type or ab.type != bc.type
        return False


class Point():
    """Represents a point in a 2D plane (x, y)"""

    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __str__(self):
        return '({},{})'.format(self.x, self.y)

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def parity(self):
        """Returns wether the sum of the x and y values is even or not"""
        return (self.x + self.y) % 2 == 0

    def get_union_with(self, p, parity):
        """Return the type of Union (line) that connects this point to another point
        given a certain parity for the diagonal lines.
        Note that vertical and horizontal lines are always possible.
        Diagonals, however, only pass through point of a certain parity
        (even if there is a diagonal coming from (0,0), odd otherwise)"""
        if self == p:
            # same points -> no connection
            return Unions.DEFAULT
        elif self.x == p.x:
            # same column -> vertical
            return Unions.ALPHA
        elif self.y == p.y:
            # same row -> horizontal
            return Unions.BETA
        elif self.parity() == parity and self.x + self.y == p.x + p.y:
            # correct parity so that diagonals pass through them
            # same number of steps away from the origin -> top to bottom, left to right
            return Unions.GAMMA
        elif self.parity() == parity and self.x - self.y == p.x - p.y:
            # correct parity so that diagonals pass through them
            # idk how to express this one... -> top to bottom, right to left
            return Unions.DELTA
        else:
            # points aren't connected -> no connection
            return Unions.DEFAULT


def comb(n, r):
    return math.factorial(n)/(math.factorial(r)*math.factorial(n-r))

def find_triangles(length, height, parity, output=None):
    combinations = comb(length*height, 3)
    print('No. of possible triangles (combinations of 3 different points): {}'.format(combinations))

    points = []
    triangles = []
    # find all the point in the grid
    for x in range(0, length):
        for y in range(0, height):
            p = Point(x, y)
            points.append(p)

    # find all the combinations of 3 points
    pos_triangles = itertools.combinations(points, 3)
    # for each triplet, find if the formed triangle is valid
    for t in pos_triangles:
        a = t[0]
        b = t[1]
        c = t[2]
        triangle = Triangle(a, b, c)
        if triangle.is_valid(parity):
            triangles.append(triangle)
            # print(triangle)

    print('No. valid triangles found: {}'.format(len(triangles)))
    with open(output, 'w') as file:
        i = 1
        for t in triangles:
            file.write('{}. {}\n'.format(i, str(t)))
            i += 1

def print_help():
    print("""4 arguments needed
    \t1. nª of triangles that form the base
    \t2. nª of triangles that form the side
    \t3. parity of the diagonals (true if a diagonal comes out of the bottom left vertex, false otherwise)
    \t4. path to output the result""")

def main():
    try:
        length = int(sys.argv[1]) + 1
        height = int(sys.argv[2]) + 1
        parity = bool(sys.argv[3])
        output = sys.argv[4]
    except ValueError:
        print('arguments are not valid')
        exit(1)
    except IndexError:
        print_help()
        exit(1)
    find_triangles(length, height, parity, output)


if __name__ == "__main__":
    main()
