from decimal import Decimal, getcontext

def calpi(amount, iterations):
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

# Example usage: Get Pi to 100 decimal places with 10 iterations
