# int folha(int g, int h, int i, int j){
#
#         int f;
#
#         f = (g + h) - (i + j);
#
#         return f;
#
# }
.data

.text

    main:
        # adiciona os argumentos da funcao nos registradores de argumentos ($a)
        li $a0,1
        li $a1,2
        li $a2,3
        li $a3,4
        
        # Program Counter (pc) controla o fluxo das instruçoes do programa
        # aponta para proxima instrucao a ser executada
        # jal guarda no $ra o endereco da prox instrucao (PC+4)
        
        jal folha
        

        move $a0, $v0

        li $v0, 1
        syscall

        li $v0, 10
        syscall
        
        

    folha:
        add $t0, $a0, $a1
        add $t1, $a2, $a3
        sub $t3, $t0, $t1

        move $v0, $t3  # returm
        
        # salta para um endereco armazenado dentro de um registrador
        jr $ra