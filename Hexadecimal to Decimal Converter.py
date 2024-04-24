'''
This script provides functionality to convert a formatted hexadecimal number to its decimal representation based on a given format string (UX.Y or SX.Y), where U indicates unsigned and S indicates signed. 

Some Background:

1. U X.Y: Unsigned
    U X.Y represents the X-digit integer part and Y-digit fractional part in X+Y bits
    e.g., U 4.3 → 1 LSB = 0.125 (〖1/2〗^3), representing a number from 0 to 15.875
    0b 00001100 U4.3 gives 1.5
2. S X.Y: Signed
    S X.Y represents the 1-digit signed part, X-digit integer part and Y-digit fractional part in 1+X+Y bits in 2s complement
    e.g., S 4.3 → 1 LSB = 0.125 (〖1/2〗^3), representing a number from -16 to 15.875
    0b 00001100 S4.3 gives 1.5
    0b 11110100 S4.3 gives -1.5

These two formatted Hex humber is widely used for converting formatted hexadecimal number read from SSS automotive sensors's registers


Functions:
0. `is_valid_hexadecimal(input_str)`: Checks if the input string is a valid char of a Hex Number
1. `parse_X_Y_format(format_str)`: Parses the format string (UX.Y or SX.Y) to extract the number of integer and fractional bits, and calculates the total number of bits.
2. `generate_value_range(int_bits, frac_bits, total_bits)`: Generates the value range based on the number of integer and fractional bits (not used in the main function).
3. `check_hex_num(hex_num, total_bits)`: Checks if the hexadecimal number is within the specified number of total bits.
4. `bin_to_decimal(binary_num, int_bits, frac_bits)`: Converts a binary number to its decimal representation (not used in the main function).
5. `hex_to_decimal(hex_num, int_bits, frac_bits, total_bits)`: Converts a hexadecimal number to its decimal representation. There are two versions of this function, one with clearer code structure (hex_to_decimal_2).
6. `get_valid_format()`: Prompts the user to input the format string (UX.Y or SX.Y) and validates it.
7. `get_valid_hexadecimal(total_bits)`: Prompts the user to input a hexadecimal number and validates it against the specified total bits.
8. `main()`: Main function that orchestrates the conversion process by getting the format string and hexadecimal number from the user, then converting the hexadecimal number to its decimal representation.

Usage:
1. Run the script.
2. Enter the format string (e.g., U9.8 or S10.0) when prompted.
3. Enter the hexadecimal number (without '0x' prefix) when prompted.
4. The script will then output the decimal representation of the provided hexadecimal number based on the specified format.
5. The user can repeat the process to convert more hexadecimal numbers with different formats.

Writen by Liubingtao0513@Gmail.com
'''

def is_valid_hexadecimal(input_str): # 0

    valid_chars = set("0123456789ABCDEFabcdef")
    return all(char in valid_chars for char in input_str)

def parse_X_Y_format(format_str): # 1

    sign = format_str[0]  # Extract (U or S)
    if sign not in ['U', 'S']:
        raise ValueError("Invalid format. Please use either U or S as the sign.")
    
    parts = format_str[1:].split('.')
    if len(parts) != 2:
        raise ValueError("Invalid format. Please use the format UX.Y or SX.Y")
    
    int_bits = int(parts[0])
    frac_bits = int(parts[1])

    if sign == 'U':
        total_bits = int_bits+frac_bits
    
    elif sign == 'S':
        total_bits = int_bits + frac_bits + 1

    return int_bits, frac_bits, total_bits


def generate_value_range(int_bits, frac_bits, total_bits): # 2
    # Not used in main function but is essential for Unit Test 001
    # Delet with CAUTION

    max_integer = (2 ** int_bits) - 1
    max_fractional = 1 - (1 / (2 ** frac_bits))
    range_max = max_integer + max_fractional
    range_min = 0
    if total_bits == int_bits + frac_bits:
        return  range_max, range_min
    else:
        range_max = range_max
        range_min = range_max - (2 ** (int_bits +1))
        return  range_max, range_min
    

def check_hex_num(hex_num, total_bits): # 3

    # Convert hexadecimal to decimal
    decimal_num = int(hex_num, 16)

    # Check if the decimal value exceeds the total bits
    if decimal_num >= 2 ** total_bits:
        return "Wrong Number"
    else:
        return "Number Valid"
    
'''

# Unit Test 001 
# For Function 1-3

input_string = "U9.8"

AA = parse_X_Y_format(input_string)
BB = generate_value_range(AA[0],AA[1],AA[2])
CC = check_hex_num("100",AA[2])
print(AA,BB,CC)

'''


def bin_to_decimal(binary_num, int_bits, frac_bits): # 4
    # Test if binary is correctly sliced into parts
    # Not used in main function but is essential for Unit Test 002
    # Delet with CAUTION

    sign = int(binary_num[0:1], 2) * (2 ** (int_bits + 1))
    integer_part = int(binary_num[1:int_bits + 1], 2)
    fractional_part = 0
    if frac_bits > 0:
        fractional_part = int(binary_num[int_bits + 1:], 2) / (2 ** frac_bits)
    decimal_num = integer_part + fractional_part - sign

    A = binary_num[0:1]
    B = binary_num[1:int_bits + 1]
    C = binary_num[int_bits + 1:]

    return (sign, integer_part, fractional_part, decimal_num), (A,B,C)



'''
# Unit Test 002
# For Function 4

DD = bin_to_decimal("1110011001",4,5,10)
print(f"")
print(DD)
'''


def hex_to_decimal(hex_num, int_bits, frac_bits, total_bits): # 5.1
    # The first draft of writing hex_to_decimal function

    # Convert hexadecimal to decimal
    decimal_num = int(hex_num, 16)
 
    # Convert decimal to binary
    binary_num = bin(decimal_num)[2:].zfill(total_bits)  # Pad 0 

    sign = 0

    if total_bits == int_bits + frac_bits: #  UX.Y has X+Y bit

        # Extract integer and fractional parts
        integer_part = int(binary_num[:int_bits], 2)
        fractional_part = 0
        if frac_bits > 0:
            fractional_part = int(binary_num[int_bits:], 2) / (2 ** frac_bits)

 
    elif  total_bits != int_bits + frac_bits: #  SX.Y has 1+X+Y bit

        sign = int(binary_num[0:1], 2) * (2 ** (int_bits + 1))
        integer_part = int(binary_num[1:int_bits + 1], 2)
        fractional_part = 0
        if frac_bits > 0:
            fractional_part = int(binary_num[int_bits + 1:], 2) / (2 ** frac_bits)

    decimal_num = integer_part + fractional_part - sign

    return decimal_num

def hex_to_decimal_2(hex_num, int_bits, frac_bits, total_bits): # 5.2
    # A Clearer way of writing hex_to_decimal function

    # Convert hexadecimal to decimal
    decimal_num = int(hex_num, 16)
 
    # Convert decimal to binary
    binary_num = bin(decimal_num)[2:].zfill(total_bits)  # Pad 0

    sign = 0
    initial = 0
    fractional_part = 0

    if total_bits != int_bits + frac_bits: #  SX.Y has 1+X+Y bit
        sign = int(binary_num[0:1], 2) * (2 ** (int_bits + 1))
        initial = 1
        int_bits += 1

    integer_part = int(binary_num[initial:int_bits], 2)
    fractional_part = 0
    if frac_bits > 0:
        fractional_part = int(binary_num[int_bits:], 2) / (2 ** frac_bits)  


    decimal_num = integer_part + fractional_part - sign

    return decimal_num

'''
# Unit Test 003
# For Function 5

EE = hex_to_decimal("0x20000",9,8,18)
FF = hex_to_decimal_2("0x20000",9,8,18)
print(f"")
print(EE)
print(FF)

'''

def get_valid_format():
# Get proper format

    while True:
        try:
            format_str = input("Enter the UX.Y / SX.Y format (e.g., U9.8 / S10.0): ")
            int_bits, frac_bits, total_bits = parse_X_Y_format(format_str)
            return int_bits, frac_bits, total_bits
        except ValueError as e:
            print("Error:", e)
            print("Please try again.")

def get_valid_hexadecimal(total_bits):
# Get proper HEX

    while True:
        hex_num = input("Enter the hexadecimal number: 0x")
        if is_valid_hexadecimal(hex_num[2:]):
            result = check_hex_num(hex_num, total_bits)
            if result == "Number Valid":
                return hex_num
            else:
                print("Invalid hexadecimal number. Please enter a valid number.")
        else:
            print("Hexadecimal number contains invalid characters. Please enter a valid hexadecimal number.")

def main():
    int_bits, frac_bits, total_bits = get_valid_format()
    hex_num = get_valid_hexadecimal(total_bits)
    
    decimal_num = hex_to_decimal_2(hex_num, int_bits, frac_bits, total_bits)
    print(f"The decimal representation is: {decimal_num}")



if __name__ == "__main__":
    while True:
        main()

