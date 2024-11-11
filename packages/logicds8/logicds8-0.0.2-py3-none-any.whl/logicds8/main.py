#class MathAndDataFunctions:
    # Basic Math Functions
def add_two_numbers(a, b):
        """Return the sum of two numbers."""
        return a + b

def multiply_two_numbers(a, b):
        """Return the product of two numbers."""
        return a * b

def calculate_square(number):
        """Return the square of a number."""
        return number ** 2

    # Set Theory Functions
def union_of_sets(set1, set2):
        """Return the union of two sets."""
        return set1 | set2

def intersection_of_sets(set1, set2):
        """Return the intersection of two sets."""
        return set1 & set2

def difference_of_sets(set1, set2):
        """Return the difference of two sets (elements in set1 but not in set2)."""
        return set1 - set2

def is_subset(subset, superset):
        """Return True if 'subset' is a subset of 'superset', otherwise False."""
        return subset <= superset

    # Linear Regression Basics
def mean(values):
        """Return the mean (average) of a list of numbers."""
        return sum(values) / len(values)

def covariance(x, y):
        """Return the covariance of two lists of numbers."""
        x_mean = self.mean(x)
        y_mean = self.mean(y)
        return sum((x_i - x_mean) * (y_i - y_mean) for x_i, y_i in zip(x, y)) / len(x)

def variance(values):
        """Return the variance of a list of numbers."""
        mean_val = self.mean(values)
        return sum((x - mean_val) ** 2 for x in values) / len(values)

def linear_regression_slope(x, y):
        """Calculate the slope of the best-fit line (simple linear regression)."""
        return self.covariance(x, y) / self.variance(x)

def linear_regression_intercept(x, y):
        """Calculate the intercept of the best-fit line (simple linear regression)."""
        return self.mean(y) - self.linear_regression_slope(x, y) * self.mean(x)

    # Probability Functions
def probability_of_event(event_outcomes, total_outcomes):
        """Return the probability of an event given possible outcomes."""
        return event_outcomes / total_outcomes

def combinations(n, k):
        """Return the number of ways to choose k elements from n elements without replacement."""
        from math import factorial
        return factorial(n) // (factorial(k) * factorial(n - k))

def permutations(n, k):
        """Return the number of ways to arrange k elements from n elements in order."""
        from math import factorial
        return factorial(n) // factorial(n - k)

    # Matrix Operations
def add_matrices(matrix1, matrix2):
        """Add two matrices of the same dimensions."""
        return [[a + b for a, b in zip(row1, row2)] for row1, row2 in zip(matrix1, matrix2)]

def transpose_matrix(matrix):
        """Return the transpose of a matrix."""
        return [list(row) for row in zip(*matrix)]

def multiply_matrices(matrix1, matrix2):
        """Multiply two matrices (matrix1 by matrix2)."""
        if len(matrix1[0]) != len(matrix2):
            raise ValueError("Number of columns in matrix1 must equal number of rows in matrix2")
        return [[sum(a * b for a, b in zip(row, col)) for col in zip(*matrix2)] for row in matrix1]

    # Prime Number Functions
def is_prime(number):
        """Return True if the number is prime, else False."""
        if number <= 1:
            return False
        for i in range(2, int(number ** 0.5) + 1):
            if number % i == 0:
                return False
        return True

def list_primes(limit):
        """Return a list of all prime numbers up to a given limit."""
        return [num for num in range(2, limit + 1) if self.is_prime(num)]

    # Calculus Functions
def derivative(f, x, h=1e-5):
        """Approximate the derivative of function f at point x."""
        return (f(x + h) - f(x - h)) / (2 * h)

    # Descriptive Statistics Functions
def calculate_mean(values):
        """Return the mean (average) of a list of numbers."""
        return sum(values) / len(values)

def calculate_median(values):
        """Return the median of a list of numbers."""
        from statistics import median
        return median(values)

def calculate_mode(values):
        """Return the mode of a list of numbers."""
        from statistics import mode
        return mode(values)

    # Tuple-related Functions
def create_and_access_tuple(self):
        """Create a tuple and demonstrate accessing its elements."""
        my_tuple = (1, 2, 3, 4, 5)
        print("Original Tuple:") 
        print(my_tuple)
        print("Element returned based on your input arg:") 
        return my_tuple[self]
   

def sum_and_product(a, b):
        """Return both the sum and the product of two numbers as a tuple."""
        return a + b, a * b

def distance_between_points(x1,y1, x2,y2):
        """Calculate the Euclidean distance between two points in 2D space."""
        x1, y1 = point1
        x2, y2 = point2
        return ((x2 - x1) ** 2 + (y2 - y1) ** 2) ** 0.5
