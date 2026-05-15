#ifndef CORE_CPU_H
#define CORE_CPU_H

#include <stdint.h>

// memory sizes
#define CPU_ROM_SIZE (1024 * 32)
#define CPU_RAM_SIZE (1024 * 2)

// 16 bit registers
#define CPU_REG_X_LOW   0x1a
#define CPU_REG_X_HIGH  0x1b
#define CPU_REG_Y_LOW   0x1c
#define CPU_REG_Y_HIGH  0x1d
#define CPU_REG_Z_LOW   0x1e
#define CPU_REG_Z_HIGH  0x1f

// io registers
#define CPU_IO_SPH 0x3e
#define CPU_IO_SPL 0x3d
#define CPU_IO_SREG 0x3f
#define CPU_IO_UDR 0x0c

// SREG flag positions
#define CPU_IO_SREG_FLAG_I (1 << 7)
#define CPU_IO_SREG_FLAG_T (1 << 6)
#define CPU_IO_SREG_FLAG_H (1 << 5)
#define CPU_IO_SREG_FLAG_S (1 << 4)
#define CPU_IO_SREG_FLAG_V (1 << 3)
#define CPU_IO_SREG_FLAG_N (1 << 2)
#define CPU_IO_SREG_FLAG_Z (1 << 1)
#define CPU_IO_SREG_FLAG_C 1

// backdoor
#define VM_BACKDOOR 0xFACE
#define VM_BACKDOOR_TERMINATE 0x01

struct cpu_state {
	uint8_t registers[32];

	uint16_t pc;  // program counter
	uint16_t ir;  // instruction register
	uint8_t sreg;  // status register
	uint16_t sp;  // stack pointer

	uint16_t program_size;  // amount of bytes loaded program uses in rom

	// memory
	uint8_t rom[CPU_ROM_SIZE];  // flash memory
	uint8_t mem[CPU_RAM_SIZE];  // SRAM
};

#endif  // CORE_CPU_H