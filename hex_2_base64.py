#!/usr/bin/env python

import unittest
from pprint import pprint
import random


base64_alphabet = [
    'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M',
    'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z',
    'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm',
    'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', 
    '0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 
    '+', '/',
]


def to_base64(raw_val):
    # how many bits wide?

    width = 0
    raw_val_copy = raw_val
    while raw_val_copy > 0:
        raw_val_copy >>= 1
        width += 1

    octets = (width + 7) // 8

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


if __name__ == '__main__':
    pass


class MyTest(unittest.TestCase):
    def test_1(self):
        hex_val = int("0x49276d206b696c6c696e6720796f757220627261696e206c696b65206120706f69736f6e6f7573206d757368726f6f6d", 16)
        expecting = 'SSdtIGtpbGxpbmcgeW91ciBicmFpbiBsaWtlIGEgcG9pc29ub3VzIG11c2hyb29t'

        result = to_base64(hex_val)
        self.assertEqual(expecting, result)
