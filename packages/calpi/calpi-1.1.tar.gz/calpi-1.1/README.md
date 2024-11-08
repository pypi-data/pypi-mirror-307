The CalPi library is currently in its alpha development phase.

Disclaimer:

    At the recommended iteration setting of 4,000, CalPi can reliably compute up to 1,000 digits of π. Reducing the iteration count may significantly decrease the accuracy of the results. Increasing iterations beyond 50,000 is possible but may cause instability or potential failures in the library’s calculations.

Functionality:

    The CalPi library is designed to calculate up to 1,000 digits of π with high precision, offering a practical tool for applications requiring precise values of π for mathematical or scientific computations. CalPi is ideal for environments that need consistent precision with moderate computational resources, like educational purposes or high-accuracy simulations.

Usage Example:
```python
from decimal import Decimal, getcontext
from calpi import calpiinfo  

# Create an instance of calpiinfo
pi_calculator = calpiinfo()

# Example usage of the calpi function to calculate Pi
amount = 100  # The number of digits of Pi you want to calculate
iterations = 1000  # Number of iterations for the Chudnovsky algorithm

# Calculate Pi with high precision
calculated_pi = pi_calculator.calpi(amount, iterations)
print(f"Calculated Pi with {amount} digits: {calculated_pi}")

# Example usage of the binaryencode function to convert a string to binary
text = "Hello, World!"  # The string to be encoded
binary_encoded = pi_calculator.binaryencode(text)
print(f"Binary Encoding of '{text}': {binary_encoded}")

# Example usage of the binarydecode function to decode the binary string back to text
binary_string = binary_encoded  # Using the previously encoded binary string
decoded_text = pi_calculator.binarydecode(binary_string)
print(f"Decoded Binary String: {decoded_text}")

```

This will output:

3.14159265358979323846264338327950288419716939937510582097494459230781640628620899862803482534211706798214808651328230664709384460955058223172535940812848111745028410270193852110555964462294895493038196442881097566593344612847564823378678316527120190914564856692346034861045432664821339360726024914127372458700660631558817488152092096282925409171536436789259036001133053054882046652138414695194151160943305727036575959195309218611738193261179310511854807446237996274956735188575272489122793818301194912983367336244065664308602139494639522473719070217986094370277053921717629317675238467481846766940513200056812714526356082778577134275778960917363717872146844090122495343014654958537105079227968925892354201995611212902196086403441815981362977477130996051870721134999999837297804995105

A note from the developer:
 This is my first library- Whether it recieves more features and updates as time progresses is uncertain, love you guys <3

For Further Reading on each feature of Calpi, visit:
https://calpi-docs.onrender.com