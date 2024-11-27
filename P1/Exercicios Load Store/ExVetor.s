.data
   v: .word 10 20 30 40 50 60 70 80 90 100  # cria um vetor
.text
    main:
    la $s0, v            # $s0 recebendo o endereco do primeiro elemento do vetor
    addi $t1, $t1, 4     # soma 4 em t1 -> para ir para o segundo elemento
    add $t2, $t1, $s0    # salva o endereco em outro reg para não perder o inicial que fica em $s0
    lw $t0, 0($t2)       # carrega o valor do elemento para o reg t0 

    addi $t1, $t1, 4     # soma 4 em t1 -> para ir para o terceiro elemento
    add $t2, $t1, $s0    # salva o endereco em outro reg para não perder o inicial que fica em $s0
    lw $t3, 0($t2)       # carrega o valor do elemento para o reg t3 

    addi $t1, $t1, 8     # soma 4 em t1 -> para ir para o quinto elemento
    add $t2, $t1, $s0    # salva o endereco em outro reg para não perder o inicial que fica em $s0
    lw $t5, 0($t2)       # carrega o valor do elemento para o reg t5

    add $t6, $t3, $t5     # soma o terceiro elem com o quinto e salva em t6
    add $t2, $t1, $s0     # salva o endereco em outro reg para não perder o inicial que fica em $s0
    addi $t1, $t1, 4      # soma 4 em t1 -> para ir para o segundo elemento
    add $t2, $t1, $s0     # salva o endereco em outro reg para não perder o inicial que fica em $s0
    sw $t6, 0($t2)        # salva o novo valor no vetor[1]
 
    lw $t7, 0($t2)       # carrega o valor do elemento para o reg t7
    
    li $v0, 1            # printar o valor de s1  -> valor do i
    move $a0, $t7
    syscall

    li $v0, 10
    syscall