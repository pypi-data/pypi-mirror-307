# pypostfix

https://github.com/Slinky802/pypostfix

**pypostfix** is a Python library for manipulating expressions in both infix and postfix notation (Reverse Polish Notation or RPN).

## Contents
- [Installation](#installation)
- [Use](#use)
- [Features](#features)
- [License](#license)
- [Contribute](#Contribute)
- [Contact](#Contact)

---

## Installation

To install the library, use pip :

``` bash
pip install pypostfix
```

---

## Use

You can use directly ```import pypostfix``` or use ```from pypostfix import RPN```and ```from pypostfix import Stack```

Basic example of calculating an infix notation by converting it to postfix and then evaluating it:

```python
from pypostfix import RPN

expression = RPN.infix_to_rpn("sin(3*2+9)")
print(expression)
print(RPN.calc_rpn(expression))
# output : 
# 3 2 * 9 + sin
# -0.9589242746631385
```

Basic example of manipulating stacks :

```python
from pypostfix import Stack

stack = Stack()
stack.push(4) # adds 4 to the stack
print(stack.size()) # outputs the size of the stack
print(stack.peek()) # outputs the top element of the stack
print(stack.size())
print(stack.pop()) # removes and outputs the top element of the stack
print(stack.isempty()) # Tests if the stack is empty
```

---

## Features

**Convert infix to postfix:** 
```python
from pypostfix import RPN

RPN.infix_to_rpn("sin(3*2+9)")
```

**Convert posfix to infix:** 
```python
from pypostfix import RPN

RPN.rpn_to_infix("3 2 + sin dup sqrt +")
RPN.rpn_to_infix("3;2;+;sin;dup;sqrt;+", sep=";")
```

**Test if a postfix expression is valid:** 
```python
from pypostfix import RPN

RPN.rpn_is_valid("3 0 /")
RPN.rpn_is_valid("3,0,/", sep=",")
```

**Evaluate a postfix expression:** 
```python
from pypostfix import RPN

RPN.calc_rpn("3 2 5 * swap /")
RPN.calc_rpn("3:2:5:*:swap:/", sep=":")
```

**Manipulate stacks:** 
```python
from pypostfix import Stack

stack = Stack()

stack.push(4)
print(stack.size())
print(stack.peek())
print(stack.size())
print(stack.pop())
print(stack.isempty())
# output :
# 1
# 4
# 1
# 4
# True
```

---

## License
This project is licensed under the MIT license - see the LICENSE file for details.

---

## Contribute

We welcome contributions to improve and expand the **pypostfix** library ! Whether you want to add a feature, fix a bug, or enhance the documentation, follow these steps to contribute:

### Steps to Contribute

1. **Fork the Repository**: Create a copy of the project on your GitHub account using the "Fork" button.

2. **Clone the Project**: Clone your fork locally to work on the code.
   ```bash
   git clone https://github.com/Slinky802/pypostfix
   cd pypostfix
   ```
3. **Create a New Branch**: Before making changes, create a new branch for your work.
    ```bash
    git checkout -b my_new_feature
    ```
4. **Make Your Changes**: Add your modifications or new features.

5. **Submit a Pull Request (PR)**: Once your changes are ready, push them to your fork, then submit a PR to the master branch of this repository.

 - Describe your changes and their purpose.
 - Mention any related issues you've resolved.
 - Request a code review.
 
### Code Review Policy
To maintain the project's stability and security, we have implemented a branch protection policy:

 - Any changes to the main branch must go through a Pull Request.
 - Each PR requires a review and may need approval before merging.
 - Only administrators and trusted contributors can merge approved PRs.

---

## Contact
Created by Alexandre Poggioli (Slinky802) - alexandrepoggioli09@gmail.com

More information on https://slinky-presentation.netlify.app


