import generator
from bitstring import BitArray


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
    sboxes = []  # TODO
    sboxesoutput = BitArray(32)
    for i in range(0, 8):
        print(i)
        # TODO
    P = [16, 7, 20, 21, 29, 12, 28, 17,
         1, 15, 23, 26, 5, 18, 31, 10,
         2, 8, 24, 14, 32, 27, 3, 9,
         19, 13, 30, 6, 22, 11, 4, 25]
    result = BitArray(32)
    counter = 0
    for i in P:
        result[counter] = sboxesoutput[i]
        counter += 1
    return result


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


def generate_keys(key64):

    def PC_1(key64):
        order = [57, 49, 41, 33, 25, 17, 9, 1,
                 58, 50, 42, 34, 26, 18, 10, 2,
                 59, 51, 43, 35, 27, 19, 11, 3,
                 60, 52, 44, 36, 63, 55, 47, 39,
                 31, 23, 15, 7, 62, 54, 46, 38,
                 30, 22, 14, 6, 61, 53, 45, 37,
                 29, 21, 13, 5, 28, 20, 12, 4]
        result = BitArray(56)
        counter = 0
        for i in order:
            result[counter] = key64[i]
            counter += 1
        return result

    def PC_2(key56):
        order = [14, 17, 11, 24, 1, 5, 3, 28,
                 15, 6, 21, 10, 23, 19, 12, 4,
                 26, 8, 16, 7, 27, 20, 13, 2,
                 41, 52, 31, 37, 47, 55, 30, 40,
                 51, 45, 33, 48, 44, 49, 39, 56,
                 34, 53, 46, 42, 50, 36, 29, 32]
        result = BitArray(48)
        counter = 0
        for i in order:
            result[counter] = key56[i]
            counter += 1
        return result

    def process_key(key56):
        C = key56[0:28]
        D = key56[28:56]
        result = BitArray(56)
        for i in range(1, 17):
            if(i == 1 or i == 2 or i == 9 or i == 16):
                firstbitC = C[0]
                firstbitD = D[0]
                C = C << 1
                D = D << 1
                C[27] = firstbitC
                D[27] = firstbitD
            else:
                firstbitC = C[0:2]
                firstbitD = D[0:2]
                C = C << 2
                D = D << 2
                C[26:28] = firstbitC
                D[26:28] = firstbitD
            result[0:28] = C
            result[28:56] = D
            yield result

    keygenerator = process_key(PC_1(key64))
    result = []
    for i in range(0, 16):
        result.append(PC_2(keygenerator.__next__()))
    return result


if __name__ == "__main__":
    number_generator = generator.create_generator()
    # number_generator.__next__()
    print('1- szyfrowanie, 2- deszyfrowanie')
    action = input()
    key = BitArray(64)
    if action == '1':
        def encrypt(plaintextbytes, key):
            keys = generate_keys(key)
            result = initial_permutation(plaintextbytes)
            for i in range(0, 16):
                result = feistel(result, keys[i])
            result = final_permutation(result)
            return result
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
