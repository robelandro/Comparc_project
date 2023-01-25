#!/usr/bin/python3
class Microprogram:
    def __init__(self, numRegisters, numALUFunctions, numBuses, instruction):
        self.numRegisters = numRegisters
        self.numALUFunctions = numALUFunctions
        self.numBuses = numBuses
        self.instruction = instruction

    def execute(self):
        print("Executing instruction: ", self.instruction)
        implementationType = input("Select implementation type (vertical or horizontal): ")
        if implementationType == "vertical":
            self._extracted_from_execute_5(
                "Vertical implementation selected", "2. Decode instruction"
            )
        elif implementationType == "horizontal":
            self._extracted_from_execute_5(
                "Horizontal implementation selected", "2. Fetch operands"
            )
        else:
            print("Invalid implementation type selected")
        print("Final control word: ")
        print("Bits representing respective microoperations")

    # TODO Rename this here and in `execute`
    def _extracted_from_execute_5(self, arg0, arg1):
        print(arg0)
        print("Microoperations: ")
        print("1. Fetch instruction")
        print(arg1)
        print("3. Execute instruction")
        print("4. Write back")

def main():
    numRegisters = int(input("Enter the number of registers: "))
    numALUFunctions = int(input("Enter the number of supported ALU functions: "))
    numBuses = int(input("Enter the number of buses (3, 2 or 1): "))
    instruction = input("Enter the instruction to execute: ")
    microprogram = Microprogram(numRegisters, numALUFunctions, numBuses, instruction)
    microprogram.execute()

if __name__ == '__main__':
    main()
