from PIL import Image


def read_pbm(file_path):
    with open(file_path, 'rb') as f:
        # Read the first three lines
        header = f.readline().decode('utf-8').strip()
        size = f.readline().decode('utf-8').strip()
        binary_data = f.read()

    # Convert binary data to list of 0s and 1s
    bits = []
    for byte in binary_data:
        byte_bits = format(byte, '08b')  # Convert byte to binary string
        # bits.extend(map(int, byte_bits))  # Convert binary string to list of ints

        # byte_bits = bin(byte)
        # byte_bits = str(byte_bits)[2:]

        bits.append(byte_bits)
    return header, size, "".join(bits)


def write_pbm(header, size, bits, output_file):
    with open(output_file, 'wb') as f:
        # Write the header and size
        f.write((header + '\n').encode('utf-8'))
        f.write((size + '\n').encode('utf-8'))

        # Convert bits list to bytes
        bytes_data = bytearray()
        for i in range(0, len(bits), 8):
            byte = bits[i:i + 8]
            byte_str = ''.join(str(bit) for bit in byte)
            byte_int = int(byte_str, 2)
            bytes_data.append(byte_int)

        # Write the binary data
        f.write(bytes_data)


def image_to_bits(image_path):
    with Image.open(image_path) as img:
        # Convert image to grayscale (if needed)
        img = img.convert('L')

        # Convert image data to binary string
        binary_data = ''.join(format(pixel, '08b') for pixel in img.tobytes())

    return binary_data


def process_bits(bits):
    # Your logic to process the bits here
    # For example, if you want to invert each bit:
    processed_bits = ''.join(str(1 - int(bit)) for bit in bits)
    return processed_bits


def bits_to_image(bits, image_size, output_path):
    # Convert binary string back to image
    data = bytearray(int(bits[i:i + 8], 2) for i in range(0, len(bits), 8))
    img = Image.frombytes('L', image_size, bytes(data))

    # Save the processed image
    img.save(output_path)


# Example usage:
# input_image_path = 'input.png'
# output_image_path = 'output.png'

# Step 1: Convert image to bits
# image_bits = image_to_bits(input_image_path)

# Step 2: Process the bits
# processed_bits = process_bits(image_bits)

# Step 3: Convert processed bits back to image
# image_size = Image.open(input_image_path).size
# bits_to_image(processed_bits, image_size, output_image_path)
