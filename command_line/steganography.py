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
        aes_key = AES_key_generate()
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

if len(sys.argv) < 4:
    display_help()

if __name__ == '__main__':

    if sys.argv[1] == "encode" or sys.argv[1] == "e":
        print("start encoding...")
        image_link = sys.argv[2]
        message = sys.argv[3]
        
        try:
            im = Image.open(image_link).convert('RGB')
            im_name = Path(image_link).stem
        except FileNotFoundError:
            print("File not found, please check the file path again")
            exit()
            
        if Path(message).is_file():
            with open(message,"rb") as f:
                message = str(f.read())
                
        print(im)
        print(message)
                
        # Encrypt the message
        img, key = encode_img(im, message, None)
        
        # Save the key
        print("The key is:",key,"saved as",f"{im_name}_key.txt")
        with open(f"{im_name}_key.txt","wb") as f:
            f.write(key)
        
        # Save the modified image
        save_image(img, f"{im_name}_encoded.png")


        # secret_message, key = AES_encrypt(message)
        
        # # save as file
        # with open(f"{im_name}_key.txt","wb") as f:
        #     f.write(key)
            
        # print("The key is:",key,"saved as",f"{im_name}_key.txt")
        
        # secret_message_str = secret_message.decode('utf-8')

        # # Encode the message into the image
        # modified_img = encode_message(im, secret_message_str)

        # Save the modified image
        # save_image(modified_img, f"{im_name}_encoded.png")
        
    elif sys.argv[1] == "decode" or sys.argv[1] == "d":
        print("start decoding...")
        image_link = sys.argv[2]
        key = sys.argv[3]
        
        try:
            img = Image.open(image_link).convert('RGB')
        except FileNotFoundError:
            print("File not found, please check the file path again")
            exit()
        
        if Path(key).is_file():
            with open(key,"rb") as f:
                key = f.read()

        # Decode hidden message
        decoded_message_bits = decode_message(img)
        # decoded_message_str = bits_to_string(decoded_message_bits)
        # print(decoded_message_str)
        # decoded_message_str = AES_decrypt(decoded_message_str,key)
        
        print("Decoded message:",decoded_message_bits)

# else:
#     display_help()