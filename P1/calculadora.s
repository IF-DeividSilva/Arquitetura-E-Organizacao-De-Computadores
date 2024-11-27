.data
    mensagem1: .asciiz " Menu \n 1 seleciona a soma.\n 2 seleciona a subtração.\n 3 seleciona a multiplicação.\n 4 seleciona a divisão.\n 5 encerra o programa.\n"
    mensagem2: .asciiz " \n Digite o primeiro num:\n"
    mensagem3: .asciiz " Digite o segundo num: \n"
    mensagem4: .asciiz " Opcao invalida, tente novamente \n "
    mensagem5: .asciiz " \n Saindo...\n"
    mensagem6: .asciiz " Resultado: "

.text
    main:
        # para mostrar string na tela mensagem2
        li $v0, 4
        la $a0, mensagem2
        syscall

        # pega o primeiro num
        li $v0, 5
        syscall

        move $t1, $v0

        # para mostrar string na tela 
        li $v0, 4
        la $a0, mensagem3
        syscall

        # pega o segundo num
        li $v0, 5
        syscall

        move $t2, $v0

        # para mostrar string na tela 
        li $v0, 4
        la $a0, mensagem1
        syscall

        # para pegar a opsao do usuario
        li $v0, 5
        syscall

        move $s1, $v0

        # verificação de opcao selecionada no menu
        addi $s2, 5
        beq $s1, $s2, end
        
        addi $s3, 1
        beq $s1, $s3,    soma

        addi $s4, 2 
        beq $s1, $s4, subracao

        addi $s5, 3
        beq $s1, $s5, multiplicacao

        addi $s7, 4
        beq $s1, $s7, divisao

        j default

    soma:
        add $t3, $t1, $t2
        j print

    subracao:
        sub $t3, $t1, $t2
        j print
    
    multiplicacao: 
        mul $t3, $t1, $t2
        j print

    divisao:
        div $t3, $t1, $t2
        j print

    default:
        # para mostrar string na tela 
        li $v0, 4
        la $a0, mensagem4
        syscall

        j end

    print:
        # para mostrar string na tela 
        li $v0, 4
        la $a0, mensagem6
        syscall

        # para mostrar resultado na tela 
        li $v0, 1
        add  $a0, $zero, $t3
        syscall

    end:
        # para mostrar string na tela 
        li $v0, 4
        la $a0, mensagem5
        syscall

        li $v0, 10
        syscall   







