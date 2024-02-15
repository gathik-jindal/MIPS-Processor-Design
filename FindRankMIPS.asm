.data
	n: 
		.word 0			#Size of the array
	k: 	
		.word 0			#Rank
	array: 	
		.space 100		#array initialization

	prompt1: 
		.asciiz "Please enter the size of the array: "
	prompt2: 
		.asciiz "Please enter the rank: "
	prompt3: 
		.asciiz "Please enter the elements: "
	prompt4: 
		.asciiz "The element is "
.text
main:
	#This is our main program from C file.
	
	
	#Input prompt for size of array..
	la $a0, prompt1
	li $v0, 4
	syscall
	
	#Input
	li $v0, 5
	syscall
	
	sw $v0, n
	
	#Input prompt for rank..
	la $a0, prompt2
	li $v0, 4
	syscall
	
	li $v0, 5
	syscall
	
	sw $v0, k
	
	#Initializing for loop:
	#Loading i=0 to $s0 and n to $s1
	li $s0, 0
	lw $s1, n
	
	#Input prompt for array elements..
	la $a0, prompt3
	li $v0, 4
	syscall
	
	#Condition check
  read: bge $s0, $s1, exit
  
    	#Input to read array elements
	li $v0, 5
	syscall
	
	#Calculating the address of the ith index and storing the input read in that location
	sll $t2, $s0, 2			#Multiplying i by 4
	sw $v0, array($t2)		#Storing the input by dereferencing the address
	
	#Increment i
	addi $s0, $s0, 1
	
	#Repeat the loop
	j read
	
	
	#target address if condition of loop is false
	exit: 
	
	#Initialize arguments for findrank procedure
	la $a0, array 			#Base address of array
	move $a1, $0			#s(start)<=0
	sub $a2, $s1, 1			#e(end)<=n-1
	lw $t5, k			
	move $a3, $t5			#k(rank)
	
	#Jump to procedure findrank
	jal findrank
	
	#findrank returns the index..
	#Caclulating the element at that index:
	sll $t0, $v0, 2
	
	#Print the element:
	la $a0, prompt4
	li $v0, 4
	syscall
	
	lw $a0, array($t0)
	li $v0, 1
	syscall
	
	#Exiting the program
	li $v0, 10
	syscall
rand:	#random number generator using time
	
	#Pushing return address onto the stack
	subi $sp, $sp, 4
    	sw $ra, ($sp)
    	
    	#using time function
	li $v0, 30
	syscall
	
	#Generating the random number 
	abs  $a0, $a0
	sll $a0, $a0, 15
	srl $a0, $a0, 15
	sll $a0, $a0, 12
	rem $a0, $a0, 14352127
	
	#Moving the return value to $v0
	move $v0, $a0
	
	#Popping the stack and using to return address to jump back.
	lw $ra, ($sp)
	addi $sp, $sp, 4
	jr $ra
	
swap:	#for swapping two elements in an array.

	#Pushing return address onto the stack
	subi $sp, $sp, 4
    	sw $ra, ($sp)
	
	#Swap
	lw $t7, 0($a0)
	lw $t8, 0($a1)
	sw $t7, 0($a1)
	sw $t8, 0($a0)
	
	#Popping the stack and using to return address to jump back.
	lw $ra, ($sp)
	addi $sp, $sp, 4
	jr $ra
partition:	#This is the partition function from our C program.

	#Pushing return address onto the stack
		subi $sp, $sp, 4
    		sw $ra, ($sp)
    		
    		
		move $t0, $a0 		#address of first element
		move $s7, $a1		#storing the value of s
	   	addi $t1, $a1, 1 	#loading i=s+1
		addi $t2, $a2, 0 	#loading j=e
		
		#Outer loop in the partition function.
		#Condition check: branch if i is greater than j
	loop:	bgt $t1, $t2, goto
				
				#Inner Loop 1
				#Condition check: branch if i is greater than j
			inner1: bgt $t1, $t2, inner2
			
				#Calculating the element at ith index and first element to compare a[i] and a[s]
				sll $t3, $t1, 2
				add $t5, $t3, $t0
				lw $t3, 0($t5)
				sll $t4, $s7, 2
				add $t6, $t4, $t0
				lw $t4, 0($t6)
				
				#Condition check 2: branch if a[i]>a[j]
				bgt $t3, $t4, inner2
				
				#If both conditions return true, increment i and loop again.
				addi $t1, $t1, 1
				j inner1
				
				#Inner loop 2, executed after one of the conditions in inner loop 1 fails.
				#Condition check: branch if i is greater than j
			inner2: bgt $t1, $t2, cond
			
				#Calculating the element at jth index and first element to compare a[j] and a[s]
				sll $t3, $t2, 2
				add $t7, $t3, $t0
				lw $t3, 0($t7)
				sll $t4, $s7, 2
				add $t6, $t4, $t0
				lw $t4, 0($t6)
				
				##Condition check 2: branch if a[j]<=a[s]
				ble $t3, $t4, cond
				#If both onditions return true, decrement j
				subi $t2, $t2, 1
				j inner2
				
				#Executed after the two loops
				#Branch if i is greater than or equal to j
			cond:	bge $t1, $t2, cont
				#Swap ith and jth element if true
				move $a0, $t5
				move $a1, $t7
				jal swap
				
				#increment i and decrement j
				addi $t1, $t1, 1
				subi $t2, $t2, 1
			cont:	j loop
			
		#If outer loop condition is false, swap elements at first index and i-1th index.
	goto:
		
		subi $t4, $t1, 1
		sll $t3, $t4, 2
		add $a0, $t3, $t0
		sll $t3, $s7, 2
		add $a1, $t3, $t0
		jal swap		#swap
		
		#return value
		move $v0, $t2
		
		#Popping the stack and using to return address to jump back.
		lw $ra, ($sp)
		addi $sp, $sp, 4
		jr $ra
findrank:
	#Pushing return address onto the stack
	subi $sp, $sp, 4
    	sw $ra, ($sp)
    	
	move $s2, $a0	#Loading base address
	move $s3, $a1	#Loading start
	move $s4, $a2	#Loading end
	move $s5, $a3	#Laoding rank
	
	
	#If condition for checking i<j
	bge $s3, $s4, else
	
	#Calling rand procedure
	jal rand
	
	#Calculating the pivot index
	sub $t9, $s4, $s3
	addi $t9, $t9, 1
	rem $t9, $v0, $t9
	add $t9, $t9, $s3
	
	#Arguments for swapping pivot element with first element
	sll $t9, $t9, 2
	add $a0, $t9, $s2
	sll $t9, $s3, 2
	add $a1, $s2, $t9
	#Swap
	jal swap
	
	#Arguments for partition
	move $a0, $s2		#Base address
	move $a1, $s3		#start
	move $a2, $s4		#end
	jal partition
	
	#Using return value k..
	move $t1, $v0
	sub $t1, $s4, $t1
	addi $t1, $t1, 1
	
	#Check if rank==e-k+1
	bne $s5, $t1, check2
	#Found the element
	#Popping the stack and return..
	lw $ra, ($sp)
	addi $sp, $sp, 4
	jr $ra
	
	#Check if rank<e-k+1
 check2:bge $s5, $t1, check3
 	#Arguments for recursively calling findrank
	move $a0,  $s2
	addi $a1, $v0, 1	#start value is now k+1
	move $a2, $s4
	move $a3, $s5
	jal findrank	#Recursive call
	
	#Pop the stack and return
	lw $ra, ($sp)
	addi $sp, $sp, 4
	jr $ra
	
	#Else
 check3: 
 	#Arguments for calling find rank recursively
 	move $a0, $s2
 	move $a1, $s3
 	subi $a2, $v0, 1		#end value is now rank-e+k-1
 	sub $a3, $s5, $t1
 	jal findrank			#Recursive call
	
	#Pop the stack and return
  	lw $ra, ($sp)
	addi $sp, $sp, 4
 	jr $ra	
	
	#Else of the first branch
   else:
   	#Return start value
   	move $v0, $s3
   	
   	#Pop the stack and return
   	lw $ra, ($sp)
	addi $sp, $sp, 4
   	jr $ra

	
