.data

.text

    main:
        li $t0, 5
        li $t2, 1
        
        #chamada de sistema para imprimir resultado
    loop:
        beq $t0, $zero, sai
        move $t1, $t0
        move $t3, $zero

    loop2:
        beq    $t1, $zero, sai2
        add $t3, $t3, $t2
        addi $t1, $t1, -1
    
        j loop2

    sai2:
        move $t2, $t3
        addi $t0, $t0, -1
        j loop

    sai:  

        li $v0, 1
        move $a0, $t2
        syscall
        li $v0, 10
        syscall