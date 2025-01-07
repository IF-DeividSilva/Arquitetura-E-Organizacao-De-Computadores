import tkinter as tk
from tkinter import scrolledtext


def carregarInstrucoes(arquivoEntrada, instrucoes):
    for linha in arquivoEntrada:
        if '#' not in linha: 
            linha = linha.replace('\n', '')
            instrucoes.append([linha[y-4:y] for y in range(4, len(linha)+4,4)])
    arquivoEntrada.close()
    
class MIPS_Simulator:
    def __init__(self):
        self.registers = [0] * 32
        self.memory = [0] * 1024
        self.pc = 0
        self.program = []

    def load_program(self, program):
        self.program = program

    def execute_instruction(self, instruction):
        opcode = instruction[0]
        if opcode == "ADD":
            self.registers[instruction[1]] = self.registers[instruction[2]] + self.registers[instruction[3]]
        elif opcode == "ADDI":
            self.registers[instruction[1]] = self.registers[instruction[2]] + instruction[3]
        elif opcode == "SUB":
            self.registers[instruction[1]] = self.registers[instruction[2]] - self.registers[instruction[3]]
        elif opcode == "MULT":
            self.registers[instruction[1]] = self.registers[instruction[2]] * self.registers[instruction[3]]
        elif opcode == "AND":
            self.registers[instruction[1]] = self.registers[instruction[2]] & self.registers[instruction[3]]
        elif opcode == "OR":
            self.registers[instruction[1]] = self.registers[instruction[2]] | self.registers[instruction[3]]
        elif opcode == "SLL":
            self.registers[instruction[1]] = self.registers[instruction[2]] << instruction[3]
        elif opcode == "LW":
            self.registers[instruction[1]] = self.memory[instruction[2] + instruction[3]]
        elif opcode == "SW":
            self.memory[instruction[2] + instruction[3]] = self.registers[instruction[1]]
        elif opcode == "LUI":
            self.registers[instruction[1]] = instruction[2] << 16
        elif opcode == "SLT":
            self.registers[instruction[1]] = 1 if self.registers[instruction[2]] < self.registers[instruction[3]] else 0
        elif opcode == "SLTI":
            self.registers[instruction[1]] = 1 if self.registers[instruction[2]] < instruction[3] else 0
        elif opcode == "IMPRIMIR_INTEIRO":
            print(self.registers[instruction[1]])
        elif opcode == "IMPRIMIR_STRING":
            print(instruction[1])
        elif opcode == "SAIR":
            exit()

    def run(self):
        while self.pc < len(self.program):
            instruction = self.program[self.pc]
            self.execute_instruction(instruction)
            self.pc += 1

    def print_registers(self):
        for i, reg in enumerate(self.registers):
            print(f"R{i}: {reg}")

class SimulatorGUI:
    def __init__(self, root, simulator):
        self.simulator = simulator
        self.root = root
        self.root.title("MIPS Simulator")

        self.text_area = scrolledtext.ScrolledText(root, width=60, height=20)
        self.text_area.grid(column=0, row=0, padx=10, pady=10)

        self.step_button = tk.Button(root, text="Step", command=self.step)
        self.step_button.grid(column=0, row=1, padx=10, pady=10)

        self.run_button = tk.Button(root, text="Run", command=self.run)
        self.run_button.grid(column=0, row=2, padx=10, pady=10)

        self.load_program()

    def load_program(self):
        program = [
            ("ADD", 1, 2, 3),
            ("ADDI", 1, 2, 10),
            ("SUB", 1, 2, 3),
            ("MULT", 1, 2, 3),
            ("AND", 1, 2, 3),
            ("OR", 1, 2, 3),
            ("SLL", 1, 2, 3),
            ("LW", 1, 2, 3),
            ("SW", 1, 2, 3),
            ("LUI", 1, 2),
            ("SLT", 1, 2, 3),
            ("SLTI", 1, 2, 10),
            ("IMPRIMIR_INTEIRO", 1),
            ("IMPRIMIR_STRING", "Hello, MIPS!"),
            ("SAIR",)
        ]
        self.simulator.load_program(program)

    def step(self):
        if self.simulator.pc < len(self.simulator.program):
            instruction = self.simulator.program[self.simulator.pc]
            self.simulator.execute_instruction(instruction)
            self.simulator.pc += 1
            self.update_text_area()

    def run(self):
        self.simulator.run()
        self.update_text_area()

    def update_text_area(self):
        self.text_area.delete(1.0, tk.END)
        for i, reg in enumerate(self.simulator.registers):
            self.text_area.insert(tk.END, f"R{i}: {reg}\n")

if __name__ == "__main__":
    simulator = MIPS_Simulator()
    root = tk.Tk()
    gui = SimulatorGUI(root, simulator)
    root.mainloop()
