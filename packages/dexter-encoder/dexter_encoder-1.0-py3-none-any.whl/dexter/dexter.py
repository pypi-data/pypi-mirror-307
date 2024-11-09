import random

class Dexter:
    def __init__(self, min_shift=10, max_shift=50, seed=None):
        """
        Initialize Dexter encoding with a specified shift range.
        Args:
            min_shift (int): Minimum shift value for encoding.
            max_shift (int): Maximum shift value for encoding.
            seed (int, optional): Seed for reproducibility in encoding shifts.
        """
        self.min_shift = min_shift
        self.max_shift = max_shift
        if seed is not None:
            random.seed(seed)

    def encode(self, data):
        """Encode the input string using random shifts, with shift values embedded.
        The output is then converted to hexadecimal."""
        encoded_chars = []
        for char in data:
            shift = random.randint(self.min_shift, self.max_shift)
            shifted_char = chr((ord(char) + shift) % 256)  # Shift the character

            # Ensure two-digit hexadecimal formatting for both shift and character
            hex_shift = format(shift, '02x')  # Convert shift value to 2-digit hex
            hex_char = format(ord(shifted_char), '02x')  # Convert shifted character to 2-digit hex
            encoded_chars.append(f"{hex_shift}{hex_char}")
        return ''.join(encoded_chars)

    def decode(self, encoded_data):
        """Decode the encoded string by reversing the embedded shifts from hexadecimal."""
        decoded_chars = []
        i = 0

        # Check if the length of encoded_data is a multiple of 4
        if len(encoded_data) % 4 != 0:
            raise ValueError("Encoded data length is incorrect. It must be a multiple of 4.")
        
        try:
            while i < len(encoded_data):
                # Extract shift and character in hexadecimal
                shift_hex = encoded_data[i:i+2]
                shifted_char_hex = encoded_data[i+2:i+4]

                # Convert hex values back to integer and character
                shift = int(shift_hex, 16)
                shifted_char = chr(int(shifted_char_hex, 16))
                original_char = chr((ord(shifted_char) - shift + 256) % 256)
                decoded_chars.append(original_char)
                i += 4
        except ValueError as e:
            raise ValueError("Invalid encoded data format.") from e

        return ''.join(decoded_chars)

# Create a default instance of Dexter
_default_dexter = Dexter()

# Expose encode and decode as module-level functions
encode = _default_dexter.encode
decode = _default_dexter.decode
