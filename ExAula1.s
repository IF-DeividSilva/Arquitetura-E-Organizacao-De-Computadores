.data
    mensagem1: .asciiz "Por favor, digite o primeiro numero:\n";         # informar que é uma cadeia de caracteres 
    mansagem2: .asciiz "Por favor, digite o segundo numero:\n";
.text

main: 
    li $v0, 4           # Para exibir mensagem na tela 
    la $a0, mensagem1   #Carrega endereco para o registrador
    syscall


    li $v0, 5           # Pegar inteiro do teclado
    syscall             # $v0 = valor digitado
    
    move $t0, $v0

    li $v0, 4           # Para exibir mensagem na tela 
    la $a0, mansagem2   #Carrega endereco para o registrador
    syscall

    li $v0, 5           # Pegar inteiro do teclado
    syscall             # $v0 = valor digitado

    move $t1, $v0



#    li $t0, 10         # Carrega um valor em um registrador ("loud imediato") 
#    li $t1, 8          # Carrega um valor em um registrador
    add $t2, $t0, $t1   # soma t0 com t1 e coloca o resultado em t2
    sub $t3, $t0, $t1   # subitrai t0 e t1 e armazena em t3
    mul $t4, $t0, $t1   # multiplica t0 e t1 e armazena em t4
    div $t5 , $t0, $t1  # divide t0 e t1 e armazena em t5


