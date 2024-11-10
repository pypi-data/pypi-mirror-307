# Math for Cannibals
This Python package provides mathematical functions to automate calculations, particularly for right triangles.

## Table of Contents

1. [Installation](#installation)
2. [Practical Information](#practical-information)
3. [Usage](#usage)
4. [Contributing](#contributing)
5. [License](#license)

## Installation

To install the package, run the following command:

```bash
pip install math_for_cannibals
```

## Practical Information

When using the class, you will be prompted to provide values for `a`, `b`, and `c`. These values represent the sides and angles of a right triangle, defined as follows:  
![right_triangle](right_triangle.png)

## Usage

### Table of Contents

1. [Configuring the Class](#configuring-the-class)
2. [Using the Class](#using-the-class)
3. [Retrieving Calculated Values](#retrieving-calculated-values)

### Configuring the Class
The class responsible for the calculations is configured like this:

```python
from math_for_cannibals.RightTriangle import RightTriangle

Rt = RightTriangle(aSide, bSide, cSide, aDegree, bDegree)
```

Here’s an example:
```python
Rt = RightTriangle(aDegree=20)
```

### Using the Class
You can use the class by entering the information you know about the triangle. The following are some example usages:

```python
Rt = RightTriangle(aDegree=20)
```

```python
Rt = RightTriangle(aSide=2, bSide=3)
```

```python
Rt = RightTriangle(aDegree=20, aSide=2)
```

### Retrieving Calculated Values
To get the calculated angles and sides of the triangle, you can use the following methods:

```python
Rt = RightTriangle(aDegree=20)
Rt.get_degrees()
```

The class has three main methods:  
- `get_degrees()` - Returns only the angles of the triangle.  
- `get_sides()` - Returns only the sides of the triangle.  
- `get_triangle()` - Returns both the sides and angles of the triangle.

## Contributing
Contributions are welcome! Please send an email explaining your proposed improvements to ensure clarity.  
Be sure to update tests as needed.

## License
[MIT](https://choosealicense.com/licenses/mit/)
