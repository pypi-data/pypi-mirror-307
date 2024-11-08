from decimal import Decimal, getcontext

class calpiinfo:
    def calpi(self, amount, iterations):
        """Calculate Pi using the Chudnovsky algorithm with high precision."""
        getcontext().prec = amount + 5  # Set precision slightly higher to avoid rounding errors

        C = 426880 * Decimal(10005).sqrt()
        M = Decimal(1)
        L = Decimal(13591409)
        X = Decimal(1)
        K = Decimal(6)
        S = L

        for i in range(1, iterations):
            M = (K**3 - 16*K) * M / (i**3)
            L += 545140134
            X *= -262537412640768000
            S += Decimal(M * L) / X
            K += 12

        pi_approx = C / S
        return str(pi_approx)[:amount + 2]  # Add 2 for the '3.'
    
    def binaryencode(self, text):
        """Convert a string to a binary representation."""
        if not isinstance(text, str):
            raise ValueError("Input must be a string.")
        return ''.join(format(ord(c), '08b') for c in text)
    
    def binarydecode(self, binary_string):
     """Decode a binary string into text."""
     # Check if the length of the binary string is a multiple of 8
     if len(binary_string) % 8 != 0:
        raise ValueError("Binary string length must be a multiple of 8.")
    
    # Split the binary string into chunks of 8 bits (1 byte)
     binary_values = [binary_string[i:i+8] for i in range(0, len(binary_string), 8)]
    
    # Convert each binary chunk into its corresponding character
     decoded_string = ''
     for bv in binary_values:
         # Ensure the binary chunk is within the valid range for ASCII characters (0-255)
        if int(bv, 2) > 255:
            raise ValueError(f"Invalid binary value: {bv}")
        decoded_string += chr(int(bv, 2))
    
     return decoded_string
