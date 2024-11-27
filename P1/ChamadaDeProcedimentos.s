.data
valor1: .word 0
valor2: .word 0
retorno: .word 0

.text
    main:
        # leitura do teclado
        li $v0, 5    #inteiro
        syscall

        # armazena o valor lido
        sw $v0, valor1

        # leitura do teclado
        li $v0, 5 #inteiro
        syscall

        # armazena o valor lido
        sw $v0, valor2

        # chamada de funcao
        # carrega os argumentos
        lw $a0, valor1
        lw $a1, valor2
        
        # chama funcao soma
        jal soma	 

        # armazenar o retorno da funcao
        sw $v0, retorno  # retorno = v0

        # printf
        lw $a0, retorno # carrega o valor do retorno em a0
        li $v0,1 # imprime inteiro
        syscall

        j exit      


    soma:
        add $v0, $a0, $a1   # v0 = a0 + a1
        jr $ra # retorna para funcao chamadora
    

    exit:
        li $v0, 10
        syscall