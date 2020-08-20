import generator
from bitstring import BitArray

# https://bitstring.readthedocs.io/en/latest/walkthrough.html


def f_fun(R0, key):
    order = [32, 1, 2, 3, 4, 5,
             4, 5, 6, 7, 8, 9,
             8, 9, 10, 11, 12, 13,
             12, 13, 14, 15, 16, 17,
             16, 17, 18, 19, 20, 21,
             20, 21, 22, 23, 24, 25,
             24, 25, 26, 27, 28, 29,
             28, 29, 30, 31, 32, 1]
    expanded = BitArray(48)
    counter = 0
    for i in order:
        expanded[counter] = R0[i]
        counter += 1
    xor = expanded ^ key
    return


def feistel(byteArray64, key48):
    result = BitArray(64)
    L = byteArray64[0:32]
    R = byteArray64[32:64]
    xor = L ^ f_fun(R, key48)
    result[0:32] = R
    result[32:64] = xor
    return result


def initial_permutation(x):
    order = [58, 50, 42, 34, 26, 18, 10, 2,
             60, 52, 44, 36, 28, 20, 12, 4,
             62, 54, 46, 38, 30, 22, 14, 6,
             64, 56, 48, 40, 32, 24, 16, 8,
             57, 49, 41, 33, 25, 17, 9, 1,
             59, 51, 43, 35, 27, 19, 11, 3,
             61, 53, 45, 37, 29, 21, 13, 5,
             63, 55, 47, 39, 31, 23, 15, 7]
    result = BitArray(64)
    counter = 0
    for i in order:
        result[counter] = x[i]
        counter += 1
    return result


def final_permutation(z):
    order = [40, 8, 48, 16, 56, 24, 64, 32,
             39, 7, 47, 15, 55, 23, 63, 31,
             38, 6, 46, 14, 54, 22, 62, 30,
             37, 5, 45, 13, 53, 21, 61, 29,
             36, 4, 44, 12, 52, 20, 60, 28,
             35, 3, 43, 11, 51, 19, 59, 27,
             34, 2, 42, 10, 50, 18, 58, 26,
             33, 1, 41, 9, 49, 17, 57, 25]
    result = BitArray(64)
    counter = 0
    for i in order:
        result[counter] = z[i]
        counter += 1
    return result


if __name__ == "__main__":
    number_generator = generator.create_generator()
    # number_generator.__next__()
    print('1- szyfrowanie, 2- deszyfrowanie')
    action = input()
    key = BitArray(64)
    if action == '1':
        def encrypt(plaintextbytes, key):
            for i in range(0, 16):
                print(i)
            return
        encryptedtext = ''
        print('tekst do zaszyfrowania (UTF-8):')
        plaintext = input()
        high = number_generator.__next__() << 32
        low = number_generator.__next__()
        key.int = high+low
        counter = 0
        plaintextbytes = BitArray(64)
        for i in plaintext:
            charcode = ord(i)
            plaintextbytes.int = charcode << ((7-counter)*8)
            counter += 1
            if(counter == 8):
                encryptedtext += encrypt(plaintextbytes, key)
                counter = 0
        if(counter != 0):
            encryptedtext += encrypt(plaintextbytes, key)
        print("klucz: " + str(key.int))
        print("zaszyfrowany tekst:")
        print(encryptedtext)
    else:
        if action == '2':
            def decrypt(encryptedtextbytes, key):
                pass
            decryptedtext = ''
            print('klucz:')
            key = BitArray(64)
            keystr = input()
            key.int = int(keystr)
            print('tekst do odszyfrowania (UTF-8):')
            encryptedtext = input()
            counter = 0
            encryptedtextbytes = BitArray(64)
            for i in plaintext:
                charcode = ord(i)
                encryptedtextbytes.int = charcode << ((7-counter)*8)
                counter += 1
                if(counter == 8):
                    decryptedtext += decrypt(encryptedtextbytes, key)
                    counter = 0
            if(counter != 0):
                decryptedtext += decrypt(encryptedtextbytes, key)
            print("odszyfrowany tekst:")
            print(decryptedtext)
