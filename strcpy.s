
.data

    MSG1: .asciiz "A ser copiada\n\n"
    MSG2:
.text
main:

       la $a1, MSG1                   # y[]
       la $a0, MSG2                   # x[]

strcpy:

       addi $sp, $sp, -4             # ajusta pilha
       sw $s0, 0($sp)

       add $s0, $zero, $zero   

L1:
     
       add $t1, $s0, $a1             # endereço de y[i] em $t1
       lb $t2, 0($t1)                  # $t2 = y[i]

       add $t3, $s0, $a0             # endereço de x[i] em $t3
       sb $t2, 0($t3)                   # x[i] = y[i]

       beq $t2, $zero, L2           # se y[i] == 0 vai para L2

       addi $s0, $s0, 1               # i = i + 1
       j L1                                  

L2:
       lw $s0, 0($sp)                   # y[i] == 0 fim da string, restaura s0
       addi $sp, $sp, 4                # retira 1 da palavra da pilha
       jr SAIR

SAIR:
   
      addi $v0, $zero, 4
      syscall