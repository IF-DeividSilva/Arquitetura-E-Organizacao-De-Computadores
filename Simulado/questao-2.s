.data

.text

main:
    # Leitura de 'a'
    li $v0, 5
    syscall
    move $t0, $v0 # t0 --> a
    
    # Leitura de 'b'
    li $v0, 5
    syscall   
    move $t1, $v0 # t1 --> b

    # Inicialização de 'x'
    move $t3, $zero # t3 --> x

    # Verificação se 'a < 0'
    slt $t4, $t0, $zero
    
    # Verificação se 'b >= 10'
    li $t5, 9
    slt $t6, $t5, $t1
    beq $t4, $t6, set_x

    # Impressão de 'x' (caso falso)
    li $v0, 1
    move $a0, $t3
    syscall
    j exit

set_x:
    # Definir 'x' como 1
    li $t3, 1

    # Impressão de 'x' (caso verdadeiro)
    li $v0, 1
    move $a0, $t3
    syscall

exit:
    # Finalizar o programa
    li $v0, 10
    syscall
