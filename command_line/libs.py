from cryptography.fernet import Fernet
import numpy as np
from PIL import Image
from matplotlib import pyplot as plt

# =========================
#        Encryption
# =========================


def AES_encrypt(message):
  # Generate a random key
  key = Fernet.generate_key()
  # Turn string to bit
  encode_message = message.encode("utf-8")

  # Encrypt the message
  cipher = Fernet(key)
  encrypted_data = cipher.encrypt(encode_message)

  return encrypted_data, key

def AES_key_generate():
    # Generate a random key
    key = Fernet.generate_key()
    return key

def AES_encrypt_with_key(message, key):
    # Turn string to bit
    encode_message = message.encode("utf-8")
    
    # Encrypt the message
    cipher = Fernet(key)
    encrypted_data = cipher.encrypt(encode_message)
    
    return encrypted_data

def AES_decrypt(encrypted_data, key):
  cipher = Fernet(key)

  # Decrypt the data
  decrypted_data = cipher.decrypt(encrypted_data)

  return decrypted_data.decode("utf-8")

# =========================
#         Encoding
# =========================

def encode_message(image, message):

    message = string_to_bits(message)
    # print("message",message)
    data = np.array(image)
    message_bits = np.array([int(bit) for bit in message])

    # Calculate the number of bits needed to encode the message, including message length
    total_bits_needed = len(data) * len(data[0]) * 3

    # Check if the message fits within the image without repetitions
    if len(message_bits) + 16 > total_bits_needed:  # Add 16 bits for message length
        raise ValueError("Message is too long to be encoded without repetitions")

    # Convert the length of the message to binary (using 16 bits)
    message_length_bits = np.array([int(bit) for bit in format(len(message), '016b')])

    # Combined both length and message
    encoded_message = np.append(message_length_bits,message_bits)

    height, width, channel = data.shape

    # Modify the least significant bit of each color channel pixel to encode the message
    for i in range(height):
        for j in range(width):
            for k in range(channel):  # Iterate over RGB channels
                if len(encoded_message) > 0:
                    new_bit = (data[i, j, k] & 0xFE) | encoded_message[0]
                    # print("modified",i,j,k,"from",bin(data[i, j, k]),"to",bin(new_bit))
                    data[i, j, k] = new_bit
                    encoded_message = encoded_message[1:]

    return Image.fromarray(data)


def display_images(original_img, modified_img):
    fig, axes = plt.subplots(1, 2, figsize=(10, 5))
    axes[0].imshow(original_img)
    axes[0].set_title('Original Image')
    axes[0].axis('off')
    axes[1].imshow(modified_img)
    axes[1].set_title('Modified Image with Hidden Message')
    axes[1].axis('off')
    plt.show()

def save_image(image, filename):
    image.save(filename)

def string_to_bits(message):
    # Convert each character to its binary representation
    # Using 8 bits for each character
    return ''.join(format(ord(char), '08b') for char in message)


# =========================
#         Decoding
# =========================

def decode_message(image):
    data = np.array(image)

    height, width, channel = data.shape

    message_length = 16 # extract the length first
    is_length_extracted = False
    message_bits = []

    # Extract the message bits from the remaining pixels
    pixel_counter = 0
    for i in range(height):
        for j in range(width):
            for k in range(channel):  # Iterate over RGB channels
                if pixel_counter < message_length:
                    # Extract the least significant bit
                    bit = data[i, j, k] & 1
                    message_bits.append(bit)
                    pixel_counter += 1
                else:
                    if not is_length_extracted:
                        is_length_extracted = True
                        # Convert the binary string to integer to get the length of the message
                        message = ''.join([str(bit) for bit in message_bits])
                        message_length = int(message,2)

                        # Extract the least significant bit that have missed
                        bit = data[i, j, k] & 1
                        message_bits = [bit]
                        pixel_counter = 1

                        continue
                    # All message bits have been extracted, exit the loop
                    break
            else:
                continue
            break
        else:
            continue
        break

    # Convert the extracted bits to a string
    message = ''.join([str(bit) for bit in message_bits])

    return message

def bits_to_string(bits):
    # Split the binary string into 8-bit chunks
    chunks = [bits[i:i+8] for i in range(0, len(bits), 8)]

    # Convert each chunk into its corresponding ASCII character
    return ''.join(chr(int(chunk, 2)) for chunk in chunks)