
# Proactivized-FDH-RSA-Signature
A secure, proactive and robust implementation of the RSA Signature Scheme which employs FDH


## File Descriptions
**firstPrimes.py**

Generate all prime numbers less than value *t* using the Sieve of Eratosthenes and store them in a file named `FfirstPrimes.txt` These are used later for generation of large random primes for RSA.

**generatePrime.py**

Generates a random *n* bit prime number. The `gen_prime_2(n)` method is called with *n* representing the number of bits desired.

Random number generation is done in 2 steps.
1. Low Level Primality Test: `gen_prime_1(n)` is called to randomly choose an odd value with minimum *n* bits. A low level primality test is applied by attempting division of the generated value with the first few hundred, pre-generated primes *(see firstPrimes.py)*
2. High Level Primality Test: As a probabilistic method of testing primality of the probable prime which passes the Low Level Primality test, **Miller Rabin** test is used. *20* iterations of the test are carried out by default.


**fileOp.py**

Contains functions to read and write data from and into files.
All files are stored locally in a ".txt" format.

***NOTE:*** *All files will be written to a Directory named* `RSAfiles` *within the working directory. To change the location 
where these files are saved, modify the following line and provide the location of the desired directory address:* `save_path = getcwd() + "\RSAfiles\\"`.


**initRSAsignature.py**

Initializes the various required values for generating RSA based signatures.
Generates *random primes*, *encryption keys*, *decryption keys* and *RSA Modulus*.
Values are stored in the same directory i.e. `RSAfiles`. 

Calls the prime generation method described in `generatePrime.py` *(default prime size = 1024 bits)* to generate a prime pair and the key generation method described in `keyGeneration.py` to generate public & private keys.


**keyGeneration.py**

Generates the public & private keys using the RSA formulae.

*Note*: The public key is randomly generated instead of being a conventional value such as *65537*

**fdh.py**

For signing of a file, the hash of the file has to be generated as it is subsequently signed using *RSA*. In this implementation, a modified version of *SHA-256* hashing algorithm is used.
The idea being to utilize the full domain of the message space in RSA. Since the default primes are *1024* bits in  size, the modulus will be of *2048* bit size. Using plain *SHA-256* under-utilizes the *RSA* capabilities to handle upto *2048* but input sizes.

For this, the file is hashed into a digest size of *2048* bits using this function utilizing repeated *SHA-256* hashing.

**signRSA.py**

Generates a signature for a given input text file.

Takes a text file as input and generates its Full Domain Hash (FDH) and signs it using the RSA public key. The signature is saved to a a file `Fsignature.txt`

**verifyRSA.py**

Verifies a given signature of a file.

Takes a file to be tested and the publically available signature to verify the file. The file is hashed using the same FDH method and the public signature is raised to the private key value to regenerate the original hash. If the two hashes are the same, the authenticity of the file is verified.

*Under construction: A proactivization mechanism to refresh shares*


