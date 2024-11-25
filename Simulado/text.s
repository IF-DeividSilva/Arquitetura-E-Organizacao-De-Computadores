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
    msg1: .asciiz "Digite a base do triangulo: "
    msg2: .asciiz "Digite a altura do triangulo: "
    msg3: .asciiz "A area do triangulo eh: "

.text
    main:
        li $v0, 4
        la $a0, msg1
        syscall

        li $v0, 5 
        syscall
        move $t0, $v0

        li $v0, 4
        la $a0, msg2
        syscall

        li $v0, 5 
        syscall
        move $t1, $v0

        move $a0, $t0
        move $a1, $t1

        jal Area

        move $t3, $v0

        li $v0, 4
        la $a0, msg3
        syscall
        
        li $v0, 1
        move $a0, $t3
        syscall

        li $v0, 10
        syscall
#float calculaAreaTriangulo(int base, int altura) {
#     int parcial = base * altura;
#     int resultado =  DivPorDois(parcial);
#
#     return resultado;
#}
    Area:
        addi $sp, $sp, -8
        sw $s0, 0($sp)
        sw $ra, 4($sp)

        mul $s0, $a0, $a1
        move $a0, $s0

        jal DividePorDois

        lw $s0, 0($sp)
        lw $ra, 4($sp)

        jr $ra
#
#   float DivPorDois(int res) {  
#    return (res / 2);
    DividePorDois:
        addi $t7, $zero, 2
        div $v0, $a0, $t7

        jr $ra
