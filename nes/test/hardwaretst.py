import sys
sys.path.append(r"C:\Users\monac\git\sandbox\sandbox\nes\hardware")
from memory import Memory
import unittest

class TestHardware(unittest.TestCase):
    
    def test_memory(self):

        memory_instance = Memory()

        print("testing failure to write values too big to memory...")
        self.assertRaises(
            ValueError,
            memory_instance.__setitem__,
            0x00F0,
            0xFFFF
        )

        print("testing failure to get values outside memory bounds...")
        self.assertRaises(
            ValueError,
            memory_instance.__getitem__,
            0x345F9571
        )

        print("testing size of memory...")
        self.assertEqual(
            65536,
            memory_instance.memory.size,
        )

        print("testing writing to memory...")
        self.assertEqual(
            0x00F0,
            memory_instance.__setitem__(0x0000, 0x00F0)
        )

        print("testing getting memory value...")
        self.assertEqual(
            0x00F0,
            memory_instance.__getitem__(0x0000)
        )

if __name__ == '__main__':
    unittest.main()
