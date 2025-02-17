.data
    msg: .asciiz "O primeiro numero eh menor"  

.text
    main:
        addi $t0, $zero, 8   
        addi $t1, $zero, 12  
        
        slt $t2, $t0, $t1    
        la $a0, msg          
        
        li $v0, 4            
        syscall    


    exit:
        li $v0, 10           
        syscall              
