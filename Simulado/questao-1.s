# Escreva um programa que receba 2 numeros
# do teclado e imprima o maior. Caso os num sejam iguais imprima o valor 0

.data

.text

    main:
        # leitura do teclado
        li $v0, 5
        syscall

        # armazena o valor lido
        move $t0, $v0

        # leitura do teclado
        li $v0, 5
        syscall

        # armazena o valor lido
        move $t1, $v0

        # comparação 
        slt $t2, $t0, $t1
        addi $t3, $t3, 1
        beq $t0, $t1, iguais
        beq $t2, $t3, resultado

        li $v0, 1
        move $a0, $t0
        syscall

        j exit

    iguais:
        li $v0, 10
        move $a0, $zero
        syscall

        j exit

    resultado:
        li $v0, 1
        move $a0, $t1
        syscall

        j exit
    
    exit:
        li $v0, 10
        syscall