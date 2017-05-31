'''
Generazione chiavi RSA

linguaggio: python 3.x

@author: Sollazzo Nicholas
@date: March 16th 2017
@version: 0.1.3
@status: GREEN

esercitazione:
fare un software in grado di generare chiavi RSA, protocollo TCP o UDP;
possibile implementarlo in una pagina web

numeri primi da: https://primes.utm.edu/lists/small/millions/ e http://www.bigprimes.net

'''

from random import randint


class Prime(object):
    """docstring for Prime."""

    def __init__(self):
        self.PRIMES = [  # tot 99
            29,  31,  37,  41,  43,  47,  53,  59,  61,  67,  71,  # 11
            73,  79,  83,  89,  97,  101, 103, 107, 109, 113, 127,
            131, 137, 139, 149, 151, 157, 163, 167, 173, 179, 181,
            191, 193, 197, 199, 211, 223, 227, 229, 233, 239, 241,
            251, 257, 263, 269, 271, 277, 281, 283, 293, 307, 311,
            313, 317, 331, 337, 347, 349, 353, 359, 367, 373, 379,
            383, 389, 397, 401, 409, 419, 421, 431, 433, 439, 443,
            449, 457, 461, 463, 467, 479, 487, 491, 499, 503, 509,
            521, 523, 541, 547, 557, 563, 569, 571, 577, 587, 593,
        ]  # 9

    def prime_factors(self, n):
        i = 2
        factors = []
        while i * i <= n:
            if n % i:
                i += 1
            else:
                n //= i
                factors.append(i)
        if n > 1:
            factors.append(n)
        return factors

    def randPrime(self):
        return self.PRIMES[randint(0, len(self.PRIMES) - 1)]

    '''
    Euclid's extended algorithm for finding the multiplicative inverse of two numbers
    '''

    def multiplicative_inverse(self, a, b):
        """
        Returns a tuple (r, i, j) such that r = gcd(a, b) = ia + jb
        """
        # r = gcd(a,b) i = multiplicitive inverse of a mod b
        #      or      j = multiplicitive inverse of b mod a
        # Neg return values for i or j are made positive mod b or a respectively
        # Iterateive Version is faster and uses much less stack space
        x = 0
        y = 1
        lx = 1
        ly = 0
        oa = a  # Remember original a/b to remove
        ob = b  # negative values from return results
        while b != 0:
            q = a // b
            (a, b) = (b, a % b)
            (x, lx) = ((lx - (q * x)), x)
            (y, ly) = ((ly - (q * y)), y)
        if lx < 0:
            lx += ob  # If neg wrap modulo orignal b
        if ly < 0:
            ly += oa  # If neg wrap modulo orignal a
        # return a , lx, ly  # Return only positive values
        return lx

    '''
    Euclid's algorithm for determining the Greatest Common Divisor (GCD)
    Use iteration to make it faster for larger integers
    '''

    def gcd(self, a, b):
        while b != 0:
            a, b = b, a % b
        return a


class RSA(object):
    """docstring for RSA."""

    def __init__(self):
        self.prime = Prime()
        self.a = self.prime.randPrime()
        self.b = self.prime.randPrime()

        while self.a == self.b:
            self.b = self.prime.randPrime()

        self.n = self.a * self.b
        self.z = (self.a - 1) * (self.b - 1)

        self.pub, self.pri = self.generate_keypair()

    def generate_keypair(self):
        # Choose an integer pub such that pub and z are coprime
        # coprime: Grated Common Divisor == 1
        pub = randint(1, self.z)

        # Use Euclid's Algorithm to verify that pub and z are coprime
        g = self.prime.gcd(pub, self.z)
        while g != 1:
            pub = randint(1, self.z)
            g = self.prime.gcd(pub, self.z)

        # Use Extended Euclid's Algorithm to generate the private key
        # no common factor with z
        pri = self.prime.multiplicative_inverse(pub, self.z)

        # Return public and private keypair
        return (pub, pri)

    # NOTE: if n<122 cannot encrypt all the alphabet
    def encrypt(self, plaintext, pubKey=True):
        # default encryted with the public key
        if pubKey:
            key = self.pub
        else:
            key = self.pri

        # Convert each letter in the plaintext to numbers based on the character using m^pub mod n
        cipher = [pow(ord(char), key, self.n) for char in plaintext]
        # Return the array of bytes
        return cipher

    def decrypt(self, ciphertext, priKey=True):
        # default decryted with the private key
        if priKey:
            key = self.pri
        else:
            key = self.pub

        # Generate the plaintext based on the ciphertext and key using c^pri mod n
        plain = [chr(pow(char, key, self.n)) for char in ciphertext]

        # Return the array of bytes as a string
        return ''.join(plain)

    def dict(self):
        return {'a': self.a, 'b': self.b, 'n': self.n, 'z': self.z, 'pri': self.pri, 'pub': self.pub}
