# MIPS Processor Design

This project involves simulating a non-pipelined MIPS processor and developing an assembler for it. Additionally, it includes three sample programs that can run on the simulated processor.

## Overview

The MIPS architecture is a RISC (Reduced Instruction Set Computer) architecture known for its simplicity and efficiency. :contentReference[oaicite:0]{index=0} This project aims to emulate a basic MIPS processor, providing insights into processor design and instruction execution.

## Features

- **Processor Simulation**: A Python-based simulation of a non-pipelined MIPS processor, capable of executing a subset of MIPS instructions.
- **Assembler**: Converts MIPS assembly language code into machine code compatible with the simulated processor.
- **Sample Programs**: Includes three assembly programs demonstrating the processor's capabilities.

## Repository Structure

- `ALU.py`: Implements the Arithmetic Logic Unit for the processor.
- `Control.py`: Manages control signals for instruction execution.
- `Memory.py`: Simulates memory components, including instruction and data memory.
- `Processor.py`: Integrates all components to simulate the MIPS processor.
- `assembler/`: Contains the assembler code and related utilities.
- `assembly_files/`: Directory with sample assembly programs.
- `README.md`: Project documentation.

## Getting Started

1. **Clone the repository**:
   ```bash
   git clone https://github.com/gathik-jindal/MIPS-Processor-Design.git
   cd MIPS-Processor-Design

2. **Run the assembler**:
  ```bash
  python assembler/assembler.py assembly_files/sample_program.asm
  ```
  This will generate a machine code file in the output/ directory.

3. **Run the processor simulation**:
  ```bash
  python Processor.py output/sample_program.obj
  ```
  This will execute the machine code on the simulated processor and display the output.

## Requirements
  Python 3.x

## License
  This project is licensed under the MIT License.
