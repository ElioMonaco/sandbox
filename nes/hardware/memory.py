# copied or adapted from https://github.com/hspaans/python-6502-emulator/tree/master

import numpy as np

class Memory:
    """Memory bank for MOT-6502 systems."""

    def __init__(self, size: int = 65536) -> None:
        """Initialize the memory.

        :param size: The size of the memory
        :return: None
        """

        """not sure why int the original coped, minimum value is set to 512.
        Here I set it to 0, maybe later it will be more clear to me why 0 was not a good choice.
        """
        if 0x0000 < (size - 1) > 0xFFFF:
            raise ValueError("Memory size is not valid")
        self.size = size
        """importantly, memory needs to be an array of integers and not floats.
        see: https://github.com/numpy/numpy/issues/5668
        """
        self.memory = np.zeros(self.size).astype(int)
        if __name__ == "__main__":
            print("Memory size:",len(self.memory))

    def __getitem__(self, address: int) -> int:
        """Get the value at the specified address.

        :param address: The address to read from
        :return: The value at the specified address
        """
        if 0x0000 < address > self.size:
            raise ValueError("Memory address is not valid")
        return self.memory[address]

    def __setitem__(self, address: int, value: int) -> int:
        """Set the value at the specified address.

        :param address: The address to write to
        :param value: The value to write to the address
        :return: the value just set at the address
        """
        if 0x0000 < address > self.size:
            raise ValueError("Memory address is not valid")
        if value.bit_length() > 8:
            raise ValueError("Value too large")
        self.memory[address] = value
        return self.memory[address]