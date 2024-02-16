.data 
  size: 
    .word 0x00000000
    
  head:
    .word 0x00000000
    
  promptSize:
    .asciiz "Enter the size of the Linked List:\n"
  
  promptEdge:
    .asciiz "Enter the connections:\n"
    
  promptTo:
    .asciiz "To node :  "
    
  promptFrom:
    .asciiz "From node :  "
    
  promptCheck:
    .asciiz "Checking for cycles now."
    
  promptNoC:
    .asciiz "\nNo cycles found.\n\nPrinting the nodes:\n"
    
  promptYesC:
    .asciiz "\nA cycle was found after node "
    
  promptBreak:  
    .asciiz "\n\nBreaking the cycle now.\n\nPrinting the nodes:\n"
    
  nl:
    .asciiz "\n"
  
  
.text
  main:
    jal makeLL            # Calling a procedure to prepare a linked list from user-input
    lw $a0, head          # Readying arguments for next procedure
    jal FloydCycleFind    # Checking for cycles
    beq $v1, $0, nocycle
    move $a0, $v0         # Readying arguments for next procedure
    lw $a1, head          #    "         "      "    "      "
    jal FloydCycleNode    # Finds the node where the cycle starts
    
    li $v0, 4
    la $a0, promptYesC    # Displays it to the user
    syscall
    move $a0, $v1         # Printing value of node to be connected to NULL 
    li $v0, 1 
    syscall 

    li $v0, 4
    la $a0, promptBreak    # Starts to break the cycle
    syscall 
    
    move $a0, $v1          # Readying arguments for next procedure        
    jal BreakCyclePrint    # Breaking cycle and printing the value too
    j endProg              # Procedure to end program
    
    
  nocycle:
  
    li $v0, 4
    la $a0, promptNoC      # Displays to the user
    syscall 
    la $a0, head           # Readying arguments for next procedure
    jal printLL            # Calling a procedure to print linked-list
    j endProg              # Procedure to end program



  makeLL: # This is to build the Linked List and return it's head
  
    # Here I ask for the size of LL
    li $v0, 4
    la $a0, promptSize
    syscall 
    
    # Here I get and store the size of LL
    li $v0, 5
    syscall 
    sw $v0, size 
    
    # Malloc the required space in the heap
    lw $v0, size 
    addiu $v0, $v0, 1 # Extra unit of space
    sll $v0, $v0, 2
    move $a0, $v0
    li $v0, 9 # Mallocing the required space from the heap
    syscall
    sw $v0, head
    
    # Set the node values
    add $t1, $0, 0
    lw $t2, size
    lw $t3, head
    
    startValMakerLoop: # Loop to set all nodes to their corresponding values and their next nodes to null
      sw $t1, 0($t3)
      addiu $t1, $t1, 1
      addiu $t3, $t3, 4
      sw $0, 0($t3)
      addiu $t3, $t3, 4
      subiu $t2, $t2, 1
      bnez $t2, startValMakerLoop
    
    # Making edges
    li $v0, 4
    la $a0, promptEdge
    syscall 
    
    lw $t1, size 
    lw $t0, head
    
    startEdgeMakerLoop:
      beq $t1, $0, return
 
      li $v0, 4
      la $a0, promptFrom # From address of edge
      syscall 
                
      li $v0, 5
      syscall 
      move $t2, $v0
      
      li $v0, 4
      la $a0, promptTo  # To address of edge
      syscall 
      
      li $v0, 5
      syscall 
      move $t3, $v0
      
      sll $t2, $t2, 3
      addiu $t2, $t2, 4 # Preparing pointer to faddress
      add $t2, $t2, $t0
      
      sll $t3, $t3, 3
      add $t3, $t3, $t0 # Preparing pointer to taddress
      
      sw $t3, 0($t2) # Creating the edge
                  
      subiu   $t1, $t1, 1 
      j startEdgeMakerLoop    
      
    return:  #Return
       jr $ra      
  
  
  
  printLL: # This is to print a linked list in order
  
    move $a1, $ra # Remembering current return address 
    lw $t0, 0($a0) # Dereferencing argument
    
    startPrintLoop: # Iterating through linked list
      beqz $t0, returna1
      lw $a0, 0($t0)
      jal printInt # Procedure to print value
      lw $t1, 4($t0)
      move $t0, $t1
      j startPrintLoop
      
    returna1:  #Return
       jr $a1    
       
         
                         
  printInt: # This is to print integer stored in $a0
  
    li $v0, 1 
    syscall 
    
    li $v0, 4
    la $a0, nl
    syscall 

    jr $ra



  FloydCycleFind:
  
    lw $t0, 4($a0)               # fp = (head);
    lw $t1, 4($a0)               # sp = (head);
        
    startFindLoop:
      beq $t0, $0, exitFindLoop  # while (fp != NULL){
      lw $t0, 4($t0)             # fp = fp -> next;
      beq $t0, $0, exitFindLoop  # if (fp == NULL) break;               
      lw $t1, 4($t1)             # sp = sp -> next;
      lw $t0, 4($t0)             # fp = fp -> next;
      beq $t0, $t1, exitFindLoop # if (fp == sp) break;
      j startFindLoop            # }
      
    exitFindLoop:
      move $v0, $t1
      seq  $v1, $t0, $t1
      jr $ra
  
  
  FloydCycleNode:
    
    lw $t0, 4($a0)			# p1 = fp -> next;
    lw $t1, 4($a1)			# p2 = head;
    lw $t1, 4($t1)			# p2 = p2 -> next;
    lw $t2, 0($a0)			# val = fp -> value;
    
    startNodeLoop:
    	beq $t0, $t1, exitNodeLoop	# while(p1 != p2){
    	lw $t2, 0($t0)                 # val = p1 -> val;
    	lw $t0, 4($t0)			# p1 = p1 -> next;
    	lw $t1, 4($t1)			# p2 = p2 -> next;
    	j startNodeLoop			# }
    	
    exitNodeLoop:
    	move $v1, $t2			# return val;  	    
    	jr $ra
  
  
  BreakCyclePrint:

    move $a1, $ra
    
    lw $t0, head			# p1 = head -> next;
    lw $t0, 4($t0)
    lw $t1, head			# val = head -> value;
    lw $t1, 0($t1)
    move $t3, $a0			# breakPoint = argument;
        
    startBreakLoop:
    	move $a0, $t1
    	jal printInt			# print(val)
        beq $t1, $t3, endBreakLoop	# while (val != breakPoint){
        move $t2, $t0			# p2 = p1;
        lw $t1, 0($t0)			# val = p1 -> value;
        lw $t0, 4($t0)			# p1 = p1 -> next;
	j startBreakLoop		# }
	
    endBreakLoop:
    	sw $0, 4($t2)
    	jr $a1

  endProg: #This is to exit the program
    li $v0, 10 
    syscall
   

