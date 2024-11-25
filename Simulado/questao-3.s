# seguido as especificações do mips para chamada de procedimento faça:
# 1) um programa, em assembly do MIPS, que receba e multiplique dois inteiros sem usar a instrucao mul do MIPS.
# e imprima o resultado na tela
# 2) o programa devera funcionar tanto para numeros inteiros positivos quanto negativos.

.data
msg1: .asciiz "Digite o primeiro inteiro: "
msg2: .asciiz "Digite o segundo inteiro: "
msg3: .asciiz "O resultado da multiplicacao e: "

.text
    main:
        # Salva os valores dos registradores $s0 e $s1 na pilha
        addi $sp, $sp, -8
        sw $s0, 0($sp)
        sw $s1, 4($sp)

        # Solicita o primeiro inteiro
        li $v0, 4
        la $a0, msg1
        syscall

        li $v0, 5
        syscall
        move $s0, $v0  # $s0 = primeiro inteiro

        # Solicita o segundo inteiro
        li $v0, 4
        la $a0, msg2
        syscall

        li $v0, 5
        syscall
        move $s1, $v0  # $s1 = segundo inteiro

        # Inicializa variáveis
        move $t2, $zero  # $t2 = acumulador (resultado)
        addi $t7, $t7, 1  
        
        # Verifica se o primeiro inteiro é negativo
        slt $t4, $s0, $zero  # $t4 = 1 se $s0 < 0, caso contrário $t4 = 0
        bne $t4, $zero, neg_num1

        # Verifica se o segundo inteiro é negativo
        slt $t5, $s1, $zero  # $t5 = 1 se $s1 < 0, caso contrário $t5 = 0
        bne $t5, $zero, neg_num2

        # Multiplicação para ambos os números positivos
        j multiplier

    neg_num1:
        # Torna o primeiro número positivo
        sub $s0, $zero, $s0
        j check_num2

    neg_num2:
        # Torna o segundo número positivo
        sub $s1, $zero, $s1
        # para o caso de ser os 2 numeros negativos
        beq $t7, $zero, multiplier
        j pos_multiplier

    aux:
        addi $t7, $zero , 0
        j neg_num2

    check_num2:
        # Verifica se ambos os números são negativos
        slt $t6, $s1, $zero  # $t6 = 1 se $s1 < 0, caso contrário $t6 = 0
        bne $t6, $zero, aux

        # Multiplicação para um número negativo
        j pos_multiplier

    pos_multiplier:
        # Loop de multiplicação caso de 1 neg
        beq $s1, $zero, sinal
        add $t2, $t2, $s0
        addi $s1, $s1, -1
        j pos_multiplier

    multiplier:
    # Loop de multiplicação para sinais iguais
        beq $s1, $zero, print_result
        add $t2, $t2, $s0
        addi $s1, $s1, -1
        j multiplier

    sinal:
        # Ajusta o sinal do resultado se necessário
        sub $t2, $zero, $t2
        j print_result

    print_result:
        # Imprime o resultado
        li $v0, 4
        la $a0, msg3
        syscall

        move $a0, $t2
        li $v0, 1
        syscall

        # Restaura os valores dos registradores $s0 e $s1 da pilha
        lw $s0, 0($sp)
        lw $s1, 4($sp)
        addi $sp, $sp, 8

        # Finaliza o programa
        li $v0, 10
        syscall

