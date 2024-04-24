# Hexadecimal to Decimal Converter

This Python script provides functionality to convert a formatted hexadecimal number to its decimal representation based on a given format string (UX.Y or SX.Y), where U indicates unsigned and S indicates signed. 

## Background

1. **U X.Y: Unsigned**
   - U X.Y represents the X-digit integer part and Y-digit fractional part in X+Y bits.
   - Example: U 4.3 → 1 LSB = 0.125 (1/2^3), representing a number from 0 to 15.875.
   - Example: 0b 00001100 U4.3 gives 1.5.
   
2. **S X.Y: Signed**
   - S X.Y represents the 1-digit signed part, X-digit integer part, and Y-digit fractional part in 1+X+Y bits in 2's complement.
   - Example: S 4.3 → 1 LSB = 0.125 (1/2^3), representing a number from -16 to 15.875.
   - Example: 0b 00001100 S4.3 gives 1.5.
   - Example: 0b 11110100 S4.3 gives -1.5.

These two formatted hexadecimal numbers are widely used for converting formatted hexadecimal numbers read from SSS automotive sensors' registers.

## Functions

0. `is_valid_hexadecimal(input_str)`: Checks if the input string is a valid hexadecimal number.
1. `parse_X_Y_format(format_str)`: Parses the format string (UX.Y or SX.Y) to extract the number of integer and fractional bits, and calculates the total number of bits.
2. `generate_value_range(int_bits, frac_bits, total_bits)`: Generates the value range based on the number of integer and fractional bits (not used in the main function).
3. `check_hex_num(hex_num, total_bits)`: Checks if the hexadecimal number is within the specified number of total bits.
4. `bin_to_decimal(binary_num, int_bits, frac_bits)`: Converts a binary number to its decimal representation (not used in the main function).
5. `hex_to_decimal(hex_num, int_bits, frac_bits, total_bits)`: Converts a hexadecimal number to its decimal representation. There are two versions of this function, one with clearer code structure (`hex_to_decimal_2`).
6. `get_valid_format()`: Prompts the user to input the format string (UX.Y or SX.Y) and validates it.
7. `get_valid_hexadecimal(total_bits)`: Prompts the user to input a hexadecimal number and validates it against the specified total bits.
8. `main()`: Main function that orchestrates the conversion process by getting the format string and hexadecimal number from the user, then converting the hexadecimal number to its decimal representation.

## Usage

1. Run the script.
2. Enter the format string (e.g., U9.8 or S10.0) when prompted.
3. Enter the hexadecimal number (without '0x' prefix) when prompted.
4. The script will then output the decimal representation of the provided hexadecimal number based on the specified format.
5. The user can repeat the process to convert more hexadecimal numbers with different formats.
