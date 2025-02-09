# Import the math module to use mathematical functions like square root
import math

# Step 1: Define the deviations in the X and Y directions
# These values represent how much the part deviates from its ideal position
x_dev = 0.003  # Deviation in the X direction (in inches)
y_dev = 0.002  # Deviation in the Y direction (in inches)

# Step 2: Calculate the diameter (Ø) using the given formula
# The formula is: Ø = 2 * sqrt(x_dev^2 + y_dev^2)
diameter = 2 * math.sqrt(x_dev**2 + y_dev**2)

# Step 3: Print the calculated diameter to verify the result
print("Calculated Diameter (Ø):", diameter)

# Step 4: Define the tolerance limit
# This is the maximum allowable diameter for the part to be considered within tolerance
tolerance = 0.008  # Tolerance limit (in inches)

# Step 5: Check if the calculated diameter is within tolerance
is_within_tolerance = diameter < tolerance

# Step 6: Print whether the part is within tolerance or not
print("Is the part within tolerance?", is_within_tolerance)
