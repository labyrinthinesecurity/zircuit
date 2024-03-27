#!/usr/bin/python3

import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import math,sys

num_steps=50
max_y=50

terms=num_steps
halfterms=int(math.floor(terms)/2.0)

# Function to generate 2D random walk with specified number of steps
def generate_random_walk(num_steps,max_y):
    # Initialize arrays to store x and y coordinates
    y = np.zeros(num_steps)
   
    y[0]=1
    # Iterate over each step
    for i in range(1,num_steps):
        # Randomly choose whether to move up, down, or stay at the same y-coordinate
        if i>=halfterms and y[i-1]>=(i-halfterms):
          y_change = np.random.choice([-1])
        elif i>=halfterms and y[i-1]<(i-halfterms):
          y_change = np.random.choice([-1,0,1])
        else:
          y_change = np.random.choice([-1,0,1])
        # Update y-coordinate based on the random choice
        if (y[i-1] + y_change) > 0 and (y[i-1] + y_change)<= max_y:
          y[i] = y[i-1] + y_change
        elif (y[i-1] + y_change)>0 and (y[i-1] + y_change)> max_y:
          y[i] = y[i-1] - y_change
        else:
          y[i] = y[i-1]
    return y

# Generate random walk
y = generate_random_walk(num_steps,max_y)

print(y)

classes=1+y[num_steps-1]

print("terms",terms,"classes",y[num_steps-1],"half",halfterms)

# Create a grid covering the range of y-values

# Plot the random walk and unoccupied cells
plt.figure(figsize=(20, 20))

for i in range(0,num_steps):
  plt.plot(i, y[i], marker='s', markersize=19, color='blue', alpha=1.0)
  for j in range(num_steps):
    if j!=y[i]:
      if i<halfterms+1:
        if j<(i-terms+classes) or j>i:
          plt.plot(i, j, marker='s', markersize=19, color='white', alpha=1.0)
        else:
          if i>0 and j>0:
            plt.plot(i, j, marker='s', markersize=19, color='gray', alpha=1.0)
      else:
        if j>=(terms-i+classes-1) or j>=i:
          plt.plot(i, j, marker='s', markersize=19, color='white', alpha=1.0)
        else:
          if i>=(terms-classes) and (j<i-terms+classes):
            plt.plot(i, j, marker='s', markersize=19, color='white', alpha=1.0)
          else:
            if i>0 and j>0:
              plt.plot(i, j, marker='s', markersize=19, color='gray', alpha=1.0)
plt.title('Partition generation process',fontsize=30)
plt.xlabel('Terms',fontsize=22)
plt.ylabel('Equivalence classes',fontsize=22)
plt.grid(False)
plt.gca().set_aspect('equal', adjustable='box')

plt.savefig('walk.png')

