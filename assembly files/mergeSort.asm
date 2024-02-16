# Written by Gathik Jindal (IMT2023089)
# Email: gathik.jindal@iiitb.ac.in

.data
	space:			.asciiz		" "
	new_line:		.asciiz		"\n"
	m_num_of_elements:	.asciiz		"Number of elements: "
	m_starting_sort:	.asciiz		"\nStarting Sort:\n"
	m_printing_elements:	.asciiz		"\nPrinting Elements:\n"
	m_high_low:		.asciiz		"High & Low: "

.text
	j 	main
	
	main:
		la	$a0, m_num_of_elements
		jal	print_string
		
		jal	input				# now $v0 contains N
		move	$a0, $v0			# now $a0 has N
		move	$s0, $v0			# now $s0 also has N
		jal	take_inputs			# taking elements of the array
		addi	$gp, $gp, -4			# making space to store N
		sw	$s0, 0($gp)			# storing N

		la	$a0, m_starting_sort
		jal	print_string
		addi	$a0, $zero, 0			# storing low as 0
		lw	$a1, 0($gp)			# storing high as N
		addi	$a1, $a1, -1			# high = N - 1
		jal	merge_sort
		
		la	$a0, m_printing_elements
		jal	print_string		
		jal	print_array

		j	end
		
	
	merge:
		la	$s0, 4($gp)			# saving actual array base pointer in 	$s0 -> A[0]
		add	$s1, $a0, $zero			# saving low of the array in		$s1 -> low
		addi	$s2, $a1, 0			# saving mid of the array in 		$s2 -> mid
		addi	$s3, $a2, 0			# saving high of the array		$s3 -> high
							# NOTE to self: these are indices and
							# not the actual memory locations
		sub	$t0, $a2, $a0			# storing the length of the
		addi	$t0, $t0, 1			# B array in--				$t0
		
		mul	$t0, $t0, -4 			# getting the number ready		$t0 is now usable
		add	$gp, $gp, $t0			# allocated the space
		add	$s6, $gp, $zero			# pointer to base array			$s6 -> base of array B that I will modify
		
		addi	$s4, $s1, 0			# int lp = low;				$s4 -> lp
		addi	$s5, $s2, 1			# int rp = mid + 1;			$s5 -> rp
		
		
		
		merge_loop1:				# while (lp <= mid && rp <= high)
		mul	$t0, $s4, 4			# getting lp*4
		add	$t0, $s0, $t0			# &arr[lp]				$t0 -> &arr[lp]
		lw	$t0, 0($t0)			# got value of arr[lp]			$t0 -> arr[lp]
		mul	$t1, $s5, 4			# getting rp*4
		add	$t1, $s0, $t1			# &arr[rp]				$t1 -> &arr[rp]
		lw	$t1, 0($t1)			# got value of arr[rp]			$t1 -> arr[rp]

		slt	$t2, $t1, $t0			# if arr[lp] > arr[rp] $t2 = 1		$t2 -> arr[lp] > arr[rp]
		beq	$t2, 1, merge_loop1_else	# else
		
		sw	$t0, 0($s6)			# b.push_back(arr[lp])
		addi	$s6, $s6, 4			# $s6++					$s6 -> $s6 + 1
		addi	$s4, $s4, 1			# lp++					$s4 -> $s4(lp) + 1
		j	merge_loop1_check		# skipping the else
		
		merge_loop1_else:
		sw	$t1, 0($s6)			# b.push_back(arr[rp])
		addi	$s6, $s6, 4			# $s6++					$s6 -> $s6 + 1
		addi	$s5, $s5, 1			# rp++					$s5 -> $s5(rp) + 1
		
		merge_loop1_check:
		slt	$t0, $s2, $s4			# if mid < lp				$t0 -> mid < lp
		slt	$t1, $s3, $s5			# if high < rp				$t2 -> high < rp
		add	$t0, $t0, $t1			# doing && condition			$t0 -> $t1 + $t0
		beq	$t0, $zero, merge_loop1		# repeating while loop
		
		
		merge_loop2:				# while (lp <= mid)
		addi	$t0, $s2, 1			# mid + 1 in $t0			$t0 -> mid + 1
		slt	$t0, $s4, $t0			# if lp <= mid				$t0 -> lp <= mid
		beq	$t0, $zero, merge_loop3		# skipping if condition fails
		
		mul	$t0, $s4, 4			# getting lp*4
		add	$t0, $s0, $t0			# &arr[lp]				$t0 -> &arr[lp]
		lw	$t0, 0($t0)			# got value of arr[lp]			$t0 -> arr[lp]
		sw	$t0, 0($s6)			# b.push_back(arr[lp])
		addi	$s6, $s6, 4			# $s6++					$s6 -> $s6 + 1
		addi	$s4, $s4, 1			# lp++					$s4 -> $s4(lp) + 1
		j	merge_loop2			# repeating loop	
		
		
		merge_loop3:				# while (rp <= high)
		slt	$t0, $s3, $s5			# if high < rp				$t0 -> $s3(high) < $s5(rp)
		bne	$t0, $zero, merge_loop4		# skipping if condition fails

		mul	$t1, $s5, 4			# getting rp*4
		add	$t1, $s0, $t1			# &arr[rp]				$t1 -> &arr[rp]
		lw	$t1, 0($t1)			# got value of arr[rp]			$t1 -> arr[rp]
		sw	$t1, 0($s6)			# b.push_back(arr[rp])
		addi	$s6, $s6, 4			# $s6++					$s6 -> $s6 + 1
		addi	$s5, $s5, 1			# rp++					$s5 -> $s5(rp) + 1
		j	merge_loop3			# repeating loop

		
		merge_loop4:
		addi	$s4, $s1, 0			# lp = low				$s4(lp) -> $s1(low)
							# $gp has the base of array B
		merge_loop4_loop:
		lw	$t0, 0($gp)			# loading the word
		mul	$t1, $s4, 4			# got index				$t1 -> index
		add	$t1, $t1, $s0			# got &arr[lp]				$t1 -> &arr[i]
		sw	$t0, 0($t1)			# saved word
		addi	$s4, $s4, 1			# incrementing $s4			$s4(lp) -> $s4 + 1
		addi	$gp, $gp, 4
		slt	$t0, $s3, $s4			# if high < lp				$t0 -> $s3(high) < $s4(lp)
		beq	$t0, $zero, merge_loop4_loop	# loop
		
		jr	$ra				# return;
		
	
	merge_sort:
		addi	$sp, $sp, -4			# making space for return addr
		sw	$ra, 0($sp)			# stored value of $ra

		addi	$s0, $a0, 0			# storing value of "low" in $s0
		addi	$s1, $a1, 0			# storing value of "high" in $s1
		
		la	$a0, m_high_low			# printing the string for debugging
		jal	print_string
		addi	$a0, $s1, 0
		jal	print_integer
		la	$a0, space
		jal	print_string
		addi	$a0, $s0, 0
		jal	print_integer
		la	$a0, new_line
		jal	print_string
		
		slt	$t1, $s0, $s1			# if low < high return, $t1 = 1
		beq	$t1, 1, cont_merge_sort
		
		lw	$ra, 0($sp)			# loading return address
		addi	$sp, $sp, 4			# exiting recursion
		jr	$ra
		
		cont_merge_sort:
		add	$t2, $s0, $s1			# $t2 = $s0 + $s1
		div	$t2, $t2, 2			# $t2 /= 2
		
		addi	$sp, $sp, -12			# allocating space for the three variables we need
		sw	$s0, 0($sp)			# saving "low"
		sw	$s1, 4($sp)			# saving "high"
		sw	$t2, 8($sp)			# saving "mid"
		
		addi	$a0, $s0, 0			# initializing arguments for first call
		addi	$a1, $t2, 0
		jal	merge_sort
		
		lw	$a0, 8($sp)			# doing same for the second
		addi	$a0, $a0, 1			# mid + 1
		lw	$a1, 4($sp)			# high
		jal	merge_sort
		
		lw	$a0, 0($sp)			# calling merge function
		lw	$a1, 8($sp)			# the arguments given are in same order as I have written
		lw	$a2, 4($sp)			# in the C++ program
		jal 	merge
		
		addi	$sp, $sp, 12			# no need for this space anymore
		lw	$ra, 0($sp)			# restoring return address
		addi	$sp, $sp, 4			# deallocating spce
		jr	$ra

	end:
		li 	$v0, 10				# system command for "exit"
			syscall
	
	take_inputs:
		addi	$sp, $sp, -4			# allocating space for return address
		sw	$ra, 0($sp)			# saving the return address

		slti	$t0, $a0, 1			# checking if n < 1
		beq	$t0, 1, exit_take_inputs
		
		jal	input
		addi	$gp, $gp, -4 			# allocating space in the static heap
		sw 	$v0, 0($gp)			# adding the value
		addi	$a0, $a0, -1			# decrementing the value passed
		jal	take_inputs			# calling input()
		
		exit_take_inputs:
		lw	$ra, 0($sp)			# restoring $ra
		addi	$sp, $sp, 4			# if so we deallocate the space and return
		jr	$ra				# returning to callee
	
	print_array:
		addi	$sp, $sp, -4			# storing the return address
		sw	$ra, 0($sp)
		
		lw	$t1, 0($gp)			# $t1 will now contain the number of elements in the array
		loop_print_array:
		slti	$t0, $t1, 1			# checking if there is anyting to print
		beq	$t0, 1, exit_print_array
		
		mul	$t2, $t1, 4			# $t2 contains the index*4 to fetch the number from
		add	$t2, $gp, $t2			# memory locatoin of the number
		lw	$a0, 0($t2)
		jal 	print_integer
		la	$a0, space			# printing a newline
		jal	print_string
		addi	$t1, $t1, -1			# we finished reading one element
		j 	loop_print_array

		exit_print_array:
		la	$a0, new_line
		jal	print_string
		lw	$ra, 0($sp)
		addi	$sp, $sp, 4			# deallocating space
		jr	$ra				# returning to callee
		
	
	input:
		li	$v0, 5				# system command for "read integer"
			syscall				# the integer read is stored in $v0
		jr	$ra				# jumping back to caller. Additionally the return value is already stored in $v0
	
	print_integer:
		li 	$v0, 1				# system command for "print integer"
			syscall				# the integer to print is already in $a0
		li	$v0, 4				# printing a string (null terminated)
		jr	$ra				# returning to callee
	
	print_string:
		li	$v0, 4
			syscall
		jr	$ra
