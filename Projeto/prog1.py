import tkinter as tk
from tkinter import scrolledtext, filedialog, messagebox
import time

# Classe de exceção personalizada
class MinhaExcecao(Exception):
    def __init__(self, mensagem, linha):
        self.mensagem = f"{mensagem} Linha {linha}."
        super().__init__(self.mensagem)
        self.exibir_popup()

    def exibir_popup(self):
        # Exibe uma janela pop-up com a mensagem de erro
        root = tk.Tk()
        messagebox.showerror("Erro", self.mensagem)
        root.destroy()

class MIPSsimulator:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Simulador MIPS")
        
        # Partes do programa
        self.codigo_linhas = []
        self.codigo_data = [] # .data
        self.codigo_text = [] # .text
        self.linha_atual = 0
        
        # Inicializando Registradores
        self.registradores = {'$zero': 0, '$v0': 0, '$v1': 0,
                              '$a0': 0, '$a1': 0, '$a2': 0, '$a3': 0,
                              '$t0': 0, '$t1': 0, '$t2': 0, '$t3': 0,
                              '$t4': 0, '$t5': 0, '$t6': 0, '$t7': 0,
                              '$s0': 0, '$s1': 0, '$s2': 0, '$s3': 0,
                              '$s4': 0, '$s5': 0, '$s6': 0, '$s7': 0,
                              '$sp': 0, '$ra': 0}
        
        # Memória em tese tanto faz (1024 posições)
        self.memoria = [0] * 1024 # funciona do 1024 pro 0
        self.data_index = [] # label - tipo - endereco - tamanho
        self.data_segment = [] # memoria heap
        
        # Contador de programa
        self.pc = 0

        self.controle = 0

        self.passou_no_syscall_10 = 0
        
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
        
    def busca_indice(self, label):
        for elemento in self.data_index:
            if label == elemento[0]:
                return elemento
        return 0
            
    def busca_tamanho(self, endereco):
        for elemento in self.data_index:
            if endereco == elemento[2]:
                return elemento[3]
        return 0
    
    # verifica quantas posicoes devem ser imprimidas se for string
    def busca_label_tamanho(self, endereco):
        for elemento in self.data_index:
            if endereco > elemento[2]:
                continue
            else:
                break
        return elemento[1], elemento[3]

    
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
        
        elif opcode == 'mult':  # multiplicar
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
            funct = "011000" # 24
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

            rd = operandos[0]
            rt = operandos[2]
            imediato = int(operandos[4])
            self.registradores[rd] = self.registradores[rt] << imediato
            
            rd = self.converter_bin(rd)
            rt = self.converter_bin(rt)
            imediato = bin(imediato)[2:]
            imediato = (self.aux_imediato[:-len(str(imediato))] + str(imediato))

            imediato = bin(imediato)[2:]
            imediato = (self.aux_imediato[:-len(str(imediato))] + str(imediato))
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
        elif opcode == 'la':
            label = operandos[2]
            rt = operandos[0] # destino
            indice = self.busca_indice(label) # busca tupla-indice
            endereco = indice[2] # pega so o endereco na memoria
            self.registradores[rt] = endereco
            self.bin = 0

        elif opcode == 'lw':  # carregar word
            self.bin = "100011"
            
            rt = operandos[0]  # destino
            imediato, rs = operandos[2].split('(')
            rs = rs[:-1]  # removendo o parênteses de fechamento

            imediato = int(imediato)
            self.registradores[rt] = self.registradores[rs] + int(imediato/4)

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
            self.data_segment[self.registradores[rs] + int(imediato/4)] = self.registradores[rt]

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
            self.bin = 0
        
        elif opcode == 'syscall':
            # Não sei se é isso
            # ou somente o opcode + funct maybe 
            self.bin = "000000"
            funct = "001100"
            self.bin = self.bin + self.aux_r + self.aux_r + self.aux_r + self.aux_r + funct

            auxV0 = self.registradores['$v0']
            if auxV0 == 1:
                self.atualizar_terminal(self.registradores['$a0'])
            elif auxV0 == 4:
                caracteristica = self.busca_label_tamanho(self.registradores['$a0'])
                if caracteristica[0] == ".asciiz":
                    comeco = self.registradores['$a0']
                    final = comeco + caracteristica[1] - 1
                    conteudo = "".join(self.data_segment[comeco:final])
                else:
                    comeco = self.registradores['$a0']
                    conteudo = self.data_segment[comeco]

                self.atualizar_terminal(conteudo)
                
            elif auxV0 == 10:
                self.passou_no_syscall_10 = 1
                print("Programa encerrado.")
                return

            else:
                print("Opcao nao implementada!")
        
        else:
            raise MinhaExcecao(f"Instrução '{opcode}' não reconhecida.", self.linha_atual)
        
        self.controle += 1
        self.linha_atual += 1
     

        
        self.instrucao_texto.insert(tk.END, f"Passo {self.controle} -> Executando:{instrucao} Bin: {self.bin} \n")
    
    def abrir_arquivo(self):
        arquivo = filedialog.askopenfilename(filetypes=[("Arquivos Assembly", "*.s")])
        if arquivo:
            with open(arquivo, 'r') as f:
                conteudo = f.read()
                self.text_area.insert(tk.END, conteudo)
                self.codigo_linhas = conteudo.splitlines()
    
        self.instrucao_texto.see(tk.END)
    
    # le, verifica e armazena todo o conteudo do programa antes do ".text:"
    def read_heading(self):
        self.linha_atual = 1
        ponteiro = 0

        if not (self.codigo_linhas[0].strip() == '.data'):
            raise MinhaExcecao("Programa não tem linha de comando \".data\".", self.linha_atual)

        subprograma = self.codigo_linhas[1:]
        self.codigo_data = []

        # adiciona na lista self.codigo_data todas as linhas ate achar o ".text:"
        # salva dados se sao dos tipos .word ou .asciiz
        # salva toda a string .asciiz em uma posicao da lista
        # salva cada numero entre virgulas em uma posicao da lista se for .word
        for linha in subprograma:
            if not (linha.strip() == ".text"):
                if linha == "":
                    self.linha_atual += 1
                    continue
                self.codigo_data += linha
                linha_aux = linha.strip().split()   # remove espacos em volta
                label = linha_aux[0].rstrip(":")    # remove : para a label
                tipo = linha_aux[1]
                endereco = ponteiro

                # salva se for .asciiz
                if tipo == ".asciiz":
                    # ["msg:", ".asciiz", ""Hello",  "world.""]
                    # a seguinte linha salva "Hello world." e, depois, tira as "
                    conteudo = " ".join(linha_aux[2:]).strip("\"")
                    tamanho = len(conteudo)

                    self.data_index.append([label, tipo, endereco, tamanho]) # adiciona ao indice
                    self.data_segment.extend(list(conteudo)) # adiciona cada caractere da string em uma posicao da memoria
                    ponteiro += len(conteudo)

                # salva se for .word
                elif tipo == ".word":
                    conteudo = "".join(linha_aux[2:])                   # pega do primeiro valor pra frente
                    conteudo = conteudo.replace(" ", "")        # remove espacos
                    numeros = conteudo.split(',')               # separa por ,
                    word = [int(numero) for numero in numeros]  # converte tudo pra lista de numeros
                    self.data_index.append([label, tipo, ponteiro, len(word)]) # adiciona ao indice
                    for elemento in word:
                        self.data_segment.append(elemento)      # adiciona cada elemento em uma posicao de memoria
                    ponteiro += len(word)

                else:
                    raise MinhaExcecao(f"Tipo {tipo} não aceito!", self.linha_atual)

                self.linha_atual += 1
            else:
                break
        
        if len(self.codigo_linhas) == self.linha_atual: # se o contador e' igual a quantidade de linhas do codigo, o programa acabou sem ".text:"
            raise MinhaExcecao("Programa não tem linha de comando \".text\".", self.linha_atual)

        # leva pra execucao o codigo desde a linha apos o ".text" ate o final
        self.codigo_text = self.codigo_linhas[self.linha_atual+1:]

    def executar_programa(self):
        self.read_heading()
        for instrucao in self.codigo_text:
            if ':' in instrucao: continue
            #if instrucao[0] == "#": continue
            self.executar_instrucao(instrucao)
            self.atualizar_interface()

        if self.passou_no_syscall_10 == 0:
            raise MinhaExcecao("Não encerrou o programa com syscall e $v0 = 10!", self.linha_atual)
    
    
    def executar_passo_a_passo(self):
        # Lê o cabeçalho apenas uma vez no início
        self.read_heading()
        self.auxlinha_atual = 0
        self.executando = True
        self.proximo_passo()

    def proximo_passo(self):
        if self.auxlinha_atual < len(self.codigo_text):
            instrucao = self.codigo_text[self.auxlinha_atual]
            if ':' not in instrucao:  # Ignora linhas com ':'
                self.executar_instrucao(instrucao)
                self.atualizar_interface()

            self.auxlinha_atual += 1

            # Pausa a execução até o próximo clique
            self.executando = False
        else:
            # Finaliza a execução
            if self.passou_no_syscall_10 == 0:
                 raise MinhaExcecao("Não encerrou o programa com syscall e $v0 = 10!", self.auxlinha_atual)

                      
    def continuar_execucao(self):
            if not self.executando:
                self.executando = True
                self.proximo_passo()


    def atualizar_terminal(self, conteudo):
        self.terminal.insert(tk.END, f"{conteudo}\n")

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