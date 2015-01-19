#!/usr/bin/python3
# A program that implements microprogrammed control:
# a. Vertical implementation
# b. Horizontal implementation)

import sys
import random

# Global variables
registers = []
alu_functions = []
instruction = []
microoperations = []
microoperation_time = []
control_word = []
bus_organization = 0
implementation_type = 0
number_of_registers = 0
number_of_alu_functions = 0
number_of_microoperations = 0
number_of_microoperation_time = 0
number_of_control_word = 0
number_of_instruction = 0

# Function to generate random registers
def generate_random_registers():
	global registers
	global number_of_registers
	registers = []
	for i in range(number_of_registers):
		registers.append(random.randint(0, 1000))

# Function to generate random ALU functions
def generate_random_alu_functions():
	global alu_functions
	global number_of_alu_functions
	alu_functions = []
	for i in range(number_of_alu_functions):
		alu_functions.append(random.randint(0, 1000))

# Function to generate random instruction
def generate_random_instruction():
	global instruction
	global number_of_instruction
	instruction = []
	for i in range(number_of_instruction):
		instruction.append(random.randint(0, 1000))

# Function to generate random microoperations
def generate_random_microoperations():
	global microoperations
	global number_of_microoperations
	microoperations = []
	for i in range(number_of_microoperations):
		microoperations.append(random.randint(0, 1000))

# Function to generate random microoperation time
def generate_random_microoperation_time():
	global microoperation_time
	global number_of_microoperation_time
	microoperation_time = []
	for i in range(number_of_microoperation_time):
		microoperation_time.append(random.randint(0, 1000))

# Function to generate random control word
def generate_random_control_word():
	global control_word
	global number_of_control_word
	control_word = []
	for i in range(number_of_control_word):
		control_word.append(random.randint(0, 1000))

# Function to display registers
def display_registers():
	global registers
	global number_of_registers
	print("Registers: ")
	for i in range(number_of_registers):
		print(registers[i])

# Function to display ALU functions
def display_alu_functions():
	global alu_functions
	global number_of_alu_functions
	print("ALU functions: ")
	for i in range(number_of_alu_functions):
		print(alu_functions[i])

# Function to display instruction
def display_instruction():
	global instruction
	global number_of_instruction
	print("Instruction: ")
	for i in range(number_of_instruction):
		print(instruction[i])

# Function to display microoperations
def display_microoperations():
	global microoperations
	global number_of_microoperations
	print("Microoperations: ")
	for i in range(number_of_microoperations):
		print(microoperations[i])

# Function to display microoperation time
def display_microoperation_time():
	global microoperation_time
	global number_of_microoperation_time
	print("Microoperation time: ")
	for i in range(number_of_microoperation_time):
		print(microoperation_time[i])

# Function to display control word
def display_control_word():
	global control_word
	global number_of_control_word
	print("Control word: ")
	for i in range(number_of_control_word):
		print(control_word[i])

# Function to display microprogrammed control
def display_microprogrammed_control():
	global registers
	global alu_functions
	global instruction
	global microoperations
	global microoperation_time
	global control_word
	global bus_organization
	global implementation_type
	global number_of_registers
	global number_of_alu_functions
	global number_of_microoperations
	global number_of_microoperation_time
	global number_of_control_word
	global number_of_instruction

	print("Microprogrammed control: ")
	print("Implementation type: ", implementation_type)
	print("Bus organization: ", bus_organization)
	print("Number of registers: ", number_of_registers)
	print("Number of ALU functions: ", number_of_alu_functions)
	print("Number of microoperations: ", number_of_microoperations)
	print("Number of microoperation time: ", number_of_microoperation_time)
	print("Number of control word: ", number_of_control_word)
	print("Number of instruction: ", number_of_instruction)
	display_registers()
	display_alu_functions()
	display_instruction()
	display_microoperations()
	display_microoperation_time()
	display_control_word()

# Function to generate random microprogrammed control
def generate_random_microprogrammed_control():
	global registers
	global alu_functions
	global instruction
	global microoperations
	global microoperation_time
	global control_word
	global bus_organization
	global implementation_type
	global number_of_registers
	global number_of_alu_functions
	global number_of_microoperations
	global number_of_microoperation_time
	global number_of_control_word
	global number_of_instruction

	implementation_type = random.randint(1, 2)
	bus_organization = random.randint(1, 3)
	number_of_registers = random.randint(1, 100)
	number_of_alu_functions = random.randint(1, 100)
	number_of_microoperations = random.randint(1, 100)
	number_of_microoperation_time = random.randint(1, 100)
	number_of_control_word = random.randint(1, 100)
	number_of_instruction = random.randint(1, 100)

	generate_random_registers()
	generate_random_alu_functions()
	generate_random_instruction()
	generate_random_microoperations()
	generate_random_microoperation_time()
	generate_random_control_word()

	display_microprogrammed_control()

if __name__ == "__main__":
	generate_random_microprogrammed_control()