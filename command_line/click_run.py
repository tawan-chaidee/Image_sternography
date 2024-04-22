import click
from pathlib import Path
from steganography import encode_img, decode_img
from PIL import Image

@click.command()
@click.argument("mode", type=click.Choice(["encode","e", "decode","d"]))
@click.argument("image_link", type=click.Path(exists=True), required=True)
@click.argument("message", type=str, required=False, default=None)
@click.option("--key", type=str, default=None)
def hello(mode, image_link, message, key):
    
    if mode == "decode" or mode == "d":
        key = message
    print("key",key)
    
    if message is not None and Path(message).is_file():
        with open(message,"rb") as f:
            message = str(f.read())
        
    if key is not None and Path(key).is_file():
        with open(key,"rb") as f:
            key = f.read()
    
    if mode == "encode" or mode == "e":
        print("start encoding...")
        image = Image.open(image_link).convert('RGB')
        
        image, key_res = encode_img(image, message, key)
        
        # Save the key
        if key is None:
            print("The key is:",key_res,"saved as",f"{Path(image_link).stem}_key.txt")
            with open(f"{Path(image_link).stem}_key.txt","wb") as f:
                f.write(key_res)
        else:
            print("The key is:",key_res)
            
        # Save the modified image
        image.save(f"{Path(image_link).stem}.png")
        print("The image is saved as",f"{Path(image_link).stem}.png")
        
    elif mode == "decode" or mode == "d":
        print("start decoding...")
        print("The key is:",key)
        image = Image.open(image_link).convert('RGB')
        
        message = decode_img(image, key)
        
        print("The message is:",message)

if __name__ == '__main__':
    hello()