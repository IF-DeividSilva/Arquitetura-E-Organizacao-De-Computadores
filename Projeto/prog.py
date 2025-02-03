#sudo apt-get install python3-tk
#sudo apt-get install python3-time
import tkinter as tk
from tkinter import scrolledtext, filedialog
import time

class MIPSsimulator:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Simulador MIPS")
        
        # Instruções
        self.instrucoes = []
        
        # Inicializando Registradores
        self.registradores = {'$zero': 0, '$v0': 0, '$v1': 0,
                              '$a0': 0, '$a1': 0, '$a2': 0, '$a3': 0,
                              '$t0': 0, '$t1': 0, '$t2': 0, '$t3': 0,
                              '$t4': 0, '$t5': 0, '$t6': 0, '$t7': 0,
                              '$s0': 0, '$s1': 0, '$s2': 0, '$s3': 0,
                              '$s4': 0, '$s5': 0, '$s6': 0, '$s7': 0,
                              '$sp': 0, '$ra': 0}
        
        # Memória em tese tanto fazz (1024 posições)
        self.memoria = [0] * 1024
        
        # Contador de programa
        self.pc = 0

        self.controle = 0
        
        # Interface gráfica
        self.meu_label = tk.Label(self.root, text="Código em Assembly", font=("Arial", 12), fg="black")
        self.meu_label.pack(padx=0, pady=0)
        self.text_area = scrolledtext.ScrolledText(self.root, wrap=tk.WORD, width=50, height=15)
        self.text_area.pack (padx=0, pady=(0 , 10))
        
        self.meu_label2 = tk.Label(self.root, text="Instruções", font=("Arial", 12), fg="black")
        self.meu_label2.pack(padx=0, pady=0)
        self.instrucao_texto = scrolledtext.ScrolledText(self.root, wrap=tk.WORD, width=100, height=5)
        self.instrucao_texto.pack(padx=1, pady=1)
        
        # Criar um Frame para os ScrolledTexts
        frame_scrolledtexts = tk.Frame(self.root)
        frame_scrolledtexts.pack(pady=10, padx=10)

        self.meu_label3 = tk.Label(frame_scrolledtexts, text="Registradores", font=("Arial", 12), fg="black")
        self.meu_label3.grid(row=0, column=0, padx=10, pady=10)

        self.registradores_texto = scrolledtext.ScrolledText(frame_scrolledtexts, wrap=tk.WORD, width=50, height=15)
        self.registradores_texto.grid(row=1, column=0, padx=10, pady=10)

        self.meu_label4 = tk.Label(frame_scrolledtexts, text="Terminal", font=("Arial", 12), fg="black")
        self.meu_label4.grid(row=0, column=1, padx=10, pady=10)

        self.terminal = scrolledtext.ScrolledText(frame_scrolledtexts, wrap=tk.WORD, width=50, height=15)
        self.terminal.grid(row=1, column=1, padx=10, pady=10)

        # Botões
        self.abrir_button = tk.Button(self.root, text="Abrir Arquivo", command=self.abrir_arquivo)
        self.abrir_button.pack()
        
        self.executar_button = tk.Button(self.root, text="Executar Programa", command=self.executar_programa)
        self.executar_button.pack()
        
        self.passo_a_passo_button = tk.Button(self.root, text="Executar Passo a Passo", command=self.executar_passo_a_passo)
        self.passo_a_passo_button.pack()

        self.proximo_passo_button = tk.Button(self.root, text="Próximo Passo", command=self.continuar_execucao)
        self.proximo_passo_button.pack()

        self.limpar_button = tk.Button(self.root, text="Limpar Interface", command=self.limpar_interface) 
        self.limpar_button.pack()
        
        self.root.mainloop()

    def abrir_arquivo(self):
        arquivo = filedialog.askopenfilename(filetypes=[("Arquivos Assembly", "*.s")])
        if arquivo:
            with open(arquivo, 'r') as f:
                conteudo = f.read()
                self.text_area.insert(tk.END, conteudo)
                self.instrucoes = conteudo.splitlines()
    
        self.instrucao_texto.see(tk.END)
    def converter_bin(self, r):
        # pulei alguns que são "inuiteis" para o projeto como '$at' 
        mapeamento = {
            "$zero": "00000",
            "$v0": "00010", "$v1": "00011", 
            "$a0": "00100", "$a1": "00101", "$a2": "00110", "$a3": "00111",
            "$t0": "01000", "$t1": "01001", "$t2": "01010", "$t3": "01011", 
            "$t4": "01100", "$t5": "01101", "$t6": "01110", "$t7": "01111",
            "$s0": "10000", "$s1": "10001", "$s2": "10010", "$s3": "10011", 
            "$s4": "10100", "$s5": "10101", "$s6": "10110", "$s7": "10111",
            "$t8": "11000", "$t9": "11001", 
            "$sp": "11101", "$fp": "11110", "$ra": "11111"
        }
        return mapeamento.get(r, "Erro Registrador")
        
    
    def executar_instrucao(self, instrucao):
        # Inicializando variáveis auxiliares
        self.bin = 0
        self.aux_r = "00000"
        self.aux_imediato = "0000000000000000"
        self.shamt = "00000"
        self.aux_funct = "000000"

        partes = instrucao.split()
        if len(partes) == 0:
            return
        # pega a instrucao
        opcode = partes[0]
        # pega os operandos (se houver) 
        # tive que fazer outro vetor, pq depois de splitar por espaço, precisa tirar as virgulas do vetor partes
        operandos = [op.strip() for op in partes[1:]] 
        operandos = [op for ops in operandos for op in ops.split(',')]

        # Logica e Aritmetica
        #----------------------------------------------------------------------------------
        if opcode == 'addi':  # adicionar imediato
            self.bin = "001000"# 8 -> opcode addi (representacao binaria)

            # os posições do vetor está bugado, está sendo gerado posicções vazias 
            # então, para pegar o valor correto, é necessário pegar de 2 em 2
            # pega o registrador de destino

            rt = operandos[0]
            # pega o registrador de origem
            rs = operandos[2]
            # pega o valor imediato
            imediato = int(operandos[4])
            self.registradores[rt] = self.registradores[rs] + imediato

            rt = self.converter_bin(rt)
            rs = self.converter_bin(rs)
            imediato = bin(imediato)[2:]
            imediato = (self.aux_imediato[:-len(str(imediato))] + str(imediato))
            self.bin = self.bin + rs + rt + imediato

        
        elif opcode == 'add':  # adicionar
            self.bin = "000000"

            rd = operandos[0]
            rs = operandos[2]
            rt = operandos[4]
            self.registradores[rd] = self.registradores[rs] + self.registradores[rt]

            # converter para string para juntar no R format
            # pega o aux rd (00000) tira o tam (tira os zeros a direita) de rd e soma com rd
            # para deixar sempre com tamanho 5 conforme as especificaoes
            rd = self.converter_bin(rd)
            rs = self.converter_bin(rs)
            rt = self.converter_bin(rt)
            
            rd = (self.aux_r[:-len(str(rd))] + str(rd))
            rs = (self.aux_r[:-len(str(rs))] + str(rs))
            rt = (self.aux_r[:-len(str(rt))] + str(rt))
            funct = "100000" # 32
            
            funct =(self.aux_funct[:-len(str(funct))] + str(funct))
            self.bin = self.bin+ rs + rt + rd + self.shamt + funct
                        
        elif opcode == 'sub':  # subtrair
            self.bin = "000000"

            rd = operandos[0]
            rs = operandos[2]
            rt = operandos[4]
            self.registradores[rd] = self.registradores[rs] - self.registradores[rt]
            
            # converter para string para juntar no R format
            # pega o aux rd (00000) tira o tam (tira os zeros a direita) de rd e soma com rd
            # para deixar sempre com tamanho 5 conforme as especificaoes
            rd = self.converter_bin(rd)
            rs = self.converter_bin(rs)
            rt = self.converter_bin(rt)
            
            rd = (self.aux_r[:-len(str(rd))] + str(rd))
            rs = (self.aux_r[:-len(str(rs))] + str(rs))
            rt = (self.aux_r[:-len(str(rt))] + str(rt)) 
            funct = "100010" # 34
            funct =(self.aux_funct[:-len(str(funct))] + str(funct)) 

            self.bin = self.bin+ rs + rt + rd + self.shamt + funct
        
        elif opcode == 'mul':  # multiplicar
            # Confirmar
            # OPCODE - 28
            # FUNCT - 2
            self.bin = "000000"

            rd = operandos[0]
            rs = operandos[2]
            rt = operandos[4]
            self.registradores[rd] = self.registradores[rs] * self.registradores[rt]
            # converter para string para juntar no R format
            # pega o aux rd (00000) tira o tam (tira os zeros a direita) de rd e soma com rd
            # para deixar sempre com tamanho 5 conforme as especificaoes
            rd = self.converter_bin(rd)
            rs = self.converter_bin(rs)
            rt = self.converter_bin(rt)

            rd = (self.aux_r[:-len(str(rd))] + str(rd))
            rs = (self.aux_r[:-len(str(rs))] + str(rs))
            rt = (self.aux_r[:-len(str(rt))] + str(rt))

            funct = "011000"  # não sei o valor(PERGUNTAR DEPOIS)

            funct =(self.aux_funct[:-len(str(funct))] + str(funct))

            self.bin = self.bin+ rs + rt + rd + self.shamt + funct
        
        elif opcode == 'and':  # e
            self.bin = "000000"

            rd = operandos[0]
            rs = operandos[2]
            rt = operandos[4]
            self.registradores[rd] = self.registradores[rs] & self.registradores[rt]
            
            # converter para string para juntar no R format
            # pega o aux rd (00000) tira o tam (tira os zeros a direita) de rd e soma com rd
            # para deixar sempre com tamanho 5 conforme as especificaoes
            rd = self.converter_bin(rd)
            rs = self.converter_bin(rs)
            rt = self.converter_bin(rt)

            rd = (self.aux_r[:-len(str(rd))] + str(rd))
            rs = (self.aux_r[:-len(str(rs))] + str(rs))
            rt = (self.aux_r[:-len(str(rt))] + str(rt))
            funct = "100100" # 36
            funct =(self.aux_funct[:-len(str(funct))] + str(funct))
            
            self.bin = self.bin+ rs + rt + rd + self.shamt + funct

        elif opcode == 'or':  # ou
            self.bin = "000000"
            
            rd = operandos[0]
            rs = operandos[2]
            rt = operandos[4]
            self.registradores[rd] = self.registradores[rs] | self.registradores[rt]

            # converter para string para juntar no R format
            # pega o aux rd (00000) tira o tam (tira os zeros a direita) de rd e soma com rd
            # para deixar sempre com tamanho 5 conforme as especificaoes
            rd = self.converter_bin(rd)
            rs = self.converter_bin(rs)
            rt = self.converter_bin(rt)

            rd = (self.aux_r[:-len(str(rd))] + str(rd))
            rs = (self.aux_r[:-len(str(rs))] + str(rs))
            rt = (self.aux_r[:-len(str(rt))] + str(rt))
            funct = "100101" # 37
            funct =(self.aux_funct[:-len(str(funct))] + str(funct))
            
            self.bin = self.bin+ rs + rt + rd + self.shamt + funct

        elif opcode == 'sll':  # deslocar para a esquerda
            self.bin = "000000"

            rs = operandos[0]
            rt = operandos[2]
            imediato = int(operandos[4])
            self.registradores[rs] = self.registradores[rt] << imediato
            
            rs = self.converter_bin(rs)
            rt = self.converter_bin(rt)
            imediato = bin(imediato)[2:]
            imediato = (self.aux_imediato[:-len(str(imediato))] + str(imediato))
            
            #imediato = bin(imediato)[2:]
            #imediato = (self.aux_imediato[:-len(str(imediato))] + str(imediato))
            self.bin = self.bin + rs + rt + imediato

            
        #---------------------------------------------------------------------------------- 
        # Condicionais

        #----------------------------------------------------------------------------------
        elif opcode == 'slt': # menor que com registradores
            self.bin = "000000"

            rd = operandos[0]
            rs = operandos[2]
            rt = operandos[4]
            self.registradores[rd] = 1 if self.registradores[rs] < self.registradores[rt] else 0

            # converter para string para juntar no R format
            # pega o aux rd (00000) tira o tam (tira os zeros a direita) de rd e soma com rd
            # para deixar sempre com tamanho 5 conforme as especificaoes
            rd = self.converter_bin(rd)
            rs = self.converter_bin(rs)
            rt = self.converter_bin(rt)

            rd = (self.aux_r[:-len(str(rd))] + str(rd))
            rs = (self.aux_r[:-len(str(rs))] + str(rs))
            rt = (self.aux_r[:-len(str(rt))] + str(rt))
            funct = "101010" # 42
            funct =(self.aux_funct[:-len(str(funct))] + str(funct))

            self.bin = self.bin+ rs + rt + rd + self.shamt + funct
            
        elif opcode == 'slti': # menor que com imediato
            self.bin = "001010"

            rt = operandos[0]
            rs = operandos[2]
            imediato = int(operandos[4])
            self.registradores[rd] = 1 if self.registradores[rs] < imediato else 0

            rt = self.converter_bin(rd)
            rs = self.converter_bin(rs)
            imediato = bin(imediato)[2:]
            imediato = (self.aux_imediato[:-len(str(imediato))] + str(imediato))
            self.bin = self.bin + rs + rt + imediato

        #----------------------------------------------------------------------------------
        # Load Store

        #----------------------------------------------------------------------------------
        elif opcode == 'lw':  # carregar word
            self.bin = "100011"
            
            rt = operandos[0]  # destino
            imediato, rs = operandos[2].split('(')
            rs = rs[:-1]  # removendo o parênteses de fechamento

            imediato = int(imediato)
            self.registradores[rt] = self.memoria[self.registradores[rs] + imediato]

            rt = self.converter_bin(rt)  # destino
            rs = self.converter_bin(rs)  # origem
            imediato = bin(imediato)[2:]
            imediato = (self.aux_imediato[:-len(str(imediato))] + str(imediato))
            self.bin = self.bin + rs + rt + imediato



        elif opcode =='sw':  # salvar word
            self.bin = "101011"

            rt = operandos[0]
            imediato, rs = operandos[2].split('(')
            rs = rs[:-1]  # removendo o parênteses de fechamento
            imediato = int(imediato)
            self.memoria[self.registradores[rs] + imediato] = self.registradores[rt]
            

            rt = self.converter_bin(rt) # destino
            rs = self.converter_bin(rs) # origem

            imediato = bin(imediato)[2:]
            imediato = (self.aux_imediato[:-len(str(imediato))] + str(imediato))
            self.bin = self.bin + rs + rt + imediato


        elif opcode == 'lui':  # carregar imediato
            self.bin = "001111"

            rt = operandos[0]
            rs = "00000"
            imediato = int(operandos[2])
            self.registradores[rt] = imediato << 16

            rt = self.converter_bin(rt)

            imediato = bin(imediato << 16)[2:]
            imediato = (self.aux_imediato[:-len(str(imediato))] + str(imediato))
            self.bin = self.bin + rs + rt + imediato

        #----------------------------------------------------------------------------------
        # Syscalls (Imprimir inteiro)
        # não tem nas instruções do mips por isso o binario esta torto
        elif opcode == 'li':  # carregar imediato

            rt = operandos[0]
            imediato = int(operandos[2])
            self.registradores[rt] = imediato
        
        elif opcode == 'syscall':
            # Não sei se é isso
            # ou somente o opcode + funct maybe 
            self.bin = "000000"
            funct = "001100"
            self.bin = self.bin + self.aux_r + self.aux_r + self.aux_r + self.aux_r + funct

            auxV0 = self.registradores['$v0']
            if auxV0 == 1:
                self.atualizar_terminal()
            elif auxV0 == 4:
                print(self.memoria[self.registradores['$v0']])
                self.registradores['$v0'] = self.memoria[self.registradores['$v0']]
                self.pc += 1
                if self.memoria[self.registradores['$v0']] == 0:
                    self.pc = self.registradores['$ra']
                    return
                
            elif auxV0 == 10:
                print("Programa encerrado.")
                return

            else:
                print("Opcao nao implementada!")
        
        else:
            raise Exception(f"Instrução '{opcode}' não reconhecida.")
        
        self.controle += 1
        # Adicione mais casos para outras instruções...
        
        self.instrucao_texto.insert(tk.END, f"Passo {self.controle} -> Executando:{instrucao} Bin: {self.bin} \n")
            
    
    def executar_programa(self):
        for instrucao in self.instrucoes:
             #####   Tirar comentario 
            self.executar_instrucao(instrucao)
            self.atualizar_interface()
    
    def executar_passo_a_passo(self):
        for instrucao in self.instrucoes:
            self.executar_instrucao(instrucao)
            self.atualizar_interface()
            self.executando = False # Pausa a execução
            # epera o usuario clicar no botão de passo a passo
            while not self.executando:
                self.root.update()
                time.sleep(0.5)
            
            
    def continuar_execucao(self):
        self.executando = True

    def atualizar_terminal(self):
        self.terminal.insert(tk.END, f"{self.registradores['$a0']}\n")

    def atualizar_interface(self):
        self.registradores_texto.delete(1.0, tk.END)
        for reg, val in self.registradores.items():
            self.registradores_texto.insert(tk.END, f"{reg}: {val}\n")
    
    def limpar_interface(self):
        self.text_area.delete(1.0, tk.END)
        self.instrucao_texto.delete(1.0, tk.END) 
        self.registradores_texto.delete(1.0, tk.END)
    
    def iniciar_simulador(self):
        self.root.mainloop()

if __name__ == "__main__":
    sim = MIPSsimulator()
    sim.iniciar_simulador()
