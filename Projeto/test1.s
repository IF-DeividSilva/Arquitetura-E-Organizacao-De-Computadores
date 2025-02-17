.data
.text
    main:
        addi $t0, $zero, 4   
        addi $t1, $zero, 5   
        mult $t2, $t0, $t1        
        
        li $v0, 1            
        addi $a0, $t2, 0        
        syscall             