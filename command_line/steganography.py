import sys
# from command_line.libs import *
import numpy as np
from PIL import Image
from matplotlib import pyplot as plt
from pathlib import Path
from libs import *

def display_help():
    print("Usage:")
    print(f"{sys.argv[0]} [mode] [file] [keys/message]")
    print("mode include: encoding, decoding")
    print("keys/message can be a file")
    
def encode_img(image, message, key=None):
    if not key:
        aes_key = AES_key_generate().decode("utf-8")
    else:
        aes_key = key
    
    secret_message = AES_encrypt_with_key(message, aes_key)
    # print("secret",secret_message)
    secret_message_str = str(secret_message.decode('ascii'))
    # secret_message_str = secret_message.decode('utf-8')
    
    # Encode the message into the image
    # modified_img = encode_message(image, secret_message)
    modified_img = encode_message(image, secret_message_str)

    return modified_img, aes_key

def decode_img(image, key):
    # Decode hidden message
    decoded_message_bits = decode_message(image)
    # print("decoded",decoded_message_bits)
    decoded_message_str = bits_to_string(decoded_message_bits)
    decoded_message_str = AES_decrypt(decoded_message_str,key)
    return decoded_message_str