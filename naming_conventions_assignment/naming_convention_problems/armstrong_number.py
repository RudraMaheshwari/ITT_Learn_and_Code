def armstrong_calculation(number):
    # Initializing Sum and Number of Digits
    armstrong_sum = 0
    digit_count = 0

    # Calculating Number of individual digits
    working_number = number
    while working_number > 0:
        digit_count = digit_count + 1
        working_number = working_number // 10

    # Finding Armstrong Number
    working_number = number
    for number in range(1, working_number + 1):
        digit = working_number % 10
        armstrong_sum = armstrong_sum + (digit ** digit_count)
        working_number //= 10
    return armstrong_sum

# End of Function

# User Input
input_number = int(input("\nPlease Enter the Number to Check for Armstrong: "))

if (input_number == armstrong_calculation(input_number)):
    print("\n %d is Armstrong Number.\n" % input_number)
else:
    print("\n %d is Not a Armstrong Number.\n" % input_number)
