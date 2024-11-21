# faca um program em assemble do mips para somar vetor de inteiros onde 
# v1 = {10,20,30,40,50,60}
# v2 = {1,2,3,4,5,6}
# e o resultado da soma deve ser armazenado em v3 e impresso na tela


.data
v1: .word 10, 20, 30, 40, 50, 60
v2: .word 1, 2, 3, 4, 5, 6
v3: .word 0, 0, 0, 0, 0, 0

.text


    main:
        la $t0, v1       # Carrega o endereço de v1 em $t0
        la $t1, v2       # Carrega o endereço de v2 em $t1
        la $t2, v3       # Carrega o endereço de v3 em $t2
        li $t3, 6        # Número de elementos no vetor

    loop:
        beq $t3, $zero, end_loop  # Se $t3 for zero, termina o loop
        lw $t4, 0($t0)            # Carrega o valor de v1[i] em $t4
        lw $t5, 0($t1)            # Carrega o valor de v2[i] em $t5
        add $t6, $t4, $t5         # Soma v1[i] e v2[i], resultado em $t6
        sw $t6, 0($t2)            # Armazena o resultado em v3[i]
        addi $t0, $t0, 4          # Incrementa o endereço de v1
        addi $t1, $t1, 4          # Incrementa o endereço de v2
        addi $t2, $t2, 4          # Incrementa o endereço de v3
        addi $t3, $t3, -1          # Decrementa o contador
        j loop                    # Volta para o início do loop

    end_loop:
        la $t2, v3       # Carrega o endereço de v3 em $t2
        li $t3, 6        # Número de elementos no vetor

    print_loop:
        beq $t3, $zero, end_print  # Se $t3 for zero, termina o loop de impressão
        lw $a0, 0($t2)             # Carrega o valor de v3[i] em $a0
        li $v0, 1                  # Código de serviço para imprimir inteiro
        syscall                    # Chama o serviço do sistema
        addi $t2, $t2, 4           # Incrementa o endereço de v3
        addi $t3, $t3, -1           # Decrementa o contador
        j print_loop               # Volta para o início do loop de impressão

    end_print:
        li $v0, 10  # Código de serviço para sair do programa
        syscall     # Chama o serviço do sistema
