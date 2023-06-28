#!/usr/bin/env python

import unittest
from pprint import pprint
import random
import fileinput

base64_alphabet = [
    'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M',
    'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z',
    'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm',
    'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', 
    '0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 
    '+', '/',
]


def width_in_octets(val):
    width = 0  # width of val in bits
    val_copy = val
    while val_copy > 0:
        val_copy >>= 1
        width += 1

    return (width + 7) // 8


def to_base64(raw_val):
    octets = width_in_octets(raw_val)

    # how many octets in the last group?

    remaining_octets = octets % 3

    bits = raw_val.to_bytes(length=octets, byteorder='big')

    # pprint(bits)

    # convert each group of 3 octets to 4 base64 digits

    mask = 2 ** 6 - 1

    result = []
    for i in range(0, octets, 3):
        x = int.from_bytes(bits[i:i+3], byteorder='big')

        c1 = base64_alphabet[(x >> 18) & mask]
        c2 = base64_alphabet[(x >> 12) & mask]
        c3 = base64_alphabet[(x >> 6) & mask]
        c4 = base64_alphabet[x & mask]

        result.append(c1)
        result.append(c2)
        result.append(c3)
        result.append(c4)

    if remaining_octets == 1:
        x = int.from_bytes(bits[-1:], byteorder='big')
        x <<= 4

        c1 = base64_alphabet[(x >> 6) & mask]
        c2 = base64_alphabet[x & mask]

        result.append(c1)
        result.append(c2)
        result.append('=')
        result.append('=')

    elif remaining_octets == 2:
        x = int.from_bytes(bits[-2:], byteorder='big')
        x <<= 2

        c1 = base64_alphabet[(x >> 12) & mask]
        c2 = base64_alphabet[(x >> 6) & mask]
        c3 = base64_alphabet[x & mask]

        result.append(c1)
        result.append(c2)
        result.append(c3)
        result.append('=')

    return ''.join(result)


def fixed_xor(v1, v2):
    """

    :param v1:  string representation of hex number
    :param v2:  ditto
    :return:  XOR of v1 and v2

    assumes that v1 and v2 are the same length.
    """
    return int(v1, 16) ^ int(v2, 16)


# challenge 3
def decrypt_single_byte_xor(s):
    """

    :param s: hex encoded string that has been encrypted
    :return:
    """
    val = int(s, 16)
    width = width_in_octets(val)

    print("################### %s" % s)
    raw_bytes = val.to_bytes(length=width, byteorder='big')
    #print(raw_bytes)

    for i in range(256):
        again = [x ^ i for x in raw_bytes]

        # chuck anything with non-printable chars

        # x = list(filter(lambda x: x < 32 or x == 127, again))
        # if len(x) > 0:
        #     continue
        #
        # chuck anything that doesn't have ascii in it
        x = list(filter(lambda x: x > 127, again))
        if len(x) > 0:
            continue

        # chuck anything that has no spaces

        x = list(filter(lambda x: chr(x) == ' ', again))
        if len(x) == 0:
            continue

        print(chr(i), ''.join([chr(k) for k in again]))


# challenge 4
def challenge_4():
    fi = fileinput.FileInput("./4.txt")
    for line in fi:
        l = line.strip()
        decrypt_single_byte_xor(l)

    # found it.  7b5a4215415d544115415d5015455447414c155c46155f4058455c5b523f
    # decrypts to the name of a song.


if __name__ == '__main__':
    challenge_4()


class MyTest(unittest.TestCase):
    def test_hex_2_base64(self):
        hex_val = int("49276d206b696c6c696e6720796f757220627261696e206c696b65206120706f69736f6e6f7573206d757368726f6f6d", 16)
        expecting = 'SSdtIGtpbGxpbmcgeW91ciBicmFpbiBsaWtlIGEgcG9pc29ub3VzIG11c2hyb29t'

        result = to_base64(hex_val)
        self.assertEqual(expecting, result)

    def test_fixed_xor(self):
        v1 = "1c0111001f010100061a024b53535009181c"
        v2 = "686974207468652062756c6c277320657965"
        expecting = int("746865206b696420646f6e277420706c6179", 16)
        self.assertEqual(expecting, fixed_xor(v1, v2))