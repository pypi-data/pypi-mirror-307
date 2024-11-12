import unittest

from ratisbona_utils.binary import BitStuffer
from ratisbona_utils.binary.binary_tools import BitUnstuffer


class MyTestCase(unittest.TestCase):
    def test_bitstuffer_shoud_stuff_as_much_bits_as_requested(self):
        bit_stuffer = BitStuffer()
        bit_stuffer.stuff_bits(0xFE_CA_12_34, 32)
        bit_stuffer.flush()
        self.assertEqual(bit_stuffer.to_bytes(), b"\xfe\xca\x12\x34")

        bit_stuffer = BitStuffer()
        bit_stuffer.stuff_bits(0xFE_CA_12_34, 16)
        bit_stuffer.flush()
        self.assertEqual(
            bit_stuffer.to_bytes(),
            b"\x12\x34",
        )

        bit_stuffer = BitStuffer()
        bit_stuffer.stuff_bits(0xFE_CA_12_34, 8)
        bit_stuffer.flush()
        self.assertEqual(
            bit_stuffer.to_bytes(),
            b"\x34",
        )

    def test_bitstuffer_must_fill_up_to_next_byte_with_0_on_flush(self):
        bit_stuffer = BitStuffer()
        bit_stuffer.stuff_bits(0xFE_CA_12_34, 15)
        bit_stuffer.flush()
        self.assertEqual(bit_stuffer.to_bytes(), (0x12_34 << 1).to_bytes(2, "big"))

    def test_unstuffer_must_reconstruct_bits(self):
        bit_unstuffer = BitUnstuffer(b"\x12\x34\x56\x78\xab\xcd\xef")
        bits = bit_unstuffer.get_bits(8)
        self.assertEqual(0x12, bits)
        bits = bit_unstuffer.get_bits(8)
        self.assertEqual(bits, 0x34)
        bits = bit_unstuffer.get_bits(8)
        self.assertEqual(bits, 0x56)
        bits = bit_unstuffer.get_bits(8)
        self.assertEqual(bits, 0x78)
        bits = bit_unstuffer.get_bits(8)
        self.assertEqual(bits, 0xAB)
        bits = bit_unstuffer.get_bits(8)
        self.assertEqual(bits, 0xCD)
        bits = bit_unstuffer.get_bits(8)
        self.assertEqual(bits, 0xEF)

    def test_stuff_and_unstuff_bits(self):
        random_testdata_3x_2to33_bits = [
            [2, 2, 3],
            [7, 5, 5],
            [1, 14, 5],
            [2, 11, 25],
            [29, 28, 9],
            [46, 27, 105],
            [53, 253, 251],
            [382, 38, 390],
            [500, 381, 480],
            [930, 761, 81],
            [1660, 535, 1064],
            [908, 3558, 2767],
            [1407, 6494, 12771],
            [25518, 1411, 19081],
            [65443, 23188, 44789],
            [113048, 65580, 30403],
            [188816, 148995, 215689],
            [499048, 300758, 88917],
            [109909, 28447, 1038224],
            [1241379, 754010, 623709],
            [840621, 493003, 2146724],
            [7080578, 6633325, 5866086],
            [13514231, 15110624, 8439533],
            [24330854, 33165880, 6505710],
            [7295787, 55200039, 5178595],
            [28429607, 6099813, 26815720],
            [235411492, 44675367, 47901737],
            [383381405, 339357961, 304902964],
            [471193697, 515116583, 989066118],
            [1064575415, 1010707593, 509209638],
            [3943487889, 3111298040, 3128685376],
        ]
        stuffer = BitStuffer()
        for idx, testdata in enumerate(random_testdata_3x_2to33_bits):
            for value in testdata:
                stuffer.stuff_bits(value, idx+2)
        binary = stuffer.to_bytes()

        unstuffer = BitUnstuffer(binary)
        for idx, testdata in enumerate(random_testdata_3x_2to33_bits):
            print(f'Testing {idx+2} Bits...')
            for expect_value in testdata:
                is_value = unstuffer.get_bits(idx + 2)
                print(f'Expected: {expect_value:x} Got: {is_value:x}')
                self.assertEqual(is_value, expect_value)


if __name__ == "__main__":
    unittest.main()
