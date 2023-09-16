# copied or adapted from https://dailystuff.nl/projects/writing-a-6502-emulator-in-python

"""Emulation of the MOT-6502 Processor."""
import memory

class Processor:
    """MOT-6502 Processor."""

    def __init__(self, memory: memory.memory) -> None:
        """Initialize the processor.

        :param memory: The memory to use
        :return: None
        """
        self.memory = memory
        self.reg_a = 0  # Accumlator A
        self.reg_y = 0  # Incex Register Y
        self.reg_x = 0  # Incex Register X

        self.program_counter = 0  # Program Counter PC
        self.stack_pointer   = 0  # Stack Pointer S
        self.cycles          = 0  # Cycles used

        self.flag_c = True  # Status flag - Carry Flag
        self.flag_z = True  # Status flag - Zero Flag
        self.flag_i = True  # Status flag - Interrupt Disable
        self.flag_d = True  # Status flag - Decimal Mode Flag
        self.flag_b = True  # Status flag - Break Command
        self.flag_v = True  # Status flag - Overflow Flag
        self.flag_n = True  # Status flag - Negative Flag

    def reset(self) -> None:
        """Reset processor to initial state.

        :return: None
        """
        self.program_counter = 0xFCE2  # Hardcoded start vector post-reset
        self.stack_pointer   = 0x01FD  # Hardcoded stack pointer post-reset
        self.cycles          = 0
        self.flag_i = True
        self.flag_d = False
        self.flag_b = True

    def read_byte(self, address: int) -> int:
        """Read a byte from memory.

        :param address: The address to read from
        :return: int
        """
        data = self.memory[address]
        self.cycles += 1
        return data


    def write_byte(self, address: int, value: int) -> None:
        """Write a byte to memory.

        :param address: The address to write to
        :param value: The value to write
        :return: None
        """
        self.memory[address] = value
        self.cycles += 1