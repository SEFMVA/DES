import generator
from bitstring import BitArray, BitStream


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
        expanded[counter] = R0[i-1]
        counter += 1
    xor = expanded ^ key
    sboxes = [
        [[14, 4, 13, 1, 2, 15, 11, 8, 3, 10, 6, 12, 5, 9, 0, 7],
         [0, 15, 7, 4, 14, 2, 13, 1, 10, 6, 12, 11, 9, 5, 3, 8],
         [4, 1, 14, 8, 13, 6, 2, 11, 15, 12, 9, 7, 3, 10, 5, 0],
         [15, 12, 8, 2, 4, 9, 1, 7, 5, 11, 3, 14, 10, 0, 6, 13]],

        [[15, 1, 8, 14, 6, 11, 3, 4, 9, 7, 2, 13, 12, 0, 5, 10],
         [3, 13, 4, 7, 15, 2, 8, 14, 12, 0, 1, 10, 6, 9, 11, 5],
         [0, 14, 7, 11, 10, 4, 13, 1, 5, 8, 12, 6, 9, 3, 2, 15],
         [13, 8, 10, 1, 3, 15, 4, 2, 11, 6, 7, 12, 0, 5, 14, 9]],

        [[10, 0, 9, 14, 6, 3, 15, 5, 1, 13, 12, 7, 11, 4, 2, 8],
         [13, 7, 0, 9, 3, 4, 6, 10, 2, 8, 5, 14, 12, 11, 15, 1],
         [13, 6, 4, 9, 8, 15, 3, 0, 11, 1, 2, 12, 5, 10, 14, 7],
         [1, 10, 13, 0, 6, 9, 8, 7, 4, 15, 14, 3, 11, 5, 2, 12]],

        [[7, 13, 14, 3, 0, 6, 9, 10, 1, 2, 8, 5, 11, 12, 4, 15],
         [13, 8, 11, 5, 6, 15, 0, 3, 4, 7, 2, 12, 1, 10, 14, 9],
         [10, 6, 9, 0, 12, 11, 7, 13, 15, 1, 3, 14, 5, 2, 8, 4],
         [3, 15, 0, 6, 10, 1, 13, 8, 9, 4, 5, 11, 12, 7, 2, 14]],

        [[2, 12, 4, 1, 7, 10, 11, 6, 8, 5, 3, 15, 13, 0, 14, 9],
         [14, 11, 2, 12, 4, 7, 13, 1, 5, 0, 15, 10, 3, 9, 8, 6],
         [4, 2, 1, 11, 10, 13, 7, 8, 15, 9, 12, 5, 6, 3, 0, 14],
         [11, 8, 12, 7, 1, 14, 2, 13, 6, 15, 0, 9, 10, 4, 5, 3]],

        [[12, 1, 10, 15, 9, 2, 6, 8, 0, 13, 3, 4, 14, 7, 5, 11],
         [10, 15, 4, 2, 7, 12, 9, 5, 6, 1, 13, 14, 0, 11, 3, 8],
         [9, 14, 15, 5, 2, 8, 12, 3, 7, 0, 4, 10, 1, 13, 11, 6],
         [4, 3, 2, 12, 9, 5, 15, 10, 11, 14, 1, 7, 6, 0, 8, 13]],

        [[4, 11, 2, 14, 15, 0, 8, 13, 3, 12, 9, 7, 5, 10, 6, 1],
         [13, 0, 11, 7, 4, 9, 1, 10, 14, 3, 5, 12, 2, 15, 8, 6],
         [1, 4, 11, 13, 12, 3, 7, 14, 10, 15, 6, 8, 0, 5, 9, 2],
         [6, 11, 13, 8, 1, 4, 10, 7, 9, 5, 0, 15, 14, 2, 3, 12]],

        [[13, 2, 8, 4, 6, 15, 11, 1, 10, 9, 3, 14, 5, 0, 12, 7],
         [1, 15, 13, 8, 10, 3, 7, 4, 12, 5, 6, 11, 0, 14, 9, 2],
         [7, 11, 4, 1, 9, 12, 14, 2, 0, 6, 10, 13, 15, 3, 5, 8],
         [2, 1, 14, 7, 4, 10, 8, 13, 15, 12, 9, 0, 3, 5, 6, 11]]
    ]
    sboxesoutput = BitArray(32)
    for i in range(0, 8):
        sbox = sboxes[i]
        index = i*6
        sbox_input = xor[index:index+6]
        row = BitArray(3)
        row[1] = sbox_input[0]
        row[2] = sbox_input[5]
        column = BitArray(5)
        column[1:5] = sbox_input[1:5]
        sboxoutput = BitStream(int=sbox[row.int][column.int], length=5)
        index2 = i*4
        sboxesoutput[index2:index2+4] = sboxoutput[1:5]
    P = [16, 7, 20, 21, 29, 12, 28, 17,
         1, 15, 23, 26, 5, 18, 31, 10,
         2, 8, 24, 14, 32, 27, 3, 9,
         19, 13, 30, 6, 22, 11, 4, 25]
    result = BitArray(32)
    counter = 0
    for i in P:
        result[counter] = sboxesoutput[i-1]
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
        result[counter] = x[i-1]
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
        result[counter] = z[i-1]
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
            result[counter] = key64[i-1]
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
            result[counter] = key56[i-1]
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
            # result = plaintextbytes
            for i in range(0, 16):
                result = feistel(result, keys[i])
            result = final_permutation(result)
            return result
        encryptedtext = BitArray()
        plaintext = ''
        try:
            f = open("plaintext.txt", "r")
            lines = f.readlines()
            plaintext = "".join(lines)
        except:
            print('tekst do zaszyfrowania (UTF-8):')
            plaintext = input()
        key[0:32] = number_generator.__next__()
        key[32:64] = number_generator.__next__()
        counter = 0
        plaintextbytes = BitArray(64)
        for i in plaintext:
            charcode = ord(i)
            plaintextbytes.uint += (charcode << ((7-counter)*8))
            # print(plaintextbytes.bin)
            counter += 1
            if(counter == 8):
                encryptedtext.append(encrypt(plaintextbytes, key))
                counter = 0
        if(counter != 0):
            encryptedtext.append(encrypt(plaintextbytes, key))
        print("klucz: " + str(key.uint))
        print("zaszyfrowany tekst:")
        print(encryptedtext)
        try:
            f = open("encrypted.txt", "w")
            f.write(str(key.uint)+"\n"+"0x"+encryptedtext.hex)
            f.close()
            print("pomyslnie zapisano do pliku")
        except:
            print("zapisywanie do pliku nie udalo sie!")

    else:
        if action == '2':
            def decrypt(encryptedtextbytes, key):
                keys = generate_keys(key)
                result = final_permutation(encryptedtextbytes)
                # result = encryptedtextbytes
                for i in range(0, 16):
                    result = feistel(result, keys[15-i])
                result = initial_permutation(result)
                resultstring = ''
                for i in range(0, 8):
                    resultstring += chr(result[i*8:(i*8)+8].uint)
                return resultstring
            decryptedtext = ''
            f = open("encrypted.txt", "r")
            lines = f.readlines()
            key = BitArray(64)
            key.uint = int(lines[0])
            encryptedtext = lines[1]
            counter = 0
            encryptedtextbytes = BitArray(encryptedtext)
            for i in range(0, int(encryptedtextbytes.length/64)):
                fragment64 = encryptedtextbytes[i*64:((i*64)+64)]
                # print(fragment64.bin)
                decryptedtext += decrypt(fragment64, key)
            print("odszyfrowany tekst:")
            print(decryptedtext)
