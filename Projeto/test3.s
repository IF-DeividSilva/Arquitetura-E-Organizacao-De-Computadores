.data
.text
    main:
        addi $t0, $zero, 6   
        addi $t1, $zero, 1
        addi $t2, $zero, 0  

        sll $s1, $t0, 1      
        lui $s2, 20         

        and $t4, $t2, $t1    #  (1 AND 0 = 0)
        or $t5, $t2, $t1     #  (1 OR 0 = 1)

        li $v0, 1            
        addi $a0, $s1, 0        
        syscall   

        li $v0, 1            
        addi $a0, $s2, 0        
        syscall             

        addi $a0, $t4, 0      
        syscall              

        addi $a0, $t5, 0       
        syscall             

        li $v0, 10          
        syscall              
