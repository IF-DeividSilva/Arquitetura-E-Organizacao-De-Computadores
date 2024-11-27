.data
    vetor: .word  4 4 4 4 4 4 3 2 1  # cria um vetor
.text
    main:
        li $s1, 0            # i=0
        li $s2, 4            # $s2 == k (k recebendo 4 no caso)
        la $s3, vetor        # $s3 recebendo o endereco do primeiro elemento do vetor 
    while:
        add $t2, $t1, $s3    # salva o endereco em outro reg para não perder o inicial que fica em $s3
        lw $t0, 0($t2)       # carrega o valor do elemento para o reg t0    
        bne $t0, $s2, sair   # compara se o valor do elemento é igual ao volor de k
        addi $s1, $s1, 1     # soma 1 em s1 -> i++
        addi $t1, $t1, 4     # soma 4 em t1 -> para ir para o segundo elemento
        j while              # jump de volta para comenco
    sair:
        li $v0, 1            # printar o valor de s1  -> valor do i
        move $a0, $s1
        syscall

        li $v0, 10
        syscall