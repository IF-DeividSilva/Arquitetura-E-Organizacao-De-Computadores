.data
string1: .asciiz "Hello World!"
valores: .word 10, 20,30

.text
la $t1, string1
lw $a0, 0($t1)
li $v0, 4
syscall
la $t2, valores
lw $t3, 0($t2)
slti $a0, $t3, 20
li $v0, 1
syscall
li $v0, 10
syscall