# Diameter and Tolerance Calculation

## Overview
This program calculates the diameter (Ø) of a part based on its deviations in the X and Y directions, using a specified formula. It then checks whether the calculated diameter falls within an allowable tolerance limit. The program outputs both the calculated diameter and whether the part is within tolerance.

## Formula
The formula used to calculate the diameter is:
diameter = 2 × √(xdev² + ydev²)

Where:
- xdev: Deviation in the X direction
- ydev: Deviation in the Y direction

## Key Steps

### 1. Input Values
The deviations in the X and Y directions are provided as:
- xdev = 0.003
- ydev = 0.002

### 2. Formula Application
The formula calculates the diameter (diameter) based on these deviations:
diameter = 2 × √((0.003)² + (0.002)²)

### 3. Tolerance Check
The calculated diameter is compared against a tolerance value of 0.008. If the diameter is less than this tolerance, the part is considered to be within specifications.

### 4. Output
The program prints:
- The calculated diameter (diameter)
- Whether the part is within tolerance

## Sample Output
Below is an example of what the program outputs:

```
Calculated Diameter (Ø): 0.007211102550927979
Is the part within tolerance? True
```