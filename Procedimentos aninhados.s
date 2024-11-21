#include <stdio.h>
#
#   float DivPorDois(int res) {  
#    return (res / 2);
#}
#float calculaAreaTriangulo(int base, int altura) {
#     int parcial = base * altura;
#     int resultado =  DivPorDois(parcial);
#
#     return resultado;
#}
#
#int main() {
#    float base, altura;
#    
#    printf("Digite a base do triângulo: ");
#    scanf("%d", &base);
#    
#    printf("Digite a altura do triângulo: ");
#    scanf("%d", &altura);
#    
#    float area = calculaAreaTriangulo(base, altura);
#    
#    printf("A area do triangulo eh: %d\n", area);
#    
#    return 0;
#}
.data

base: .word 0
altura: .word 0
area: .word 0

mensagem1: .asciiz "Digite a base do triangulo: \n"
mensagem2: .asciiz "Digite a altura do triangulo: \n"
mensagem3: .asciiz "A area do triangulo eh: "


.text
    DivPorDois:
        addi $t0, $t0,2
        div $v0, $a0, $t0

        jr $ra # retorna pra area



    Area:
        # alocar mem
        add $sp, $sp, -8
        sw $s0, 4($sp)
        sw $ra, 8($sp)

        mul $s0, $a0,$a1
        move $a0 , $s0

        jal DivPorDois

        lw $ra, 8($sp)
        lw $s0, 4($sp)

        #desalocar mem
        add $sp, $sp, 8

        jr $ra

    main:
        # para mostrar a string na tela
        li $v0, 4 
        la $a0, mensagem1
        syscall

        # pega o num da base
        li $v0, 5
        syscall

        move $t2, $v0

        # mostrar a string na tela
        li $v0, 4
        la $a0, mensagem2
        syscall

        # pega o num da base
        li $v0, 5
        syscall

        move $t3, $v0

        move $a0, $t2
        move $a1, $t3


        jal Area
        move $t5, $v0

        # para mostrar a string na tela
        li $v0, 4 
        la $a0, mensagem3
        syscall

        li $v0, 4
        move $a0, $t5
    
        li $v0, 10
        syscall





