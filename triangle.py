#!/usr/bin/python3

from z3 import *
import sys

# Define the maximum degree of the polynomials
max_degree = 4  # Example maximum degree

X = Int('X')

# Define the variables representing the coefficients of the polynomials
coefficients_a = [Int('coeff_a_' + str(i)) for i in range(max_degree + 1)]
coefficients_b = [Int('coeff_b_' + str(i)) for i in range(max_degree + 1)]
coefficients_c = [Int('coeff_c_' + str(i)) for i in range(max_degree + 1)]

#print(coefficients_a[-1])
#sys.exit()
# Find the degrees of the polynomials
degree_a = max_degree - coefficients_a[-1]
degree_b = max_degree - coefficients_b[-1]
degree_c = max_degree - coefficients_c[-1]

def polynomial_expr(coefficients):
    return [coefficients[i] * (X**i) for i in range(len(coefficients))]

# Define the variables representing the distances
#dist_a_b=Sqrt(Sum([(coefficients_a[i] - coefficients_b[i])**2 for i in range(max_degree + 1)]))
#dist_a_c=Sqrt(Sum([(coefficients_a[i] - coefficients_c[i])**2 for i in range(max_degree + 1)]))
#dist_b_c=Sqrt(Sum([(coefficients_b[i] - coefficients_c[i])**2 for i in range(max_degree + 1)]))

s= Solver()
s.add(degree_a.is_int())
s.add(degree_b.is_int())
s.add(degree_c.is_int())

if s.check() == sat:
  model = s.model()
  # Extract the integer values of the degrees
  degree_a_value = model.eval(degree_a, model_completion=True).as_long()
  degree_b_value = model.eval(degree_b, model_completion=True).as_long()
  degree_c_value = model.eval(degree_c, model_completion=True).as_long()
  min_distance=None
  # Calculate the Euclidean distances for each i
  for i in range(abs(degree_a_value - degree_b_value) + 1):
    # Multiply the polynomial with the highest degree by i
    polynomial_a_i = polynomial_expr([coefficients_a[j] if j + i <= degree_a_value else 0 for j in range(max_degree + 1)])
    # Calculate the Euclidean distance between the polynomials
    distance = Sqrt(Sum([(polynomial_a_i[j] - coefficients_b[j])**2 for j in range(max_degree + 1)]))
    # Update the minimum distance
    if min_distance is None:
      min_distance = distance+i
    else:
      min_distance = If(distance < min_distance, distance, min_distance)    
    polynomial_b_i = polynomial_expr([coefficients_b[j] if j + i <= degree_b_value else 0 for j in range(max_degree + 1)])
    distance = Sqrt(Sum([(polynomial_b_i[j] - coefficients_a[j])**2 for j in range(max_degree + 1)]))
    # Update the minimum distance
    if min_distance is None:
      min_distance = distance+i
    else:
      min_distance = If(distance < min_distance, distance, min_distance)    
    dist_a_b=min_distance

  min_distance=None
  for i in range(abs(degree_c_value - degree_b_value) + 1):
    # Multiply the polynomial with the highest degree by i
    polynomial_c_i = polynomial_expr([coefficients_c[j] if j + i <= degree_c_value else 0 for j in range(max_degree + 1)])
    # Calculate the Euclidean distance between the polynomials
    distance = Sqrt(Sum([(polynomial_c_i[j] - coefficients_b[j])**2 for j in range(max_degree + 1)]))
    # Update the minimum distance
    if min_distance is None:
      min_distance = distance+i
    else:
      min_distance = If(distance < min_distance, distance, min_distance)
    polynomial_b_i = polynomial_expr([coefficients_b[j] if j + i <= degree_b_value else 0 for j in range(max_degree + 1)])
    distance = Sqrt(Sum([(polynomial_b_i[j] - coefficients_c[j])**2 for j in range(max_degree + 1)]))
    # Update the minimum distance
    if min_distance is None:
      min_distance = distance+i
    else:
      min_distance = If(distance < min_distance, distance, min_distance)
    dist_b_c=min_distance

  min_distance=None
  # Calculate the Euclidean distances for each i
  for i in range(abs(degree_a_value - degree_c_value) + 1):
    # Multiply the polynomial with the highest degree by i
    polynomial_a_i = polynomial_expr([coefficients_a[j] if j + i <= degree_a_value else 0 for j in range(max_degree + 1)])
    # Calculate the Euclidean distance between the polynomials
    distance = Sqrt(Sum([(polynomial_a_i[j] - coefficients_c[j])**2 for j in range(max_degree + 1)]))
    # Update the minimum distance
    if min_distance is None:
      min_distance = distance+i
    else:
      min_distance = If(distance < min_distance, distance, min_distance)
    polynomial_c_i = polynomial_expr([coefficients_c[j] if j + i <= degree_c_value else 0 for j in range(max_degree + 1)])
    distance = Sqrt(Sum([(polynomial_c_i[j] - coefficients_a[j])**2 for j in range(max_degree + 1)]))
    # Update the minimum distance
    if min_distance is None:
      min_distance = distance+i
    else:
      min_distance = If(distance < min_distance, distance, min_distance)
    dist_a_c=min_distance

# distances are non-negative
#s.add(dist_a_b >= 0, dist_b_c >= 0, dist_a_c >= 0)
# Add constraints representing the triangle inequality
#s.add(dist_a_b + dist_b_c >= dist_a_c)
#s.add(dist_a_b + dist_a_c >= dist_b_c)
#s.add(dist_b_c + dist_a_c >= dist_a_b)
s.add(degree_a>=0)
s.add(degree_b>=0)
s.add(degree_c>=0)
s.add(degree_a<=max_degree)
s.add(degree_b<=max_degree)
s.add(degree_c<=max_degree)
s.add(X>1)

for coeff in coefficients_a:
  s.add(coeff >= 1)
for coeff in coefficients_b:
  s.add(coeff >= 2)
for coeff in coefficients_c:
  s.add(coeff >= 0)
#s.add(coefficients_a[max_degree]>0)
#s.add(coefficients_b[0]>0)

# Check if the triangle inequality holds
if s.check() == sat:
    print("Triangle inequality holds.")
    m = s.model()
#    print('dist_a_b',m.eval(dist_a_b, model_completion=True).as_long())
#    print('dist_b_c',m.eval(dist_b_c, model_completion=True).as_long())
#    print('dist_a_c',m.eval(dist_a_c, model_completion=True).as_long())
    print('dist_a_b',m.eval(dist_a_b, model_completion=True))
    print('dist_b_c',m.eval(dist_b_c, model_completion=True))
    print('dist_a_c',m.eval(dist_a_c, model_completion=True))
    print(m)
else:
    print("Triangle inequality doesnt hold.")
