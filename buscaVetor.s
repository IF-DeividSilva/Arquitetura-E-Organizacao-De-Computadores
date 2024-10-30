#int vetor[] = {3, 0, 1, 2, -6, -2, 4, 10, 3, 7, 8, -9, -15, -20, -87, -100}
#
#printf("Seja bem vindo! \nPor favor entre com um valor inteiro para pesquisar no vetor\n\n");
#scanf("%i", elemento);
#
#while(vetor[i] != -100){
#
#    if(vetor[i] == elemento){
#        printf("Elemento %i encontrado\n\n", elemento );
#        exit(0);
#    }
#
#    i++;
#}
#
#printf("Elemento não encontrado\n\n");
#exit(0);


.data 

vetor: .word 3 0 1 2 -6 -2 4 10 3 7 8 -9 -15 -20 -87 -100 # cria vetor
mensagem1: .asciiz " Seja bem vindo! \nPor favor entre com um valor inteiro para pesquisar no vetor\n\n"
mensagem2: .asciiz "Elemento nao encontrado\n"

.text
    main:
        li $s1, 0  # i=0
        li $s2, -100
        la $s3, vetor # recebe o endereco do primeiro elem do vetor

        # para mostrar string na tela mensagem2
        li $v0, 4
        la $a0, mensagem1
        syscall
        
        # pega o num
        li $v0, 5
        syscall

        move $t2, $v0

    while:
        add $t2, $t1, $s3    # salva o endereco em outro reg para não perder o inicial que fica em $s3
        lw $t0, 0($t2)       # salva em $t0 o elemento do vetor
        bne $t0, $t2, true   # caso o valor digitado seja igual a algum valor do vetor pula pra true
        bne $t0, $s2, sair   # compara se o valor do elemento é igual ao volor de k
        addi $s1, $s1, 1     # i++
        addi $t1, $t1, 4     # soma 4 para ir para o prox endereco
        j while

    true:
        li $v0, 1            # printar o valor 
        move $a0, $s1
        syscall
    
    sair:
        # para mostrar string na tela mensagem2
        li $v0, 4
        la $a0, mensagem2
        syscall

        li $v0, 10
        syscall

